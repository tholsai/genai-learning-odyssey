# Quick Start Guide - Running the GenAI Requirements Automation Backend

This guide will walk you through setting up and running the FastAPI backend application.

## Prerequisites

1. **Python 3.10+** installed on your system
2. **UV package manager** - Install from https://github.com/astral-sh/uv
   ```bash
   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Ollama with Mistral model** - Install Ollama from https://ollama.ai and pull the Mistral model
4. (Optional) **Azure DevOps credentials** - If you want to use the ADO push feature

## Step 1: Install Dependencies

Open a terminal in the project root directory and run:

```bash
# Install all dependencies using UV
uv sync
```

This will:
- Create a virtual environment
- Install all required packages (FastAPI, OpenAI, ChromaDB, sentence-transformers, etc.)
- Set up the development environment

**Note**: The first time you run this, it may take a few minutes as it downloads:
- The sentence-transformers model (~90MB)
- ChromaDB dependencies
- Other Python packages

## Step 2: Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Navigate to backend directory
cd backend

# Create .env file (Windows PowerShell)
New-Item -Path .env -ItemType File

# Or create manually with the following content:
```

Add the following content to `backend/.env` (optional - defaults work if Ollama is running):

```env
# Optional: Ollama settings (defaults: http://localhost:11434/v1, model: mistral)
OLLAMA_API_BASE=http://localhost:11434/v1
OLLAMA_MODEL=mistral
TEMPERATURE=0.7
MAX_TOKENS=4000

# Optional: Azure DevOps (only if using ADO push)
ADO_ORG_URL=https://dev.azure.com/your-org
ADO_PAT=your_personal_access_token
ADO_PROJECT=your-project-name

# Optional: Customize embedding model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Important**: Make sure Ollama is running and the Mistral model is downloaded:
```bash
# Install Ollama from https://ollama.ai
# Then pull the Mistral model:
ollama pull mistral
```

## Step 3: Run the Application

From the `backend/` directory, run:

```bash
# Option 1: Using UV to run
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python directly (if virtual environment is activated)
python app.py

# Option 3: Using the run script
python run.py
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 4: Access the API

Once the server is running, you can access:

1. **API Root**: http://localhost:8000/
2. **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
3. **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
4. **Health Check**: http://localhost:8000/health

## Step 5: Test the Endpoints

### Option A: Using the Interactive Swagger UI (Recommended)

1. Open http://localhost:8000/docs in your browser
2. You'll see all available endpoints with "Try it out" buttons
3. Click on any endpoint to test it interactively

### Option B: Using cURL or PowerShell

#### 1. Test Health Endpoint
```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

#### 2. Upload a Document
```powershell
# PowerShell - Upload a PDF or DOCX file
$filePath = "path\to\your\specification.pdf"
$uri = "http://localhost:8000/api/v1/upload"
$form = @{
    file = Get-Item -Path $filePath
}
Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

#### 3. Generate Artifacts
```powershell
# PowerShell - Generate requirements artifacts
$body = @{
    spec_text = "The system should allow users to login and manage their profiles."
    artifact_types = @("epic", "stories", "use_cases")
    output_format = "docx"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/generate" -Method Post -Body $body -ContentType "application/json"
```

#### 4. Chat with the Bot
```powershell
# PowerShell - Chat endpoint
$body = @{
    message = "What are the main features in the specification?"
    use_rag = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" -Method Post -Body $body -ContentType "application/json"
```

### Option C: Using Python Script

Create a test script `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. Health check
response = requests.get("http://localhost:8000/health")
print("Health:", response.json())

# 2. Generate artifacts
generate_data = {
    "spec_text": """
    The system is a user management platform that allows:
    - User registration and authentication
    - Profile management
    - Role-based access control
    """,
    "artifact_types": ["epic", "stories"],
    "output_format": "docx"
}

response = requests.post(
    f"{BASE_URL}/generate",
    json=generate_data
)
print("\nGenerate Response:")
print(json.dumps(response.json(), indent=2))

# 3. Chat
chat_data = {
    "message": "What features are mentioned in the specification?",
    "use_rag": True
}

response = requests.post(
    f"{BASE_URL}/chat",
    json=chat_data
)
print("\nChat Response:")
print(response.json()["response"])
```

Run it:
```bash
uv run python test_api.py
```

## Step 6: View Generated Results

### Generated Files Location

After running the generate endpoint, files are saved in:
- **Location**: `backend/data/generated/`
- **Format**: `{artifact_type}_{uuid}.{doc_type}`
- **Example**: `epic_a1b2c3d4.docx`, `stories_e5f6g7h8.pdf`

### Download Files via API

```powershell
# Download a generated DOCX file
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/download/docx?artifact_type=epic" -OutFile "downloaded_epic.docx"

# Download a generated PDF file
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/download/pdf?artifact_type=stories" -OutFile "downloaded_stories.pdf"
```

## Complete Workflow Example

Here's a complete workflow to test the entire system:

### 1. Start the Server
```bash
cd backend
uv run uvicorn app:app --reload
```

### 2. Upload a Specification (using Swagger UI)
- Go to http://localhost:8000/docs
- Find `POST /api/v1/upload`
- Click "Try it out"
- Upload a PDF or DOCX file
- Click "Execute"
- Note the `file_path` from the response

### 3. Generate Artifacts
- Find `POST /api/v1/generate`
- Click "Try it out"
- Use the request body:
```json
{
  "spec_text": "Your specification text here, or use spec_file_path from upload response",
  "artifact_types": ["epic", "stories", "use_cases", "tdd", "data_model"],
  "output_format": "docx"
}
```
- Click "Execute"
- Check the `file_paths` in the response

### 4. Download Generated Files
- Find `GET /api/v1/download/{doc_type}`
- Click "Try it out"
- Enter `doc_type` as "docx" or "pdf"
- Optionally add `artifact_type` query parameter
- Click "Execute"
- The file will download automatically

### 5. Chat with the Bot
- Find `POST /api/v1/chat`
- Click "Try it out"
- Use request body:
```json
{
  "message": "What are the main requirements?",
  "use_rag": true
}
```
- Click "Execute"
- View the AI response

## Troubleshooting

### Issue: "Connection refused" or "Cannot connect to Ollama"
**Solution**: 
- Make sure Ollama is running: `ollama serve` (or start it as a service)
- Verify the Mistral model is downloaded: `ollama list`
- If Mistral is not installed, run: `ollama pull mistral`
- Check that Ollama is accessible at http://localhost:11434

### Issue: "Module not found" errors
**Solution**: Make sure you've run `uv sync` and are using `uv run` to execute commands

### Issue: Port 8000 already in use
**Solution**: Change the port:
```bash
uv run uvicorn app:app --reload --port 8001
```

### Issue: ChromaDB or embeddings errors
**Solution**: The first run will download models. Wait for the download to complete. Check your internet connection.

### Issue: File upload fails
**Solution**: 
- Ensure the file is PDF or DOCX format
- Check that `backend/data/spec/` directory exists (it should be created automatically)
- Verify file permissions

## Next Steps

1. **Customize the LLM prompts** in `backend/core/llm_engine.py`
2. **Adjust chunking strategy** in `backend/core/rag_retriever.py`
3. **Modify artifact generation** by updating the system prompts
4. **Add authentication** if deploying to production
5. **Configure Azure DevOps** to push artifacts automatically

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/v1/upload` | Upload and parse document |
| POST | `/api/v1/generate` | Generate requirements artifacts |
| GET | `/api/v1/download/{doc_type}` | Download generated document |
| POST | `/api/v1/chat` | Chat with AI assistant |
| POST | `/api/v1/ado/push` | Push artifacts to Azure DevOps |

For detailed API documentation, visit http://localhost:8000/docs

