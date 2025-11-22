"""LLM engine for generating content using Ollama/Mistral."""
from typing import List, Dict, Any, Optional
from openai import OpenAI
from core.config import settings
from core.rag_retriever import RAGRetriever


class LLMEngine:
    """Engine for LLM-based content generation using Ollama/Mistral."""
    
    def __init__(self, rag_retriever: Optional[RAGRetriever] = None):
        """Initialize LLM engine with Ollama client."""
        # Initialize OpenAI client with Ollama's OpenAI-compatible API
        # Ollama doesn't require authentication, so we use a dummy API key
        # Set longer timeout for local model inference
        self.client = OpenAI(
            api_key="ollama",  # Dummy key, not used by Ollama
            base_url=settings.ollama_api_base,
            timeout=600.0  # 10 minutes timeout for Ollama requests
        )
        self.model = settings.ollama_model
        self.temperature = settings.temperature
        self.max_tokens = settings.max_tokens
        self.rag_retriever = rag_retriever
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate text using LLM."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens
        )
        
        return response.choices[0].message.content
    
    def generate_with_context(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate response using provided context (RAG)."""
        enhanced_prompt = f"""Context:
{context}

Question: {query}

Please answer the question based on the provided context. If the context doesn't contain enough information, say so."""
        
        return self.generate(
            prompt=enhanced_prompt,
            system_prompt=system_prompt or "You are a helpful assistant that answers questions based on provided context."
        )
    
    def generate_requirements_artifacts(
        self,
        spec_text: str,
        artifact_type: str
    ) -> str:
        """Generate requirements artifacts (epic, stories, use cases, TDD, data model)."""
        system_prompts = {
            "epic": """You are a requirements analyst. Generate a well-structured epic document based on the functional specification. 
            Include: title, description, acceptance criteria, and business value.""",
            
            "stories": """You are a requirements analyst. Generate user stories based on the functional specification.
            For each story, include: title, user story format (As a... I want... So that...), acceptance criteria, and story points.""",
            
            "use_cases": """You are a requirements analyst. Generate detailed use cases based on the functional specification.
            For each use case, include: use case name, actors, preconditions, main flow, alternative flows, and postconditions.""",
            
            "tdd": """You are a test engineer. Generate Test-Driven Development (TDD) test cases based on the functional specification.
            Include: test scenarios, test cases with steps, expected results, and test data requirements.""",
            
            "data_model": """You are a data architect. Generate a data model based on the functional specification.
            Include: entities, attributes, relationships, data types, and constraints. Format as ER diagram description or JSON schema."""
        }
        
        system_prompt = system_prompts.get(
            artifact_type.lower(),
            "You are a requirements analyst. Generate structured requirements artifacts."
        )
        
        prompt = f"""Based on the following functional specification, generate {artifact_type}:

{spec_text}

Please provide a comprehensive, well-structured {artifact_type} document."""
        
        return self.generate(prompt=prompt, system_prompt=system_prompt)
    
    def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        use_rag: bool = True
    ) -> str:
        """Chat with the LLM, optionally using RAG for context."""
        if use_rag and self.rag_retriever:
            # Retrieve relevant context
            context = self.rag_retriever.retrieve_context(query=message, n_results=5)
            
            if context:
                return self.generate_with_context(
                    query=message,
                    context=context,
                    system_prompt="You are a helpful assistant for requirements automation. Answer questions based on the provided context from functional specifications and generated artifacts."
                )
        
        # Fallback to regular generation
        return self.generate(
            prompt=message,
            system_prompt="You are a helpful assistant for requirements automation. Help users with questions about functional specifications, requirements artifacts, and the system."
        )

