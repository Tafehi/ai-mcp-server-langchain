"""
Strava Tool Server
https://www.strava.com/
"""

import os
import sys
import httpx
import asyncio
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()
strava_client_id = os.getenv("STRAVA_CLIENT_ID")
strava_client_secret = os.getenv("STRAVA_CLIENT_SECRET")
strava_access_token = os.getenv("STRAVA_ACCESS_TOKEN")
strava_endpoint = os.getenv("STRAVA_END_POINT")

# Initialize MCP
mcp = FastMCP(name="strava", host="localhost", port=8001)

@mcp.tool()
async def get_strava_activities(per_page: int = 10) -> list:
    """
    Fetch recent activities from Strava using the API.
    """
    print(f"Strava Client ID: {strava_client_id}")
    print(f"Strava Client Secret: {strava_client_secret}")
    print(f"Fetching up to {per_page} activities from Strava API...")

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
        return response.json()
    else:
        raise Exception(f"Strava API request failed: {response.status_code} - {response.text}")

# Optional: test the tool manually
async def test_tool():
    try:
        activities = await get_strava_activities()
        print("Response type:", type(activities))
        print("Response content:", activities)

        for activity in activities:
            if isinstance(activity, dict):
                print(f"{activity['name']} - {activity['distance']} meters")
            else:
                print("Unexpected activity format:", activity)
    except Exception as e:
        print("Error during test:", e)

if __name__ == "__main__":
    # asyncio.run(test_tool())
    print("Starting Strava MCP server on http://localhost:8001/mcp/")
    mcp.run(transport="streamable-http")
