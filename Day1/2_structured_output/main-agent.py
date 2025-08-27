import os
from dotenv import load_dotenv

load_dotenv()
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel


# Using create_react_agent instead of building a custom graph
# Internally, agents create a graph and execute it automatically
checkpointer = InMemorySaver()


class TaskPlan(BaseModel):
    priority: str
    estimated_time: str
    steps: list[str]
    resources_needed: list[str]


def demonstrate_task_planning():
    agent = create_react_agent(
        model="groq:llama-3.3-70b-versatile",
        tools=[],
        prompt="You are a project manager. Create detailed task plans with clear steps.",
        response_format=TaskPlan,
    )

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Create a plan for organizing a team meeting",
                }
            ]
        },
        {"configurable": {"thread_id": "task_demo"}},
    )

    structured = response["structured_response"]
    print(f"\n Priority: {structured.priority}")
    print(f" Estimated Time: {structured.estimated_time}")
    print(f" Steps:")
    for i, step in enumerate(structured.steps, 1):
        print(f"   {i}. {step}")
    print(f"  Resources Needed:")
    for resource in structured.resources_needed:
        print(f"   • {resource}")


demonstrate_task_planning()
