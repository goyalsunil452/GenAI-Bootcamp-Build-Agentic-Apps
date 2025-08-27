"""
GitHub MCP Agent - Simple GitHub Operations

This file demonstrates how to connect AI to GitHub using MCP.
The AI can search repositories, read files, and add content.
"""

import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()


async def setup_github_mcp():
    print("Setting up GitHub MCP connection...")

    # Create MCP client for GitHub
    client = MultiServerMCPClient(
        {
            "github": {
                "command": "volta",
                "args": ["run", "npx", "-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")},
                "transport": "stdio",
            }
        }
    )

    print("Connected to GitHub MCP server")

    # Get available GitHub tools
    tools = await client.get_tools()
    print(f"Found {len(tools)} GitHub tools:")

    for i, tool in enumerate(tools[:10], 1):  # Show first 10 tools
        print(f"  {i}. {tool.name}")

    if len(tools) > 10:
        print(f"  ... and {len(tools) - 10} more tools")

    return client, tools


async def create_github_agent(tools):
    """
    Create AI agent with GitHub tools
    """
    print("\nCreating AI agent with GitHub access...")

    agent = create_react_agent(
        model="groq:deepseek-r1-distill-llama-70b",
        tools=tools,
        prompt="You are a helpful AI assistant with access to GitHub tools. When users ask about GitHub operations, use the appropriate tools. For reading files, use get_file_contents. For creating files, use create_or_update_file. For searching repositories, use search_repositories. Always provide the exact parameters the tools need.",
    )

    print("AI agent created successfully")
    return agent


async def demonstrate_github_operations(agent):
    """
    Demonstrate various GitHub operations
    """
    print("\nDemonstrating GitHub operations...")

    # Test 1: Search repositories
    print("\nTest 1: Searching repositories")
    print("User: 'Search for repositories about Python machine learning'")

    try:
        response = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Search for repositories about Python machine learning",
                    }
                ]
            }
        )

        print(f"AI Response: {response['messages'][-1].content}")

    except Exception as e:
        print(f"Error: {e}")

    # Test 2: Read a file from a repository
    print("\nTest 2: Reading a file from repository")
    print(
        "User: 'Read the README.md file from the goyalsunil452/DSA-Questions repository'"
    )

    try:
        response = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Read the README.md file from the goyalsunil452/DSA-Questions repository",
                    }
                ]
            }
        )

        print(f"AI Response: {response['messages'][-1].content}")

    except Exception as e:
        print(f"Error: {e}")

    # Test 3: Create a simple file
    print("\nTest 3: Creating a file")
    print(
        "User: 'Create a file called hello.txt with content Hello World in the goyalsunil452/DSA-Questions repository'"
    )

    try:
        response = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Create a file called hello.txt with content Hello World in the goyalsunil452/DSA-Questions repository",
                    }
                ]
            }
        )

        print(f"AI Response: {response['messages'][-1].content}")

    except Exception as e:
        print(f"Error: {e}")


async def interactive_github_demo(agent):
    """
    Interactive demo where user can ask GitHub questions
    """
    print("\nInteractive GitHub Demo")
    print("Type 'quit' to exit")
    print()

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        try:
            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]}
            )

            print(f"AI: {response['messages'][-1].content}")

        except Exception as e:
            print(f"Error: {e}")

        print()


async def main():
    """
    Main function to run the GitHub MCP demo
    """
    try:
        # Check if GitHub token is available
        if not os.getenv("GITHUB_TOKEN"):
            print("Error: GITHUB_TOKEN not found in .env file")
            print("Please add your GitHub Personal Access Token to .env file")
            return

        # Set up MCP connection
        client, tools = await setup_github_mcp()

        # Create AI agent
        agent = await create_github_agent(tools)

        # Demonstrate operations
        await demonstrate_github_operations(agent)

        # Interactive demo
        await interactive_github_demo(agent)

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("  1. GITHUB_TOKEN is set in .env file")
        print("  2. Node.js and npm are installed")
        print("  3. Required packages are installed")


if __name__ == "__main__":
    asyncio.run(main())
