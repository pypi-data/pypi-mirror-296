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

from cyclarity_sdk.platform_api.Iplatform_connector import IPlatformConnectorApi
from cyclarity_sdk.platform_api.connectors.cli_connector import CliConnector
from cyclarity_sdk.sdk_models.artifacts import TestArtifact, TestReportDescription, ArtifactType
from cyclarity_sdk.sdk_models.findings import Finding, PTFinding, FindingModelType
from cyclarity_sdk.sdk_models import ExecutionState, ExecutionStatus
from clarity_common.models.common_models.models import MessageType
from typing import Optional

class PlatformApi:
    def __init__(self, platform_connector: Optional[IPlatformConnectorApi] = None):
        if not platform_connector:
            platform_connector = CliConnector()
        self.set_api(platform_connector)

    def set_api(self, platform_api: IPlatformConnectorApi):
        self.platform_connector = platform_api
    #the function we used in the example above
    def send_test_report_description(self, description: str):
        execution_metadata = self.platform_connector.get_execution_meta_data()

        test_report_description = TestReportDescription(
            type=ArtifactType.REPORT_DESCRIPTION,
            description=description
        )

        artifact = TestArtifact(
            execution_metadata=execution_metadata,
            type=MessageType.TEST_ARTIFACT,
            data=test_report_description
        )

        return self.platform_connector.send_artifact(artifact)

    def send_finding(self, pt_finding: PTFinding):
        execution_metadata = self.platform_connector.get_execution_meta_data()
        
        finding = Finding(
            metadata=execution_metadata,
            model_type=FindingModelType.PT_FINDING,
            data=pt_finding,
            type=MessageType.FINDING
        )

        return self.platform_connector.send_finding(finding)

    def send_execution_state(self, percentage: int, status: ExecutionStatus, error_message: str = None):
        execution_metadata = self.platform_connector.get_execution_meta_data()

        execution_state = ExecutionState(
            execution_metadata=execution_metadata,
            percentage=percentage,
            status=status,
            error_message=error_message
        )

        return self.platform_connector.send_state(execution_state)
In the
PlatformApi
class, the
execution_metadata
is fetched using the
get_execution_meta_data()
method of the
platform_connector

### Additional Classes Used by PlatformApi

The `PlatformApi` class utilizes several additional classes for its functionality, which are imported from various modules. Here are these classes along with their definitions:

```python
from cyclarity_sdk.platform_api.Iplatform_connector import IPlatformConnectorApi

class IPlatformConnectorApi(ABC):
    @abstractmethod
    def send_artifact(self, test_artifact: TestArtifact):
        raise NotImplementedError(
            f'send_artifact was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def send_finding(self, finding: Finding):
        raise NotImplementedError(
            f'send_finding was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def send_state(self, execution_state: ExecutionState):
        raise NotImplementedError(
            f'send_state was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def get_execution_meta_data(self) -> ExecutionMetadata:
        raise NotImplementedError(
            f'send_state was not defined for class {self.__class__.__name__}')  # noqa


from cyclarity_sdk.sdk_models.artifacts import TestArtifact, TestReportDescription,ArtifactType
class TestArtifact(BaseModel):
    execution_metadata: ExecutionMetadata
    type: MessageType = MessageType.TEST_ARTIFACT
    data: Union[TestReportDescription, ScanGraph]

class TestReportDescription(BaseModel):
    type: ArtifactType
    description: str

class ArtifactType(str, Enum):
    ''' ____WARNING____'''
    '''Please note that changing this strings can effect visualization of
      results in the reports because we query artifact table base on those and
      they kept in the artifacts table in the subtype attribute as strings '''

    REPORT_DESCRIPTION = "report_description"
    SCAN_GRAPH = "scan_graph"

from cyclarity_sdk.sdk_models.findings import Finding, PTFinding, FindingModelType
from typing import Optional

class Finding(BaseModel):
    metadata: ExecutionMetadata
    model_type: FindingModelType
    data: PTFinding
    type: MessageType = MessageType.FINDING

    @computed_field
    @property
    def subtype(self) -> FindingType:
        return self.data.type

class PTFinding(BaseModel):
    topic: str = Field(description="Subject")
    status: FindingStatus = Field(description="status of the finding")
    type: FindingType = Field(description="The type of the finding")
    assessment_category: AssessmentCategory = Field(AssessmentCategory.PENTEST, description="assessment category")  # noqa
    assessment_technique: AssessmentTechnique = Field(AssessmentTechnique.NETWORK_ANALYSIS, description="assessment technique")  # noqa
    purpose: str = Field(description="purpose of the test")
    description: str = Field(description="description")
    preconditions: Optional[str] = Field(None, description="precondition for the test")  # noqa
    steps: Optional[str] = Field(None, description="steps performed for executing the test")  # noqa
    threat: Optional[str] = Field(None, description="threat description")
    recommendations: Optional[str] = Field(None, description="recommendations")
    expertise: Optional[Expertise] = Field(None, description="expertise needed by the attack in order to manipulate it")  # noqa
    access: Optional[Access] = Field(None, description="access needed in order to perform this attack")  # noqa
    time: Optional[ElapsedTime] = Field(None, description="the estimated time it takes to execute the exploit")  # noqa
    equipment: Optional[Equipment] = Field(None, description="required equipment level needed in order to execute the exploit")  # noqa
    knowledge_of_target: Optional[KnowledgeOfTarget] = Field(None, description="")  # noqa
    cwe_number: Optional[int] = Field(None, description="cwe num")

    # Custom validator that checks if different fields are matching 'RiskModel'
    @field_validator('expertise', 'access', 'time', 'equipment',
                     'knowledge_of_target', mode="before")
    def convert_enum_attributes_to_model(cls, v, info):
        """
        Convert enums values to pydantic model
        """
        field_to_enum_mapping = {
            'expertise': Expertise,
            'access': Access,
            'time': ElapsedTime,
            'equipment': Equipment,
            'knowledge_of_target': KnowledgeOfTarget
        }
        enum_class = field_to_enum_mapping.get(info.field_name)
        if not enum_class:
            raise ValueError(f"No enum class found for field "
                             f"{info.field_name}")
        if isinstance(v, dict):
            # Cover the case where the information is already a dict.
            return RiskModel(**v)
        if isinstance(v, str):
            try:
                return getattr(enum_class, v)
            except AttributeError:
                raise ValueError(f"{v} is not a valid value for enum class"
                                 f" {enum_class} and field {info.field_name}")
        return v

    @computed_field
    @property
    def cwe_description(self) -> str:
        try:
            cwe_db = CWEDatabase()
            weakness = cwe_db.get(self.cwe_number)
            return weakness.description
        except Exception:
            return 'N.A'  # not available

    @computed_field
    @property
    def sum(self) -> int:
        risk_sum = 0
        for field_name, field_value in self:
            if isinstance(field_value, Enum) and isinstance(
                    field_value.value, RiskModel):
                risk_sum += field_value.value.risk_value
        return risk_sum

    @computed_field
    @property
    def attack_difficulty(self) -> str:
        if self.type != FindingType.FINDING:
            return "None"
        elif self.sum < 14:
            return "Very Low"
        elif self.sum < 20:
            return "Low"
        elif self.sum < 25:
            return "Moderate"
        elif self.sum < 35:
            return "High"
        return "Very High"


class Finding(BaseModel):
    metadata: ExecutionMetadata
    model_type: FindingModelType
    data: PTFinding
    type: MessageType = MessageType.FINDING

    @computed_field
    @property
    def subtype(self) -> FindingType:
        return self.data.type

class FindingModelType(str, Enum):
    PT_FINDING = "pt_finding"

from cyclarity_sdk.sdk_models import ExecutionState, ExecutionStatus
class ExecutionState(BaseModel):
    '''Data structure to be send via topic::execution-state'''
    execution_metadata: ExecutionMetadata
    percentage: int
    status: ExecutionStatus
    error_message: Optional[str]

class ExecutionStatus(str, Enum):
    TIMEOUT = "TIMEOUT"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED_SUCCESSFULLY = "COMPLETED"
    COMPLETED_WITH_ERROR = "FAILED"
    STOPPED = "STOPPED"

from clarity_common.models.common_models.models import MessageType
class MessageType(str, Enum):
    # Supported types for test step deployment
    LOG = "LOG"
    TEST_STATE = "TEST_STATE"
    EXECUTION_STATE = "EXECUTION_STATE"
    FINDING = "FINDING"
    TEST_ARTIFACT = "TEST_ARTIFACT"
    EXECUTION_OUTPUT = "EXECUTION_OUTPUT"


