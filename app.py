import streamlit as st
import mcp
from mcp.server.fastmcp import FastMCP
from mcp_server import mcp_server


if __name__ == "__main__":
    print("Starting MCP Server....")
    server_start = mcp_server.MCPServer(
        llm_model="mistral.mixtral-8x7b-instruct-v0:1",
        llm_provider="aws",
        transport_protocol="stdio",
    ).start_server()


### Streamlit app for MCP Server

# # Set page configuration
# st.set_page_config(page_title="LLM Chatbot", layout="wide")

# # Sidebar: LLM Provider Selection
# st.sidebar.title("LLM Configuration")

# # Provider selection
# provider = st.sidebar.selectbox("Select LLM Provider", ["aws", "ollama"])

# # Model options based on provider
# model_options = {
#     "aws": [
#         "mistral.mixtral-8x7b-instruct-v0:1",
#         "amazon.titan-text-lite-v1",
#         "anthropic.claude-3-7-sonnet-20250219-v1:0"
#     ],
#     "ollama": [
#         "llama3.2:latest",
#         "gemma3:latest",
#         "mistral:latest"
#     ]
# }

# # Default model selection
# default_model = "mistral.mixtral-8x7b-instruct-v0:1" if provider == "aws" else "llama3.2:latest"
# model = st.sidebar.selectbox("Select Model", model_options[provider], index=model_options[provider].index(default_model))

# # Sidebar: Logs
# st.sidebar.markdown("### Logs")
# if provider == "aws":
#     st.sidebar.text_area("AWS Logs", "AWS log output will appear here...", height=150)
# else:
#     st.sidebar.text_area("Ollama Logs", "Ollama log output will appear here...", height=150)

# # Main area: Chatbot interface
# st.title("🧠 LLM Chatbot")

# # Chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # User input
# if prompt := st.chat_input("Ask me anything..."):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Simulated response
#     response = f"Simulated response from {provider.upper()} model `{model}`."
#     st.session_state.messages.append({"role": "assistant", "content": response})
#     with st.chat_message("assistant"):
#         st.markdown(response)
