"""
Chatbot controller
Purpose: Accept user question → retrieve answer → return response
"""

from src.rag.retriever import retrieve


def ask_chatbot(question: str):

    print("\nSearching legal database...")

    answer = retrieve(question)

    return answer