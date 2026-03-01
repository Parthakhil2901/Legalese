'''Purpose:
Converts text → vector embedding.'''
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-large-en-v1.5")

def get_embedding(text):

    embedding = model.encode(text, normalize_embeddings=True)

    return embedding