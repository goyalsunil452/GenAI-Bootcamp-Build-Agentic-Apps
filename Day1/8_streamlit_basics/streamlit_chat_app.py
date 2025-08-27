"""
Streamlit Chat Application

A chat interface built with Streamlit that uses LangGraph agent with memory.
This demonstrates proper state management and conversation context.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


def initialize_session_state():
    """
    Initialize session state for chat history and agent
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_title" not in st.session_state:
        st.session_state.chat_title = "New Chat"

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = "main_thread"

    if "agent" not in st.session_state:
        st.session_state.agent = None
        st.session_state.checkpointer = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}


def create_agent():
    """
    Create LangGraph agent with memory
    """
    try:
        # Create checkpoint saver for conversation memory
        checkpointer = InMemorySaver()

        # Create agent with memory
        agent = create_react_agent(
            model="groq:llama-3.1-8b-instant",  # Smaller, faster model with different limits
            tools=[],
            prompt="You are a helpful AI assistant. Remember our conversation and provide helpful responses.",
            checkpointer=checkpointer,
        )

        return agent, checkpointer

    except Exception as e:
        st.error(f"Error creating agent: {str(e)}")
        return None, None


def add_message(role, content):
    """
    Add a message to the chat history
    """
    st.session_state.messages.append({"role": role, "content": content})

    # Set chat title based on first user message
    if role == "user" and len(st.session_state.messages) == 1:
        st.session_state.chat_title = (
            content[:50] + "..." if len(content) > 50 else content
        )

    # Save this chat to history (both for new chats and ongoing conversations)
    save_chat_to_history()


def save_chat_to_history():
    """
    Save current chat to history
    """
    if st.session_state.messages:
        # Use thread_id as the key to ensure consistency
        chat_key = st.session_state.thread_id
        st.session_state.chat_history[chat_key] = {
            "title": st.session_state.chat_title,
            "messages": st.session_state.messages.copy(),
            "thread_id": st.session_state.thread_id,
        }


def load_chat_from_history(thread_id):
    """
    Load a specific chat from history
    """
    if thread_id in st.session_state.chat_history:
        chat_data = st.session_state.chat_history[thread_id]
        st.session_state.messages = chat_data["messages"].copy()
        st.session_state.chat_title = chat_data["title"]
        st.session_state.thread_id = thread_id
        st.rerun()  # Update sidebar immediately


def delete_chat(thread_id):
    """
    Delete a specific chat from history
    """
    if thread_id in st.session_state.chat_history:
        del st.session_state.chat_history[thread_id]
        # If we're deleting the current chat, clear it
        if thread_id == st.session_state.thread_id:
            st.session_state.messages = []
            st.session_state.chat_title = "New Chat"
        st.rerun()  # Update sidebar immediately


def get_ai_response_streaming(user_message):
    """
    Get streaming response from LangGraph agent with memory
    """
    try:
        # Ensure agent is created
        if st.session_state.agent is None:
            st.session_state.agent, st.session_state.checkpointer = create_agent()
            if st.session_state.agent is None:
                st.error("Failed to create AI agent")
                return None

        # Get streaming response from agent with thread_id for memory
        # Use the same approach as main.py - stream events in real-time
        response_stream = st.session_state.agent.stream(
            {"messages": [{"role": "user", "content": user_message}]},
            {"configurable": {"thread_id": st.session_state.thread_id}},
        )

        return response_stream

    except Exception as e:
        st.error(f"Error in streaming: {str(e)}")
        return None


def get_ai_response(user_message):
    """
    Get response from LangGraph agent with memory (non-streaming fallback)
    """
    try:
        # Ensure agent is created
        if st.session_state.agent is None:
            st.session_state.agent, st.session_state.checkpointer = create_agent()
            if st.session_state.agent is None:
                return "Sorry, I couldn't initialize the AI agent."

        # Get response from agent with thread_id for memory
        response = st.session_state.agent.invoke(
            {"messages": [{"role": "user", "content": user_message}]},
            {"configurable": {"thread_id": st.session_state.thread_id}},
        )

        return response["messages"][-1].content

    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


def display_chat_history():
    """
    Display the chat history
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    """
    Main chat application
    """
    st.set_page_config(page_title="AI Chatbot", page_icon="💬", layout="wide")

    # Initialize session state
    initialize_session_state()

    # Sidebar for chat history and management
    with st.sidebar:
        # New chat button at the top
        if st.button("+ New Chat", use_container_width=True, type="primary"):
            # Save current chat before starting new one
            if st.session_state.messages:
                save_chat_to_history()

            st.session_state.messages = []
            st.session_state.chat_title = "New Chat"
            # Generate new thread ID for new conversation
            import time

            st.session_state.thread_id = f"thread_{int(time.time())}"
            st.rerun()  # Update sidebar immediately

        st.divider()

        # Display list of saved chats
        if st.session_state.chat_history:
            for thread_id, chat_data in st.session_state.chat_history.items():
                # Create a container for each chat with title and delete button
                col1, col2 = st.columns([4, 1])

                with col1:
                    # Chat title button
                    if st.button(
                        chat_data["title"],
                        key=f"chat_{thread_id}",
                        use_container_width=True,
                        help=f"Click to continue this conversation",
                    ):
                        load_chat_from_history(thread_id)

                with col2:
                    # Delete button
                    if st.button(
                        "🗑️", key=f"delete_{thread_id}", help="Delete this chat"
                    ):
                        delete_chat(thread_id)

                # Show message count below each chat
                st.caption(f"{len(chat_data['messages'])} messages")
                st.divider()
        else:
            st.write("No previous chats yet")

    # Main chat area
    st.title("AI Chatbot")
    st.write("Chat with an AI powered by LangGraph Agent with Memory")

    # Display current chat title
    if st.session_state.messages:
        st.subheader(f"💬 {st.session_state.chat_title}")

    st.divider()

    # Display chat history
    if st.session_state.messages:
        display_chat_history()
    else:
        # Welcome message for new chat
        st.info("👋 Start a new conversation by typing a message below!")

    # Chat input
    if prompt := st.chat_input("What would you like to chat about?"):
        # Add user message
        add_message("user", prompt)

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response with streaming
        with st.chat_message("assistant"):
            try:
                # Get streaming response
                response_stream = get_ai_response_streaming(prompt)

                # Check if we got a valid response stream
                if response_stream is None:
                    st.error("Failed to get AI response. Please try again.")
                    return

                # Stream the response in real-time
                chunk_count = 0

                try:
                    # Create a text container for streaming
                    text_container = st.empty()
                    current_text = ""

                    # Process chunks and simulate real-time streaming
                    for event in response_stream:
                        for value in event.values():
                            # Extract content from the event value
                            if "messages" in value and value["messages"]:
                                chunk_content = value["messages"][-1].content

                                if chunk_content:
                                    current_text += chunk_content
                                    # Update the container with accumulated response
                                    text_container.markdown(current_text + "▌")
                                    chunk_count += 1

                                    # Small delay to simulate real-time streaming
                                    import time

                                    time.sleep(0.05)  # 50ms delay between chunks

                    # Final update without cursor
                    if current_text:
                        text_container.markdown(current_text)
                        full_response = current_text
                    else:
                        st.error("❌ No response content extracted from chunks")
                        # Try to get a non-streaming response as fallback
                        response = get_ai_response(prompt)
                        text_container.markdown(response)
                        add_message("assistant", response)
                        return

                except Exception as async_error:
                    st.error(f"Async processing error: {str(async_error)}")
                    # Fallback to non-streaming
                    response = get_ai_response(prompt)
                    message_placeholder.markdown(response)
                    add_message("assistant", response)
                    return

                # Add AI response to session state
                add_message("assistant", full_response)

            except Exception as e:
                # Fallback to non-streaming if streaming fails
                st.error(f"Streaming failed, using fallback: {str(e)}")
                try:
                    response = get_ai_response(prompt)
                    message_placeholder.markdown(response)
                    add_message("assistant", response)
                except Exception as fallback_error:
                    st.error(
                        f"Both streaming and fallback failed: {str(fallback_error)}"
                    )
                    # Show a simple error message
                    message_placeholder.markdown(
                        "Sorry, I encountered an error. Please try again."
                    )
                    add_message(
                        "assistant", "Sorry, I encountered an error. Please try again."
                    )

            st.rerun()
            # Note: Removed st.rerun() as it was causing errors
            # The sidebar will update on the next user interaction


if __name__ == "__main__":
    main()
