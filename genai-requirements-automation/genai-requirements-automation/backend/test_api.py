"""Simple test script to verify the API is working."""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"


def test_health():
    """Test the health endpoint."""
    print("=" * 50)
    print("Testing Health Endpoint")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_generate():
    """Test the generate endpoint."""
    print("\n" + "=" * 50)
    print("Testing Generate Endpoint")
    print("=" * 50)
    
    spec_text = """
    Functional Specification: User Management System
    
    The system should provide the following features:
    
    1. User Authentication
       - Users can register with email and password
       - Users can login with credentials
       - Password reset functionality
       - Session management
    
    2. User Profile Management
       - Users can view their profile
       - Users can update profile information
       - Profile picture upload
       - Account settings
    
    3. Role-Based Access Control
       - Admin role with full access
       - User role with limited access
       - Role assignment and management
    """
    
    data = {
        "spec_text": spec_text,
        "artifact_types": ["epic", "stories"],
        "output_format": "docx"
    }
    
    try:
        print("Sending generate request...")
        response = requests.post(
            f"{API_BASE}/generate",
            json=data,
            timeout=120  # Longer timeout for LLM generation
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Message: {result['message']}")
            print(f"Generated artifacts: {list(result['artifacts'].keys())}")
            print(f"File paths: {list(result['file_paths'].keys())}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_chat():
    """Test the chat endpoint."""
    print("\n" + "=" * 50)
    print("Testing Chat Endpoint")
    print("=" * 50)
    
    data = {
        "message": "What are the main features in a user management system?",
        "use_rag": False  # Set to False if no documents uploaded yet
    }
    
    try:
        print("Sending chat request...")
        response = requests.post(
            f"{API_BASE}/chat",
            json=data,
            timeout=60
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result['response']}")
            print(f"Used RAG: {result['used_rag']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("GenAI Requirements Automation API Test")
    print("=" * 50)
    print("\nMake sure the server is running on http://localhost:8000")
    print("Press Ctrl+C to cancel, or wait 5 seconds to continue...")
    
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    
    results = []
    
    # Test health
    results.append(("Health Check", test_health()))
    
    # Test chat (doesn't require upload)
    results.append(("Chat", test_chat()))
    
    # Test generate (requires Ollama running with Mistral model)
    print("\n" + "=" * 50)
    print("Note: Generate test requires Ollama running with Mistral model")
    print("=" * 50)
    try:
        results.append(("Generate", test_generate()))
    except Exception as e:
        print(f"Generate test failed: {e}")
        results.append(("Generate", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print(f"\nOverall: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")


if __name__ == "__main__":
    main()

