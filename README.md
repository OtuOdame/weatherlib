# weatherlib

`weatherlib` is a lightweight Python library for getting a readable summary of
current weather by city. It uses Open-Meteo's geocoding and forecast APIs to
find a location and report its temperature, apparent temperature, humidity,
wind speed, and weather conditions.

Pass an optional `location` hint to help choose the right match when multiple
cities share a name. The result is returned as a formatted string.

```python
from wlib import get_weather_message

print(get_weather_message("Paris", location="France"))
```

The library requires the `requests` package and an internet connection. Weather
data is provided by [Open-Meteo](https://open-meteo.com/).
