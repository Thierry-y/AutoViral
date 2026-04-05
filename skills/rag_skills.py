from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.tools import tool

@tool
def search_product_knowledge(query: str) -> str:
    """
    当你需要了解产品的核心卖点、详细参数、使用说明或品牌信息时，必须使用此工具。
    输入应该是一个具体的查询问题。
    """
    try:
        # Connect to the existing local vector database
        local_embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
        vector_db = Chroma(
            persist_directory="db",
            embedding_function=local_embeddings
        )
        
        # Search for the top 3 most relevant segments
        results = vector_db.similarity_search(query, k=3)
        
        if not results:
            return "No relevant product information found in the database for this query."
            
        # Concatenate search results into a text block for the LLM
        formatted_results = []
        for i, doc in enumerate(results):
            source = doc.metadata.get('source', 'Unknown Source')
            formatted_results.append(f"[Source: {source}]\nContent: {doc.page_content}")
            
        return "\n\n".join(formatted_results)
        
    except Exception as e:
        return f"An error occurred while querying the database: {str(e)}"

# =========================================
# Local Testing Code 
# =========================================
if __name__ == "__main__":
    print("=== Starting RAG Tool Independent Test ===")
    
    # Simulate a query issued by the Agent
    # Update this query based on the actual content in your data/ folder
    test_query = "display information" 
    
    print(f"Executing query: {test_query}")
    result = search_product_knowledge.invoke({"query": test_query})
    
    print("\n--- Raw Information Returned to Agent ---")
    print(result)
    print("------------------------------------------")