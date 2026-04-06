import os
from utils.document_utils import load_all_documents_from_data
from utils.knowledge_manager import sync_knowledge_base
from skills.rag_skills import search_product_knowledge
from prompts.xhs_prompts import XHS_STUFFING_TEMPLATE, XHS_RAG_AGENT_TEMPLATE

# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage 

MAX_CONTEXT_LENGTH = 11451

def start_interactive_agent():
    raw_docs = load_all_documents_from_data()
    total_text = "\n\n".join([doc.page_content for doc in raw_docs])
    text_length = len(total_text)
    
    print("🧠 Connecting to local Ollama model...")
    llm = ChatOllama(model="qwen3.5:27b", temperature=0.7)
    
    chat_history = []

    if text_length < MAX_CONTEXT_LENGTH:
        print("🟢 SYSTEM: Short document detected. Entering [Full Context Mode].")
        prompt = ChatPromptTemplate.from_messages([
            ("system", XHS_STUFFING_TEMPLATE),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("user", "{input}")
        ])
        chain = prompt | llm
        mode = "STUFFING"
    else:
        print("🔴 SYSTEM: Long document detected. Entering [RAG Agent Mode].")
        sync_knowledge_base()
        tools = [search_product_knowledge]
        prompt = ChatPromptTemplate.from_messages([
            ("system", XHS_RAG_AGENT_TEMPLATE),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_tool_calling_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
        mode = "RAG"

    print("\n🚀 Xiaohongshu(rednote) Viral Copywriter is ready! Type 'exit' or 'quit' to stop.")
    
    while True:
        user_input = input("\n👤 User: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye! Looking forward to your next creation.")
            break

        try:
            if mode == "STUFFING":
                response = chain.invoke({
                    "input": user_input,
                    "product_data": total_text,
                    "chat_history": chat_history 
                })
                answer = response.content
            else:
                response = executor.invoke({
                    "input": user_input,
                    "chat_history": chat_history 
                })
                answer = response["output"]

            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=answer))

            print(f"\n🤖 Master:\n{answer}")
            
        except Exception as e:
            print(f"\n⚠️ Oops, the model encountered an error: {e}")
            print("Please check if the Ollama service is running or if the model name is correct.")

if __name__ == "__main__":
    start_interactive_agent()