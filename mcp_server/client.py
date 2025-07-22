from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from models.ollama_model import OllamaLLM
from models.bedrock_model import BedrockLLM
import traceback

# class MCPClient:
#     def __init__(self, llm_model, llm_provider):
#         self.llm_model = llm_model
#         self.llm_provider = llm_provider


async def agents(llm_model, llm_provider, question):
    try:
        print(
            f"Setting up MCP Client with model: {llm_model} and provider: {llm_provider}"
        )
        if llm_provider == "aws":
            model = BedrockLLM(llm_model).get_llm()
        elif llm_provider == "ollama":
            model = OllamaLLM(llm_model).get_llm()
        else:
            raise ValueError("Unsupported LLM provider. Choose 'aws' or 'ollama'.")
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {e}")

    print(
        f"LLM Model: {model['llm_model']} from {model['llm_provider']} is initialized successfully."
    )

    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["tools/math_tool.py"],
                "transport": "stdio",
            },
            # "weather": {
            #     "url": "https://api.weatherapi.com/v1/current.json",  # Ensure server is running here
            #     "transport": "streamable_http",
            # }
        }
    )
    print("Connecting to MCP tools and agents")

    try:
        tools = await client.get_tools()
    except* Exception as eg:
        print("ExceptionGroup caught during tool loading:")
        traceback.print_exception(eg)
        raise RuntimeError(f"Failed to load tools: {eg}")

    print(f"Loaded Tools: {[tool.name for tool in tools]}")
    agent = create_react_agent(model=model["llm_model"], tools=tools)

    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    print(f"Response: {response}")
    print(f"Agent Response: {response['messages'][-1].content}")
    return response["messages"][-1].content
