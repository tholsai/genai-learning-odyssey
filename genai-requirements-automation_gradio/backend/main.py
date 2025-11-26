from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from pdf_processor import PDFProcessor
from openai_service import OpenAIService
# from azure_devops_service import AzureDevOpsService
from document_generator import DocumentGenerator
from models import GeneratedDocuments

# Load environment variables
load_dotenv()

app = FastAPI(title="GenAI Requirements-Automation", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
openai_service = OpenAIService(os.getenv("OPENAI_API_KEY"))
azure_service = None  # Will be initialized when needed

@app.post("/generate-documents")
async def generate_documents(file: UploadFile = File(...)):
    """Generate all project documents from uploaded PDF"""
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Extract text from PDF
        pdf_text = PDFProcessor.extract_text_from_pdf(file.file)
        cleaned_text = PDFProcessor.clean_text(pdf_text)
        
        if not cleaned_text.strip():
            raise HTTPException(status_code=400, detail="No text content found in PDF")
        
        # Generate documents using OpenAI
        documents = openai_service.generate_documents(cleaned_text)
        
        return {
            "status": "success",
            "documents": documents.dict(),
            "markdown_report": DocumentGenerator.generate_markdown_report(documents),
            "json_export": DocumentGenerator.generate_json_export(documents),
            "ado_import": DocumentGenerator.generate_ado_import_json(documents)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/push-to-ado")
async def push_to_ado(documents: GeneratedDocuments):
    """Push generated documents to Azure DevOps"""
    try:
        # Initialize Azure service when needed
        if not all([os.getenv("AZURE_DEVOPS_ORG_URL"), os.getenv("AZURE_DEVOPS_PAT"), os.getenv("AZURE_DEVOPS_PROJECT")]):
            raise HTTPException(status_code=400, detail="Azure DevOps not configured")
        
        from azure_devops_service import AzureDevOpsService
        azure_service = AzureDevOpsService(
            os.getenv("AZURE_DEVOPS_ORG_URL"),
            os.getenv("AZURE_DEVOPS_PAT"),
            os.getenv("AZURE_DEVOPS_PROJECT")
        )
        
        results = azure_service.push_all_items(documents.epics, documents.stories)
        
        return {
            "status": "success",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "GenAI Document Generator is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)