import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(location):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={os.getenv('OPENWEATHER_API_KEY')}"
    )
    data = response.json()
    return data

