# 🚀 **Agentic Application Development - Learning Path**

Welcome to the comprehensive learning journey of building agentic applications! This repository contains everything we covered on Day 1, organized into logical, progressive chapters.

## 📖 **Day 1 Learning Path Overview**

### **🎯 What You'll Learn**
- **LangChain & LangGraph Fundamentals** - Core concepts and setup
- **Structured AI Responses** - Using Pydantic for predictable outputs
- **Tool Integration** - How AI agents can use external tools
- **Multi-step Conversations** - Building complex conversation flows
- **Model Context Protocol (MCP)** - Connecting AI to real-world services
- **GitHub Integration** - AI agents that can work with repositories
- **Streamlit Basics** - Building user interfaces for your agents

### **📁 Chapter Structure**

| Chapter | Topic | Description | Key Concepts |
|---------|-------|-------------|--------------|
| 1 | **LangChain & LangGraph Basics** | Foundation setup and streaming | LangChain, LangGraph, Groq, streaming |
| 2 | **Structured Output** | Pydantic models for AI responses | Pydantic, validation, schemas |
| 3 | **Chatbot** | Basic conversational AI | Chat loops, user interaction |
| 4 | **Tools Introduction** | Understanding AI tools | Tool concepts, integration |
| 5 | **LangGraph Tools** | Tools in LangGraph framework | LangGraph, tool execution |
| 6 | **Multi-step Chat** | Complex conversation flows | Memory, context, threading |
| 7 | **MCP Deep Dive** | Model Context Protocol | MCP, external services |
| 8 | **GitHub Agent** | AI + GitHub integration | GitHub API, repository operations |
| 9 | **Streamlit Basics** | Web interface creation | Streamlit, UI components |
| 10 | **MCP Server** | Custom MCP implementations | Custom tools, server creation |

## 📖 **Day 2 – Learning Path Overview**

### **🎯 What You'll Learn (Day 2)**
- **Multi‑Model Models (Gemini)**: Text‑to‑image and image understanding
- **Embeddings + Vector DBs**: Create embeddings and store/search with Chroma
- **RAG with Smart Chunking**: Scrape → split → deduplicate → retrieve → answer with Groq
- **Multi‑Agent Architectures**: Simple supervisor flows and hand‑offs
- **Run Models Locally (Ollama)**: Pull/run models and integrate in apps

### **📁 Chapter Structure (Day 2)**

| Chapter | Topic | Description | Key Concepts |
|---------|-------|-------------|--------------|
| 1 | **Multi‑Model Models (Gemini)** | Image generation and captioning demos | `gemini-2.0-flash`, multimodal prompts |
| 2 | **RAG + Embeddings** | Web scraping, smart chunking, embeddings, vector store | Smart chunking, `GoogleGenerativeAIEmbeddings`, `Chroma`, similarity search |
| 3 | **Multi‑Agent Architectures** | Supervisor example for task orchestration | Agent roles, hand‑offs, scoring |
| 4 | **Running Models Locally (Ollama)** | Local LLM setup and usage | `ollama pull/run`, local inference, integration |


## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8+
- Node.js 18+ (for MCP servers)
- Volta (for Node.js version management)

### **Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd "Agentic App"

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Install Node.js tools (if using Volta)
volta install node@20
volta install npm@bundled
```

### **Environment Variables**
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_token_here
```

## 🔧 **Key Technologies Used**

- **LangChain** - AI application framework
- **LangGraph** - Stateful, multi-actor applications
- **Groq** - Fast LLM inference
- **Pydantic** - Data validation and serialization
- **MCP** - Model Context Protocol for tool integration
- **Streamlit** - Web application framework



###
https://huggingface.co/spaces
