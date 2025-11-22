"""Chatbot router for interactive Q&A."""
from fastapi import APIRouter, HTTPException, Body
from typing import List, Optional
from pydantic import BaseModel
from core.llm_engine import LLMEngine
from core.rag_retriever import RAGRetriever


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    use_rag: bool = True
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    used_rag: bool


# Initialize components
rag_retriever = RAGRetriever()
llm_engine = LLMEngine(rag_retriever=rag_retriever)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest = Body(...)):
    """
    Chat with the AI assistant.
    
    The chatbot can help with:
    - General questions about the system
    - Questions about uploaded functional specifications
    - Questions about generated artifacts (epics, stories, use cases, TDD, data models)
    
    - **message**: User's message/question
    - **use_rag**: Whether to use RAG for context retrieval (default: True)
    - **conversation_history**: Previous conversation messages (optional)
    """
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
    
    try:
        # Convert conversation history if provided
        history = None
        if request.conversation_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ]
        
        # Generate response
        response = llm_engine.chat(
            message=request.message,
            conversation_history=history,
            use_rag=request.use_rag
        )
        
        return ChatResponse(
            response=response,
            used_rag=request.use_rag
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating chat response: {str(e)}"
        )

