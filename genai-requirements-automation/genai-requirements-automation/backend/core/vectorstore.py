"""Vector store using ChromaDB for document storage and retrieval."""
import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from core.config import settings
from core.embeddings import EmbeddingGenerator


class VectorStore:
    """ChromaDB vector store for storing and retrieving document embeddings."""
    
    def __init__(self):
        """Initialize ChromaDB client and collection."""
        self.embedding_generator = EmbeddingGenerator()
        self.client = None
        self.collection = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize ChromaDB client and collection."""
        os.makedirs(settings.chroma_persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name=settings.collection_name
            )
        except Exception:
            # Collection doesn't exist, create it
            self.collection = self.client.create_collection(
                name=settings.collection_name,
                metadata={"description": "Requirements documents and generated artifacts"}
            )
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add documents to the vector store."""
        if not texts:
            return []
        
        # Generate embeddings
        embeddings = self.embedding_generator.generate_embeddings_batch(texts)
        
        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc_{i}_{hash(text[:50])}" for i, text in enumerate(texts)]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        if not query or not query.strip():
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        if results["documents"] and len(results["documents"][0]) > 0:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None,
                    "id": results["ids"][0][i] if results["ids"] else None
                })
        
        return formatted_results
    
    def delete_documents(self, ids: List[str]) -> bool:
        """Delete documents by IDs."""
        try:
            self.collection.delete(ids=ids)
            return True
        except Exception as e:
            print(f"Error deleting documents: {str(e)}")
            return False
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        count = self.collection.count()
        return {
            "collection_name": settings.collection_name,
            "document_count": count
        }

