# LangGraph Basics

## What is LangGraph?

LangGraph is a framework for building stateful, multi-step AI applications. Think of it as a way to create AI agents that can:
- Remember conversation history
- Make decisions about what to do next
- Use tools and external services
- Maintain state across multiple interactions

## Core Concepts

### 1. State
The shared data structure that represents your application's current state. In our case, it stores conversation messages.

### 2. Nodes
Functions that do the actual work. Each node receives the current state, performs some action, and returns updated state.

### 3. Edges
Connections between nodes that determine what happens next. They can be:
- **START** → First node to run
- **Node → Node** → Sequential execution
- **Node → END** → Stop execution

### 4. Graph
The complete workflow that connects all nodes and edges together.

### 5. Checkpoints (Memory)
A way to save and restore conversation state. Think of it as the agent's memory.

## What We Built

### main.py - Basic Graph
```python
# Define our state structure
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Create the graph
graph_builder = StateGraph(State)

# Add our chat node
def chatBot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build the flow: START → chatBot → END
graph_builder.add_node("chatBot", chatBot)
graph_builder.add_edge(START, "chatBot")
graph_builder.add_edge("chatBot", END)

# Compile the graph
graph = graph_builder.compile()
```

### simple_checkpoint.py - Memory with Checkpoints
```python
# Create a checkpoint saver to remember conversations
checkpointer = InMemorySaver()

# Create agent with checkpointer connected
agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[],
    prompt="You are a helpful assistant. Remember our conversation.",
    checkpointer=checkpointer,  # This connects memory to the agent
)

# Send message with thread_id to maintain memory
response = agent.invoke(
    {"messages": [{"role": "user", "content": user_input}]},
    {"configurable": {"thread_id": thread_id}}
)
```

## How It Works

### Basic Graph (main.py)
1. **User sends message** → Goes to START
2. **START** → Routes to "chatBot" node
3. **chatBot node** → Processes message with AI model
4. **chatBot node** → Returns AI response
5. **Response** → Goes to END (conversation complete)

### With Memory (simple_checkpoint.py)
1. **User sends message** → Agent processes it
2. **Response generated** → Stored in memory with thread_id
3. **Next message** → Agent remembers previous conversation
4. **Context maintained** → AI can reference past messages

## Key Benefits

- **Stateful**: Remembers conversation history
- **Structured**: Clear flow of what happens when
- **Extensible**: Easy to add more nodes and logic
- **Streaming**: Can show responses in real-time
- **Memory**: Maintains conversation context across messages

## What This Enables

With this foundation, we can now:
- Add more nodes for different tasks
- Create conditional logic (if/then decisions)
- Integrate tools and external services
- Build complex multi-step workflows
- Maintain conversation memory across sessions

## Next Steps

- Add conversation memory to main.py
- Integrate tools (like file operations)
- Create conditional decision-making
- Build multi-agent systems

This is the foundation for building sophisticated AI applications that can do more than just chat.

