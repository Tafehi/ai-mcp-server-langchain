import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from llm.ollama_model import OllamaLLM
from llm.bedrock_model import BedrockLLM
from langchain_ollama.chat_models import ChatOllama
from langchain_aws import ChatBedrockConverse


class MCPClient:
    def __init__(self, llm_model, llm_provider):
        self.llm_model = llm_model
        self.llm_provider = llm_provider

    def chat_bot(self):
        try:
            if self.llm_provider == "aws":
                llm_model = ChatBedrockConverse(
                    model="anthropic.claude-3-sonnet-20240229-v1:0",
                    temperature=0.2,
                    max_tokens=None,
                    # other params...
                )
            elif self.llm_provider == "ollama":
                llm_model = ChatOllama(
                    model="llama3",
                    temperature=0.2,
                    num_predict=256,
                    # other params ...
                )
            else:
                raise ValueError("Unsupported LLM provider. Choose 'aws' or 'ollama'.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {e}")
        server_params = StdioServerParameters(
            command="python",  # Command to execute
            args=["mcp_server.py"],  # Arguments for the command (our server script)
        )
        run_agent = _run_agent(llm_model, server_params)


async def _run_agent(llm_model, server_params):

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("MCP Session Initialized.")
            tools = await load_mcp_tools(session)
            print(f"Loaded Tools: {[tool.name for tool in tools]}")
            agent = create_react_agent(llm_model, tools)
            print("ReAct Agent Created.")
            print(f"Invoking agent with query")
            response = await agent.ainvoke(
                {
                    "messages": [
                        (
                            "user",
                            "What is (7+9)x17, then give me sine of the output recieved and then tell me What's the weather in Torronto, Canada?",
                        )
                    ]
                }
            )
            print("Agent invocation complete.")
            # Return the content of the last message (usually the agent's final answer)
            return response["messages"][-1].content
