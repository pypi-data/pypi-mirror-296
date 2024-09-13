# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'ApplicationSourceResourceSettingsArgs',
    'ApplicationSourceRuntimeParameterValueArgs',
    'CustomModelGuardConfigurationArgs',
    'CustomModelGuardConfigurationInterventionArgs',
    'CustomModelGuardConfigurationInterventionConditionArgs',
    'CustomModelOverallModerationConfigurationArgs',
    'CustomModelResourceSettingsArgs',
    'CustomModelRuntimeParameterValueArgs',
    'CustomModelSourceRemoteRepositoryArgs',
    'DeploymentSettingsArgs',
    'DeploymentSettingsAssociationIdArgs',
    'DeploymentSettingsPredictionsSettingsArgs',
    'LlmBlueprintLlmSettingsArgs',
    'LlmBlueprintVectorDatabaseSettingsArgs',
    'VectorDatabaseChunkingParametersArgs',
]

@pulumi.input_type
class ApplicationSourceResourceSettingsArgs:
    def __init__(__self__, *,
                 replicas: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] replicas: The replicas for the Application Source.
        """
        if replicas is not None:
            pulumi.set(__self__, "replicas", replicas)

    @property
    @pulumi.getter
    def replicas(self) -> Optional[pulumi.Input[int]]:
        """
        The replicas for the Application Source.
        """
        return pulumi.get(self, "replicas")

    @replicas.setter
    def replicas(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "replicas", value)


@pulumi.input_type
class ApplicationSourceRuntimeParameterValueArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 type: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: The name of the runtime parameter.
        :param pulumi.Input[str] type: The type of the runtime parameter.
        :param pulumi.Input[str] value: The value of the runtime parameter (type conversion is handled internally).
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The name of the runtime parameter.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of the runtime parameter.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the runtime parameter (type conversion is handled internally).
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class CustomModelGuardConfigurationArgs:
    def __init__(__self__, *,
                 intervention: pulumi.Input['CustomModelGuardConfigurationInterventionArgs'],
                 name: pulumi.Input[str],
                 stages: pulumi.Input[Sequence[pulumi.Input[str]]],
                 template_name: pulumi.Input[str],
                 deployment_id: Optional[pulumi.Input[str]] = None,
                 input_column_name: Optional[pulumi.Input[str]] = None,
                 llm_type: Optional[pulumi.Input[str]] = None,
                 openai_api_base: Optional[pulumi.Input[str]] = None,
                 openai_credential: Optional[pulumi.Input[str]] = None,
                 openai_deployment_id: Optional[pulumi.Input[str]] = None,
                 output_column_name: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input['CustomModelGuardConfigurationInterventionArgs'] intervention: The intervention for the guard configuration.
        :param pulumi.Input[str] name: The name of the guard configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] stages: The list of stages for the guard configuration.
        :param pulumi.Input[str] template_name: The template name of the guard configuration.
        :param pulumi.Input[str] deployment_id: The deployment ID of this guard.
        :param pulumi.Input[str] input_column_name: The input column name of this guard.
        :param pulumi.Input[str] llm_type: The LLM type for this guard.
        :param pulumi.Input[str] openai_api_base: The OpenAI API base URL for this guard.
        :param pulumi.Input[str] openai_credential: The ID of an OpenAI credential for this guard.
        :param pulumi.Input[str] openai_deployment_id: The ID of an OpenAI deployment for this guard.
        :param pulumi.Input[str] output_column_name: The output column name of this guard.
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
    def intervention(self) -> pulumi.Input['CustomModelGuardConfigurationInterventionArgs']:
        """
        The intervention for the guard configuration.
        """
        return pulumi.get(self, "intervention")

    @intervention.setter
    def intervention(self, value: pulumi.Input['CustomModelGuardConfigurationInterventionArgs']):
        pulumi.set(self, "intervention", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the guard configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def stages(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The list of stages for the guard configuration.
        """
        return pulumi.get(self, "stages")

    @stages.setter
    def stages(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "stages", value)

    @property
    @pulumi.getter(name="templateName")
    def template_name(self) -> pulumi.Input[str]:
        """
        The template name of the guard configuration.
        """
        return pulumi.get(self, "template_name")

    @template_name.setter
    def template_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "template_name", value)

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> Optional[pulumi.Input[str]]:
        """
        The deployment ID of this guard.
        """
        return pulumi.get(self, "deployment_id")

    @deployment_id.setter
    def deployment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deployment_id", value)

    @property
    @pulumi.getter(name="inputColumnName")
    def input_column_name(self) -> Optional[pulumi.Input[str]]:
        """
        The input column name of this guard.
        """
        return pulumi.get(self, "input_column_name")

    @input_column_name.setter
    def input_column_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "input_column_name", value)

    @property
    @pulumi.getter(name="llmType")
    def llm_type(self) -> Optional[pulumi.Input[str]]:
        """
        The LLM type for this guard.
        """
        return pulumi.get(self, "llm_type")

    @llm_type.setter
    def llm_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "llm_type", value)

    @property
    @pulumi.getter(name="openaiApiBase")
    def openai_api_base(self) -> Optional[pulumi.Input[str]]:
        """
        The OpenAI API base URL for this guard.
        """
        return pulumi.get(self, "openai_api_base")

    @openai_api_base.setter
    def openai_api_base(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "openai_api_base", value)

    @property
    @pulumi.getter(name="openaiCredential")
    def openai_credential(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of an OpenAI credential for this guard.
        """
        return pulumi.get(self, "openai_credential")

    @openai_credential.setter
    def openai_credential(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "openai_credential", value)

    @property
    @pulumi.getter(name="openaiDeploymentId")
    def openai_deployment_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of an OpenAI deployment for this guard.
        """
        return pulumi.get(self, "openai_deployment_id")

    @openai_deployment_id.setter
    def openai_deployment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "openai_deployment_id", value)

    @property
    @pulumi.getter(name="outputColumnName")
    def output_column_name(self) -> Optional[pulumi.Input[str]]:
        """
        The output column name of this guard.
        """
        return pulumi.get(self, "output_column_name")

    @output_column_name.setter
    def output_column_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "output_column_name", value)


@pulumi.input_type
class CustomModelGuardConfigurationInterventionArgs:
    def __init__(__self__, *,
                 action: pulumi.Input[str],
                 condition: pulumi.Input['CustomModelGuardConfigurationInterventionConditionArgs'],
                 message: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] action: The action of the guard intervention.
        :param pulumi.Input['CustomModelGuardConfigurationInterventionConditionArgs'] condition: The list of conditions for the guard intervention.
        :param pulumi.Input[str] message: The message of the guard intervention.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "condition", condition)
        if message is not None:
            pulumi.set(__self__, "message", message)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[str]:
        """
        The action of the guard intervention.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[str]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Input['CustomModelGuardConfigurationInterventionConditionArgs']:
        """
        The list of conditions for the guard intervention.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: pulumi.Input['CustomModelGuardConfigurationInterventionConditionArgs']):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        The message of the guard intervention.
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message", value)


@pulumi.input_type
class CustomModelGuardConfigurationInterventionConditionArgs:
    def __init__(__self__, *,
                 comparand: pulumi.Input[float],
                 comparator: pulumi.Input[str]):
        """
        :param pulumi.Input[float] comparand: The comparand of the guard condition.
        :param pulumi.Input[str] comparator: The comparator of the guard condition.
        """
        pulumi.set(__self__, "comparand", comparand)
        pulumi.set(__self__, "comparator", comparator)

    @property
    @pulumi.getter
    def comparand(self) -> pulumi.Input[float]:
        """
        The comparand of the guard condition.
        """
        return pulumi.get(self, "comparand")

    @comparand.setter
    def comparand(self, value: pulumi.Input[float]):
        pulumi.set(self, "comparand", value)

    @property
    @pulumi.getter
    def comparator(self) -> pulumi.Input[str]:
        """
        The comparator of the guard condition.
        """
        return pulumi.get(self, "comparator")

    @comparator.setter
    def comparator(self, value: pulumi.Input[str]):
        pulumi.set(self, "comparator", value)


@pulumi.input_type
class CustomModelOverallModerationConfigurationArgs:
    def __init__(__self__, *,
                 timeout_action: Optional[pulumi.Input[str]] = None,
                 timeout_sec: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] timeout_action: The timeout action of the overall moderation configuration.
        :param pulumi.Input[int] timeout_sec: The timeout in seconds of the overall moderation configuration.
        """
        if timeout_action is not None:
            pulumi.set(__self__, "timeout_action", timeout_action)
        if timeout_sec is not None:
            pulumi.set(__self__, "timeout_sec", timeout_sec)

    @property
    @pulumi.getter(name="timeoutAction")
    def timeout_action(self) -> Optional[pulumi.Input[str]]:
        """
        The timeout action of the overall moderation configuration.
        """
        return pulumi.get(self, "timeout_action")

    @timeout_action.setter
    def timeout_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "timeout_action", value)

    @property
    @pulumi.getter(name="timeoutSec")
    def timeout_sec(self) -> Optional[pulumi.Input[int]]:
        """
        The timeout in seconds of the overall moderation configuration.
        """
        return pulumi.get(self, "timeout_sec")

    @timeout_sec.setter
    def timeout_sec(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout_sec", value)


@pulumi.input_type
class CustomModelResourceSettingsArgs:
    def __init__(__self__, *,
                 memory_mb: Optional[pulumi.Input[int]] = None,
                 network_access: Optional[pulumi.Input[str]] = None,
                 replicas: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] memory_mb: The memory in MB for the Custom Model.
        :param pulumi.Input[str] network_access: The network access for the Custom Model.
        :param pulumi.Input[int] replicas: The replicas for the Custom Model.
        """
        if memory_mb is not None:
            pulumi.set(__self__, "memory_mb", memory_mb)
        if network_access is not None:
            pulumi.set(__self__, "network_access", network_access)
        if replicas is not None:
            pulumi.set(__self__, "replicas", replicas)

    @property
    @pulumi.getter(name="memoryMb")
    def memory_mb(self) -> Optional[pulumi.Input[int]]:
        """
        The memory in MB for the Custom Model.
        """
        return pulumi.get(self, "memory_mb")

    @memory_mb.setter
    def memory_mb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "memory_mb", value)

    @property
    @pulumi.getter(name="networkAccess")
    def network_access(self) -> Optional[pulumi.Input[str]]:
        """
        The network access for the Custom Model.
        """
        return pulumi.get(self, "network_access")

    @network_access.setter
    def network_access(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_access", value)

    @property
    @pulumi.getter
    def replicas(self) -> Optional[pulumi.Input[int]]:
        """
        The replicas for the Custom Model.
        """
        return pulumi.get(self, "replicas")

    @replicas.setter
    def replicas(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "replicas", value)


@pulumi.input_type
class CustomModelRuntimeParameterValueArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 type: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: The name of the runtime parameter.
        :param pulumi.Input[str] type: The type of the runtime parameter.
        :param pulumi.Input[str] value: The value of the runtime parameter (type conversion is handled internally).
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The name of the runtime parameter.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of the runtime parameter.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the runtime parameter (type conversion is handled internally).
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class CustomModelSourceRemoteRepositoryArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str],
                 ref: pulumi.Input[str],
                 source_paths: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        :param pulumi.Input[str] id: The ID of the source remote repository.
        :param pulumi.Input[str] ref: The reference of the source remote repository.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_paths: The list of source paths in the source remote repository.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "ref", ref)
        pulumi.set(__self__, "source_paths", source_paths)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        The ID of the source remote repository.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def ref(self) -> pulumi.Input[str]:
        """
        The reference of the source remote repository.
        """
        return pulumi.get(self, "ref")

    @ref.setter
    def ref(self, value: pulumi.Input[str]):
        pulumi.set(self, "ref", value)

    @property
    @pulumi.getter(name="sourcePaths")
    def source_paths(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The list of source paths in the source remote repository.
        """
        return pulumi.get(self, "source_paths")

    @source_paths.setter
    def source_paths(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "source_paths", value)


@pulumi.input_type
class DeploymentSettingsArgs:
    def __init__(__self__, *,
                 association_id: Optional[pulumi.Input['DeploymentSettingsAssociationIdArgs']] = None,
                 challenger_analysis: Optional[pulumi.Input[bool]] = None,
                 prediction_row_storage: Optional[pulumi.Input[bool]] = None,
                 predictions_settings: Optional[pulumi.Input['DeploymentSettingsPredictionsSettingsArgs']] = None):
        """
        :param pulumi.Input['DeploymentSettingsAssociationIdArgs'] association_id: Used to associate predictions back to your actual data.
        :param pulumi.Input[bool] challenger_analysis: Used to compare the performance of the deployed model with the challenger models.
        :param pulumi.Input[bool] prediction_row_storage: Used to score predictions made by the challenger models and compare performance with the deployed model.
        :param pulumi.Input['DeploymentSettingsPredictionsSettingsArgs'] predictions_settings: Settings for the predictions.
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
    def association_id(self) -> Optional[pulumi.Input['DeploymentSettingsAssociationIdArgs']]:
        """
        Used to associate predictions back to your actual data.
        """
        return pulumi.get(self, "association_id")

    @association_id.setter
    def association_id(self, value: Optional[pulumi.Input['DeploymentSettingsAssociationIdArgs']]):
        pulumi.set(self, "association_id", value)

    @property
    @pulumi.getter(name="challengerAnalysis")
    def challenger_analysis(self) -> Optional[pulumi.Input[bool]]:
        """
        Used to compare the performance of the deployed model with the challenger models.
        """
        return pulumi.get(self, "challenger_analysis")

    @challenger_analysis.setter
    def challenger_analysis(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "challenger_analysis", value)

    @property
    @pulumi.getter(name="predictionRowStorage")
    def prediction_row_storage(self) -> Optional[pulumi.Input[bool]]:
        """
        Used to score predictions made by the challenger models and compare performance with the deployed model.
        """
        return pulumi.get(self, "prediction_row_storage")

    @prediction_row_storage.setter
    def prediction_row_storage(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "prediction_row_storage", value)

    @property
    @pulumi.getter(name="predictionsSettings")
    def predictions_settings(self) -> Optional[pulumi.Input['DeploymentSettingsPredictionsSettingsArgs']]:
        """
        Settings for the predictions.
        """
        return pulumi.get(self, "predictions_settings")

    @predictions_settings.setter
    def predictions_settings(self, value: Optional[pulumi.Input['DeploymentSettingsPredictionsSettingsArgs']]):
        pulumi.set(self, "predictions_settings", value)


@pulumi.input_type
class DeploymentSettingsAssociationIdArgs:
    def __init__(__self__, *,
                 auto_generate_id: pulumi.Input[bool],
                 feature_name: pulumi.Input[str],
                 required_in_prediction_requests: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] auto_generate_id: Whether to automatically generate an association ID.
        :param pulumi.Input[str] feature_name: The name of the feature to use as the association ID.
        :param pulumi.Input[bool] required_in_prediction_requests: Whether the association ID is required in prediction requests.
        """
        pulumi.set(__self__, "auto_generate_id", auto_generate_id)
        pulumi.set(__self__, "feature_name", feature_name)
        pulumi.set(__self__, "required_in_prediction_requests", required_in_prediction_requests)

    @property
    @pulumi.getter(name="autoGenerateId")
    def auto_generate_id(self) -> pulumi.Input[bool]:
        """
        Whether to automatically generate an association ID.
        """
        return pulumi.get(self, "auto_generate_id")

    @auto_generate_id.setter
    def auto_generate_id(self, value: pulumi.Input[bool]):
        pulumi.set(self, "auto_generate_id", value)

    @property
    @pulumi.getter(name="featureName")
    def feature_name(self) -> pulumi.Input[str]:
        """
        The name of the feature to use as the association ID.
        """
        return pulumi.get(self, "feature_name")

    @feature_name.setter
    def feature_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "feature_name", value)

    @property
    @pulumi.getter(name="requiredInPredictionRequests")
    def required_in_prediction_requests(self) -> pulumi.Input[bool]:
        """
        Whether the association ID is required in prediction requests.
        """
        return pulumi.get(self, "required_in_prediction_requests")

    @required_in_prediction_requests.setter
    def required_in_prediction_requests(self, value: pulumi.Input[bool]):
        pulumi.set(self, "required_in_prediction_requests", value)


@pulumi.input_type
class DeploymentSettingsPredictionsSettingsArgs:
    def __init__(__self__, *,
                 max_computes: pulumi.Input[int],
                 min_computes: pulumi.Input[int],
                 real_time: pulumi.Input[bool]):
        """
        :param pulumi.Input[int] max_computes: The maximum number of computes to use for predictions.
        :param pulumi.Input[int] min_computes: The minimum number of computes to use for predictions.
        :param pulumi.Input[bool] real_time: Whether to use real-time predictions.
        """
        pulumi.set(__self__, "max_computes", max_computes)
        pulumi.set(__self__, "min_computes", min_computes)
        pulumi.set(__self__, "real_time", real_time)

    @property
    @pulumi.getter(name="maxComputes")
    def max_computes(self) -> pulumi.Input[int]:
        """
        The maximum number of computes to use for predictions.
        """
        return pulumi.get(self, "max_computes")

    @max_computes.setter
    def max_computes(self, value: pulumi.Input[int]):
        pulumi.set(self, "max_computes", value)

    @property
    @pulumi.getter(name="minComputes")
    def min_computes(self) -> pulumi.Input[int]:
        """
        The minimum number of computes to use for predictions.
        """
        return pulumi.get(self, "min_computes")

    @min_computes.setter
    def min_computes(self, value: pulumi.Input[int]):
        pulumi.set(self, "min_computes", value)

    @property
    @pulumi.getter(name="realTime")
    def real_time(self) -> pulumi.Input[bool]:
        """
        Whether to use real-time predictions.
        """
        return pulumi.get(self, "real_time")

    @real_time.setter
    def real_time(self, value: pulumi.Input[bool]):
        pulumi.set(self, "real_time", value)


@pulumi.input_type
class LlmBlueprintLlmSettingsArgs:
    def __init__(__self__, *,
                 max_completion_length: Optional[pulumi.Input[int]] = None,
                 system_prompt: Optional[pulumi.Input[str]] = None,
                 temperature: Optional[pulumi.Input[float]] = None,
                 top_p: Optional[pulumi.Input[float]] = None):
        """
        :param pulumi.Input[int] max_completion_length: The maximum number of tokens allowed in the completion. The combined count of this value and prompt tokens must be below the model's maximum context size, where prompt token count is comprised of system prompt, user prompt, recent chat history, and vector database citations.
        :param pulumi.Input[str] system_prompt: Guides the style of the LLM response. It is a 'universal' prompt, prepended to all individual prompts.
        :param pulumi.Input[float] temperature: Controls the randomness of model output, where higher values return more diverse output and lower values return more deterministic results.
        :param pulumi.Input[float] top_p: Threshold that controls the selection of words included in the response, based on a cumulative probability cutoff for token selection. Higher numbers return more diverse options for outputs.
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
    def max_completion_length(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of tokens allowed in the completion. The combined count of this value and prompt tokens must be below the model's maximum context size, where prompt token count is comprised of system prompt, user prompt, recent chat history, and vector database citations.
        """
        return pulumi.get(self, "max_completion_length")

    @max_completion_length.setter
    def max_completion_length(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_completion_length", value)

    @property
    @pulumi.getter(name="systemPrompt")
    def system_prompt(self) -> Optional[pulumi.Input[str]]:
        """
        Guides the style of the LLM response. It is a 'universal' prompt, prepended to all individual prompts.
        """
        return pulumi.get(self, "system_prompt")

    @system_prompt.setter
    def system_prompt(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "system_prompt", value)

    @property
    @pulumi.getter
    def temperature(self) -> Optional[pulumi.Input[float]]:
        """
        Controls the randomness of model output, where higher values return more diverse output and lower values return more deterministic results.
        """
        return pulumi.get(self, "temperature")

    @temperature.setter
    def temperature(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "temperature", value)

    @property
    @pulumi.getter(name="topP")
    def top_p(self) -> Optional[pulumi.Input[float]]:
        """
        Threshold that controls the selection of words included in the response, based on a cumulative probability cutoff for token selection. Higher numbers return more diverse options for outputs.
        """
        return pulumi.get(self, "top_p")

    @top_p.setter
    def top_p(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "top_p", value)


@pulumi.input_type
class LlmBlueprintVectorDatabaseSettingsArgs:
    def __init__(__self__, *,
                 max_documents_retrieved_per_prompt: Optional[pulumi.Input[int]] = None,
                 max_tokens: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] max_documents_retrieved_per_prompt: The maximum number of documents to retrieve from the Vector Database.
        :param pulumi.Input[int] max_tokens: The maximum number of tokens to retrieve from the Vector Database.
        """
        if max_documents_retrieved_per_prompt is not None:
            pulumi.set(__self__, "max_documents_retrieved_per_prompt", max_documents_retrieved_per_prompt)
        if max_tokens is not None:
            pulumi.set(__self__, "max_tokens", max_tokens)

    @property
    @pulumi.getter(name="maxDocumentsRetrievedPerPrompt")
    def max_documents_retrieved_per_prompt(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of documents to retrieve from the Vector Database.
        """
        return pulumi.get(self, "max_documents_retrieved_per_prompt")

    @max_documents_retrieved_per_prompt.setter
    def max_documents_retrieved_per_prompt(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_documents_retrieved_per_prompt", value)

    @property
    @pulumi.getter(name="maxTokens")
    def max_tokens(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of tokens to retrieve from the Vector Database.
        """
        return pulumi.get(self, "max_tokens")

    @max_tokens.setter
    def max_tokens(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_tokens", value)


@pulumi.input_type
class VectorDatabaseChunkingParametersArgs:
    def __init__(__self__, *,
                 chunk_overlap_percentage: Optional[pulumi.Input[int]] = None,
                 chunk_size: Optional[pulumi.Input[int]] = None,
                 chunking_method: Optional[pulumi.Input[str]] = None,
                 embedding_model: Optional[pulumi.Input[str]] = None,
                 is_separator_regex: Optional[pulumi.Input[bool]] = None,
                 separators: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[int] chunk_overlap_percentage: The percentage of overlap between chunks.
        :param pulumi.Input[int] chunk_size: The size of the chunks.
        :param pulumi.Input[str] chunking_method: The method used to chunk the data.
        :param pulumi.Input[str] embedding_model: The id of the Embedding Model.
        :param pulumi.Input[bool] is_separator_regex: Whether the separator is a regex.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] separators: The separators used to split the data.
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
    def chunk_overlap_percentage(self) -> Optional[pulumi.Input[int]]:
        """
        The percentage of overlap between chunks.
        """
        return pulumi.get(self, "chunk_overlap_percentage")

    @chunk_overlap_percentage.setter
    def chunk_overlap_percentage(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "chunk_overlap_percentage", value)

    @property
    @pulumi.getter(name="chunkSize")
    def chunk_size(self) -> Optional[pulumi.Input[int]]:
        """
        The size of the chunks.
        """
        return pulumi.get(self, "chunk_size")

    @chunk_size.setter
    def chunk_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "chunk_size", value)

    @property
    @pulumi.getter(name="chunkingMethod")
    def chunking_method(self) -> Optional[pulumi.Input[str]]:
        """
        The method used to chunk the data.
        """
        return pulumi.get(self, "chunking_method")

    @chunking_method.setter
    def chunking_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "chunking_method", value)

    @property
    @pulumi.getter(name="embeddingModel")
    def embedding_model(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the Embedding Model.
        """
        return pulumi.get(self, "embedding_model")

    @embedding_model.setter
    def embedding_model(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "embedding_model", value)

    @property
    @pulumi.getter(name="isSeparatorRegex")
    def is_separator_regex(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the separator is a regex.
        """
        return pulumi.get(self, "is_separator_regex")

    @is_separator_regex.setter
    def is_separator_regex(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_separator_regex", value)

    @property
    @pulumi.getter
    def separators(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The separators used to split the data.
        """
        return pulumi.get(self, "separators")

    @separators.setter
    def separators(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "separators", value)


