'''

Build a cloud based weather SMS service using Python, Twilio and PythonAnywhere

'''
from pyowm import OWM
from twilio.rest import Client

from credentials import (my_twilio_number, account_sid,
                         auth_token, my_phone_number,
                         owm_api_key)


# Instantiate an owm object

owm = OWM(owm_api_key)

forecast = owm.weather_at_place("Dusseldorf, DE")

weather = forecast.get_weather()


def umbrellaNotRequired():


    rain = weather.get_rain()

    status = weather.get_status().lower().strip()

    if len(rain) == 0 or status == "clear":

        return True


def send_weather_sms():


    client = Client(account_sid, auth_token)


    if owm.is_API_online:

        if umbrellaNotRequired():


            temperature = weather.get_temperature("celsius")["temp"]

            humidity = weather.get_humidity()

            client.messages.create(
                from_=my_twilio_number,
                to=my_phone_number,
                body=f'''
                    Hey, sky is clear and you ain't need an umbrella. Weather details:
                    1. Humidity:{humidity} %, 
                    2. Temperature:{temperature} celsius
                ''')

    else:

        client.messages.create(
            from_=my_twilio_number,
            to=my_phone_number,
            body='''
                    Hey, weather service not available and check it out by yourself
                    ''')


if __name__ == '__main__':


    send_weather_sms()
