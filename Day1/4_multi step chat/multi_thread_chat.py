import os
from dotenv import load_dotenv
load_dotenv()
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

# Create a single agent that can handle multiple conversation threads
checkpointer = InMemorySaver()
agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",  
    tools=[],  
    prompt="You are a versatile AI assistant that can adapt to different conversation contexts and personalities.",
    checkpointer=checkpointer
)

def run_conversation_thread(thread_id, conversation_name, messages):
    """Run a conversation thread and return the final response"""
    print(f"\n{'='*50}")
    print(f"🎭 {conversation_name.upper()} THREAD")
    print(f"{'='*50}")
    
    config = {"configurable": {"thread_id": thread_id}}
    
    for i, message in enumerate(messages):
        print(f"\n👤 User: {message}")
        
        response = agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config
        )
        
        assistant_response = response["messages"][-1]["content"]
        print(f"🤖 Assistant: {assistant_response}")
    
    return response

def main():
    print("🚀 MULTI-THREADED AI CONVERSATION DEMO")
    print("This demonstrates how one AI agent can maintain separate conversation contexts!")
    
    # Thread 1: Personal Assistant (caring and helpful)
    personal_messages = [
        "Hi! I'm feeling a bit stressed today. Can you help me relax?",
        "What's my mood right now?",
        "Can you give me a motivational quote?"
    ]
    
    # Thread 2: Work Colleague (professional and focused)
    work_messages = [
        "Good morning! I have a project deadline coming up. Any tips?",
        "What was my main concern about the project?",
        "Can you help me prioritize my tasks?"
    ]
    
    # Thread 3: Creative Writing Partner (imaginative and artistic)
    creative_messages = [
        "Hello! I want to write a story about a magical forest. Any ideas?",
        "What was my story idea about?",
        "Can you help me develop a character for this story?"
    ]
    
    # Run all three threads
    personal_result = run_conversation_thread("personal_assistant", "Personal Assistant", personal_messages)
    work_result = run_conversation_thread("work_colleague", "Work Colleague", work_messages)
    creative_result = run_conversation_thread("creative_writer", "Creative Writing Partner", creative_messages)
    
    # Demonstrate memory isolation
    print(f"\n{'='*50}")
    print("🧠 MEMORY ISOLATION TEST")
    print(f"{'='*50}")
    
    # Test each thread's memory independently
    test_configs = [
        ("personal_assistant", "Personal thread - What's my mood?"),
        ("work_colleague", "Work thread - What was my project concern?"),
        ("creative_writer", "Creative thread - What was my story idea?")
    ]
    
    for thread_id, test_message in test_configs:
        config = {"configurable": {"thread_id": thread_id}}
        response = agent.invoke(
            {"messages": [{"role": "user", "content": test_message}]},
            config
        )
        print(f"\n{test_message}")
        print(f"🤖 Response: {response['messages'][-1]['content']}")
    
    print(f"\n{'='*50}")
    print("✨ DEMONSTRATION COMPLETE!")
    print("Each thread maintained its own conversation context!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
