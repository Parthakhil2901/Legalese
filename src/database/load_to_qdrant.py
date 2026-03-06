import os

from src.embeddings.embedder import get_embedding
from src.database.qdrant_db import create_collection, insert_batch

DATA_FOLDER = "data/legal_docs/ipc"

print("Loading legal documents...")

documents = []

for filename in os.listdir(DATA_FOLDER):

    filepath = os.path.join(DATA_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8") as f:

        text = f.read()

        documents.append(text)

print(f"{len(documents)} documents loaded.")


print("Creating embedding to determine vector size...")

first_embedding = get_embedding(documents[0])

vector_size = len(first_embedding)

create_collection(vector_size)


print("Storing documents in Qdrant using batch insertion...")

batch_size = 32

for i in range(0, len(documents), batch_size):

    batch_docs = documents[i:i + batch_size]

    batch_embeddings = []

    for doc in batch_docs:

        embedding = get_embedding(doc)

        batch_embeddings.append(embedding)

    insert_batch(i, batch_embeddings, batch_docs)

    print(f"Stored batch {i} to {i + len(batch_docs)}")


print("All documents successfully stored in Qdrant.")