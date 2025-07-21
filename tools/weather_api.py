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


class WeatherAPI:
    def __init__(self, city_name):
        load_dotenv()
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.city_name = city_name
        self.base_url = "https://api.weatherapi.com/v1/current.json"

    @mcp.Tool()
    def get_weather(self):
        """
        Fetch current weather for a given city using WeatherAPI.com.
        Returns a dictionary with city, temperature (C), and condition.
        """
        print(f"Server received weather request: {self.city_name}")
        params = {"key": self.api_key, "q": self.city_name, "aqi": "no"}
        response = requests.get(self.base_url, params=params)
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


# if __name__ == "__main__":
#     weather_api = WeatherAPI(city_name="oslo")
#     try:
#         weather_data = weather_api.get_weather()
#         print(weather_data)
#     except Exception as e:
#         print(f"Error fetching weather data: {e}")
