"""Embeddings generation using sentence-transformers."""
from typing import List
from sentence_transformers import SentenceTransformer
from core.config import settings


class EmbeddingGenerator:
    """Generate embeddings for text using sentence-transformers."""
    
    def __init__(self, model_name: str = None):
        """Initialize the embedding model."""
        self.model_name = model_name or settings.embedding_model
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model."""
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        if not texts:
            return []
        
        # Filter out empty texts
        valid_texts = [text for text in texts if text and text.strip()]
        if not valid_texts:
            return []
        
        embeddings = self.model.encode(valid_texts, normalize_embeddings=True)
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings."""
        if self.model is None:
            self._load_model()
        return self.model.get_sentence_embedding_dimension()

