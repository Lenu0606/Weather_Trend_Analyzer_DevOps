import requests
import csv
import os
from datetime import datetime

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

print("=" * 65)
print("REAL-TIME WEATHER TREND ANALYZER USING AI")
print("=" * 65)

city = input("\nEnter city or place name: ").strip()

if city == "":
    print("Please enter a city or place name.")
    exit()

print("\nSTEP 1 - REAL-TIME WEATHER DATA COLLECTION")
print("-" * 65)

geocode_url = "https://geocoding-api.open-meteo.com/v1/search"

geocode_params = {
    "name": city,
    "count": 1,
    "language": "en",
    "format": "json"
}

try:

    response = requests.get(
        geocode_url,
        params=geocode_params,
        timeout=15
    )

    response.raise_for_status()

    location_data = response.json()

except requests.exceptions.RequestException as error:

    print("Unable to connect to location serice.")
    print("Error:", error)
    exit()

if "results" not in location_data:
    print("Location not found.")
    exit()

if len(location_data["results"]) == 0:
    print("Location not found.")
    exit()

place = location_data["results"][0]

city_name = place["name"]
country = place.get("country", "")
latitude = place["latitude"]
longitude = place["longitude"]

print("\nLocation found successfully.")

print("City      :", city_name)
print("Country   :", country)
print("Latitude  :", latitude)
print("Longitude :", longitude)

data_folder = "data"

if not os.path.exists(data_folder):
    os.makedirs(data_folder)

weather_file = os.path.join(
    data_folder,
    "weather_data.csv"
)

clean_file = os.path.join(
    data_folder,
    "clean_weather_data.csv"
)

change_file = os.path.join(
    data_folder,
    "weather_change_data.csv"
)

ai_file = os.path.join(
    data_folder,
    "ai_weather_trend_results.csv"
)

final_file = os.path.join(
    data_folder,
    "final_weather_trend.csv"
)

weather_url = "https://api.open-meteo.com/v1/forecast"

weather_params = {
    
    "latitude": latitude,
    "longitude": longitude,

    "current": (
        "temperature_2m,"
        "relative_humidity_2m,"
        "apparent_temperature,"
        "precipitation,"
        "rain,"
        "weather_code,"
        "cloud_cover,"
        "surface_pressure,"
        "wind_speed_10m,"
        "wind_direction_10m"
    ),

    "timezone": "auto"
}

try:

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=15
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

except requests.exceptions.RequestException as error:

    print("\nWeather service error.")
    print("Error:", error)
    exit()


current = weather_data["current"]

recorded_time = current["time"]

temperature = current.get("temperature_2m")
humidity = current.get("relative_humidity_2m")
feels_like = current.get("apparent_temperature")
precipitation = current.get("precipitation")
rain = current.get("rain")
weather_code = current.get("weather_code")
cloud_cover = current.get("cloud_cover")
pressure = current.get("surface_pressure")
wind_speed = current.get("wind_speed_10m")
wind_direction = current.get("wind_direction_10m")

print("\n" + "=" * 65)
print("REAL-TIME WEATHER OBSERVATION")
print("=" * 65)


print("Location      :", city_name + ", " + country)
print("Recorded Time :", recorded_time)
print("Temperature   :", temperature, "C")
print("Feels Like    :", feels_like, "C")
print("Humidity      :", humidity, "%")
print("Precipitation :", precipitation, "mm")
print("Rain          :", rain, "mm")
print("Cloud Cover   :", cloud_cover, "%")
print("Surface Pressure    :", pressure, "hPa")
print("Wind Speed    :", wind_speed, "km/h")
print("Wind Direction :", wind_direction)
print("Weather Code   :", weather_code)

print("=" * 65)

file_exists = os.path.exists(weather_file)

with open(
    weather_file,
    "a",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    if not file_exists:

        writer.writerow([
            "City",
            "Country",
            "Latitude",
            "Longitude",
            "Recorded Time",
            "Temperature C",
            "Feels Like C",
            "Humidity %",
            "Precipitation mm",
            "Rain mm",
            "Cloud Cover %",
            "Pressure hPa",
            "Wind Speed kmh",
            "Wind Direction",
            "Weather Code",
        ])


    writer.writerow([
        city_name,
        country,
        latitude,
        longitude,
        recorded_time,
        temperature,
        feels_like,
        humidity,
        precipitation,
        rain,
        cloud_cover,
        pressure,
        wind_speed,
        wind_direction,
        weather_code
    ])

print("\nObservation saved to:", weather_file)



print("\nStep 2 - DATA QUALITY CHECK")
print("-" * 65)

with open(
    weather_file,
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)
    rows = list(reader)

print("Total observations:", len(rows))


columns_to_check = [
    "City",
    "Recorded Time",
    "Temperature C",
    "Feels Like C",
    "Humidity %",
    "Precipitation mm",
    "Rain mm",
    "Cloud Cover %",
    "Pressure hPa",
    "Wind Speed kmh",
    "Wind Direction",
]

empty_values = 0

for row in rows:

    for column in columns_to_check:

        value = row.get(column, "")

        if value is None or value.strip() == "":
            empty_values += 1


invalid_temperature = 0

for row in rows:

    try:

        value = float(row["Temperature C"])

        if value < -50 or value > 60:
            invalid_temperature += 1

    except (ValueError, TypeError):
        invalid_temperature += 1

invalid_humidity = 0

for row in rows:

    try:

        value = float(row["Humidity %"])

        if value < 0 or value > 100:
            invalid_humidity += 1

    except (ValueError, TypeError):
        invalid_humidity += 1

print("\nData Quality Report")

print("Empty values     :", empty_values)
print("Invalid temperature  :", invalid_temperature)
print("Invalid humidity   :", invalid_humidity)

if(
    empty_values == 0
    and invalid_temperature == 0
    and invalid_humidity == 0
):

    print("\nData quality check passed.")

else:

    print("\nSome data quality problems were found.")

print("\nStep 3 - DATA PREPARATION")
print("-" * 65)

unique_rows = []

seen = set()

duplicates_removed = 0

for row in rows:

    key = (
        row["City"],
        row["Recorded Time"]
    )

    if key not in seen:

        seen.add(key)
        unique_rows.append(row)

    else:

        duplicates_removed += 1


numeric_columns = [
    "Latitude",
    "Longitude",
    "Temperature C",
    "Feels Like C",
    "Humidity %",
    "Precipitation mm",
    "Rain mm",
    "Cloud Cover %",
    "Pressure hPa",
    "Wind Speed kmh",
    "Wind Direction",
    "Weather Code"
]

clean_rows = []

for row in unique_rows:

    valid = True

    for column in numeric_columns:

        try:

            row[column] = float(row[column])

        except (ValueError, TypeError):

            valid = False
            break

    if valid:
        clean_rows.append(row)


def get_time(row):

    try:

        return datetime.fromisoformat(
            row["Recorded Time"]
        )

    except ValueError:

        return datetime.min



clean_rows.sort(
    key=lambda row: (
        row["City"],
        get_time(row)
    )
)



fieldnames = [
    "City",
    "Country",
    "Latitude",
    "Longitude",
    "Recorded Time",
    "Temperature C",
    "Feels Like C",
    "Humidity %",
    "Precipitation mm",
    "Rain mm",
    "Cloud Cover %",
    "Pressure hPa",
    "Wind Speed kmh",
    "Wind Direction",
    "Weather Code"
]

with open(
    clean_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(clean_rows)

print("Original observations  :", len(rows))
print("Duplicates removed     :", duplicates_removed)
print("Clean observations     :", len(clean_rows))


print("\nClean data saved to:", clean_file)

print("\nSTEP 4 - WEATHER TREND ANALYSIS")
print("-" * 65)

if len(clean_rows) < 2:

    print("\nOnly one observation is available.")
    print("More observations are needed to calculated")
    print("weather changes.")

    print("\nThe first observation has been collected.")
    print("Run the program again later to collect")
    print("another observation.")

    exit()

previous_by_city = {}

change_rows = []

for row in clean_rows:

    city_value = row["City"]

    temperature = float(
        row["Temperature C"]
    )

    humidity = float(
        row["Humidity %"]
    )

    pressure = float(
        row["Pressure hPa"]
    )

    wind_speed = float(
        row["Wind Speed kmh"]
    )

    cloud_cover = float(
        row["Cloud Cover %"]
    )

    rain_value = float(
        row["Rain mm"]
    )

    if city_value not in previous_by_city:


        temperature_change = 0
        humidity_change = 0
        pressure_change = 0
        wind_change = 0
        cloud_change = 0
        rain_change = 0

    else:

        previous = previous_by_city[city_value]

        temperature_change = (
            temperature -
            float(previous["Temperature C"])
        )

        humidity_change = (
            humidity -
            float(previous["Humidity %"])
        )

        pressure_change = (
            pressure -
            float(previous["Pressure hPa"])
        )

        wind_change = (
            wind_speed -
            float(previous["Wind Speed kmh"])
        )

        cloud_change = (
            cloud_cover -
            float(previous["Cloud Cover %"])
        )

        rain_change = (
            rain_value -
            float(previous["Rain mm"])
        )

    new_row = row.copy()

    new_row["Temperature Change"] = round(
        temperature_change,
        2
    )

    new_row["Humidity Change"] = round(
        humidity_change,
        2
    )

    new_row["Pressure Change"] = round(
        pressure_change,
        2
    )

    new_row["Wind Change"] = round(
        wind_change,
        2
    )

    new_row["Cloud Change"] = round(
        cloud_change,
        2
    )

    new_row["Rain Change"] = round(
        rain_change,
        2
    )

    change_rows.append(new_row)

    previous_by_city[city_value] = row

change_fields = fieldnames + [
    "Temperature Change",
    "Humidity Change",
    "Pressure Change",
    "Wind Change",
    "Cloud Change",
    "Rain Change",
]

with open(
    change_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=change_fields
    )

    writer.writeheader()
    writer.writerows(change_rows)

print("Weather changes calculated successfully.")

print("Change data saved to:", change_file)

print("\nSTEP 5 - AI WEATHER TREND ANALYSIS")
print("-" * 65)

if len(change_rows) < 10:

    print("\nAI analysis needs at least 10 observations.")

    print("Current observations:",
          len(change_rows))

    print("\nThe data collection part is working.")
    print("Run main.py again later to collect more")
    print("weather observations.")

    exit()


features = [
    "Temperature C",
    "Humidity %",
    "Pressure hPa",
    "Wind Speed kmh",
    "Cloud Cover %",
    "Rain mm",
    "Temperature Change",
    "Humidity Change",
    "Pressure Change",
    "Wind Change",
    "Cloud Change",
    "Rain Change"
]

ai_data = []

valid_ai_rows = []

for row in change_rows:

    try:

        values = []

        for feature in features:

            values.append(
                float(row[feature])
            )

        ai_data.append(values)

        valid_ai_rows.append(row)

    except (ValueError, TypeError, KeyError):

        pass


print("Valid observations for AI:",
      len(ai_data))

if len(ai_data) < 10:

    print("\nNot enough valid observations for AI.")
    exit()

scaler = StandardScaler()

scaled_data = scaler.fit_transform(
    ai_data
)

model = IsolationForest(
    contamination=0.10,
    random_state=42
)

model.fit(scaled_data)

predictions = model.predict(
    scaled_data
)

scores = model.decision_function(
    scaled_data
)

ai_rows = []

for index, row in enumerate(valid_ai_rows):

    new_row = row.copy()

    if predictions[index] == 1:

        new_row["AI Trend Result"] = "NORMAL"

    else:

        new_row["AI Trend Result"] = "UNUSUAL"

    new_row["Anomaly Score"] = round(
        scores[index],
        4
    )

    ai_rows.append(new_row)

ai_fields = list(change_fields)

ai_fields.append("AI Trend Result")
ai_fields.append("Anomaly Score")


with open(
    ai_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=ai_fields,
        extrasaction="ignore"
    )

    writer.writeheader()
    writer.writerows(ai_rows)

normal_count = 0
unusual_count = 0

for row in ai_rows:

    if row["AI Trend Result"] == "NORMAL":

        normal_count += 1

    else:

        unusual_count += 1

print("\nAI analysis completed.")

print("Normal observations :",
      normal_count)
print("Unusual observations:",
      unusual_count)

print("AI results saved to:",
      ai_file)



print("\nSTEP 6 - FINAL WEATHER TREND RESULT")
print("-" * 65)

def find_trend(value):

    value = float(value)

    if value > 0.5:

        return "INCREASING"

    elif value < -0.5:

        return "DECREASING"
    else:
        return "STABLE"


final_rows = []

for row in ai_rows:

    new_row = row.copy()

    temperature_trend = find_trend(
        row["Temperature Change"]
    )

    humidity_trend = find_trend(
        row["Humidity Change"]
    )

    pressure_trend = find_trend(
        row["Pressure Change"]
    )

    wind_trend = find_trend(
        row["Wind Change"]
    )

    cloud_trend = find_trend(
        row["Cloud Change"]
    )

    rain_trend = find_trend(
        row["Rain Change"]
    )

    new_row["Temperature Trend"] = (
        temperature_trend
    )

    new_row["Humidity Trend"] = (
        humidity_trend
    )

    new_row["Pressure Trend"] = (
        pressure_trend
    )

    new_row["Wind Trend"] = (
        wind_trend
    )
    new_row["Cloud Trend"] = (
        cloud_trend
    )
    new_row["Rain Trend"] = (
        rain_trend
    )


    if row["AI Trend Result"] == "UNUSUAL":

        final_result = "UNUSUAL WEATHER TREND"

    elif (
        temperature_trend != "STABLE"
        or humidity_trend != "STABLE"
        or pressure_trend != "STABLE"
    ):

        final_result = (
            "WEATHER CONDITIONS ARE CHANGING"
        )
        
    else:

        final_result = (
            "WEATHER CONDITIONS ARE STABLE"
        )

    new_row["Final Weather Trend"]=(
        final_result
    )

    final_rows.append(new_row)


final_fields = ai_fields + [
    "Temperature Trend",
    "Humidity Trend",
    "Pressure Trend",
    "Wind Trend",
    "Cloud Trend",
    "Rain Trend",
    "Final Weather Trend",
]

with open(
    final_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=final_fields
    )

    writer.writeheader()
    writer.writerows(final_rows)

print("\n" + "=" * 65)
print("FINAL WEATHER TREND RESULT")
print("=" * 65)

latest = final_rows[-1]

print("\nLocation  :",
      latest["City"],
      ",",
      latest["Country"])

print("Recorded Time:", latest["Recorded Time"])

print("Temperature :", latest["Temperature C"],"C")
print("Humidity :", latest["Humidity %"], "%")
print("Pressure :", latest["Pressure hPa"], "hPa")
print("Wind Speed :", latest["Wind Speed kmh"],"km/h")
print("\nTemperature Trend:", latest["Temperature Trend"])
print("Humidity Trend:", latest["Humidity Trend"])
print("Pressure Trend:", latest["Pressure Trend"])
print("Wind Trend :", latest["Wind Trend"])
print("Cloud Trend :", latest["Cloud Trend"])
print("Rain Trend :", latest["Rain Trend"])

print("\nAI Result :", latest["AI Trend Result"])
print("Anomaly Score :", latest["Anomaly Score"])

print("\nFINAL WEATHER TREND:", latest["Final Weather Trend"])

print("\n" + "=" * 65)
print("PROJECT ANALYSIS COMPLETED")
print("=" * 65)

print("\nFinal result saved to:")
print(final_file)

print("\nAll major steps completed successfully.")
print("REAL-TIME WEATHER TREND ANALYZER USING AI")
print("=" * 65)
