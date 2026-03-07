"""
LexIntel Legal AI Chatbot
Streamlit UI Interface
"""

import streamlit as st
import sys
from pathlib import Path
import uuid

# Add parent directory to path to import src modules
sys.path.append(str(Path(__file__).parent.parent))

from src.chatbot.chatbot_enhanced import ask_chatbot
from src.document_processing.document_processor import process_uploaded_document
from src.database.qdrant_db import delete_session_documents


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "uploaded_documents" not in st.session_state:
        st.session_state.uploaded_documents = []
    
    if "search_mode" not in st.session_state:
        st.session_state.search_mode = "ipc"  # Default to IPC search


def main():
    # Page configuration
    st.set_page_config(
        page_title="LexIntel Legal AI Chatbot",
        page_icon="⚖️",
        layout="wide"
    )

    # Initialize session state
    initialize_session_state()

    # App header
    st.title("⚖️ LexIntel Legal AI Chatbot")
    st.markdown("Ask legal questions from IPC sections or upload your own documents.")
    st.divider()
    
    # Sidebar for document upload and settings
    with st.sidebar:
        st.header("📄 Document Upload")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload legal documents (PDF, DOC, DOCX)",
            type=["pdf", "doc", "docx"],
            accept_multiple_files=True,
            help="Upload your legal documents to ask questions about them"
        )
        
        # Process uploaded files
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Check if already processed
                if uploaded_file.name not in st.session_state.uploaded_documents:
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        # Read file content
                        file_content = uploaded_file.read()
                        
                        # Process document
                        result = process_uploaded_document(
                            file_content,
                            uploaded_file.name,
                            st.session_state.session_id
                        )
                        
                        if result["success"]:
                            st.session_state.uploaded_documents.append(uploaded_file.name)
                            st.success(f"✅ {result['message']}")
                        else:
                            st.error(f"❌ {result['error']}")
        
        # Show uploaded documents
        if st.session_state.uploaded_documents:
            st.subheader("Uploaded Documents")
            for doc in st.session_state.uploaded_documents:
                st.text(f"📄 {doc}")
        
        st.divider()
        
        # Search mode selection
        st.header("🔍 Search Mode")
        
        search_options = ["IPC Database", "Uploaded Documents", "Both"]
        search_mode_map = {
            "IPC Database": "ipc",
            "Uploaded Documents": "uploaded",
            "Both": "both"
        }
        
        selected_mode = st.radio(
            "Choose search source:",
            search_options,
            index=0,
            help="Select where to search for answers"
        )
        
        st.session_state.search_mode = search_mode_map[selected_mode]
        
        st.divider()
        
        # Actions
        st.header("Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("Delete Docs", use_container_width=True):
                if st.session_state.uploaded_documents:
                    delete_session_documents(st.session_state.session_id)
                    st.session_state.uploaded_documents = []
                    st.success("Documents deleted!")
                    st.rerun()
        
        st.divider()
        
        # About section
        st.header("About")
        st.info(
            "🔹 **IPC Database**: Search Indian Penal Code sections\n\n"
            "🔹 **Uploaded Documents**: Search your uploaded documents\n\n"
            "🔹 **Both**: Search across all sources"
        )
        
        st.caption("LexIntel © 2026")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask your legal question..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Searching legal database..."):
                response = ask_chatbot(
                    prompt,
                    session_id=st.session_state.session_id,
                    search_mode=st.session_state.search_mode
                )
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
