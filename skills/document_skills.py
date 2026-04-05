import os
from typing import List
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredODTLoader
)
from langchain_core.documents import Document

# Mapping between file extensions and their corresponding loaders
LOADER_MAPPING = {
    ".pdf": PyPDFLoader,
    ".docx": UnstructuredWordDocumentLoader,
    ".doc": UnstructuredWordDocumentLoader,
    ".pptx": UnstructuredPowerPointLoader,
    ".ppt": UnstructuredPowerPointLoader,
    ".odt": UnstructuredODTLoader,
}

def load_all_documents_from_data(data_dir: str = "data") -> List[Document]:
    """
    Scans all supported documents in the specified directory and returns a list of LangChain Documents.
    """
    if not os.path.exists(data_dir):
        print(f"❌ Error: Directory '{data_dir}' does not exist.")
        return []

    all_docs = []
    
    # Iterate through the mapping and load each file format
    for ext, loader_class in LOADER_MAPPING.items():
        # Using glob pattern to recursively find all files with the specific extension
        print(f"📂 Scanning for {ext} files...")
        loader = DirectoryLoader(
            data_dir,
            glob=f"**/*{ext}",
            loader_cls=loader_class,
            show_progress=True,
            use_multithreading=True
        )
        
        try:
            sub_docs = loader.load()
            if sub_docs:
                print(f"✅ Successfully loaded {len(sub_docs)} chunks from {ext} files.")
                all_docs.extend(sub_docs)
        except Exception as e:
            print(f"⚠️ Error occurred while loading {ext} format: {e}")

    print(f"\n✨ Scan complete! Total document chunks loaded: {len(all_docs)}")
    return all_docs

# =========================================
# Local Testing Code 
# =========================================
if __name__ == "__main__":
    docs = load_all_documents_from_data()
    if docs:
        print(f"Preview of the first chunk: {docs[0].page_content[:200]}...")
        print(f"Source Metadata: {docs[0].metadata}")