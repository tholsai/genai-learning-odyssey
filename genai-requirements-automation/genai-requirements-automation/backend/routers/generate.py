"""Generate router for creating requirements artifacts."""
from fastapi import APIRouter, HTTPException, Body
from typing import List, Optional
from pydantic import BaseModel
from core.llm_engine import LLMEngine
from core.rag_retriever import RAGRetriever
from core.file_generator import FileGenerator
from core.config import settings
import os


router = APIRouter(prefix="/generate", tags=["generate"])


class GenerateRequest(BaseModel):
    """Request model for generate endpoint."""
    spec_text: Optional[str] = None
    spec_file_path: Optional[str] = None
    artifact_types: List[str] = ["epic", "stories", "use_cases", "tdd", "data_model"]
    output_format: str = "docx"  # docx or pdf


class GenerateResponse(BaseModel):
    """Response model for generate endpoint."""
    message: str
    artifacts: dict
    file_paths: dict


# Initialize components
rag_retriever = RAGRetriever()
llm_engine = LLMEngine(rag_retriever=rag_retriever)
file_generator = FileGenerator()


def _load_spec_from_file(file_path: str) -> str:
    """Load specification text from file."""
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    
    from core.document_parser import DocumentParser
    parsed = DocumentParser.parse_document(file_path)
    return parsed["text"]


@router.post("", response_model=GenerateResponse)
async def generate_artifacts(request: GenerateRequest = Body(...)):
    """
    Generate requirements artifacts from functional specification.
    
    - **spec_text**: Direct specification text (optional if spec_file_path provided)
    - **spec_file_path**: Path to specification file (optional if spec_text provided)
    - **artifact_types**: List of artifacts to generate (epic, stories, use_cases, tdd, data_model)
    - **output_format**: Output format (docx or pdf)
    """
    # Get specification text
    spec_text = request.spec_text
    if not spec_text and request.spec_file_path:
        spec_text = _load_spec_from_file(request.spec_file_path)
    
    if not spec_text:
        raise HTTPException(
            status_code=400,
            detail="Either spec_text or spec_file_path must be provided"
        )
    
    # Validate artifact types
    valid_types = ["epic", "stories", "use_cases", "tdd", "data_model"]
    artifact_types = [t.lower() for t in request.artifact_types]
    invalid_types = [t for t in artifact_types if t not in valid_types]
    
    if invalid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid artifact types: {invalid_types}. Valid types: {valid_types}"
        )
    
    # Validate output format
    if request.output_format.lower() not in ["docx", "pdf"]:
        raise HTTPException(
            status_code=400,
            detail="output_format must be 'docx' or 'pdf'"
        )
    
    try:
        artifacts = {}
        file_paths = {}
        
        # Generate each artifact type
        for artifact_type in artifact_types:
            # Generate content using LLM
            content = llm_engine.generate_requirements_artifacts(
                spec_text=spec_text,
                artifact_type=artifact_type
            )
            
            artifacts[artifact_type] = content
            
            # Generate file
            file_path = file_generator.generate_artifact_file(
                content=content,
                artifact_type=artifact_type,
                doc_type=request.output_format.lower()
            )
            file_paths[artifact_type] = file_path
        
        return GenerateResponse(
            message=f"Successfully generated {len(artifacts)} artifacts",
            artifacts=artifacts,
            file_paths=file_paths
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating artifacts: {str(e)}"
        )

