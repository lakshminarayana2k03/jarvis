# modules/weather.py
import requests

def get_local_weather(city: str) -> str:
    """
    Fetch simple weather info for a given city using wttr.in API.
    Returns a short string like 'Hyderabad: 🌤 +32°C'.
    """
    try:
        url = f"https://wttr.in/{city}?format=3"   # short format: City: Weather Temp
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Sorry, I couldn't fetch the weather right now."
    except Exception as e:
        return f"Error fetching weather: {e}"
