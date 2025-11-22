"""Document parser for PDF and DOCX files."""
import os
from typing import List, Dict, Any
from pathlib import Path
import pdfplumber
from docx import Document
from fastapi import UploadFile
import aiofiles


class DocumentParser:
    """Parser for extracting text from PDF and DOCX documents."""
    
    @staticmethod
    async def save_uploaded_file(file: UploadFile, upload_dir: str) -> str:
        """Save uploaded file to disk."""
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return file_path
    
    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        """Parse PDF file and extract text."""
        text_content = []
        metadata = {
            "file_type": "pdf",
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "pages": 0
        }
        
        try:
            with pdfplumber.open(file_path) as pdf:
                metadata["pages"] = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        text_content.append({
                            "page": page_num,
                            "text": text.strip()
                        })
                
                full_text = "\n\n".join([page["text"] for page in text_content])
                
                return {
                    "text": full_text,
                    "pages": text_content,
                    "metadata": metadata
                }
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def parse_docx(file_path: str) -> Dict[str, Any]:
        """Parse DOCX file and extract text."""
        text_content = []
        metadata = {
            "file_type": "docx",
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "paragraphs": 0
        }
        
        try:
            doc = Document(file_path)
            paragraphs = []
            
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text.strip())
                    text_content.append({
                        "paragraph": len(paragraphs),
                        "text": para.text.strip()
                    })
            
            metadata["paragraphs"] = len(paragraphs)
            full_text = "\n\n".join(paragraphs)
            
            return {
                "text": full_text,
                "paragraphs": text_content,
                "metadata": metadata
            }
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {str(e)}")
    
    @staticmethod
    def parse_document(file_path: str) -> Dict[str, Any]:
        """Parse document based on file extension."""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == ".pdf":
            return DocumentParser.parse_pdf(file_path)
        elif file_ext in [".docx", ".doc"]:
            return DocumentParser.parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

