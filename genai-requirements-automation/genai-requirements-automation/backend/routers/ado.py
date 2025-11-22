"""Azure DevOps router for pushing artifacts."""
from fastapi import APIRouter, HTTPException, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from core.config import settings
import os
from pathlib import Path


router = APIRouter(prefix="/ado", tags=["azure-devops"])


class ADOPushRequest(BaseModel):
    """Request model for ADO push endpoint."""
    artifact_types: Optional[List[str]] = None  # If None, push all
    work_item_type: str = "User Story"  # User Story, Epic, Feature, etc.
    project_name: Optional[str] = None
    area_path: Optional[str] = None
    iteration_path: Optional[str] = None


class ADOPushResponse(BaseModel):
    """Response model for ADO push endpoint."""
    message: str
    work_items_created: List[Dict[str, Any]]
    errors: List[str]


def _validate_ado_config():
    """Validate Azure DevOps configuration."""
    if not settings.ado_org_url:
        raise ValueError("Azure DevOps organization URL not configured")
    if not settings.ado_pat:
        raise ValueError("Azure DevOps Personal Access Token not configured")
    if not settings.ado_project:
        raise ValueError("Azure DevOps project not configured")


def _parse_artifact_content(file_path: str) -> Dict[str, Any]:
    """Parse artifact content from file."""
    from core.document_parser import DocumentParser
    
    file_ext = Path(file_path).suffix.lower()
    
    # Parse based on file type
    if file_ext == ".docx":
        parsed = DocumentParser.parse_docx(file_path)
        content = parsed["text"]
    elif file_ext == ".pdf":
        parsed = DocumentParser.parse_pdf(file_path)
        content = parsed["text"]
    else:
        # Try reading as text file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            content = ""
    
    # Extract title and description
    title = Path(file_path).stem.replace("_", " ").title()
    description = content[:1000] if content else "No content available"
    
    return {
        "title": title,
        "description": description,
        "full_content": content
    }


def _create_work_item(
    org_url: str,
    pat: str,
    project: str,
    work_item_type: str,
    title: str,
    description: str,
    area_path: Optional[str] = None,
    iteration_path: Optional[str] = None
) -> Dict[str, Any]:
    """Create a work item in Azure DevOps."""
    try:
        from azure.devops.connection import Connection
        from msrest.authentication import BasicAuthentication
        from azure.devops.v7_0.work_item_tracking.models import JsonPatchOperation
        
        # Create connection
        credentials = BasicAuthentication('', pat)
        connection = Connection(base_url=org_url, creds=credentials)
        wit_client = connection.clients.get_work_item_tracking_client()
        
        # Prepare work item fields
        patch_document = [
            JsonPatchOperation(
                op="add",
                path="/fields/System.Title",
                value=title
            ),
            JsonPatchOperation(
                op="add",
                path="/fields/System.Description",
                value=description
            )
        ]
        
        if area_path:
            patch_document.append(
                JsonPatchOperation(
                    op="add",
                    path="/fields/System.AreaPath",
                    value=area_path
                )
            )
        
        if iteration_path:
            patch_document.append(
                JsonPatchOperation(
                    op="add",
                    path="/fields/System.IterationPath",
                    value=iteration_path
                )
            )
        
        # Create work item
        work_item = wit_client.create_work_item(
            document=patch_document,
            project=project,
            type=work_item_type
        )
        
        return {
            "id": work_item.id,
            "url": work_item.url,
            "title": work_item.fields.get("System.Title", ""),
            "work_item_type": work_item_type
        }
    
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="Azure DevOps SDK not properly installed"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating work item: {str(e)}"
        )


@router.post("/push", response_model=ADOPushResponse)
async def push_to_ado(request: ADOPushRequest = Body(...)):
    """
    Push generated artifacts to Azure DevOps as work items.
    
    - **artifact_types**: List of artifact types to push (if None, pushes all)
    - **work_item_type**: Type of work item to create (User Story, Epic, Feature, etc.)
    - **project_name**: Azure DevOps project name (overrides config)
    - **area_path**: Area path for work items
    - **iteration_path**: Iteration path for work items
    """
    # Validate configuration
    try:
        _validate_ado_config()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Determine which artifacts to push
    artifact_types = request.artifact_types or ["epic", "stories", "use_cases", "tdd", "data_model"]
    valid_types = ["epic", "stories", "use_cases", "tdd", "data_model"]
    artifact_types = [t.lower() for t in artifact_types if t.lower() in valid_types]
    
    if not artifact_types:
        raise HTTPException(
            status_code=400,
            detail="No valid artifact types specified"
        )
    
    # Get project name
    project = request.project_name or settings.ado_project
    
    work_items_created = []
    errors = []
    
    try:
        generated_dir = settings.generated_dir
        
        if not os.path.exists(generated_dir):
            raise HTTPException(
                status_code=404,
                detail="No generated documents found"
            )
        
        # Process each artifact type
        for artifact_type in artifact_types:
            # Find files for this artifact type
            pattern = f"{artifact_type}_*"
            files = list(Path(generated_dir).glob(pattern))
            
            if not files:
                errors.append(f"No files found for artifact type: {artifact_type}")
                continue
            
            # Process the most recent file
            file_path = max(files, key=os.path.getmtime)
            
            try:
                # Parse artifact content
                artifact_data = _parse_artifact_content(str(file_path))
                
                # Create work item
                work_item = _create_work_item(
                    org_url=settings.ado_org_url,
                    pat=settings.ado_pat,
                    project=project,
                    work_item_type=request.work_item_type,
                    title=f"{artifact_type.upper()}: {artifact_data['title']}",
                    description=artifact_data['description'],
                    area_path=request.area_path,
                    iteration_path=request.iteration_path
                )
                
                work_items_created.append(work_item)
            
            except Exception as e:
                errors.append(f"Error processing {artifact_type}: {str(e)}")
        
        if not work_items_created and errors:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create work items: {', '.join(errors)}"
            )
        
        return ADOPushResponse(
            message=f"Successfully created {len(work_items_created)} work items",
            work_items_created=work_items_created,
            errors=errors
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error pushing to Azure DevOps: {str(e)}"
        )

