'''Purpose:
Implements retrieval algorithm.'''
from src.embedder import get_embedding
from src.qdrant_db import search
from src.reranker import rerank

def retrieve(query):

    query_embedding = get_embedding(query)

    results = search(query_embedding)

    docs = [result.payload["text"] for result in results]

    ranked_docs = rerank(query, docs)

    return ranked_docs