import openai
from typing import Optional

class ChatbotService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.context_documents = ""
        self.conversation_history = []
    
    def set_context(self, documents_content: str):
        """Set the context from generated documents"""
        self.context_documents = documents_content
        self.conversation_history = []
    
    def ask_question(self, question: str) -> str:
        """Answer questions based only on the provided context"""
        try:
            if not self.context_documents:
                return "No documents available. Please generate documents first."
            
            system_prompt = f"""
            You are a helpful assistant that answers questions ONLY based on the provided document context.
            
            IMPORTANT RULES:
            1. Only use information from the provided context
            2. If the answer is not in the context, say "I don't have that information in the current documents"
            3. Do not make up or hallucinate any information
            4. Be concise and accurate
            
            CONTEXT DOCUMENTS:
            {self.context_documents}
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                *self.conversation_history,
                {"role": "user", "content": question}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                top_p=1,
                messages=messages,
                temperature=0.1,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            # Keep only last 10 exchanges to manage context length
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return answer
            
        except Exception as e:
            return f"Error processing question: {str(e)}"