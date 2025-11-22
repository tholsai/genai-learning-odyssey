"""Download router for retrieving generated documents."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
from pathlib import Path
from core.config import settings
import os


router = APIRouter(prefix="/download", tags=["download"])


@router.get("/{doc_type}")
async def download_document(doc_type: str, artifact_type: Optional[str] = None):
    """
    Download a generated document.
    
    - **doc_type**: Document type (docx or pdf)
    - **artifact_type**: Type of artifact (epic, stories, use_cases, tdd, data_model)
                         If not provided, returns the most recent file
    """
    # Validate doc_type
    if doc_type.lower() not in ["docx", "pdf"]:
        raise HTTPException(
            status_code=400,
            detail="doc_type must be 'docx' or 'pdf'"
        )
    
    try:
        generated_dir = settings.generated_dir
        
        if not os.path.exists(generated_dir):
            raise HTTPException(
                status_code=404,
                detail="No generated documents found"
            )
        
        # If artifact_type is specified, find that specific file
        if artifact_type:
            valid_artifact_types = ["epic", "stories", "use_cases", "tdd", "data_model"]
            if artifact_type.lower() not in valid_artifact_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid artifact_type. Valid types: {valid_artifact_types}"
                )
            
            # Look for file matching pattern
            pattern = f"{artifact_type}_*.{doc_type.lower()}"
            files = list(Path(generated_dir).glob(pattern))
            
            if not files:
                raise HTTPException(
                    status_code=404,
                    detail=f"No {doc_type} file found for artifact type: {artifact_type}"
                )
            
            # Get the most recent file
            file_path = max(files, key=os.path.getmtime)
        
        else:
            # Find the most recent file of the specified type
            pattern = f"*.{doc_type.lower()}"
            files = list(Path(generated_dir).glob(pattern))
            
            if not files:
                raise HTTPException(
                    status_code=404,
                    detail=f"No {doc_type} files found"
                )
            
            # Get the most recent file
            file_path = max(files, key=os.path.getmtime)
        
        # Return file
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type=f"application/{doc_type.lower()}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading document: {str(e)}"
        )

