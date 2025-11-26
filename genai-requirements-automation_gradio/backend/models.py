from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class DocumentType(str, Enum):
    EPIC = "epic"
    STORY = "story"
    USE_CASE = "use_case"
    TECHNICAL_DESIGN = "technical_design"
    DATA_MODEL = "data_model"

class ADOWorkItem(BaseModel):
    title: str
    description: str
    work_item_type: str
    acceptance_criteria: Optional[str] = None
    priority: Optional[int] = 2

class Epic(BaseModel):
    title: str
    description: str
    business_value: str
    acceptance_criteria: str

class Story(BaseModel):
    title: str
    description: str
    acceptance_criteria: str
    story_points: Optional[int] = None
    epic_link: Optional[str] = None

class UseCase(BaseModel):
    title: str
    actor: str
    preconditions: str
    main_flow: List[str]
    alternative_flows: Optional[List[str]] = None
    postconditions: str

class TechnicalDesign(BaseModel):
    title: str
    overview: str
    architecture: str
    components: List[str]
    technologies: List[str]
    data_flow: str
    security_considerations: str

class DataModel(BaseModel):
    title: str
    entities: List[dict]
    relationships: List[dict]
    constraints: List[str]

class BusinessRequirementDoc(BaseModel):
    title: str
    executive_summary: str
    business_objectives: List[str]
    functional_requirements: List[str]
    non_functional_requirements: List[str]
    assumptions: List[str]
    constraints: List[str]

class FunctionalSpecDoc(BaseModel):
    title: str
    overview: str
    system_functions: List[dict]
    user_interfaces: List[dict]
    data_requirements: List[str]
    business_rules: List[str]
    validation_rules: List[str]

class TestCase(BaseModel):
    test_id: str
    test_name: str
    description: str
    preconditions: str
    test_steps: List[str]
    expected_result: str
    priority: str

class GeneratedDocuments(BaseModel):
    epics: List[Epic]
    stories: List[Story]
    use_cases: List[UseCase]
    technical_design: TechnicalDesign
    data_model: DataModel
    business_requirement_doc: Optional[BusinessRequirementDoc] = None
    functional_spec_doc: Optional[FunctionalSpecDoc] = None
    test_cases: Optional[List[TestCase]] = None