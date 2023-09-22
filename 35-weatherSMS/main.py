import requests
from twilio.rest import Client


API_KEY = "08a5a03f4b7e89316d901e3cb2ac1732"
MY_LAT = 42.3557242
MY_LON = 1.4537151
CURRENT_WEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather?"
FORECAST_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast?"

ACCOUNT_SID = "test"
AUTH_TOKEN = "test"

parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": API_KEY,
    "cnt": 4
}

response = requests.get(FORECAST_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()


forecasted_weather = []
for i in range(4):
    weather_code = data["list"][i]["weather"][0]["id"]
    forecasted_weather.append(weather_code)

if any(forecasted_weather) < 700:
    rain_coming = True

if rain_coming:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body="It's gonna rain today",
        from_="phone_number",
        to="another_phone_number"
    )
    print(message.status)
