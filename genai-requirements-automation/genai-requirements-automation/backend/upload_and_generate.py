"""Example script to upload a document and generate artifacts."""
import requests
import json
import sys
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000/api/v1"


def upload_document(file_path: str):
    """Upload a document to the server."""
    print(f"\n{'='*60}")
    print("Step 1: Uploading Document")
    print(f"{'='*60}")
    print(f"File: {file_path}")
    
    if not Path(file_path).exists():
        print(f"[ERROR] File not found: {file_path}")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (Path(file_path).name, f, 'application/pdf' if file_path.endswith('.pdf') else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
            response = requests.post(f"{BASE_URL}/upload", files=files, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Upload successful!")
            print(f"  File name: {result['file_name']}")
            print(f"  File path: {result['file_path']}")
            print(f"  Indexed: {result['indexed']}")
            return result
        else:
            print(f"[ERROR] Upload failed: {response.status_code}")
            print(f"  {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Upload error: {e}")
        return None


def generate_artifacts(spec_file_path: str = None, spec_text: str = None, artifact_types: list = None):
    """Generate requirements artifacts."""
    print(f"\n{'='*60}")
    print("Step 2: Generating Artifacts")
    print(f"{'='*60}")
    
    if artifact_types is None:
        artifact_types = ["epic", "stories", "use_cases", "tdd", "data_model"]
    
    data = {
        "artifact_types": artifact_types,
        "output_format": "docx"
    }
    
    if spec_file_path:
        data["spec_file_path"] = spec_file_path
        print(f"Using file: {spec_file_path}")
    elif spec_text:
        data["spec_text"] = spec_text
        print(f"Using provided text (length: {len(spec_text)} chars)")
    else:
        print("[ERROR] Either spec_file_path or spec_text must be provided")
        return None
    
    print(f"Generating: {', '.join(artifact_types)}")
    print("This may take 30-60 seconds...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate",
            json=data,
            timeout=180  # 3 minutes timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Generation successful!")
            print(f"  Message: {result['message']}")
            print(f"\nGenerated files:")
            for artifact_type, file_path in result['file_paths'].items():
                print(f"  - {artifact_type}: {file_path}")
            return result
        else:
            print(f"[ERROR] Generation failed: {response.status_code}")
            print(f"  {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("[ERROR] Generation timed out. The request took too long.")
        return None
    except Exception as e:
        print(f"[ERROR] Generation error: {e}")
        return None


def download_file(doc_type: str = "docx", artifact_type: str = None):
    """Download a generated file."""
    print(f"\n{'='*60}")
    print("Step 3: Downloading File")
    print(f"{'='*60}")
    
    url = f"{BASE_URL}/download/{doc_type}"
    params = {}
    if artifact_type:
        params["artifact_type"] = artifact_type
        print(f"Downloading: {artifact_type}.{doc_type}")
    else:
        print(f"Downloading: latest {doc_type} file")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            filename = f"{artifact_type or 'latest'}.{doc_type}"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"[OK] Downloaded: {filename}")
            return filename
        else:
            print(f"[ERROR] Download failed: {response.status_code}")
            print(f"  {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Download error: {e}")
        return None


def main():
    """Main workflow."""
    print("\n" + "="*60)
    print("GenAI Requirements Automation - Upload & Generate")
    print("="*60)
    
    # Check if file path provided as argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Example: use a sample file or prompt user
        file_path = input("\nEnter path to your specification file (PDF/DOCX): ").strip()
        if not file_path:
            print("\n[INFO] No file provided. Using sample text instead.")
            file_path = None
    
    # Step 1: Upload document (if file provided)
    upload_result = None
    if file_path:
        upload_result = upload_document(file_path)
        if not upload_result:
            print("\n[WARN] Upload failed. Trying with sample text...")
            file_path = None
    
    # Step 2: Generate artifacts
    if upload_result:
        generate_result = generate_artifacts(
            spec_file_path=upload_result['file_path'],
            artifact_types=["epic", "stories", "use_cases"]
        )
    else:
        # Use sample text
        sample_text = """
        Functional Specification: User Management System
        
        The system should provide the following features:
        
        1. User Authentication
           - Users can register with email and password
           - Users can login with credentials
           - Password reset functionality
        
        2. User Profile Management
           - Users can view and update their profile
           - Profile picture upload
           - Account settings
        
        3. Role-Based Access Control
           - Admin role with full access
           - User role with limited access
        """
        generate_result = generate_artifacts(
            spec_text=sample_text,
            artifact_types=["epic", "stories"]
        )
    
    if not generate_result:
        print("\n[ERROR] Generation failed. Exiting.")
        return
    
    # Step 3: Download files (optional)
    print("\n" + "="*60)
    print("Download Options")
    print("="*60)
    download_choice = input("\nDownload generated files? (y/n): ").strip().lower()
    
    if download_choice == 'y':
        for artifact_type in generate_result['file_paths'].keys():
            download_file("docx", artifact_type)
    
    print("\n" + "="*60)
    print("Complete!")
    print("="*60)
    print("\nGenerated files are available at:")
    print("  backend/data/generated/")
    print("\nYou can also access the API at:")
    print("  http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    main()

