'''Purpose:
Converts text → vector embedding.'''
from sentence_transformers import SentenceTransformer

print("Loading BGE-large model (first run may take few minutes)...")

model = SentenceTransformer("BAAI/bge-large-en-v1.5")

print("BGE-large model loaded successfully.")


def get_embedding(text: str):

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding