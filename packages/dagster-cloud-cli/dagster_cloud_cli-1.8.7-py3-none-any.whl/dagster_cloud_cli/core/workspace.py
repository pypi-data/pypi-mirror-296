import os
from typing import Any, Dict, List, NamedTuple, Optional

import dagster._check as check
import yaml
from dagster._core.instance.ref import InstanceRef
from dagster._serdes import serialize_value, whitelist_for_serdes
from dagster._utils.merger import merge_dicts

from .agent_queue import AgentQueue


@whitelist_for_serdes
class GitMetadata(
    NamedTuple(
        "_GitMetadata",
        [("commit_hash", Optional[str]), ("url", Optional[str])],
    )
):
    def __new__(cls, commit_hash=None, url=None):
        return super(GitMetadata, cls).__new__(
            cls,
            check.opt_str_param(commit_hash, "commit_hash"),
            check.opt_str_param(url, "url"),
        )


@whitelist_for_serdes
class PexMetadata(
    NamedTuple(
        "_PexMetadata",
        [
            # pex_tag is a string like 'deps-234y4384.pex:source-39y3474.pex' that idenfies
            # the pex files to execute
            ("pex_tag", str),
            # python_version determines which pex base docker image to use
            # only one of PexMetadata.python_version or CodeLocationDeployData.image should be specified
            ("python_version", Optional[str]),
        ],
    )
):
    def __new__(cls, pex_tag, python_version=None):
        return super(PexMetadata, cls).__new__(
            cls,
            check.str_param(pex_tag, "pex_tag"),
            check.opt_str_param(python_version, "python_version"),
        )

    def resolve_image(self) -> Optional[str]:
        if not self.python_version:
            return None
        agent_image_tag = os.getenv("DAGSTER_CLOUD_AGENT_IMAGE_TAG")
        serverless_service_name = os.getenv("SERVERLESS_SERVICE_NAME")
        if not agent_image_tag or not serverless_service_name:
            return None
        if serverless_service_name in ["serverless-agents", "serverless-agents-public-demo"]:
            return f"657821118200.dkr.ecr.us-west-2.amazonaws.com/dagster-cloud-serverless-base-py{self.python_version}:{agent_image_tag}"
        else:
            return f"878483074102.dkr.ecr.us-west-2.amazonaws.com/dagster-cloud-serverless-base-py{self.python_version}:{agent_image_tag}"


def get_instance_ref_for_user_code(instance_ref: InstanceRef) -> InstanceRef:
    # Remove fields from InstanceRef that may not be compatible with earlier
    # versions of dagster and aren't actually needed by user code

    custom_instance_class_data = instance_ref.custom_instance_class_data
    if custom_instance_class_data:
        config_dict = custom_instance_class_data.config_dict
        new_config_dict = {
            key: val for key, val in config_dict.items() if key not in {"agent_queues"}
        }

        user_code_launcher_config = config_dict.get("user_code_launcher", {}).get("config")
        if user_code_launcher_config:
            new_config_dict["user_code_launcher"]["config"] = {
                key: val
                for key, val in user_code_launcher_config.items()
                if key not in {"agent_metrics"}
            }

        custom_instance_class_data = custom_instance_class_data._replace(
            config_yaml=yaml.dump(new_config_dict)
        )

    return instance_ref._replace(custom_instance_class_data=custom_instance_class_data)


# History of CodeLocationDeployData
# 1. Removal of `enable_metrics` field
# 2. Renamed from `CodeDeploymentMetadata` to `CodeLocationDeployData``
@whitelist_for_serdes(storage_name="CodeDeploymentMetadata")
class CodeLocationDeployData(
    NamedTuple(
        "_CodeDeploymentMetadata",
        [
            ("image", Optional[str]),
            ("python_file", Optional[str]),
            ("package_name", Optional[str]),
            ("module_name", Optional[str]),
            ("working_directory", Optional[str]),
            ("executable_path", Optional[str]),
            ("attribute", Optional[str]),
            ("git_metadata", Optional[GitMetadata]),
            ("container_context", Dict[str, Any]),
            ("cloud_context_env", Dict[str, Any]),
            ("pex_metadata", Optional[PexMetadata]),
            ("agent_queue", Optional[AgentQueue]),
        ],
    )
):
    def __new__(
        cls,
        image=None,
        python_file=None,
        package_name=None,
        module_name=None,
        working_directory=None,
        executable_path=None,
        attribute=None,
        git_metadata=None,
        container_context=None,
        cloud_context_env=None,
        pex_metadata=None,
        agent_queue=None,
    ):
        check.invariant(
            len([val for val in [python_file, package_name, module_name] if val]) == 1,
            "Must supply exactly one of a file name, a package name, or a module name",
        )

        return super(CodeLocationDeployData, cls).__new__(
            cls,
            check.opt_str_param(image, "image"),
            check.opt_str_param(python_file, "python_file"),
            check.opt_str_param(package_name, "package_name"),
            check.opt_str_param(module_name, "module_name"),
            check.opt_str_param(working_directory, "working_directory"),
            check.opt_str_param(executable_path, "executable_path"),
            check.opt_str_param(attribute, "attribute"),
            check.opt_inst_param(git_metadata, "git_metadata", GitMetadata),
            check.opt_dict_param(container_context, "container_context", key_type=str),
            check.opt_dict_param(cloud_context_env, "cloud_context_env", key_type=str),
            check.opt_inst_param(pex_metadata, "pex_metadata", PexMetadata),
            check.opt_str_param(agent_queue, "agent_queue"),
        )

    def with_cloud_context_env(self, cloud_context_env: Dict[str, Any]) -> "CodeLocationDeployData":
        return self._replace(cloud_context_env=cloud_context_env)

    def get_multipex_server_command(
        self,
        port: Optional[int],
        socket: Optional[str] = None,
        metrics_enabled: bool = False,
    ) -> List[str]:
        return (
            ["dagster-cloud", "pex", "grpc", "--host", "0.0.0.0"]
            + (["--port", str(port)] if port else [])
            + (["--socket", str(socket)] if socket else [])
            + (["--enable-metrics"] if metrics_enabled else [])
        )

    def get_multipex_server_env(self) -> Dict[str, str]:
        return {"DAGSTER_CURRENT_IMAGE": self.image} if self.image else {}

    def get_grpc_server_command(self, metrics_enabled: bool = False) -> List[str]:
        return (
            ([self.executable_path, "-m"] if self.executable_path else [])
            + [
                "dagster",
                "api",
                "grpc",
            ]
            + (["--enable-metrics"] if metrics_enabled else [])
        )

    def get_grpc_server_env(
        self,
        port: Optional[int],
        location_name: str,
        instance_ref: Optional[InstanceRef],
        socket: Optional[str] = None,
    ) -> Dict[str, str]:
        return merge_dicts(
            {
                "DAGSTER_LOCATION_NAME": location_name,
                "DAGSTER_INJECT_ENV_VARS_FROM_INSTANCE": "1",
                "DAGSTER_CLI_API_GRPC_LAZY_LOAD_USER_CODE": "1",
                "DAGSTER_CLI_API_GRPC_HOST": "0.0.0.0",
            },
            (
                {
                    "DAGSTER_INSTANCE_REF": serialize_value(
                        get_instance_ref_for_user_code(instance_ref)
                    )
                }
                if instance_ref
                else {}
            ),
            ({"DAGSTER_CLI_API_GRPC_PORT": str(port)} if port else {}),
            ({"DAGSTER_CLI_API_GRPC_SOCKET": str(socket)} if socket else {}),
            ({"DAGSTER_CURRENT_IMAGE": self.image} if self.image else {}),
            ({"DAGSTER_CLI_API_GRPC_PYTHON_FILE": self.python_file} if self.python_file else {}),
            ({"DAGSTER_CLI_API_GRPC_MODULE_NAME": self.module_name} if self.module_name else {}),
            ({"DAGSTER_CLI_API_GRPC_PACKAGE_NAME": self.package_name} if self.package_name else {}),
            (
                {"DAGSTER_CLI_API_GRPC_WORKING_DIRECTORY": self.working_directory}
                if self.working_directory
                else {}
            ),
            ({"DAGSTER_CLI_API_GRPC_ATTRIBUTE": self.attribute} if self.attribute else {}),
            (
                {"DAGSTER_CLI_API_GRPC_USE_PYTHON_ENVIRONMENT_ENTRY_POINT": "1"}
                if self.executable_path
                else {}
            ),
        )
