import requests


def get_weather_message(city, location=None):
    # --- 1. Turn the city name into coordinates ---
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 10, "language": "en"},
        timeout=10,
    ).json()

    results = geo.get("results")
    if not results:
        return f"Could not find a city called '{city}'."

    # --- 2. Pick the right match ---
    match = results[0]
    if location:
        location = location.lower()
        for r in results:
            country = r.get("country", "").lower()
            code = r.get("country_code", "").lower()
            region = (r.get("admin1") or "").lower()
            if location in (country, code, region):
                match = r
                break

    # --- 3. Get the current weather for those coordinates ---
    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": match["latitude"],
            "longitude": match["longitude"],
            "current": "temperature_2m,apparent_temperature,"
                       "relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "auto",
        },
        timeout=10,
    ).json()["current"]

    # --- 4. Turn the weather code into words ---
    conditions = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Rime fog",
        51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
        61: "Light rain", 63: "Rain", 65: "Heavy rain",
        71: "Light snow", 73: "Snow", 75: "Heavy snow",
        80: "Rain showers", 81: "Rain showers", 82: "Violent showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with hail",
    }
    description = conditions.get(weather["weather_code"], "Unknown")

    # --- 5. Build the message ---
    name = f"{match['name']}, {match['country']}"
    return (
        f"{name} — {weather['temperature_2m']}°C\n"
        f"{description}, feels like {weather['apparent_temperature']}°C\n"
        f"Humidity {weather['relative_humidity_2m']}% · "
        f"Wind {weather['wind_speed_10m']} km/h"
    )