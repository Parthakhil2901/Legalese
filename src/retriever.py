"""
Retriever module
Purpose: Convert user query → embedding → search Qdrant → return best legal text
"""

from src.embedder import get_embedding
from src.qdrant_db import search


def retrieve(query: str):

    # Step 1: convert query to vector embedding
    query_embedding = get_embedding(query)

    # Step 2: search vector database
    results = search(query_embedding)

    if len(results) == 0:
        return "No relevant legal document found."

    # Step 3: extract best match text
    best_match = results[0].payload["text"]

    return best_match