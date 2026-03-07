"""
LLM Engine using Mistral AI
"""

import os
from dotenv import load_dotenv
from mistralai import Mistral
from src.llm.prompt_templates import LEGAL_QA_SYSTEM_PROMPT, create_legal_qa_prompt

# Load environment variables from .env file
load_dotenv()


class MistralLLM:
    """
    Mistral AI LLM wrapper for generating legal responses
    """
    
    def __init__(self, api_key: str = None, model: str = "mistral-large-latest"):
        """
        Initialize Mistral AI client
        
        Args:
            api_key: Mistral API key (if None, will look for MISTRAL_API_KEY env var)
            model: Mistral model to use
        """
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Mistral API key not found. Set MISTRAL_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = Mistral(api_key=self.api_key)
        self.model = model
    
    def generate_response(self, user_question: str, retrieved_context: str) -> str:
        """
        Generate a response using Mistral AI based on retrieved context
        
        Args:
            user_question: The user's question
            retrieved_context: Retrieved legal text from the database
        
        Returns:
            Generated response from Mistral AI
        """
        try:
            # Create the prompt
            user_prompt = create_legal_qa_prompt(user_question, retrieved_context)
            
            # Call Mistral AI
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": LEGAL_QA_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=1000
            )
            
            # Extract and return the response
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"


# Global instance (will be initialized on first use)
_mistral_instance = None


def get_mistral_llm() -> MistralLLM:
    """
    Get or create the global Mistral LLM instance
    
    Returns:
        MistralLLM instance
    """
    global _mistral_instance
    if _mistral_instance is None:
        _mistral_instance = MistralLLM()
    return _mistral_instance


def generate_legal_response(user_question: str, retrieved_context: str) -> str:
    """
    Helper function to generate a legal response
    
    Args:
        user_question: The user's question
        retrieved_context: Retrieved legal text from database
    
    Returns:
        Generated response
    """
    llm = get_mistral_llm()
    return llm.generate_response(user_question, retrieved_context)