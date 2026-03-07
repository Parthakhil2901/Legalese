"""
Retriever module
Purpose: Convert user query → embedding → search Qdrant → return best legal text
"""

from src.embeddings.embedder import get_embedding
from src.database.qdrant_db import search
from src.llm.llm_engine import generate_legal_response


def retrieve(query: str, use_llm: bool = True):
    """
    Retrieve relevant legal information and optionally generate LLM response
    
    Args:
        query: User's legal question
        use_llm: Whether to use Mistral AI to generate a response (default: True)
    
    Returns:
        Generated response or raw retrieved text
    """

    # Step 1: convert query to vector embedding
    query_embedding = get_embedding(query)

    # Step 2: search vector database
    results = search(query_embedding)

    if len(results) == 0:
        return "No relevant legal document found."

    # Step 3: extract best match text
    best_match = results[0].payload["text"]
    
    # Step 4: Use Mistral AI to generate a natural response
    if use_llm:
        try:
            response = generate_legal_response(query, best_match)
            return response
        except Exception as e:
            # Fallback to raw text if LLM fails
            print(f"LLM generation failed: {e}")
            return f"Retrieved Context:\n{best_match}"
    
    return best_match