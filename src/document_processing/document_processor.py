"""
Document Processor
Purpose: Process uploaded documents and store them in vector database
"""

from typing import List, Dict
import uuid
from src.document_processing.pdf_loader import load_document
from src.document_processing.chunker import chunk_text
from src.embeddings.embedder import get_embedding
from src.database.qdrant_db import insert_user_document, search_user_documents


def process_uploaded_document(file_content: bytes, filename: str, session_id: str) -> Dict:
    """
    Process an uploaded document and store it in the database
    
    Args:
        file_content: Raw file content as bytes
        filename: Original filename
        session_id: User session identifier
    
    Returns:
        Dictionary with processing results
    """
    try:
        # Extract file extension
        file_extension = filename.split('.')[-1].lower()
        
        # Load document text
        print(f"Loading document: {filename}")
        text = load_document(file_content, file_extension)
        
        if not text or len(text.strip()) == 0:
            return {
                "success": False,
                "error": "No text could be extracted from the document"
            }
        
        # Chunk the text
        print("Chunking document...")
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        
        if len(chunks) == 0:
            return {
                "success": False,
                "error": "Could not create chunks from document"
            }
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Process chunks and store in database
        print(f"Processing {len(chunks)} chunks...")
        for chunk in chunks:
            # Generate embedding
            embedding = get_embedding(chunk)
            
            # Store in database with metadata
            insert_user_document(
                embedding=embedding,
                text=chunk,
                doc_id=doc_id,
                filename=filename,
                session_id=session_id
            )
        
        return {
            "success": True,
            "document_id": doc_id,
            "filename": filename,
            "chunks": len(chunks),
            "message": f"Successfully processed {filename} ({len(chunks)} chunks)"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing document: {str(e)}"
        }


def query_uploaded_documents(query: str, session_id: str, limit: int = 3) -> List[Dict]:
    """
    Search within user's uploaded documents
    
    Args:
        query: User's search query
        session_id: User session identifier
        limit: Maximum number of results
    
    Returns:
        List of search results
    """
    try:
        # Generate query embedding
        query_embedding = get_embedding(query)
        
        # Search in user's documents
        results = search_user_documents(query_embedding, session_id, limit)
        
        return results
        
    except Exception as e:
        print(f"Error searching documents: {e}")
        return []
