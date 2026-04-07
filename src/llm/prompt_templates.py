"""
Prompt templates for LLM generation
"""

LEGAL_QA_SYSTEM_PROMPT = """You are LexIntel, an expert legal AI assistant specializing in Indian Penal Code (IPC).
Your role is to provide accurate, clear, and helpful legal information based on the context provided.

Guidelines:
- Use the provided legal context to answer the user's question
- Be precise and cite relevant IPC sections when applicable
- If the context doesn't contain enough information, acknowledge the limitation
- Use clear, professional language
- Avoid making definitive legal judgments - provide information only
- Structure your response clearly with relevant details
"""

def create_legal_qa_prompt(user_question: str, retrieved_context: str) -> str:
    """
    Create a prompt for legal Q&A using retrieved context
    
    Args:
        user_question: The user's legal question
        retrieved_context: Retrieved legal text from the database
    
    Returns:
        Formatted prompt string
    """
    prompt = f"""Context from IPC Database:
{retrieved_context}

User Question: {user_question}

Based on the context provided above, please provide a clear and accurate answer to the user's question. If the context is relevant, explain how it applies to their question. If the context doesn't fully address their question, acknowledge this and provide what information you can.

Answer:"""
    
    return prompt