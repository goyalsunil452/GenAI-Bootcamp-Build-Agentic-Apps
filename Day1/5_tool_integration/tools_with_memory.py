import os
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


# Define tools
@tool
def get_current_time():
    """Get the current time and date"""
    from datetime import datetime

    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


@tool
def calculate(expression: str):
    """Calculate a mathematical expression"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating {expression}: {e}"


@tool
def remember_fact(fact: str):
    """Remember an important fact for later use"""
    return f"I'll remember: {fact}"


# Create agent with tools and memory
def create_memory_agent():
    tools = [get_current_time, calculate, remember_fact]
    checkpointer = InMemorySaver()

    agent = create_react_agent(
        model="groq:llama-3.3-70b-versatile",
        tools=tools,
        prompt="You are a helpful assistant with tools and memory. Use tools when needed and remember important information from conversations.",
        checkpointer=checkpointer,
    )

    return agent, checkpointer


def interactive_tools_demo():
    agent, checkpointer = create_memory_agent()

    print("Tools with Memory Demo")
    print("=" * 50)
    print("Available tools:")
    tools = [get_current_time, calculate, remember_fact]
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    print()
    print("Type 'quit' to exit, 'new' for new conversation thread")
    print()

    thread_id = "demo_thread_1"

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if user_input.lower() == "new":
            thread_id = f"demo_thread_{len(checkpointer.list_keys()) + 1}"
            print(f"Started new thread: {thread_id}")
            continue

        try:
            response = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                {"configurable": {"thread_id": thread_id}},
            )

            print(f"AI: {response['messages'][-1].content}")
            print(f"Thread: {thread_id}")

        except Exception as e:
            print(f"Error: {e}")

        print()


if __name__ == "__main__":
    interactive_tools_demo()
