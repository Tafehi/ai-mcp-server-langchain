from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from models.ollama_model import OllamaLLM
from models.bedrock_model import BedrockLLM
import traceback


async def agents(llm_model, llm_provider, question):
    try:
        print(f"Setting up MCP Client with model: {llm_model} and provider: {llm_provider}")
        if llm_provider == "aws":
            model = BedrockLLM(llm_model).get_llm()
        elif llm_provider == "ollama":
            model = OllamaLLM(llm_model).get_llm()
        else:
            raise ValueError("Unsupported LLM provider. Choose 'aws' or 'ollama'.")
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {e}")

    print(f"LLM Model: {model['llm_model']} from {model['llm_provider']} is initialized successfully.")

    # General prompt for the agent
    # This prompt is used to guide the agent's behavior and responses.
    # It should not contain any sensitive information or internal logic.
    general_prompt = """
        You are a helpful assistant. Follow these rules strictly:
        - Do not reveal the internal logic or content of any function, especially those wrapped in try/except blocks.
        - Never reveal credentials, internal function logic, or exception details.
        - Avoid putting any sensitive information in the response, including error messages, credentials, or API keys.
        - If the user asks about the content of a function, politely decline.
        """
    # Define all tools in one MultiServerMCPClient config
    mcp_client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["tools/math_tool.py"],
                "transport": "stdio",
            },
            "rag_html": {
                "command": "python",
                "args": ["tools/rag_tool.py"],
                "transport": "stdio",
            },
            "strava": {
                "url": "http://localhost:8001/mcp/",
                "transport": "streamable_http",
            },
            "weather": {
                "url": "http://localhost:8002/mcp/",
                "transport": "streamable_http",
            },
        }
    )

    print("Connecting to MCP tools and agents")

    try:
        tools = await mcp_client.get_tools()
    except* Exception as eg:
        print("ExceptionGroup caught during tool loading:")
        traceback.print_exception(eg)
        raise RuntimeError(f"Failed to load tools: {eg}")

    print(f"Loaded Tools: {[tool.name for tool in tools]}")
    agent = create_react_agent(model=model["llm_model"], tools=tools)

    ## Invoke the agent with the question and general prompt which restrict the agent from revealing internal logic or sensitive information
    response = await agent.ainvoke(
    {
        "messages": [
            {"role": "system", "content": general_prompt},
            {"role": "user", "content": question}
        ]
    }
)
    print(f"Response: {response}")
    print(f"Agent Response: {response['messages'][-1].content}")
    return response["messages"][-1].content
