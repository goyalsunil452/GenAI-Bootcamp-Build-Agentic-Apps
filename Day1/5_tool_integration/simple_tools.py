import os
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()


# Define simple tools
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
def count_words(text: str):
    """Count the number of words in a text"""
    word_count = len(text.split())
    return f"Word count: {word_count}"


# Create agent with tools
def create_simple_agent():
    tools = [get_current_time, calculate, count_words]

    agent = create_react_agent(
        model="groq:llama-3.3-70b-versatile",
        tools=tools,
        prompt="You are a helpful assistant with access to tools. Use the tools when needed to help users.",
    )

    return agent


# Test the agent
if __name__ == "__main__":
    agent = create_simple_agent()

    print("Simple Tool Integration Demo")
    print("=" * 40)
    print("Available tools:")
    tools = [get_current_time, calculate, count_words]
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    print()

    # Test queries
    test_queries = [
        "What time is it?",
        "Calculate 15 * 8 + 3",
        "How many words are in 'Hello world this is a test'?",
        "What's the weather like?",
    ]

    for query in test_queries:
        print(f"User: {query}")
        try:
            response = agent.invoke({"messages": [{"role": "user", "content": query}]})
            print(f"AI: {response['messages'][-1].content}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 40)
