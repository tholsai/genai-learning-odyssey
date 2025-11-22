"""Upload router for handling file uploads and parsing."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from core.document_parser import DocumentParser
from core.rag_retriever import RAGRetriever
from core.config import settings
import os


router = APIRouter(prefix="/upload", tags=["upload"])


class UploadResponse(BaseModel):
    """Response model for upload endpoint."""
    message: str
    file_path: str
    file_name: str
    file_type: str
    parsed_content: dict
    indexed: bool


# Initialize components
document_parser = DocumentParser()
rag_retriever = RAGRetriever()


@router.post("", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and parse a functional specification document (PDF or DOCX).
    
    - **file**: The document file to upload (PDF or DOCX format)
    """
    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".pdf", ".docx", ".doc"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Only PDF and DOCX files are supported."
        )
    
    try:
        # Save uploaded file
        file_path = await document_parser.save_uploaded_file(
            file=file,
            upload_dir=settings.upload_dir
        )
        
        # Parse document
        parsed_content = document_parser.parse_document(file_path)
        
        # Index document in vector store for RAG
        indexed = False
        try:
            metadata = {
                "file_name": file.filename,
                "file_type": file_ext,
                "file_path": file_path,
                "source": "uploaded_spec"
            }
            rag_retriever.index_document(
                text=parsed_content["text"],
                metadata=metadata
            )
            indexed = True
        except Exception as e:
            print(f"Warning: Failed to index document: {str(e)}")
        
        return UploadResponse(
            message="File uploaded and parsed successfully",
            file_path=file_path,
            file_name=file.filename,
            file_type=file_ext,
            parsed_content=parsed_content,
            indexed=indexed
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

