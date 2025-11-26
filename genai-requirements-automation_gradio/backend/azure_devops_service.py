import requests
import json
from typing import List
from models import Epic, Story, UseCase

class AzureDevOpsService:
    def __init__(self, organization_url: str, personal_access_token: str, project_name: str):
        self.organization_url = organization_url
        self.project_name = project_name
        self.pat = personal_access_token
        self.headers = {
            'Content-Type': 'application/json-patch+json',
            'Authorization': f'Basic {self._encode_pat(personal_access_token)}',
            'Accept': 'application/json'
        }
    
    def _encode_pat(self, pat: str) -> str:
        """Encode PAT for basic auth"""
        import base64
        return base64.b64encode(f':{pat}'.encode('utf-8')).decode('ascii')
    
    def create_epic(self, epic: Epic) -> int:
        """Create an Epic using REST API"""
        try:
            url = f"{self.organization_url}/{self.project_name}/_apis/wit/workitems/$Epic?api-version=7.0"
            
            document = [
                {"op": "add", "path": "/fields/System.Title", "value": epic.title},
                {"op": "add", "path": "/fields/System.Description", "value": epic.description},
                {"op": "add", "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria", "value": epic.acceptance_criteria}
            ]
            
            response = requests.post(url, json=document, headers=self.headers)
            if response.status_code == 200:
                return response.json()['id']
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error creating epic: {str(e)}")
    
    def create_user_story(self, story: Story, epic_id: int = None) -> int:
        """Create a User Story using REST API"""
        try:
            url = f"{self.organization_url}/{self.project_name}/_apis/wit/workitems/$Product Backlog Item?api-version=7.0"
            
            document = [
                {"op": "add", "path": "/fields/System.Title", "value": story.title},
                {"op": "add", "path": "/fields/System.Description", "value": story.description},
                {"op": "add", "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria", "value": story.acceptance_criteria}
            ]
            
            if story.story_points:
                document.append({"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints", "value": story.story_points})
            
            if epic_id:
                document.append({"op": "add", "path": "/fields/System.Parent", "value": epic_id})
            
            response = requests.post(url, json=document, headers=self.headers)
            if response.status_code == 200:
                return response.json()['id']
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error creating user story: {str(e)}")
    
    def create_task(self, use_case: UseCase, epic_id: int = None) -> int:
        """Create a Task for Use Case using REST API"""
        try:
            url = f"{self.organization_url}/{self.project_name}/_apis/wit/workitems/$Task?api-version=7.0"
            
            document = [
                {"op": "add", "path": "/fields/System.Title", "value": use_case.title},
                {"op": "add", "path": "/fields/System.Description", "value": f"Actor: {use_case.actor}\nPreconditions: {use_case.preconditions}\nMain Flow: {', '.join(use_case.main_flow)}\nPostconditions: {use_case.postconditions}"}
            ]
            
            if epic_id:
                document.append({"op": "add", "path": "/fields/System.Parent", "value": epic_id})
            
            response = requests.post(url, json=document, headers=self.headers)
            if response.status_code == 200:
                return response.json()['id']
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error creating task: {str(e)}")
    
    def push_all_items(self, epics: List[Epic], stories: List[Story], use_cases: List[UseCase] = None) -> dict:
        """Push all epics, stories, and use cases to Azure DevOps"""
        results = {"epics": [], "stories": [], "use_cases": [], "errors": []}
        
        epic_mapping = {}
        for epic in epics:
            try:
                epic_id = self.create_epic(epic)
                epic_mapping[epic.title] = epic_id
                results["epics"].append({"title": epic.title, "id": epic_id})
            except Exception as e:
                results["errors"].append(f"Epic '{epic.title}': {str(e)}")
        
        for story in stories:
            try:
                epic_id = epic_mapping.get(story.epic_link) if story.epic_link else None
                story_id = self.create_user_story(story, epic_id)
                results["stories"].append({"title": story.title, "id": story_id})
            except Exception as e:
                results["errors"].append(f"Story '{story.title}': {str(e)}")
        
        if use_cases:
            for use_case in use_cases:
                try:
                    # Link use case to first epic if available
                    epic_id = list(epic_mapping.values())[0] if epic_mapping else None
                    task_id = self.create_task(use_case, epic_id)
                    results["use_cases"].append({"title": use_case.title, "id": task_id})
                except Exception as e:
                    results["errors"].append(f"Use Case '{use_case.title}': {str(e)}")
        
        return results