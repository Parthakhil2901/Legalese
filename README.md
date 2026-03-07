# LexIntel - Legal AI Chatbot

An AI-powered legal assistant specializing in Indian Penal Code (IPC) using RAG (Retrieval Augmented Generation) and Mistral AI.

## Features

- 🔍 Semantic search through IPC sections using vector embeddings
- 🤖 Natural language responses powered by Mistral AI
- 💬 Interactive Streamlit chat interface
- 📚 Vector database storage using Qdrant
- 🎯 Accurate legal information retrieval
- 📄 **Document Upload**: Upload PDF, DOC, DOCX files and ask questions about them
- 🔀 **Multi-Source Search**: Search IPC database, uploaded documents, or both
- 🗑️ **Document Management**: Manage and delete uploaded documents per session

## Architecture

1. **User Query** → Converted to embeddings using sentence-transformers
2. **Vector Search** → Searches Qdrant database for relevant IPC sections
3. **Context Retrieval** → Retrieves most relevant legal text
4. **LLM Generation** → Mistral AI generates a natural, accurate response
5. **Response Delivery** → User receives clear legal information

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Mistral AI API Key

Get your API key from [Mistral AI Console](https://console.mistral.ai/)

Set the environment variable:

**Windows (PowerShell):**
```powershell
$env:MISTRAL_API_KEY="your_mistral_api_key_here"
```

**Linux/Mac:**
```bash
export MISTRAL_API_KEY="your_mistral_api_key_here"
```

Or create a `.env` file (copy from `.env.example`):
```
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 3. Run the Application

**Streamlit UI (Recommended):**
```bash
streamlit run ui/streamlit_ui.py
```

**Terminal Interface:**
```bash
python app.py
```

## Project Structure

```
Legalese/
├── app.py                    # Terminal interface
├── ui/
│   └── streamlit_ui.py       # Streamlit chat interface
├── src/
│   ├── chatbot/
│   │   └── chatbot.py        # Main chatbot controller
│   ├── rag/
│   │   └── retriever.py      # RAG retrieval logic
│   ├── llm/
│   │   ├── llm_engine.py     # Mistral AI integration
│   │   └── prompt_templates.py
│   ├── embeddings/
│   │   └── embedder.py       # Embedding generation
│   └── database/
│       └── qdrant_db.py      # Vector database operations
└── data/
    └── legal_docs/           # IPC sections data
```

## Usage

### Basic Usage (IPC Database)

1. Launch the Streamlit interface
2. Type your legal question in the chat input
3. The system will:
   - Search the IPC database for relevant sections
   - Pass the context to Mistral AI
   - Generate a clear, accurate response
4. View the response in natural language

### Document Upload Feature

1. **Upload Documents**:
   - Click on the sidebar's "Document Upload" section
   - Upload PDF, DOC, or DOCX files
   - Wait for processing confirmation
   - Uploaded documents are stored per session

2. **Select Search Mode**:
   - **IPC Database**: Search only in Indian Penal Code sections
   - **Uploaded Documents**: Search only in your uploaded files
   - **Both**: Search across IPC and your documents

3. **Ask Questions**:
   - Type questions related to your uploaded documents
   - Get AI-generated answers based on your document content
   - Switch between search modes anytime

4. **Manage Documents**:
   - View uploaded documents in the sidebar
   - Clear chat history without deleting documents
   - Delete all uploaded documents using "Delete Docs" button

### Example Queries

**IPC Database:**
- "What is Section 302 of IPC?"
- "Explain defamation under Indian law"

**Uploaded Documents:**
- "Summarize the main points of this contract"
- "What are the liability clauses?"
- "Explain the terms and conditions"

## Technologies Used

- **Streamlit** - Web interface
- **Mistral AI** - LLM for response generation
- **Sentence Transformers** - Text embeddings
- **Qdrant** - Vector database
- **PyPDF2** - PDF document processing
- **python-docx** - Word document processing
- **Python 3.11+**

## License

© 2026 LexIntel