# LangChain & LangGraph Basics

## Structure

### langchain/ folder
- **simple_chat.py** - Basic LangChain usage with `init_chat_model`
- **streaming_chat.py** - Streaming chat with `ChatGroq`

### langgraph/ folder  
- **main.py** - Advanced LangGraph implementation with state management
- **simple_checkpoint.py** - LangGraph with memory using InMemorySaver

## What Each File Shows

### simple_chat.py
```python
model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")
response = model.invoke("What is Groq?")
print(response.content)
```
**Learning**: Basic model initialization and single response generation

### streaming_chat.py
```python
for chunk in model.stream(user_input):
    print(chunk.content, end="", flush=True)
```
**Learning**: Streaming responses word by word for better user experience

### main.py (LangGraph)
**Learning**: State management, graph-based conversation flow, advanced streaming

### simple_checkpoint.py (LangGraph + Memory)
**Learning**: How to maintain conversation memory using checkpoints and thread_id

## How to Run

1. Install: `pip install -r requirements.txt`
2. Set up `.env` file with GROQ_API_KEY
3. Run examples:
   - `python langchain/simple_chat.py`
   - `python langchain/streaming_chat.py`
   - `python langgraph/main.py`
   - `python langgraph/simple_checkpoint.py`

## Learning Progression

1. **Start with simple_chat.py** - Understand basic LangChain
2. **Try streaming_chat.py** - See streaming difference
3. **Move to main.py** - Learn LangGraph concepts
4. **Try simple_checkpoint.py** - Understand conversation memory

## Key Concepts Covered

- **LangChain**: Basic AI model interaction
- **Streaming**: Real-time response generation
- **LangGraph**: Stateful, structured workflows
- **Checkpoints**: Conversation memory and persistence
