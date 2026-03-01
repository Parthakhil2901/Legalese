'''Purpose:
Controls chatbot logic.'''
from src.retriever import retrieve

def chatbot(query):

    answer = retrieve(query)

    return answer