"""
Enhanced Chatbot Controller
Handles both IPC queries and user document queries
"""

from src.rag.retriever import retrieve
from src.document_processing.document_processor import query_uploaded_documents
from src.llm.llm_engine import generate_legal_response


def ask_chatbot(question: str, session_id: str = None, search_mode: str = "ipc"):
    """
    Main chatbot function with support for IPC and uploaded documents
    
    Args:
        question: User's question
        session_id: Session identifier for user documents
        search_mode: "ipc" for IPC database, "uploaded" for user documents, "both" for both
    
    Returns:
        Generated answer
    """
    print(f"\nSearching legal database (mode: {search_mode})...")
    
    if search_mode == "uploaded" and session_id:
        # Search only in uploaded documents
        results = query_uploaded_documents(question, session_id, limit=3)
        
        if len(results) == 0:
            return "No relevant information found in your uploaded documents. Please upload documents first."
        
        # Combine top results
        context = "\n\n".join([result.payload["text"] for result in results[:3]])
        
        # Generate response with Mistral AI
        try:
            response = generate_legal_response(question, context)
            return response
        except Exception as e:
            return f"Retrieved Context:\n{context}"
    
    elif search_mode == "both" and session_id:
        # Search both IPC and uploaded documents
        # First try uploaded documents
        user_results = query_uploaded_documents(question, session_id, limit=2)
        
        # Also search IPC database
        ipc_answer = retrieve(question, use_llm=False)
        
        # Combine contexts
        contexts = []
        if len(user_results) > 0:
            contexts.append("From your uploaded documents:")
            contexts.extend([result.payload["text"] for result in user_results[:2]])
        
        if ipc_answer and ipc_answer != "No relevant legal document found.":
            contexts.append("\nFrom IPC database:")
            contexts.append(ipc_answer)
        
        if len(contexts) == 0:
            return "No relevant information found."
        
        combined_context = "\n\n".join(contexts)
        
        # Generate response with Mistral AI
        try:
            response = generate_legal_response(question, combined_context)
            return response
        except Exception as e:
            return f"Retrieved Context:\n{combined_context}"
    
    else:
        # Default: search IPC database only
        answer = retrieve(question, use_llm=True)
        return answer
