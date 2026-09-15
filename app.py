import requests

location = input("Enter your location: ")

geo_url = "https://geocoding-api.open-meteo.com/v1/search"

geo_params = {
    "name": location,
    "count": 1,
    "language": "en",
    "format": "json"
}

geo_response = requests.get(geo_url, params=geo_params)
geo_data = geo_response.json()

if "results" not in geo_data:
    print("Location not found.")

else:
    place = geo_data["results"][0]["name"]
    country = geo_data["results"][0]["country"]
    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    weather_data = weather_response.json()

    if "current" not in weather_data:
        print("Weather data could not be collected.")
        print(weather_data)
        exit()
    current = weather_data["current"]

    print("\n--------------------------------------")
    print("REAL-TIME WEATHER INFORMATION")
    print("----------------------------------------")
    print("Location:", place)
    print("Country:", country)
    print("Temperature:", current["temperature_2m"], "C")
    print("Humidity:", current["relative_humidity_2m"], "%")
    print("Wind Speed:", current["wind_speed_10m"], "km/h")
    print("Precipitation:", current["precipitation"], "mm")
    print("-----------------------------------------")