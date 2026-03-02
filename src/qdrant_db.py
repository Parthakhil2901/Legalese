'''Purpose:
Connects to Qdrant vector database.'''
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# connect to Qdrant running in Docker
client = QdrantClient(
    host="localhost",
    port=6333,
    timeout=60  # increase timeout safety
)

collection_name = "legal_docs"


def create_collection(vector_size: int):

    print("Creating collection in Qdrant...")

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )

    print("Collection created successfully.")


def insert_batch(start_id: int, embeddings: list, texts: list):

    points = []

    for i, (embedding, text) in enumerate(zip(embeddings, texts)):

        points.append(
            PointStruct(
                id=start_id + i,
                vector=embedding.tolist(),
                payload={"text": text}
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points,
        wait=True
    )


def search(query_embedding):

    results = client.search(

        collection_name=collection_name,

        query_vector=query_embedding.tolist(),

        limit=5

    )

    return results