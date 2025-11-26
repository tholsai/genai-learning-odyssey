import openai
import json
from typing import Dict, Any
from models import GeneratedDocuments, Epic, Story, UseCase, TechnicalDesign, DataModel, BusinessRequirementDoc, FunctionalSpecDoc, TestCase

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_documents(self, business_requirements: str) -> GeneratedDocuments:
        """Generate all required documents from business requirements"""
        
        prompt = f"""
        Based on the following business requirements, generate comprehensive project documentation:

        BUSINESS REQUIREMENTS:
        {business_requirements}

        Please generate the following in valid JSON format:
        {{
            "epics": [
                {{
                    "title": "Epic title",
                    "description": "Detailed epic description",
                    "business_value": "Business value statement",
                    "acceptance_criteria": "Epic acceptance criteria"
                }}
            ],
            "stories": [
                {{
                    "title": "User story title",
                    "description": "As a [user], I want [goal] so that [benefit]",
                    "acceptance_criteria": "Given/When/Then format criteria",
                    "story_points": 5,
                    "epic_link": "Related epic title"
                }}
            ],
            "use_cases": [
                {{
                    "title": "Use case title",
                    "actor": "Primary actor",
                    "preconditions": "Required preconditions",
                    "main_flow": ["Step 1", "Step 2", "Step 3"],
                    "alternative_flows": ["Alternative step 1"],
                    "postconditions": "Expected postconditions"
                }}
            ],
            "technical_design": {{
                "title": "Technical Design Document",
                "overview": "System overview",
                "architecture": "Architecture description",
                "components": ["Component 1", "Component 2"],
                "technologies": ["Technology 1", "Technology 2"],
                "data_flow": "Data flow description",
                "security_considerations": "Security requirements"
            }},
            "data_model": {{
                "title": "Data Model",
                "entities": [
                    {{
                        "name": "Entity1",
                        "attributes": ["attr1", "attr2"],
                        "primary_key": "id"
                    }}
                ],
                "relationships": [
                    {{
                        "from": "Entity1",
                        "to": "Entity2",
                        "type": "one-to-many"
                    }}
                ],
                "constraints": ["Constraint 1", "Constraint 2"]
            }},
            "business_requirement_doc": {{
                "title": "Business Requirements Document",
                "executive_summary": "Executive summary",
                "business_objectives": ["Objective 1", "Objective 2"],
                "functional_requirements": ["Requirement 1", "Requirement 2"],
                "non_functional_requirements": ["NFR 1", "NFR 2"],
                "assumptions": ["Assumption 1"],
                "constraints": ["Constraint 1"]
            }},
            "functional_spec_doc": {{
                "title": "Functional Specification Document",
                "overview": "System functional overview",
                "system_functions": [{{"name": "Function1", "description": "Description"}}],
                "user_interfaces": [{{"name": "UI1", "description": "UI Description"}}],
                "data_requirements": ["Data requirement 1"],
                "business_rules": ["Business rule 1"],
                "validation_rules": ["Validation rule 1"]
            }},
            "test_cases": [{{
                "test_id": "TC001",
                "test_name": "Test case name",
                "description": "Test description",
                "preconditions": "Test preconditions",
                "test_steps": ["Step 1", "Step 2"],
                "expected_result": "Expected result",
                "priority": "High"
            }}]
        }}

        Ensure all content is relevant, detailed, and follows software development best practices.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                top_p=1,
                messages=[
                    {"role": "system", "content": "You are an expert business analyst and technical architect. Generate comprehensive project documentation based on business requirements."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            
            # Parse JSON response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_content = content[json_start:json_end]
            
            data = json.loads(json_content)
            
            # Convert to Pydantic models
            epics = [Epic(**epic) for epic in data['epics']]
            stories = [Story(**story) for story in data['stories']]
            use_cases = [UseCase(**uc) for uc in data['use_cases']]
            technical_design = TechnicalDesign(**data['technical_design'])
            data_model = DataModel(**data['data_model'])
            
            # Handle new document types
            business_req_doc = BusinessRequirementDoc(**data['business_requirement_doc']) if 'business_requirement_doc' in data else None
            functional_spec_doc = FunctionalSpecDoc(**data['functional_spec_doc']) if 'functional_spec_doc' in data else None
            test_cases = [TestCase(**tc) for tc in data['test_cases']] if 'test_cases' in data else None
            
            return GeneratedDocuments(
                epics=epics,
                stories=stories,
                use_cases=use_cases,
                technical_design=technical_design,
                data_model=data_model,
                business_requirement_doc=business_req_doc,
                functional_spec_doc=functional_spec_doc,
                test_cases=test_cases
            )
            
        except Exception as e:
            raise Exception(f"Error generating documents: {str(e)}")