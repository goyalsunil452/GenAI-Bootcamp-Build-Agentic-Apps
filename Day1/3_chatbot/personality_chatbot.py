import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Initialize the chat model
model = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-8b-instant"
)


def personality_chatbot():
    print("Personality Chatbot - You are talking to a friendly AI assistant!")
    print("Type 'quit' to exit, 'personality' to change AI personality")
    print()

    # Define different personalities
    personalities = {
        "friendly": "You are a very friendly and helpful AI assistant. Always be cheerful and supportive.",
        "professional": "You are a professional and formal AI assistant. Be concise and business-like.",
        "creative": "You are a creative and imaginative AI assistant. Think outside the box and be artistic.",
        "teacher": "You are a patient and educational AI assistant. Explain things clearly and provide examples.",
    }

    current_personality = "friendly"
    conversation = [{"role": "system", "content": personalities[current_personality]}]

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye! It was nice chatting with you!")
            break

        if user_input.lower() == "personality":
            print("\nAvailable personalities:")
            for i, (name, desc) in enumerate(personalities.items(), 1):
                print(f"  {i}. {name.capitalize()}")

            try:
                choice = int(input("Choose personality (1-4): ")) - 1
                personality_names = list(personalities.keys())
                if 0 <= choice < len(personality_names):
                    current_personality = personality_names[choice]
                    conversation = [
                        {
                            "role": "system",
                            "content": personalities[current_personality],
                        }
                    ]
                    print(f"Changed to {current_personality} personality!")
                else:
                    print("Invalid choice, keeping current personality.")
            except ValueError:
                print("Invalid input, keeping current personality.")
            continue

        # Add user message to conversation
        conversation.append({"role": "user", "content": user_input})

        try:
            # Get AI response
            response = model.invoke(conversation)

            # Add AI response to conversation
            conversation.append({"role": "assistant", "content": response.content})

            print(f"AI ({current_personality}): {response.content}")

        except Exception as e:
            print(f"Error: {e}")

        print()


if __name__ == "__main__":
    personality_chatbot()
