from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
import os
import openai  # or use Azure OpenAI SDK

mcp = FastMCP("HTML QA Server")

# Load and cache HTML content
html_text = ""
html_dir = "./documents/latest/"

for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        with open(os.path.join(html_dir, filename), "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            # Extract visible text
            text = soup.get_text(separator="\n", strip=True)
            html_text += text + "\n"

@mcp.tool
def search_html(question: str) -> str:
    """Search HTML content for relevant context and answer the question."""
    keywords = question.lower().split()
    matches = [line for line in html_text.split('\n') if any(k in line.lower() for k in keywords)]
    context = "\n".join(matches[:10])  # limit context size

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Answer based on the provided HTML content."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    mcp.run(transport="stdio")
