"""
Document Loader
Purpose: Load and extract text from PDF and DOC/DOCX files
"""

import io
from typing import Union
import PyPDF2
from docx import Document


def load_pdf(file_content: Union[bytes, io.BytesIO]) -> str:
    """
    Extract text from PDF file
    
    Args:
        file_content: PDF file content as bytes or BytesIO
    
    Returns:
        Extracted text as string
    """
    try:
        if isinstance(file_content, bytes):
            file_content = io.BytesIO(file_content)
        
        pdf_reader = PyPDF2.PdfReader(file_content)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error loading PDF: {str(e)}")


def load_docx(file_content: Union[bytes, io.BytesIO]) -> str:
    """
    Extract text from DOCX file
    
    Args:
        file_content: DOCX file content as bytes or BytesIO
    
    Returns:
        Extracted text as string
    """
    try:
        if isinstance(file_content, bytes):
            file_content = io.BytesIO(file_content)
        
        doc = Document(file_content)
        text = ""
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error loading DOCX: {str(e)}")


def load_document(file_content: Union[bytes, io.BytesIO], file_type: str) -> str:
    """
    Load document based on file type
    
    Args:
        file_content: File content as bytes or BytesIO
        file_type: File extension (pdf, doc, docx)
    
    Returns:
        Extracted text
    """
    file_type = file_type.lower().replace('.', '')
    
    if file_type == 'pdf':
        return load_pdf(file_content)
    elif file_type in ['doc', 'docx']:
        return load_docx(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_type}. Supported: PDF, DOC, DOCX")
