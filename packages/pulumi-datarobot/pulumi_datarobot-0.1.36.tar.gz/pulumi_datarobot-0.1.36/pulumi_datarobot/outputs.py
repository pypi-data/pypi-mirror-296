# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs

__all__ = [
    'ApplicationSourceResourceSettings',
    'ApplicationSourceRuntimeParameterValue',
    'CustomModelGuardConfiguration',
    'CustomModelGuardConfigurationIntervention',
    'CustomModelGuardConfigurationInterventionCondition',
    'CustomModelOverallModerationConfiguration',
    'CustomModelResourceSettings',
    'CustomModelRuntimeParameterValue',
    'CustomModelSourceRemoteRepository',
    'DeploymentSettings',
    'DeploymentSettingsAssociationId',
    'DeploymentSettingsPredictionsSettings',
    'LlmBlueprintLlmSettings',
    'LlmBlueprintVectorDatabaseSettings',
    'VectorDatabaseChunkingParameters',
]

@pulumi.output_type
class ApplicationSourceResourceSettings(dict):
    def __init__(__self__, *,
                 replicas: Optional[int] = None):
        """
        :param int replicas: The replicas for the Application Source.
        """
        if replicas is not None:
            pulumi.set(__self__, "replicas", replicas)

    @property
    @pulumi.getter
    def replicas(self) -> Optional[int]:
        """
        The replicas for the Application Source.
        """
        return pulumi.get(self, "replicas")


@pulumi.output_type
class ApplicationSourceRuntimeParameterValue(dict):
    def __init__(__self__, *,
                 key: str,
                 type: str,
                 value: str):
        """
        :param str key: The name of the runtime parameter.
        :param str type: The type of the runtime parameter.
        :param str value: The value of the runtime parameter (type conversion is handled internally).
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The name of the runtime parameter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the runtime parameter.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the runtime parameter (type conversion is handled internally).
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class CustomModelGuardConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "templateName":
            suggest = "template_name"
        elif key == "deploymentId":
            suggest = "deployment_id"
        elif key == "inputColumnName":
            suggest = "input_column_name"
        elif key == "llmType":
            suggest = "llm_type"
        elif key == "openaiApiBase":
            suggest = "openai_api_base"
        elif key == "openaiCredential":
            suggest = "openai_credential"
        elif key == "openaiDeploymentId":
            suggest = "openai_deployment_id"
        elif key == "outputColumnName":
            suggest = "output_column_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomModelGuardConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomModelGuardConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomModelGuardConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 intervention: 'outputs.CustomModelGuardConfigurationIntervention',
                 name: str,
                 stages: Sequence[str],
                 template_name: str,
                 deployment_id: Optional[str] = None,
                 input_column_name: Optional[str] = None,
                 llm_type: Optional[str] = None,
                 openai_api_base: Optional[str] = None,
                 openai_credential: Optional[str] = None,
                 openai_deployment_id: Optional[str] = None,
                 output_column_name: Optional[str] = None):
        """
        :param 'CustomModelGuardConfigurationInterventionArgs' intervention: The intervention for the guard configuration.
        :param str name: The name of the guard configuration.
        :param Sequence[str] stages: The list of stages for the guard configuration.
        :param str template_name: The template name of the guard configuration.
        :param str deployment_id: The deployment ID of this guard.
        :param str input_column_name: The input column name of this guard.
        :param str llm_type: The LLM type for this guard.
        :param str openai_api_base: The OpenAI API base URL for this guard.
        :param str openai_credential: The ID of an OpenAI credential for this guard.
        :param str openai_deployment_id: The ID of an OpenAI deployment for this guard.
        :param str output_column_name: The output column name of this guard.
        """
        pulumi.set(__self__, "intervention", intervention)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "stages", stages)
        pulumi.set(__self__, "template_name", template_name)
        if deployment_id is not None:
            pulumi.set(__self__, "deployment_id", deployment_id)
        if input_column_name is not None:
            pulumi.set(__self__, "input_column_name", input_column_name)
        if llm_type is not None:
            pulumi.set(__self__, "llm_type", llm_type)
        if openai_api_base is not None:
            pulumi.set(__self__, "openai_api_base", openai_api_base)
        if openai_credential is not None:
            pulumi.set(__self__, "openai_credential", openai_credential)
        if openai_deployment_id is not None:
            pulumi.set(__self__, "openai_deployment_id", openai_deployment_id)
        if output_column_name is not None:
            pulumi.set(__self__, "output_column_name", output_column_name)

    @property
    @pulumi.getter
    def intervention(self) -> 'outputs.CustomModelGuardConfigurationIntervention':
        """
        The intervention for the guard configuration.
        """
        return pulumi.get(self, "intervention")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the guard configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def stages(self) -> Sequence[str]:
        """
        The list of stages for the guard configuration.
        """
        return pulumi.get(self, "stages")

    @property
    @pulumi.getter(name="templateName")
    def template_name(self) -> str:
        """
        The template name of the guard configuration.
        """
        return pulumi.get(self, "template_name")

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> Optional[str]:
        """
        The deployment ID of this guard.
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter(name="inputColumnName")
    def input_column_name(self) -> Optional[str]:
        """
        The input column name of this guard.
        """
        return pulumi.get(self, "input_column_name")

    @property
    @pulumi.getter(name="llmType")
    def llm_type(self) -> Optional[str]:
        """
        The LLM type for this guard.
        """
        return pulumi.get(self, "llm_type")

    @property
    @pulumi.getter(name="openaiApiBase")
    def openai_api_base(self) -> Optional[str]:
        """
        The OpenAI API base URL for this guard.
        """
        return pulumi.get(self, "openai_api_base")

    @property
    @pulumi.getter(name="openaiCredential")
    def openai_credential(self) -> Optional[str]:
        """
        The ID of an OpenAI credential for this guard.
        """
        return pulumi.get(self, "openai_credential")

    @property
    @pulumi.getter(name="openaiDeploymentId")
    def openai_deployment_id(self) -> Optional[str]:
        """
        The ID of an OpenAI deployment for this guard.
        """
        return pulumi.get(self, "openai_deployment_id")

    @property
    @pulumi.getter(name="outputColumnName")
    def output_column_name(self) -> Optional[str]:
        """
        The output column name of this guard.
        """
        return pulumi.get(self, "output_column_name")


@pulumi.output_type
class CustomModelGuardConfigurationIntervention(dict):
    def __init__(__self__, *,
                 action: str,
                 condition: 'outputs.CustomModelGuardConfigurationInterventionCondition',
                 message: Optional[str] = None):
        """
        :param str action: The action of the guard intervention.
        :param 'CustomModelGuardConfigurationInterventionConditionArgs' condition: The list of conditions for the guard intervention.
        :param str message: The message of the guard intervention.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "condition", condition)
        if message is not None:
            pulumi.set(__self__, "message", message)

    @property
    @pulumi.getter
    def action(self) -> str:
        """
        The action of the guard intervention.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def condition(self) -> 'outputs.CustomModelGuardConfigurationInterventionCondition':
        """
        The list of conditions for the guard intervention.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        """
        The message of the guard intervention.
        """
        return pulumi.get(self, "message")


@pulumi.output_type
class CustomModelGuardConfigurationInterventionCondition(dict):
    def __init__(__self__, *,
                 comparand: float,
                 comparator: str):
        """
        :param float comparand: The comparand of the guard condition.
        :param str comparator: The comparator of the guard condition.
        """
        pulumi.set(__self__, "comparand", comparand)
        pulumi.set(__self__, "comparator", comparator)

    @property
    @pulumi.getter
    def comparand(self) -> float:
        """
        The comparand of the guard condition.
        """
        return pulumi.get(self, "comparand")

    @property
    @pulumi.getter
    def comparator(self) -> str:
        """
        The comparator of the guard condition.
        """
        return pulumi.get(self, "comparator")


@pulumi.output_type
class CustomModelOverallModerationConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "timeoutAction":
            suggest = "timeout_action"
        elif key == "timeoutSec":
            suggest = "timeout_sec"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomModelOverallModerationConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomModelOverallModerationConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomModelOverallModerationConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 timeout_action: Optional[str] = None,
                 timeout_sec: Optional[int] = None):
        """
        :param str timeout_action: The timeout action of the overall moderation configuration.
        :param int timeout_sec: The timeout in seconds of the overall moderation configuration.
        """
        if timeout_action is not None:
            pulumi.set(__self__, "timeout_action", timeout_action)
        if timeout_sec is not None:
            pulumi.set(__self__, "timeout_sec", timeout_sec)

    @property
    @pulumi.getter(name="timeoutAction")
    def timeout_action(self) -> Optional[str]:
        """
        The timeout action of the overall moderation configuration.
        """
        return pulumi.get(self, "timeout_action")

    @property
    @pulumi.getter(name="timeoutSec")
    def timeout_sec(self) -> Optional[int]:
        """
        The timeout in seconds of the overall moderation configuration.
        """
        return pulumi.get(self, "timeout_sec")


@pulumi.output_type
class CustomModelResourceSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "memoryMb":
            suggest = "memory_mb"
        elif key == "networkAccess":
            suggest = "network_access"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomModelResourceSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomModelResourceSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomModelResourceSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 memory_mb: Optional[int] = None,
                 network_access: Optional[str] = None,
                 replicas: Optional[int] = None):
        """
        :param int memory_mb: The memory in MB for the Custom Model.
        :param str network_access: The network access for the Custom Model.
        :param int replicas: The replicas for the Custom Model.
        """
        if memory_mb is not None:
            pulumi.set(__self__, "memory_mb", memory_mb)
        if network_access is not None:
            pulumi.set(__self__, "network_access", network_access)
        if replicas is not None:
            pulumi.set(__self__, "replicas", replicas)

    @property
    @pulumi.getter(name="memoryMb")
    def memory_mb(self) -> Optional[int]:
        """
        The memory in MB for the Custom Model.
        """
        return pulumi.get(self, "memory_mb")

    @property
    @pulumi.getter(name="networkAccess")
    def network_access(self) -> Optional[str]:
        """
        The network access for the Custom Model.
        """
        return pulumi.get(self, "network_access")

    @property
    @pulumi.getter
    def replicas(self) -> Optional[int]:
        """
        The replicas for the Custom Model.
        """
        return pulumi.get(self, "replicas")


@pulumi.output_type
class CustomModelRuntimeParameterValue(dict):
    def __init__(__self__, *,
                 key: str,
                 type: str,
                 value: str):
        """
        :param str key: The name of the runtime parameter.
        :param str type: The type of the runtime parameter.
        :param str value: The value of the runtime parameter (type conversion is handled internally).
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The name of the runtime parameter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the runtime parameter.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the runtime parameter (type conversion is handled internally).
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class CustomModelSourceRemoteRepository(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "sourcePaths":
            suggest = "source_paths"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomModelSourceRemoteRepository. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomModelSourceRemoteRepository.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomModelSourceRemoteRepository.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 ref: str,
                 source_paths: Sequence[str]):
        """
        :param str id: The ID of the source remote repository.
        :param str ref: The reference of the source remote repository.
        :param Sequence[str] source_paths: The list of source paths in the source remote repository.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "ref", ref)
        pulumi.set(__self__, "source_paths", source_paths)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the source remote repository.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ref(self) -> str:
        """
        The reference of the source remote repository.
        """
        return pulumi.get(self, "ref")

    @property
    @pulumi.getter(name="sourcePaths")
    def source_paths(self) -> Sequence[str]:
        """
        The list of source paths in the source remote repository.
        """
        return pulumi.get(self, "source_paths")


@pulumi.output_type
class DeploymentSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "associationId":
            suggest = "association_id"
        elif key == "challengerAnalysis":
            suggest = "challenger_analysis"
        elif key == "predictionRowStorage":
            suggest = "prediction_row_storage"
        elif key == "predictionsSettings":
            suggest = "predictions_settings"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DeploymentSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DeploymentSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DeploymentSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 association_id: Optional['outputs.DeploymentSettingsAssociationId'] = None,
                 challenger_analysis: Optional[bool] = None,
                 prediction_row_storage: Optional[bool] = None,
                 predictions_settings: Optional['outputs.DeploymentSettingsPredictionsSettings'] = None):
        """
        :param 'DeploymentSettingsAssociationIdArgs' association_id: Used to associate predictions back to your actual data.
        :param bool challenger_analysis: Used to compare the performance of the deployed model with the challenger models.
        :param bool prediction_row_storage: Used to score predictions made by the challenger models and compare performance with the deployed model.
        :param 'DeploymentSettingsPredictionsSettingsArgs' predictions_settings: Settings for the predictions.
        """
        if association_id is not None:
            pulumi.set(__self__, "association_id", association_id)
        if challenger_analysis is not None:
            pulumi.set(__self__, "challenger_analysis", challenger_analysis)
        if prediction_row_storage is not None:
            pulumi.set(__self__, "prediction_row_storage", prediction_row_storage)
        if predictions_settings is not None:
            pulumi.set(__self__, "predictions_settings", predictions_settings)

    @property
    @pulumi.getter(name="associationId")
    def association_id(self) -> Optional['outputs.DeploymentSettingsAssociationId']:
        """
        Used to associate predictions back to your actual data.
        """
        return pulumi.get(self, "association_id")

    @property
    @pulumi.getter(name="challengerAnalysis")
    def challenger_analysis(self) -> Optional[bool]:
        """
        Used to compare the performance of the deployed model with the challenger models.
        """
        return pulumi.get(self, "challenger_analysis")

    @property
    @pulumi.getter(name="predictionRowStorage")
    def prediction_row_storage(self) -> Optional[bool]:
        """
        Used to score predictions made by the challenger models and compare performance with the deployed model.
        """
        return pulumi.get(self, "prediction_row_storage")

    @property
    @pulumi.getter(name="predictionsSettings")
    def predictions_settings(self) -> Optional['outputs.DeploymentSettingsPredictionsSettings']:
        """
        Settings for the predictions.
        """
        return pulumi.get(self, "predictions_settings")


@pulumi.output_type
class DeploymentSettingsAssociationId(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoGenerateId":
            suggest = "auto_generate_id"
        elif key == "featureName":
            suggest = "feature_name"
        elif key == "requiredInPredictionRequests":
            suggest = "required_in_prediction_requests"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DeploymentSettingsAssociationId. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DeploymentSettingsAssociationId.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DeploymentSettingsAssociationId.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_generate_id: bool,
                 feature_name: str,
                 required_in_prediction_requests: bool):
        """
        :param bool auto_generate_id: Whether to automatically generate an association ID.
        :param str feature_name: The name of the feature to use as the association ID.
        :param bool required_in_prediction_requests: Whether the association ID is required in prediction requests.
        """
        pulumi.set(__self__, "auto_generate_id", auto_generate_id)
        pulumi.set(__self__, "feature_name", feature_name)
        pulumi.set(__self__, "required_in_prediction_requests", required_in_prediction_requests)

    @property
    @pulumi.getter(name="autoGenerateId")
    def auto_generate_id(self) -> bool:
        """
        Whether to automatically generate an association ID.
        """
        return pulumi.get(self, "auto_generate_id")

    @property
    @pulumi.getter(name="featureName")
    def feature_name(self) -> str:
        """
        The name of the feature to use as the association ID.
        """
        return pulumi.get(self, "feature_name")

    @property
    @pulumi.getter(name="requiredInPredictionRequests")
    def required_in_prediction_requests(self) -> bool:
        """
        Whether the association ID is required in prediction requests.
        """
        return pulumi.get(self, "required_in_prediction_requests")


@pulumi.output_type
class DeploymentSettingsPredictionsSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "maxComputes":
            suggest = "max_computes"
        elif key == "minComputes":
            suggest = "min_computes"
        elif key == "realTime":
            suggest = "real_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DeploymentSettingsPredictionsSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DeploymentSettingsPredictionsSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DeploymentSettingsPredictionsSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 max_computes: int,
                 min_computes: int,
                 real_time: bool):
        """
        :param int max_computes: The maximum number of computes to use for predictions.
        :param int min_computes: The minimum number of computes to use for predictions.
        :param bool real_time: Whether to use real-time predictions.
        """
        pulumi.set(__self__, "max_computes", max_computes)
        pulumi.set(__self__, "min_computes", min_computes)
        pulumi.set(__self__, "real_time", real_time)

    @property
    @pulumi.getter(name="maxComputes")
    def max_computes(self) -> int:
        """
        The maximum number of computes to use for predictions.
        """
        return pulumi.get(self, "max_computes")

    @property
    @pulumi.getter(name="minComputes")
    def min_computes(self) -> int:
        """
        The minimum number of computes to use for predictions.
        """
        return pulumi.get(self, "min_computes")

    @property
    @pulumi.getter(name="realTime")
    def real_time(self) -> bool:
        """
        Whether to use real-time predictions.
        """
        return pulumi.get(self, "real_time")


@pulumi.output_type
class LlmBlueprintLlmSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "maxCompletionLength":
            suggest = "max_completion_length"
        elif key == "systemPrompt":
            suggest = "system_prompt"
        elif key == "topP":
            suggest = "top_p"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LlmBlueprintLlmSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LlmBlueprintLlmSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LlmBlueprintLlmSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 max_completion_length: Optional[int] = None,
                 system_prompt: Optional[str] = None,
                 temperature: Optional[float] = None,
                 top_p: Optional[float] = None):
        """
        :param int max_completion_length: The maximum number of tokens allowed in the completion. The combined count of this value and prompt tokens must be below the model's maximum context size, where prompt token count is comprised of system prompt, user prompt, recent chat history, and vector database citations.
        :param str system_prompt: Guides the style of the LLM response. It is a 'universal' prompt, prepended to all individual prompts.
        :param float temperature: Controls the randomness of model output, where higher values return more diverse output and lower values return more deterministic results.
        :param float top_p: Threshold that controls the selection of words included in the response, based on a cumulative probability cutoff for token selection. Higher numbers return more diverse options for outputs.
        """
        if max_completion_length is not None:
            pulumi.set(__self__, "max_completion_length", max_completion_length)
        if system_prompt is not None:
            pulumi.set(__self__, "system_prompt", system_prompt)
        if temperature is not None:
            pulumi.set(__self__, "temperature", temperature)
        if top_p is not None:
            pulumi.set(__self__, "top_p", top_p)

    @property
    @pulumi.getter(name="maxCompletionLength")
    def max_completion_length(self) -> Optional[int]:
        """
        The maximum number of tokens allowed in the completion. The combined count of this value and prompt tokens must be below the model's maximum context size, where prompt token count is comprised of system prompt, user prompt, recent chat history, and vector database citations.
        """
        return pulumi.get(self, "max_completion_length")

    @property
    @pulumi.getter(name="systemPrompt")
    def system_prompt(self) -> Optional[str]:
        """
        Guides the style of the LLM response. It is a 'universal' prompt, prepended to all individual prompts.
        """
        return pulumi.get(self, "system_prompt")

    @property
    @pulumi.getter
    def temperature(self) -> Optional[float]:
        """
        Controls the randomness of model output, where higher values return more diverse output and lower values return more deterministic results.
        """
        return pulumi.get(self, "temperature")

    @property
    @pulumi.getter(name="topP")
    def top_p(self) -> Optional[float]:
        """
        Threshold that controls the selection of words included in the response, based on a cumulative probability cutoff for token selection. Higher numbers return more diverse options for outputs.
        """
        return pulumi.get(self, "top_p")


@pulumi.output_type
class LlmBlueprintVectorDatabaseSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "maxDocumentsRetrievedPerPrompt":
            suggest = "max_documents_retrieved_per_prompt"
        elif key == "maxTokens":
            suggest = "max_tokens"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LlmBlueprintVectorDatabaseSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LlmBlueprintVectorDatabaseSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LlmBlueprintVectorDatabaseSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 max_documents_retrieved_per_prompt: Optional[int] = None,
                 max_tokens: Optional[int] = None):
        """
        :param int max_documents_retrieved_per_prompt: The maximum number of documents to retrieve from the Vector Database.
        :param int max_tokens: The maximum number of tokens to retrieve from the Vector Database.
        """
        if max_documents_retrieved_per_prompt is not None:
            pulumi.set(__self__, "max_documents_retrieved_per_prompt", max_documents_retrieved_per_prompt)
        if max_tokens is not None:
            pulumi.set(__self__, "max_tokens", max_tokens)

    @property
    @pulumi.getter(name="maxDocumentsRetrievedPerPrompt")
    def max_documents_retrieved_per_prompt(self) -> Optional[int]:
        """
        The maximum number of documents to retrieve from the Vector Database.
        """
        return pulumi.get(self, "max_documents_retrieved_per_prompt")

    @property
    @pulumi.getter(name="maxTokens")
    def max_tokens(self) -> Optional[int]:
        """
        The maximum number of tokens to retrieve from the Vector Database.
        """
        return pulumi.get(self, "max_tokens")


@pulumi.output_type
class VectorDatabaseChunkingParameters(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "chunkOverlapPercentage":
            suggest = "chunk_overlap_percentage"
        elif key == "chunkSize":
            suggest = "chunk_size"
        elif key == "chunkingMethod":
            suggest = "chunking_method"
        elif key == "embeddingModel":
            suggest = "embedding_model"
        elif key == "isSeparatorRegex":
            suggest = "is_separator_regex"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VectorDatabaseChunkingParameters. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VectorDatabaseChunkingParameters.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VectorDatabaseChunkingParameters.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 chunk_overlap_percentage: Optional[int] = None,
                 chunk_size: Optional[int] = None,
                 chunking_method: Optional[str] = None,
                 embedding_model: Optional[str] = None,
                 is_separator_regex: Optional[bool] = None,
                 separators: Optional[Sequence[str]] = None):
        """
        :param int chunk_overlap_percentage: The percentage of overlap between chunks.
        :param int chunk_size: The size of the chunks.
        :param str chunking_method: The method used to chunk the data.
        :param str embedding_model: The id of the Embedding Model.
        :param bool is_separator_regex: Whether the separator is a regex.
        :param Sequence[str] separators: The separators used to split the data.
        """
        if chunk_overlap_percentage is not None:
            pulumi.set(__self__, "chunk_overlap_percentage", chunk_overlap_percentage)
        if chunk_size is not None:
            pulumi.set(__self__, "chunk_size", chunk_size)
        if chunking_method is not None:
            pulumi.set(__self__, "chunking_method", chunking_method)
        if embedding_model is not None:
            pulumi.set(__self__, "embedding_model", embedding_model)
        if is_separator_regex is not None:
            pulumi.set(__self__, "is_separator_regex", is_separator_regex)
        if separators is not None:
            pulumi.set(__self__, "separators", separators)

    @property
    @pulumi.getter(name="chunkOverlapPercentage")
    def chunk_overlap_percentage(self) -> Optional[int]:
        """
        The percentage of overlap between chunks.
        """
        return pulumi.get(self, "chunk_overlap_percentage")

    @property
    @pulumi.getter(name="chunkSize")
    def chunk_size(self) -> Optional[int]:
        """
        The size of the chunks.
        """
        return pulumi.get(self, "chunk_size")

    @property
    @pulumi.getter(name="chunkingMethod")
    def chunking_method(self) -> Optional[str]:
        """
        The method used to chunk the data.
        """
        return pulumi.get(self, "chunking_method")

    @property
    @pulumi.getter(name="embeddingModel")
    def embedding_model(self) -> Optional[str]:
        """
        The id of the Embedding Model.
        """
        return pulumi.get(self, "embedding_model")

    @property
    @pulumi.getter(name="isSeparatorRegex")
    def is_separator_regex(self) -> Optional[bool]:
        """
        Whether the separator is a regex.
        """
        return pulumi.get(self, "is_separator_regex")

    @property
    @pulumi.getter
    def separators(self) -> Optional[Sequence[str]]:
        """
        The separators used to split the data.
        """
        return pulumi.get(self, "separators")


