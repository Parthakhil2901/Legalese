'''Purpose:
Connects to Qdrant vector database.'''
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
import uuid

# connect to Qdrant running in Docker
client = QdrantClient(
    host="localhost",
    port=6333,
    timeout=60  # increase timeout safety
)

collection_name = "legal_docs"
user_docs_collection = "user_uploaded_docs"


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


# ========== User Uploaded Documents Functions ==========

def ensure_user_docs_collection(vector_size: int = 1024):
    """
    Create user documents collection if it doesn't exist
    
    Args:
        vector_size: Size of the embedding vectors
    """
    try:
        client.get_collection(collection_name=user_docs_collection)
        print(f"Collection '{user_docs_collection}' already exists.")
    except:
        print(f"Creating collection '{user_docs_collection}'...")
        client.create_collection(
            collection_name=user_docs_collection,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{user_docs_collection}' created successfully.")


def insert_user_document(embedding, text: str, doc_id: str, filename: str, session_id: str):
    """
    Insert a chunk from user-uploaded document into database
    
    Args:
        embedding: Vector embedding of the text
        text: Text chunk
        doc_id: Document identifier
        filename: Original filename
        session_id: User session identifier
    """
    # Ensure collection exists
    ensure_user_docs_collection(vector_size=len(embedding))
    
    # Create point with metadata
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding.tolist(),
        payload={
            "text": text,
            "document_id": doc_id,
            "filename": filename,
            "session_id": session_id,
            "source": "user_upload"
        }
    )
    
    client.upsert(
        collection_name=user_docs_collection,
        points=[point],
        wait=True
    )


def search_user_documents(query_embedding, session_id: str, limit: int = 3):
    """
    Search within user's uploaded documents
    
    Args:
        query_embedding: Query vector embedding
        session_id: User session identifier
        limit: Maximum number of results
    
    Returns:
        Search results
    """
    try:
        # Check if collection exists
        client.get_collection(collection_name=user_docs_collection)
        
        # Search with session filter
        results = client.search(
            collection_name=user_docs_collection,
            query_vector=query_embedding.tolist(),
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="session_id",
                        match=MatchValue(value=session_id)
                    )
                ]
            ),
            limit=limit
        )
        
        return results
    except:
        # Collection doesn't exist yet
        return []


def delete_session_documents(session_id: str):
    """
    Delete all documents for a specific session
    
    Args:
        session_id: User session identifier
    """
    try:
        client.delete(
            collection_name=user_docs_collection,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="session_id",
                        match=MatchValue(value=session_id)
                    )
                ]
            )
        )
        print(f"Deleted documents for session: {session_id}")
    except Exception as e:
        print(f"Error deleting session documents: {e}")