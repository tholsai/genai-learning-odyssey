import json
from typing import Dict, Any
from models import GeneratedDocuments
from jinja2 import Template

class DocumentGenerator:
    @staticmethod
    def generate_markdown_report(documents: GeneratedDocuments) -> str:
        """Generate a comprehensive markdown report"""
        
        template = Template("""
# Project Documentation

## Epics

{% for epic in epics %}
### {{ epic.title }}

**Description:** {{ epic.description }}

**Business Value:** {{ epic.business_value }}

**Acceptance Criteria:**
{{ epic.acceptance_criteria }}

---
{% endfor %}

## User Stories

{% for story in stories %}
### {{ story.title }}

**Description:** {{ story.description }}

**Story Points:** {{ story.story_points or 'Not estimated' }}

**Epic Link:** {{ story.epic_link or 'None' }}

**Acceptance Criteria:**
{{ story.acceptance_criteria }}

---
{% endfor %}

## Use Cases

{% for use_case in use_cases %}
### {{ use_case.title }}

**Actor:** {{ use_case.actor }}

**Preconditions:** {{ use_case.preconditions }}

**Main Flow:**
{% for step in use_case.main_flow %}
{{ loop.index }}. {{ step }}
{% endfor %}

{% if use_case.alternative_flows %}
**Alternative Flows:**
{% for flow in use_case.alternative_flows %}
- {{ flow }}
{% endfor %}
{% endif %}

**Postconditions:** {{ use_case.postconditions }}

---
{% endfor %}

## Technical Design

### {{ technical_design.title }}

**Overview:** {{ technical_design.overview }}

**Architecture:** {{ technical_design.architecture }}

**Components:**
{% for component in technical_design.components %}
- {{ component }}
{% endfor %}

**Technologies:**
{% for tech in technical_design.technologies %}
- {{ tech }}
{% endfor %}

**Data Flow:** {{ technical_design.data_flow }}

**Security Considerations:** {{ technical_design.security_considerations }}

## Data Model

### {{ data_model.title }}

**Entities:**
{% for entity in data_model.entities %}
- **{{ entity.name }}**
  - Attributes: {{ entity.attributes | join(', ') }}
  - Primary Key: {{ entity.primary_key }}
{% endfor %}

**Relationships:**
{% for rel in data_model.relationships %}
- {{ rel.from }} → {{ rel.to }} ({{ rel.type }})
{% endfor %}

**Constraints:**
{% for constraint in data_model.constraints %}
- {{ constraint }}
{% endfor %}
        """)
        
        return template.render(
            epics=documents.epics,
            stories=documents.stories,
            use_cases=documents.use_cases,
            technical_design=documents.technical_design,
            data_model=documents.data_model
        )
    
    @staticmethod
    def generate_json_export(documents: GeneratedDocuments) -> str:
        """Generate JSON export of all documents"""
        return json.dumps(documents.dict(), indent=2)
    
    @staticmethod
    def generate_ado_import_json(documents: GeneratedDocuments) -> str:
        """Generate JSON format suitable for ADO import"""
        ado_items = []
        
        # Add epics
        for epic in documents.epics:
            ado_items.append({
                "work_item_type": "Epic",
                "title": epic.title,
                "description": epic.description,
                "business_value": epic.business_value,
                "acceptance_criteria": epic.acceptance_criteria
            })
        
        # Add stories
        for story in documents.stories:
            ado_items.append({
                "work_item_type": "User Story",
                "title": story.title,
                "description": story.description,
                "acceptance_criteria": story.acceptance_criteria,
                "story_points": story.story_points,
                "epic_link": story.epic_link
            })
        
        return json.dumps({"work_items": ado_items}, indent=2)