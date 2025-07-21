import mcp
from mcp.server.fastmcp import FastMCP

# from tools.web_api import WebAPI
# from tools.weather_api import WeatherAPI
# from tools.math_utils import MathTool
from llm.ollama_model import OllamaLLM
from llm.bedrock_model import BedrockLLM


mcp = FastMCP("Math")


class MCPServer:
    def __init__(self, llm_model, llm_provider, transport_protocol):
        self.llm_model = llm_model
        self.llm_provider = llm_provider
        self.transport_protocol = transport_protocol

    def start_server(self):
        mcp.run(transport=self.transport_protocol)
