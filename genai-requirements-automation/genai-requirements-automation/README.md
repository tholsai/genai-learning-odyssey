# GenAI Requirements Automation

A FastAPI backend for automating requirements generation using GenAI. This system can parse functional specifications, generate requirements artifacts (epics, stories, use cases, TDD tests, data models), and push them to Azure DevOps.

## Features

- **Document Upload & Parsing**: Upload and parse PDF/DOCX functional specifications
- **AI-Powered Generation**: Generate epics, user stories, use cases, TDD test cases, and data models
- **RAG-Powered Chatbot**: Interactive chatbot for questions about specifications and generated artifacts
- **Document Generation**: Export generated artifacts as DOCX or PDF
- **Azure DevOps Integration**: Push generated artifacts as work items to Azure DevOps

## Architecture

The application follows a modular architecture:

### Core Modules
- `core/document_parser.py`: Parses PDF and DOCX files
- `core/vectorstore.py`: ChromaDB vector store for document embeddings
- `core/embeddings.py`: Sentence-transformers for generating embeddings
- `core/rag_retriever.py`: RAG retriever for context-aware retrieval
- `core/llm_engine.py`: LLM engine using Ollama/Mistral for content generation
- `core/file_generator.py`: Generates DOCX and PDF files

### Routers
- `routers/upload.py`: File upload and parsing endpoints
- `routers/generate.py`: Artifact generation endpoints
- `routers/download.py`: Document download endpoints
- `routers/chatbot.py`: Chatbot endpoints
- `routers/ado.py`: Azure DevOps integration endpoints

## Setup

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Create a `.env` file in the `backend` directory (see `.env.example` for template):
```bash
cp .env.example backend/.env
```

3. Ensure Ollama is running with Mistral model:
```bash
# Make sure Ollama is installed and running
# Pull the Mistral model if not already downloaded
ollama pull mistral
```

4. (Optional) Configure your environment variables in `backend/.env`:
```env
# Ollama settings (defaults work if Ollama is on localhost:11434)
OLLAMA_API_BASE=http://localhost:11434/v1
OLLAMA_MODEL=mistral

# Azure DevOps (optional)
ADO_ORG_URL=https://dev.azure.com/your-org
ADO_PAT=your_personal_access_token
ADO_PROJECT=your-project-name
```

### Running the Application

From the `backend` directory:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Or using Python directly:
```bash
cd backend
python app.py
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI) is available at `http://localhost:8000/docs`

## API Endpoints

### POST `/api/v1/upload`
Upload and parse a functional specification document (PDF or DOCX).

**Request**: Multipart form data with `file` field

**Response**: 
```json
{
  "message": "File uploaded and parsed successfully",
  "file_path": "data/spec/document.pdf",
  "file_name": "document.pdf",
  "file_type": ".pdf",
  "parsed_content": {...},
  "indexed": true
}
```

### POST `/api/v1/generate`
Generate requirements artifacts from functional specification.

**Request Body**:
```json
{
  "spec_text": "Functional specification text...",
  "spec_file_path": null,
  "artifact_types": ["epic", "stories", "use_cases", "tdd", "data_model"],
  "output_format": "docx"
}
```

**Response**:
```json
{
  "message": "Successfully generated 5 artifacts",
  "artifacts": {
    "epic": "...",
    "stories": "...",
    ...
  },
  "file_paths": {
    "epic": "data/generated/epic_abc123.docx",
    ...
  }
}
```

### GET `/api/v1/download/{doc_type}`
Download a generated document.

**Parameters**:
- `doc_type`: "docx" or "pdf"
- `artifact_type` (query param, optional): Specific artifact type to download

**Response**: File download

### POST `/api/v1/chat`
Chat with the AI assistant.

**Request Body**:
```json
{
  "message": "What are the main features in the specification?",
  "use_rag": true,
  "conversation_history": null
}
```

**Response**:
```json
{
  "response": "Based on the specification...",
  "used_rag": true
}
```

### POST `/api/v1/ado/push`
Push generated artifacts to Azure DevOps.

**Request Body**:
```json
{
  "artifact_types": ["epic", "stories"],
  "work_item_type": "User Story",
  "project_name": null,
  "area_path": null,
  "iteration_path": null
}
```

**Response**:
```json
{
  "message": "Successfully created 2 work items",
  "work_items_created": [
    {
      "id": 12345,
      "url": "https://dev.azure.com/...",
      "title": "EPIC: ...",
      "work_item_type": "User Story"
    }
  ],
  "errors": []
}
```

## Project Structure

```
.
├── backend/
│   ├── app.py                 # Main FastAPI application
│   ├── core/                  # Core modules
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration settings
│   │   ├── document_parser.py
│   │   ├── embeddings.py
│   │   ├── file_generator.py
│   │   ├── llm_engine.py
│   │   ├── rag_retriever.py
│   │   └── vectorstore.py
│   ├── routers/               # API routers
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   ├── generate.py
│   │   ├── download.py
│   │   ├── chatbot.py
│   │   └── ado.py
│   └── data/                  # Data directories
│       ├── spec/              # Uploaded specifications
│       ├── generated/         # Generated artifacts
│       ├── downloads/         # Download cache
│       └── embeddings/       # ChromaDB storage
├── pyproject.toml             # Project dependencies (uv)
└── README.md
```

## Configuration

Configuration is managed through environment variables and `core/config.py`. Key settings:

- **LLM Settings**: Ollama API base URL, model name (Mistral), temperature, max tokens
- **Embeddings**: Model name, chunk size, chunk overlap
- **Vector Store**: ChromaDB persistence directory, collection name
- **Azure DevOps**: Organization URL, PAT, project name
- **File Storage**: Upload, generated, and download directories

## Development

### Adding New Artifact Types

1. Update the `generate_requirements_artifacts` method in `core/llm_engine.py`
2. Add the new type to valid artifact types in `routers/generate.py`
3. Update file generator titles in `core/file_generator.py`

### Extending RAG Capabilities

The RAG system uses ChromaDB for vector storage and sentence-transformers for embeddings. To customize:

1. Modify embedding model in `core/embeddings.py`
2. Adjust chunking strategy in `core/rag_retriever.py`
3. Update retrieval parameters in `core/llm_engine.py`

## License

MIT

