## Open-Meteo
#
# Free, open-source weather API.
# No API key required.
# Offers hourly forecasts, historical data, and more.
#


import os
import httpx
import asyncio
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# class WeatherAPI:
#     def __init__(self, city_name):
#         load_dotenv()
#         self.api_key = os.getenv("WEATHER_API_KEY")
#         self.city_name = city_name
#         self.base_url = "https://api.weatherapi.com/v1/current.json"


# Load environment variables
load_dotenv()
url = os.getenv("WEATHER_URL")
api_key = os.getenv("WEATHER_API_KEY")

# Initialize MCP
mcp = FastMCP(name="weather", host="localhost", port=8002)


@mcp.tool()
async def get_weather(city_name: str) -> dict:
    """
    Fetch current weather for a given city uasing api call.
    Args:
        city_name (str): Name of the city to fetch weather for.
    Returns a dictionary with city, temperature (C), country, latitude, longitude, wind_speed (kph) and condition.
    """
     # Placeholder response
    print(f"Server received weather request: {city_name}")
    params = {"key": api_key, "q": city_name, "aqi": "no"}
    print(f"Requesting weather data for {city_name} with params: {params}")

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=5)

    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "latitude": data["location"]["lat"],
            "longitude": data["location"]["lon"],
            "last_updated": data["current"]["last_updated"],
            "temperature_c": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "wind_kph": data["current"]["wind_kph"],
        }
    else:
        raise Exception(
            f"API request failed: {response.status_code} - {response.json()}"
        )


if __name__ == "__main__":
    print("Running MCP server on http://localhost:8005")

    # response = asyncio.run(get_weather("Oslo"))  # Example call to test the function
    # print(f"Weather in {response['city']}, {response}:")
    mcp.run(transport="streamable-http")
