# LangChain Basics 

## What is LangChain?
LangChain is a framework that makes it easier to build applications that use large language models (LLMs). Think of it as a toolkit that provides standard ways to work with AI models, regardless of which company provides them.
Documentation:https://python.langchain.com/docs/tutorials/
Integration:https://python.langchain.com/docs/integrations/chat/

## Why to Chose LangChain

We chose LangChain because it gives us:
- A consistent way to work with different AI providers (like Groq, OpenAI, etc.)
- Built-in tools for building conversations and workflows
- Standard patterns that other developers understand
- A growing ecosystem of integrations and tools

## What We Actually Built

### 1. Basic Setup and Environment
**Setup Groq Key**
https://groq.com/
Create key - https://console.groq.com/keys
https://console.groq.com/docs/models


Setting up development environment:

```python
# Install the required packages
pip install "langchain[groq]"
or 
pip install -r requirements.txt
As all the packages are mentioned here
# Set up environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Get our API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

**Why we did this**: We needed a way to securely store our API key and install the right packages. The `[groq]` part tells pip to install both LangChain and the Groq integration.

### 2. Model Initialization

Create a chat model:

```python
from langchain_groq import ChatGroq

model = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
)
```

**What this does**: Creates a connection to Groq's AI model. The `model_name` specifies which specific AI model we want to use.

### 3. Basic Chat Implementation

built a simple chat function:

```python
def chat_with_ai(user_input):
    response = model.invoke(user_input)
    return response.content
```

**What this does**: Takes user input, sends it to the AI model, and returns the response.

**Why this approach**: Simple and straightforward - good for understanding the basics before adding complexity.

### 4. Streaming Implementation

The most important thing we learned was streaming:

```python
def stream_chat(user_input):
    for chunk in model.stream(user_input):
        print(chunk.content, end="", flush=True)
    print()  # New line at the end
```

**What streaming does**: Instead of waiting for the complete AI response, we get it piece by piece as it's generated.

**Why streaming matters**: 
- Users see responses immediately
- Feels more interactive and responsive
- Better user experience overall

## Key Concepts We Learned

### 1. Model Providers vs. Models

- **Model Provider**: The company/service that hosts the AI (like Groq, OpenAI)
- **Model**: The specific AI model (like llama-3.1-8b-instant)

LangChain abstracts away the differences between providers, so we can switch from Groq to OpenAI by changing just a few lines of code.

### 2. Environment Variables

Use `.env` files to store sensitive information like API keys:

```env
GROQ_API_KEY=your_actual_api_key_here
```


### 3. Error Handling

We implemented basic error handling:

```python
try:
    response = model.invoke(user_input)
    return response.content
except Exception as e:
    return f"Sorry, I encountered an error: {str(e)}"
```


## Next Steps

Now that we understand LangChain basics, we can:
1. Add conversation memory (so the AI remembers previous messages)
2. Integrate tools (so the AI can do things like search the web or access files)
3. Build more complex workflows
4. Add user interfaces

This pattern will be useful as we build more complex applications.

## What This Enables

With LangChain basics under our belt, we can now:
- Build chatbots that feel natural and responsive
- Create AI-powered applications that integrate with other services
- Develop workflows that use AI for decision-making
- Build applications that can be deployed and used by others

