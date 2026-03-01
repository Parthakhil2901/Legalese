import os
from src.embedder import get_embedding
from src.qdrant_db import create_collection, insert_document
from src.chatbot import chatbot

folder = "data/legal_docs"

documents = []

for file in os.listdir(folder):

    with open(os.path.join(folder, file), "r", encoding="utf-8") as f:

        documents.append(f.read())


embedding = get_embedding(documents[0])

vector_size = len(embedding)

create_collection(vector_size)


for i, doc in enumerate(documents):

    emb = get_embedding(doc)

    insert_document(i, emb, doc)


while True:

    query = input("Ask legal question: ")

    answer = chatbot(query)

    print("\nAnswer:\n", answer)