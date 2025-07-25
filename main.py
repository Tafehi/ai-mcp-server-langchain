import asyncio
import streamlit as st
from mcp_server import client


# def main():
#     asyncio.run(
#         client.agents(
#             "llama3.2:latest", "ollama", "what is the current weather in Oslo?"
#         )
#     )


# if __name__ == "__main__":
#     main()

### Streamlit app for MCP Server

# Set page configuration
st.set_page_config(page_title="LLM Chatbot", layout="wide")

# Sidebar: LLM Provider Selection
st.sidebar.title("LLM Configuration")

# Provider selection with default set to "ollama"
provider = st.sidebar.selectbox("Select LLM Provider", ["aws", "ollama"], index=1)

# Model options based on provider
model_options = {
    "ollama": [
        "llama3.2:latest",
        "orionstar/orion14b-q4:latest",
        "prompt/hermes-2-pro",
    ],
    "aws": [
        "anthropic.claude-3-7-sonnet-20250219-v1:0",
        "mistral.mixtral-8x7b-instruct-v0:1",
        "anthropic.claude-3-haiku-20240307-v1:0",
    ],
}

# Default model selection
default_model = (
    "llama3.2:latest"
    if provider == "ollama"
    else "anthropic.claude-3-7-sonnet-20250219-v1:0"
)

model = st.sidebar.selectbox(
    "Select Model",
    model_options[provider],
    index=model_options[provider].index(default_model),
)

# Sidebar: Loaded Agents/Tools
st.sidebar.markdown("### Logs for Agents/Tools from MCP Server")
log_placeholder = "logs related to the agents and tools generated from MCP server will appear here."
st.sidebar.text_area("Logs", log_placeholder, height=150)

# Main area: Chatbot interface
st.title("🧠 MCP Server Chatbot Developed by LangChain/LangGraph")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    async def run_agent():
        return await client.agents(
            llm_model=model, llm_provider=provider, question=prompt
        )

    response = asyncio.run(run_agent())
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
