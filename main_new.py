import requests
from twilio.rest import Client
import os

# Twilio account
account_sid = 'ACb331f5e83df08bdaa4bb4f46a6424fb9'
auth_token = os.environ.get("AUTH_TOKEN")

# Weather API
api_key = os.environ.get("weather_api")
weather_api = "http://api.weatherapi.com/v1/forecast.json"

# my_coordinates
MY_LAT = 43.216640
MY_LNG = 27.911810

parameters = {
    "q": (MY_LAT, MY_LNG),
    "key": api_key,
    "alerts": "no",
    "aqi": "no"
}

response = requests.get(weather_api, params=parameters)
response.raise_for_status()
print(response.status_code)

date_section = response.json()["forecast"]["forecastday"][0]
# print(date_section)
hour_section_today = date_section["hour"]
# print(f"Hour section: {hour_section_today}")

it_will_rain = False

for j in hour_section_today:
    hour = j["time"]
    condition = int(j["condition"]["code"])
    condition_text = j["condition"]["text"]
    date = hour.split()[0]
    day = date.split("-")[2]
    month = date.split("-")[1]
    hour_exact = int(hour.split()[1].split(":")[0])
    minutes = int(hour.split()[1].split(":")[1])

    if 7 < hour_exact <= 19 and 1150 <= condition <= 1282:
        # print(f"date: {date}, day: {day}, month: {month}")
        # print(f"hour: {hour_exact}, minutes: {minutes}")
        # print(f"Be careful!During this time of the day the forecast says: {condition_text},"
        #       f" so you should bring an umbrella!")
        # print("***********\n")
        it_will_rain = True

# checking the status of the boolean variable:
# print(it_will_rain)

if it_will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It appears to be raining today, make sure you take your umbrella!",
        from_="virtual_phone_number",
        to="your_phone_number"
    )
    print(message.status)
else:
    print("no message sent")

