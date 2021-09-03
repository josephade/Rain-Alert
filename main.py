import requests
import os
from twilio.rest import Client
#from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "9e56f2d75a6e0822069a90b488b1ef54"
account_sid = "AC528813b348cd5cbb4d0823e557faf38b"
auth_token = os.environ.get("b2cdb01dcf40c2c2dde4a79b6dd95919")

weather_params = {
    "lat": 53.344100,
    "lon": -6.267490,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_="+13213513160",
        to="+353899482942"
    )
    print(message.status)
