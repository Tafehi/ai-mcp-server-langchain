"""
Strava Tool Server
https://www.strava.com/
"""

import os
import httpx
import asyncio
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()
strava_client_id = os.getenv("STRAVA_CLIENT_ID")
strava_access_token = os.getenv("STRAVA_ACCESS_TOKEN")
strava_endpoint = os.getenv("STRAVA_END_POINT")
strava_detail_endpoint = os.getenv("STRAVA_DETAIL_ENDPOINT")

# Initialize MCP
mcp = FastMCP(name="strava", host="localhost", port=8001)

@mcp.tool()
async def get_strava_activities(per_page: int = 10) -> list:
    """
    Fetch recent activities from Strava using the API.
    Args:
        per_page (int): Number of activities to fetch per page. Default is 10.
    Returns:
        list: A list of activities with details like name, distance, and more. tell me my strongest activity.
        suggestions: "tell me my strongest activity", "what is my longest activity"
        give me suggestion for other activities which I can do.
    """

    if not strava_client_id or not strava_access_token:
        raise ValueError("Strava credentials are not set in environment variables.")


    headers = {
        "Authorization": f"Bearer {strava_access_token}"
    }
    params = {
        "per_page": per_page,
        "page": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(strava_endpoint, headers=headers, params=params, timeout=10)

    if response.status_code == 200:
        # print(f"response: {response.json()}")
        return response.json()
    else:
        raise Exception(f"Strava API request failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # asyncio.run(get_strava_activities())
    print("Starting Strava MCP server on http://localhost:8001/mcp/")
    mcp.run(transport="streamable-http")
