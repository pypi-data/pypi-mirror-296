Project description
CyClarity SDK

Introduction

CyClarity SDK is a Python package that provides an interface for interacting with the CyClarity platform. It includes classes and methods for creating, managing, and interacting with various resources on the platform.

Installation

You can install the CyClarity SDK using pip:

pip install cyclarity-sdk

Usage

Here are examples of how to use the classes in the CyClarity SDK. Runnable The Runnable class is a base class for creating objects that can be run with setup and teardown phases. It has setup, run, and teardown methods that need to be implemented. 

This is the structure of a runnable:
```python
from cyclarity_sdk.runnable import Runnable, BaseResultsModel

class MyResult(BaseResultsModel):
res_str: str

class MyRunnable(Runnable[MyResult]):
desc: str
cli_args: str
#self.platform_api inherited attribute,initiates PlatformApi class
def setup(self):  
    self.logger.info("Setting up")  
#the run function is the first function to be initiated when a runnable is executed.
def run(self):  
    self.logger.info("Running")  
    self.platform_api.send_test_report_description("This is a test description")  
    return MyResult(res_str="success!")  

def teardown(self, exception_type, exception_value, traceback):  
    self.logger.info("Tearing down")  


if you are working on the web snippet here is an example on how to create a runnable:

from typing import Optional
from cyclarity_sdk.expert_builder import Runnable, BaseResultsModel
from cyclarity_sdk.sdk_models.findings import PTFinding
import cyclarity_sdk.sdk_models.findings.types as PTFindingTypes
from cyclarity_sdk.sdk_models.types import ExecutionStatus

class SnippetResults(BaseResultsModel):
    test_output: str

class SnippetRunnable(Runnable[SnippetResults]):
    input_str: str = 'test'
    input_int: int = 0
    results: Optional[SnippetResults] = None
     
    def run(self) -> SnippetResults:
        self.platform_api.send_test_report_description('This is dummy description for test')
        self.platform_api.send_finding(PTFinding(topic='hello world', status=PTFindingTypes.FindingStatus.FINISHED, type=PTFindingTypes.FindingType.FINDING, assessment_category=PTFindingTypes.AssessmentCategory.FUNCTIONAL_TEST, assessment_technique=PTFindingTypes.AssessmentTechnique.OTHER_EXPLORATION, purpose='Snippet example', description='This is an example snippet on how to user platform_api'))
        self.platform_api.send_execution_state(1, ExecutionStatus.RUNNING)
        return SnippetResults(test_output='success')

    def setup(self):
        self.logger.info('setting up SnippetRunnable')

    def teardown(self, exception_type=None, exception_value=None, traceback=None):
        self.logger.info('setting up SnippetRunnable')

PlatformApi
The PlatformApi class provides methods for interacting with the CyClarity platform. It is used within a Runnable instance through the self.platform_api attribute.

from _typeshed import Incomplete
from cyclarity_sdk.platform_api.Iplatform_connector import IPlatformConnectorApi as IPlatformConnectorApi
from cyclarity_sdk.sdk_models.findings import PTFinding as PTFinding

class PlatformApi:
    def __init__(self, platform_connector: IPlatformConnectorApi | None = None) -> None: ...
    def send_test_report_description(self, description: str): ...
    def send_finding(self, pt_finding: PTFinding): ...
    def report_test_progress(self, percentage: int): ...

### Additional Classes Used by PlatformApi

The `PlatformApi` class utilizes several additional classes for its functionality, which are imported from various modules. Here are these classes along with their definitions:

```python
from pydantic import BaseModel
from cyclarity_sdk.sdk_models import ExecutionMetadata, MessageType
from cyclarity_sdk.sdk_models.artifacts.types import ArtifactType

class TestArtifact(BaseModel):
    execution_metadata: ExecutionMetadata
    type: MessageType
    data: TestReportDescription | ScanGraph

class TestReportDescription(BaseModel):
    type: ArtifactType
    description: str

class ArtifactType(str, Enum):
    REPORT_DESCRIPTION = 'report_description'
    SCAN_GRAPH = 'scan_graph'


from pydantic import BaseModel, Field, computed_field, field_validator
from enum import Enum
from .types import FindingStatus, FindingType, AssessmentCategory, AssessmentTechnique,FindingModelType
from cyclarity_sdk.sdk_models import ExecutionMetadata, MessageType

class Finding(BaseModel):
    metadata: ExecutionMetadata
    model_type: FindingModelType
    data: PTFinding
    type: MessageType

class PTFinding(BaseModel):
    topic: str
    status: FindingStatus
    type: FindingType
    assessment_category: AssessmentCategory
    assessment_technique: AssessmentTechnique
    purpose: str
    description: str

class FindingModelType(str, Enum):
    PT_FINDING = 'pt_finding'

class FindingStatus(str, Enum):
    FINISHED = 'Finished'
    PARTIALLY_PERFORMED = 'Partially Performed'
    NOT_PERFORMED = 'Not Performed'

class FindingType(str, Enum):
    FINDING = 'Finding'
    NON_FINDING = 'Non Finding'
    INSIGHT = 'Insight'
    ADDITIONAL_INFORMATION = 'Additional Information'

class AssessmentCategory(str, Enum):
    FUNCTIONAL_TEST = 'functional test'
    PENTEST = 'pentest'
    VULNERABILITY_ANALYSIS = 'vulnerability analysis'
    INCIDENT = 'incident'
    CODE_REVIEW = 'code review'
    UNKNOWN = 'unknown'

class AssessmentTechnique(str, Enum):
    SPEC_BASED_TEST_CASE = 'specification-based test case'
    HARDWARE_ANALYSIS = 'hardware analysis'
    BINARY_ANALYSIS = 'binary analysis'
    INTERFACE_ANALYSIS = 'interface analysis'
    NETWORK_ANALYSIS = 'network analysis'
    CODE_REVIEW = 'code review'
    SPECIFICATION_REVIEW = 'specification review'
    CVE_SEARCH = 'CVE search'
    OTHER_EXPLORATION = 'other exploration'
    UNKNOWN = 'unknown'


from typing import Optional
from pydantic import BaseModel
from enum import Enum
from cyclarity_sdk.sdk_models.types import ExecutionStatus 
class ExecutionMetadata(BaseModel):
    execution_id: str
    agent_id: str | None
    test_id: str
    step_id: str | None
    step_name: str | None
    step_version: str | None

class ExecutionState(BaseModel):
    execution_metadata: ExecutionMetadata
    percentage: int
    status: ExecutionStatus
    error_message: str | None

class ExecutionStatus(str, Enum):
    TIMEOUT = 'TIMEOUT'
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    COMPLETED_SUCCESSFULLY = 'COMPLETED'
    COMPLETED_WITH_ERROR = 'FAILED'
    STOPPED = 'STOPPED'

class MessageType(str, Enum):
    LOG = 'LOG'
    TEST_STATE = 'TEST_STATE'
    EXECUTION_STATE = 'EXECUTION_STATE'
    FINDING = 'FINDING'
    TEST_ARTIFACT = 'TEST_ARTIFACT'
    EXECUTION_OUTPUT = 'EXECUTION_OUTPUT'

    Equipment, KnowledgeOfTarget, FindingModelType, RiskModel
## Dependencies

This package requires Python 3.x. It also depends on the following Python libraries:

- pydantic
- _typeshed
- typing

