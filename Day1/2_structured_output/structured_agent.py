import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

load_dotenv()


# Define structured output model
class TaskPlan(BaseModel):
    priority: str
    estimated_time: str
    steps: list[str]
    resources_needed: list[str]


# Create agent with structured output
agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[],
    prompt="You are a project manager. Create detailed task plans with clear steps.",
    response_format=TaskPlan,
)

# Get structured response
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Create a plan for organizing a team meeting"}
        ]
    }
)

# Access structured data
structured = response["structured_response"]
print(f"Priority: {structured.priority}")
print(f"Estimated Time: {structured.estimated_time}")
print(f"Steps:")
for i, step in enumerate(structured.steps, 1):
    print(f"  {i}. {step}")
print(f"Resources Needed:")
for resource in structured.resources_needed:
    print(f"  • {resource}")
