# How to Upload Documents and Generate Outputs

This guide shows you how to upload functional specification documents and generate requirements artifacts.

## Method 1: Using Swagger UI (Easiest - Recommended)

### Step 1: Open the API Documentation
1. Open your browser and go to: **http://127.0.0.1:8000/docs**
2. You'll see all available endpoints with interactive forms

### Step 2: Upload a Document
1. Find the **`POST /api/v1/upload`** endpoint
2. Click **"Try it out"**
3. Click **"Choose File"** and select your PDF or DOCX file
4. Click **"Execute"**
5. You'll see a response with the parsed content and file path

**Example Response:**
```json
{
  "message": "File uploaded and parsed successfully",
  "file_path": "data/spec/your-document.pdf",
  "file_name": "your-document.pdf",
  "file_type": ".pdf",
  "parsed_content": {...},
  "indexed": true
}
```

### Step 3: Generate Artifacts
1. Find the **`POST /api/v1/generate`** endpoint
2. Click **"Try it out"**
3. Fill in the request body. You have two options:

   **Option A: Use uploaded file**
   ```json
   {
     "spec_file_path": "data/spec/your-document.pdf",
     "artifact_types": ["epic", "stories", "use_cases", "tdd", "data_model"],
     "output_format": "docx"
   }
   ```

   **Option B: Paste specification text directly**
   ```json
   {
     "spec_text": "The system should allow users to login, manage profiles, and have role-based access control...",
     "artifact_types": ["epic", "stories", "use_cases"],
     "output_format": "docx"
   }
   ```

4. Click **"Execute"**
5. Wait for the generation to complete (may take 30-60 seconds)
6. You'll see generated content and file paths

**Example Response:**
```json
{
  "message": "Successfully generated 5 artifacts",
  "artifacts": {
    "epic": "Generated epic content...",
    "stories": "Generated stories content...",
    ...
  },
  "file_paths": {
    "epic": "data/generated/epic_abc123.docx",
    "stories": "data/generated/stories_def456.docx",
    ...
  }
}
```

### Step 4: Download Generated Files
1. Find the **`GET /api/v1/download/{doc_type}`** endpoint
2. Click **"Try it out"**
3. Enter:
   - `doc_type`: `docx` or `pdf`
   - `artifact_type` (optional): `epic`, `stories`, `use_cases`, `tdd`, or `data_model`
4. Click **"Execute"**
5. The file will download automatically

---

## Method 2: Using PowerShell Commands

### Step 1: Upload a Document
```powershell
# Upload a PDF or DOCX file
$filePath = "C:\path\to\your\specification.pdf"
$uri = "http://127.0.0.1:8000/api/v1/upload"

$form = @{
    file = Get-Item -Path $filePath
}

$response = Invoke-RestMethod -Uri $uri -Method Post -Form $form
Write-Host "Upload successful!"
Write-Host "File path: $($response.file_path)"
```

### Step 2: Generate Artifacts
```powershell
# Generate artifacts from uploaded file
$body = @{
    spec_file_path = "data/spec/your-document.pdf"  # Use the file_path from upload response
    artifact_types = @("epic", "stories", "use_cases", "tdd", "data_model")
    output_format = "docx"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/generate" -Method Post -Body $body -ContentType "application/json"

Write-Host "Generated artifacts:"
$response.file_paths
```

### Step 3: Download Generated Files
```powershell
# Download a specific artifact
$artifactType = "epic"
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/download/docx?artifact_type=$artifactType" -OutFile "downloaded_$artifactType.docx"

# Or download the most recent file
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/download/docx" -OutFile "downloaded_latest.docx"
```

---

## Method 3: Using Python Script

Create a file `upload_and_generate.py`:

```python
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Step 1: Upload a document
print("Step 1: Uploading document...")
file_path = "path/to/your/specification.pdf"  # Change this to your file

with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{BASE_URL}/upload", files=files)

if response.status_code == 200:
    upload_result = response.json()
    print(f"✓ Upload successful: {upload_result['file_name']}")
    uploaded_file_path = upload_result['file_path']
else:
    print(f"✗ Upload failed: {response.text}")
    exit(1)

# Step 2: Generate artifacts
print("\nStep 2: Generating artifacts...")
generate_data = {
    "spec_file_path": uploaded_file_path,
    "artifact_types": ["epic", "stories", "use_cases", "tdd", "data_model"],
    "output_format": "docx"
}

response = requests.post(
    f"{BASE_URL}/generate",
    json=generate_data,
    timeout=120  # Longer timeout for generation
)

if response.status_code == 200:
    generate_result = response.json()
    print(f"✓ Generation successful!")
    print(f"Generated {len(generate_result['artifacts'])} artifacts")
    
    # Show file paths
    print("\nGenerated files:")
    for artifact_type, file_path in generate_result['file_paths'].items():
        print(f"  - {artifact_type}: {file_path}")
else:
    print(f"✗ Generation failed: {response.text}")
    exit(1)

# Step 3: Download files (optional)
print("\nStep 3: Downloading files...")
for artifact_type in generate_result['file_paths'].keys():
    try:
        response = requests.get(
            f"{BASE_URL}/download/docx",
            params={"artifact_type": artifact_type}
        )
        if response.status_code == 200:
            filename = f"downloaded_{artifact_type}.docx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✓ Downloaded: {filename}")
    except Exception as e:
        print(f"✗ Failed to download {artifact_type}: {e}")

print("\n✓ Complete!")
```

Run it:
```bash
uv run python upload_and_generate.py
```

---

## Complete Workflow Example

Here's a complete example using the Swagger UI:

1. **Open**: http://127.0.0.1:8000/docs

2. **Upload Document**:
   - POST `/api/v1/upload`
   - Upload your PDF/DOCX file
   - Note the `file_path` from response

3. **Generate Artifacts**:
   - POST `/api/v1/generate`
   - Use this request body:
   ```json
   {
     "spec_file_path": "data/spec/your-file.pdf",
     "artifact_types": ["epic", "stories", "use_cases", "tdd", "data_model"],
     "output_format": "docx"
   }
   ```
   - Wait for generation (30-60 seconds)
   - View the generated content in the response

4. **Download Files**:
   - GET `/api/v1/download/docx?artifact_type=epic`
   - GET `/api/v1/download/docx?artifact_type=stories`
   - etc.

5. **Chat with AI** (Optional):
   - POST `/api/v1/chat`
   - Ask questions about your specification:
   ```json
   {
     "message": "What are the main features in the specification?",
     "use_rag": true
   }
   ```

---

## Generated Files Location

All generated files are saved in:
- **Directory**: `backend/data/generated/`
- **Format**: `{artifact_type}_{uuid}.{doc_type}`
- **Example**: `epic_a1b2c3d4.docx`, `stories_e5f6g7h8.pdf`

You can also access them directly from the file system or download via the API.

---

## Tips

1. **File Formats**: Supported formats are PDF and DOCX
2. **Generation Time**: First generation may take longer (30-60 seconds) as models load
3. **File Size**: Large documents may take longer to process
4. **RAG Chat**: Enable `use_rag: true` in chat to get answers based on your uploaded documents
5. **Output Format**: Choose `docx` or `pdf` based on your preference

---

## Troubleshooting

**Upload fails:**
- Check file is PDF or DOCX format
- Ensure file is not corrupted
- Check file size (very large files may timeout)

**Generation fails:**
- Check that Ollama is running (`ollama serve`)
- Verify Mistral model is downloaded (`ollama list`)
- If model not found, run `ollama pull mistral`
- Check the error message in the response

**Download fails:**
- Ensure you've generated artifacts first
- Check the artifact_type matches what was generated
- Verify files exist in `backend/data/generated/`

