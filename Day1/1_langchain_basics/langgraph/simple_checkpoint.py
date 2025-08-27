import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# Create a checkpoint saver to remember conversations
checkpointer = InMemorySaver()

# Create a simple agent
agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[],
    prompt="You are a helpful assistant. Remember our conversation.",
    checkpointer=checkpointer,
)


def chat_with_memory():
    print("LangGraph Chat with Memory (Checkpoint)")
    print("Type 'quit' to exit")
    print("Type 'new' to start a new conversation thread")
    print()

    # Start with a new thread
    thread_id = "demo_thread_1"

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if user_input.lower() == "new":
            # Start a new conversation thread
            thread_id = f"demo_thread_{len(checkpointer.list_keys()) + 1}"
            print(f"Started new thread: {thread_id}")
            continue

        try:
            # Send message with thread_id to maintain memory
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
    chat_with_memory()
