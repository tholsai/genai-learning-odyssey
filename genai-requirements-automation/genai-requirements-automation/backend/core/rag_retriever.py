"""RAG (Retrieval Augmented Generation) retriever for context-aware retrieval."""
from typing import List, Dict, Any, Optional
from core.vectorstore import VectorStore
from core.config import settings


class RAGRetriever:
    """Retriever for RAG-based question answering."""
    
    def __init__(self, vectorstore: Optional[VectorStore] = None):
        """Initialize RAG retriever with vector store."""
        self.vectorstore = vectorstore or VectorStore()
    
    def chunk_text(
        self,
        text: str,
        chunk_size: int = None,
        chunk_overlap: int = None
    ) -> List[str]:
        """Split text into chunks for embedding."""
        chunk_size = chunk_size or settings.chunk_size
        chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            if chunk.strip():
                chunks.append(chunk.strip())
            
            # Move start position with overlap
            start = end - chunk_overlap
        
        return chunks
    
    def index_document(
        self,
        text: str,
        metadata: Dict[str, Any],
        chunk_size: int = None,
        chunk_overlap: int = None
    ) -> List[str]:
        """Index a document by chunking and storing in vector store."""
        # Chunk the text
        chunks = self.chunk_text(text, chunk_size, chunk_overlap)
        
        if not chunks:
            return []
        
        # Prepare metadatas for each chunk
        metadatas = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_index"] = i
            chunk_metadata["total_chunks"] = len(chunks)
            metadatas.append(chunk_metadata)
        
        # Add to vector store
        ids = self.vectorstore.add_documents(
            texts=chunks,
            metadatas=metadatas
        )
        
        return ids
    
    def retrieve_context(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Retrieve relevant context for a query."""
        results = self.vectorstore.search(
            query=query,
            n_results=n_results,
            filter_metadata=filter_metadata
        )
        
        if not results:
            return ""
        
        # Combine retrieved documents into context
        context_parts = []
        for result in results:
            context_parts.append(result["document"])
        
        return "\n\n".join(context_parts)
    
    def retrieve_with_metadata(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve context with metadata."""
        return self.vectorstore.search(
            query=query,
            n_results=n_results,
            filter_metadata=filter_metadata
        )

