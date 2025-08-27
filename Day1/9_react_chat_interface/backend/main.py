"""
FastAPI Backend for React Chat Interface

This backend provides streaming chat responses using direct Groq API calls.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
import requests
import json

# Initialize FastAPI app
app = FastAPI(title="Chat API", version="1.0.0")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"


class ChatResponse(BaseModel):
    message: str
    thread_id: str


# Groq API configuration - Set your API key here
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def get_groq_response(message: str, stream: bool = False):
    """Get response from Groq API"""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": message}],
        "stream": stream,
        "temperature": 0.7,
        "max_tokens": 1000,
    }

    if stream:
        # For streaming, we'll handle it differently
        response = requests.post(GROQ_API_URL, headers=headers, json=data, stream=True)
        return response
    else:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        return response.json()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Chat API is running!", "status": "healthy"}


@app.post("/chat/stream")
async def stream_chat(request: ChatRequest):
    """Stream chat response from Groq API"""
    try:
        # Get streaming response from Groq
        response = get_groq_response(request.message, stream=True)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Groq API error"
            )

        async def generate():
            """Generate streaming response chunks"""
            try:
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode("utf-8")
                        if line_str.startswith("data: "):
                            data_str = line_str[6:]  # Remove 'data: ' prefix

                            if data_str == "[DONE]":
                                # Send completion signal
                                yield f"data: {json.dumps({'type': 'complete'})}\n\n"
                                break

                            try:
                                data = json.loads(data_str)
                                if "choices" in data and len(data["choices"]) > 0:
                                    choice = data["choices"][0]
                                    if (
                                        "delta" in choice
                                        and "content" in choice["delta"]
                                    ):
                                        content = choice["delta"]["content"]
                                        if content:
                                            # Send chunk as Server-Sent Event
                                            yield f"data: {json.dumps({'content': content, 'type': 'chunk'})}\n\n"
                            except json.JSONDecodeError:
                                continue

            except Exception as e:
                # Send error signal
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Streaming failed: {str(e)}")


@app.post("/chat")
async def chat(request: ChatRequest):
    """Non-streaming chat response (fallback)"""
    try:
        # Get response from Groq
        response_data = get_groq_response(request.message, stream=False)

        if "choices" in response_data and len(response_data["choices"]) > 0:
            message_content = response_data["choices"][0]["message"]["content"]
            return ChatResponse(message=message_content, thread_id=request.thread_id)
        else:
            raise HTTPException(
                status_code=500, detail="Invalid response from Groq API"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
