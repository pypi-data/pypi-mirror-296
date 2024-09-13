# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .api_token_credential import *
from .application_source import *
from .basic_credential import *
from .custom_application import *
from .custom_model import *
from .dataset_from_file import *
from .deployment import *
from .get_global_model import *
from .google_cloud_credential import *
from .llm_blueprint import *
from .playground import *
from .prediction_environment import *
from .provider import *
from .qa_application import *
from .registered_model import *
from .remote_repository import *
from .use_case import *
from .vector_database import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_datarobot.config as __config
    config = __config
else:
    config = _utilities.lazy_import('pulumi_datarobot.config')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "datarobot",
  "mod": "index/apiTokenCredential",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/apiTokenCredential:ApiTokenCredential": "ApiTokenCredential"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/applicationSource",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/applicationSource:ApplicationSource": "ApplicationSource"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/basicCredential",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/basicCredential:BasicCredential": "BasicCredential"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/customApplication",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/customApplication:CustomApplication": "CustomApplication"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/customModel",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/customModel:CustomModel": "CustomModel"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/datasetFromFile",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/datasetFromFile:DatasetFromFile": "DatasetFromFile"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/deployment",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/deployment:Deployment": "Deployment"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/googleCloudCredential",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/googleCloudCredential:GoogleCloudCredential": "GoogleCloudCredential"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/llmBlueprint",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/llmBlueprint:LlmBlueprint": "LlmBlueprint"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/playground",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/playground:Playground": "Playground"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/predictionEnvironment",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/predictionEnvironment:PredictionEnvironment": "PredictionEnvironment"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/qaApplication",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/qaApplication:QaApplication": "QaApplication"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/registeredModel",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/registeredModel:RegisteredModel": "RegisteredModel"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/remoteRepository",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/remoteRepository:RemoteRepository": "RemoteRepository"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/useCase",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/useCase:UseCase": "UseCase"
  }
 },
 {
  "pkg": "datarobot",
  "mod": "index/vectorDatabase",
  "fqn": "pulumi_datarobot",
  "classes": {
   "datarobot:index/vectorDatabase:VectorDatabase": "VectorDatabase"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "datarobot",
  "token": "pulumi:providers:datarobot",
  "fqn": "pulumi_datarobot",
  "class": "Provider"
 }
]
"""
)
