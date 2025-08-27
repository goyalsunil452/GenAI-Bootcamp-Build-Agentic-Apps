import asyncio
import os
from turtle import delay
from dotenv import load_dotenv

load_dotenv()
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def run_agent():
    client = MultiServerMCPClient(
        {
            "EducosysFileSystem": {
                "command": "python",
                "args": ["./mcp-server/filesystem_mcp.py"],
                "transport": "stdio",
            },
        }
    )

    tools = await client.get_tools()
    print(f"Found {len(tools)} total tools")
    print("\nAvailable tools:")
    for i, tool in enumerate(tools):
        print(f"   {i+1}. {tool.name}")
    agent = create_react_agent(
        model="groq:llama-3.1-8b-instant",
        tools=tools,
        prompt="You are a helpful AI assistant with access filesystem tools. IMPORTANT: Only use the tools that are actually available. For EducosysFileSystem operations, use addFile , addFolder, deleteFile to list directory contents. Always provide the full path when using RyukFileSystem tools.",
    )
    file_response1 = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "create a file called 'funny.txt' in the current directory",
                }
            ]
        },
    )
    await asyncio.sleep(1)
    print(file_response1["messages"][-1].content)
    print("--------------------------------")
    file_response2 = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "delete file called 'funny.txt' in the current directory",
                }
            ]
        },
    )
    print("--------------------------------")
    print(file_response2["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(run_agent())
