"""Configuration settings for the application."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    api_title: str = "GenAI Requirements Automation API"
    api_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # File Storage
    upload_dir: str = "data/spec"
    generated_dir: str = "data/generated"
    downloads_dir: str = "data/downloads"
    embeddings_dir: str = "data/embeddings"
    
    # LLM Settings (Ollama/Mistral)
    ollama_api_base: str = "http://localhost:11434/v1"
    ollama_model: str = "mistral:7b"  # Local Mistral model via Ollama
    temperature: float = 0.7
    max_tokens: int = 4000
    
    # Embeddings Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Vector Store Settings
    chroma_persist_directory: str = "data/embeddings/chroma"
    collection_name: str = "requirements_docs"
    
    # Azure DevOps Settings
    ado_org_url: Optional[str] = None
    ado_pat: Optional[str] = None
    ado_project: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env (like old OPENAI_API_KEY)


settings = Settings()

