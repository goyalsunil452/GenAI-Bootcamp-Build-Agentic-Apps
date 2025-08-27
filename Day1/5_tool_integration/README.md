# Tool Integration in LangGraph

## What are Tools?

Tools are functions that AI agents can use to perform specific tasks. They extend the agent's capabilities beyond just conversation.

## Why Use Tools?

- **Real actions** - AI can do things like calculations, get time, access data
- **Extended capabilities** - Beyond just generating text
- **Practical applications** - Agents can actually help with real tasks
- **Modular design** - Easy to add new capabilities

## Files

### simple_tools.py
Basic tool creation and usage. Shows how to define tools and give them to agents.

### tools_with_memory.py
Tools working with conversation memory. Demonstrates persistent tool usage across conversations.

## What Each File Shows

### simple_tools.py
```python
@tool
def get_current_time():
    """Get the current time and date"""
    from datetime import datetime
    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Create agent with tools
agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[get_current_time, calculate, count_words],
    prompt="Use the tools when needed to help users."
)
```
**Learning**: How to create tools and give them to agents

### tools_with_memory.py
```python
# Tools with memory
agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=tools,
    checkpointer=checkpointer  # Enables memory
)
```
**Learning**: How tools work with conversation memory

## Key Concepts

### 1. @tool Decorator
Marks a function as a tool that agents can use.

### 2. Tool Description
The docstring tells the AI what the tool does and when to use it.

### 3. Tool Integration
Agents automatically decide when and how to use available tools.

### 4. Tool Memory
Tools can work across multiple conversations, maintaining context.

## How Tools Work

1. **User asks question** - "What time is it?"
2. **AI analyzes** - Determines if tools are needed
3. **Tool selection** - Chooses appropriate tool (get_current_time)
4. **Tool execution** - Runs the tool function
5. **Response generation** - Uses tool result to answer user

## Available Tools in Examples

- **get_current_time** - Returns current date and time
- **calculate** - Performs mathematical calculations
- **count_words** - Counts words in text
- **remember_fact** - Stores information for later use

## How to Run

1. Install: `pip install -r requirements.txt`
2. Set up `.env` file with GROQ_API_KEY
3. Run examples:
   - `python simple_tools.py`
   - `python tools_with_memory.py`

## Learning Progression

1. **Start with simple_tools.py** - Understand basic tool creation
2. **Try tools_with_memory.py** - See tools with conversation memory
3. **Experiment with tools** - Ask questions that require tool usage

## What This Enables

- **Functional AI agents** - Can perform actual tasks
- **Extended capabilities** - Beyond just conversation
- **Practical applications** - Real-world problem solving
- **Foundation for MCP** - Understanding how tools work

## Next Steps

- Learn about MCP (Model Context Protocol) for external tools
- Create custom tools for specific use cases
- Integrate with databases and APIs
- Build production-ready tool systems

## Note

This covers basic tool integration. For advanced external tool integration (GitHub, filesystem, etc.), see the MCP Deep Dive chapter.
