import requests
import os
import dotenv
dotenv.load_dotenv()

def forecast_Weather(city: str, days: str) -> dict:
    """
    Retrieves weather forecast data for a given city and number of days.

    Args:
        city (str): The name of the city.
        days (str): Number of days for the forecast (e.g., "1" for today).

    Returns:
        dict: Weather forecast data in JSON format.
    """
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q": city, "days": days}

    headers = {
        "X-RapidAPI-Key": f"{os.getenv('RAPIDAPI_KEY')}",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    weather_data = {
        "location": data["location"],
        "current": data["current"],
        "forecast": data["forecast"]
    }
    return weather_data
    

