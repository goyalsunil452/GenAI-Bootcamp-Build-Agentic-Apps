from dotenv import load_dotenv

load_dotenv()
from langchain.chat_models import init_chat_model

import getpass
import os

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_chroma import Chroma

# Import smart chunking functions
from smart_chunking import (
    create_smart_chunks,
    post_retrieval_deduplication,
    get_chunking_stats,
)

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Initialize ChromaDB vector store
vectorstore = Chroma(
    collection_name="educosys_genai_info",
    embedding_function=embeddings,
    persist_directory="./chroma_genai",
)

# Load and chunk documents
loader = WebBaseLoader(web_paths=["https://www.educosys.com/course/genai"])
docs = loader.load()

# Use smart chunking module
all_splits = create_smart_chunks(docs, chunk_size=1000, chunk_overlap=200)

# Get chunking statistics
stats = get_chunking_stats(len(docs), len(all_splits))
print(
    f"Chunking efficiency: {stats['efficiency_gain']} ({stats['reduction_percentage']}% reduction)"
)

# Create embeddings for each chunk
chunk_embeddings = []

for i, chunk in enumerate(all_splits):
    # Get embedding for this chunk
    embedding_vector = embeddings.embed_query(chunk.page_content)

    # Store chunk with its embedding
    chunk_info = {
        "chunk": chunk,
        "embedding": embedding_vector,
        "embedding_dimensions": len(embedding_vector),
    }
    chunk_embeddings.append(chunk_info)

# Store chunks in ChromaDB
try:
    vectorstore.add_documents(documents=all_splits)

    # Check total stored chunks
    total_stored = vectorstore._collection.count()
    print(f"Total chunks in ChromaDB: {total_stored}")

except Exception as e:
    print(f"Error storing in ChromaDB: {e}")

print("Website extraction, chunking, embedding, and storage completed successfully!")

# Initialize Groq LLM
llm = init_chat_model("llama-3.1-8b-instant", model_provider="groq")


# Create a retrieval tool for the agent
@tool
def retrieve_context(query: str) -> str:
    """Retrieve relevant context from the knowledge base based on the query."""
    try:
        # Get relevant documents from ChromaDB
        relevant_docs = vectorstore.similarity_search(query, k=3)

        if not relevant_docs:
            return "No relevant information found in the knowledge base."

        # Use post-retrieval deduplication from smart chunking module
        unique_docs = post_retrieval_deduplication(relevant_docs)

        # Combine unique contexts
        context = "\n\n---\n\n".join([doc.page_content for doc in unique_docs])

        return f"Relevant context from the knowledge base:\n\n{context}"

    except Exception as e:
        return f"Error retrieving context: {str(e)}"


# Create the RAG agent
agent_executor = create_react_agent(llm, [retrieve_context])

# Test the RAG agent
input_message = "Tell me about MCP topic?"

try:
    for event in agent_executor.stream(
        {"messages": [{"role": "user", "content": input_message}]}, stream_mode="values"
    ):
        if "messages" in event and event["messages"]:
            latest_message = event["messages"][-1]
            if hasattr(latest_message, "pretty_print"):
                latest_message.pretty_print()
            else:
                print(f"Agent: {latest_message.content}")

except Exception as e:
    print(f"Error in RAG agent: {e}")

    try:
        response = agent_executor.invoke(
            {"messages": [{"role": "user", "content": input_message}]}
        )
        print(f"Agent Response: {response['messages'][-1].content}")
    except Exception as e2:
        print(f"Fallback also failed: {e2}")
