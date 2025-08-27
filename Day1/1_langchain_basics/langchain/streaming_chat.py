import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

# Streaming response - shows text as it generates
for chunk in model.stream("What is Groq?"):
    print(chunk.content, end="", flush=True)
print()  # New line at the end
