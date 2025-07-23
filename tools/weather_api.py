## Open-Meteo
#
# Free, open-source weather API.
# No API key required.
# Offers hourly forecasts, historical data, and more.
#


import os
import requests
from dotenv import load_dotenv
import mcp
from mcp.server.fastmcp import FastMCP


mcp = FastMCP(name="weather")


# class WeatherAPI:
#     def __init__(self, city_name):
#         load_dotenv()
#         self.api_key = os.getenv("WEATHER_API_KEY")
#         self.city_name = city_name
#         self.base_url = "https://api.weatherapi.com/v1/current.json"
load_dotenv()

url = os.getenv("WEATHER_URL")
api_key = os.getenv("WEATHER_API_KEY")
# city_name = "Oslo"  # Default city for testing

@mcp.tool()
def get_weather(city_name: str) -> dict:
    """
    Fetch current weather for a given city using WeatherAPI.com.
    Returns a dictionary with city, temperature (C), and condition.
    """
    print(f"Server received weather request: {city_name}")
    params = {"key": api_key, "q": city_name, "aqi": "no"}
    print(f"Requesting weather data for {city_name} with params: {params}")
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["location"]["name"],
            "temperature_c": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
        }
    else:
        raise Exception(
            f"API request failed: {response.status_code} - {response.json()}"
        )


if __name__ == "__main__":
    print("Running server with Streamable HTTP transport for weather API...")
    mcp.run(transport="streamable-http", 
            host="localhost", port=8000)  # Adjust host and port as needed
    # print("Weather API server is up and running.")
    # respond = get_weather(city_name)  # Test the function on server start
    # print(f"Weather data for {city_name}: {respond}")
