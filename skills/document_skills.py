import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredODTLoader
)

def read_local_document(file_path: str) -> str:
    """
    Read local documents (supports PDF, DOCX, PPTX, ODT) and extract plain text.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        return f"System Prompt: File not found at {file_path}. Please check the path."

    # Get file extension
    extension = file_path.split('.')[-1].lower()
    print(f"Parsing {extension.upper()} file...")
    
    try:
        if extension == 'pdf':
            loader = PyPDFLoader(file_path)
            
        elif extension in ['doc', 'docx']:
            loader = UnstructuredWordDocumentLoader(file_path)
            
        elif extension in ['ppt', 'pptx']:
            loader = UnstructuredPowerPointLoader(file_path)

        elif extension == 'odt': 
            loader = UnstructuredODTLoader(file_path)
            
        else:
            return f"System Prompt: File format .{extension} is not currently supported."
            
        # Execute loading and merge text content
        documents = loader.load()
        text_content = "\n".join([doc.page_content for doc in documents])
        
        print(f"Parsing successful! Extracted {len(text_content)} characters.")
        return text_content
        
    except Exception as e:
        return f"System Prompt: An unknown error occurred while reading the file: {str(e)}"

# =========================================
# Local Testing Code 
# =========================================
if __name__ == "__main__":
    # Ensure this path matches your local environment
    test_file = "data/leaflet.pdf"
    content = read_local_document(test_file)
    print(content)
    print("Document loader module loaded successfully.")