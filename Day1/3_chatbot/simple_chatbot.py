import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Initialize the chat model
model = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-8b-instant"
)


def simple_chatbot():
    print("Simple Chatbot")
    print("Type 'quit' to exit")
    print()

    # Store conversation history
    conversation = []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # Add user message to conversation
        conversation.append({"role": "user", "content": user_input})

        try:
            # Get AI response
            response = model.invoke(conversation)

            # Add AI response to conversation
            conversation.append({"role": "assistant", "content": response.content})

            print(f"AI: {response.content}")

        except Exception as e:
            print(f"Error: {e}")

        print()


if __name__ == "__main__":
    simple_chatbot()
