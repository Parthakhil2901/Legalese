'''Purpose:
Connects to Qdrant vector database.'''
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

client = QdrantClient("localhost", port=6333)

collection_name = "legal_docs"


def create_collection(vector_size):

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )


def insert_document(id, embedding, text):

    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=id,
                vector=embedding.tolist(),
                payload={"text": text}
            )
        ]
    )


def search(query_embedding):

    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding.tolist(),
        limit=1
    )

    return results