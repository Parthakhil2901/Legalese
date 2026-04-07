'''
Purpose:
Splits large legal documents into smaller chunks.
Why needed:

Embedding models have token limits.

Also improves search accuracy.
'''

from typing import List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Input text to chunk
        chunk_size: Maximum number of words per chunk
        overlap: Number of overlapping words between chunks
    
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    
    if len(words) == 0:
        return []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
        
        # Break if we've reached the end
        if i + chunk_size >= len(words):
            break
    
    return chunks