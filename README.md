
# Build a cloud based weather SMS service using Python, Twilio and PythonAnywhere


#### Have you always been forgetful about checking the weather before going outdoors and got really washed out by the rainy days? In this tutorial, I'm sharing with you how to build a cloud-based weather SMS service that runs as scheduled to message you about the weather determining if you need an umbrella or not during the day.



## Prerequisites

### 1. [Twilio](https://www.twilio.com/): Twilio Account, Phone number, and account sid and auth token. 
### 2. A [PythonAnywhere account](https://pythonanywhere.com)
### 3. An [Open Weather Map acount](https://openweathermap.org/) and API Key

## How this works? !

<img src="https://docs.google.com/drawings/d/e/2PACX-1vQwO6F1_4IminFN_0HXfrJDfrwDeLv2qD0C76h5vfmY5GmKZEDHaQjYlN3-l04jR4fgvW-InPGK1GUN/pub?w=960&amp;h=720">

As this diagram indicates, we will have a Python script that's running in a cloud environment ([PythonAnywhere](https://pythonanywhere.com)) which will be scheduled to run daily to send HTTP request to [Open Weather API](https://openweathermap.org/api) to fetch a current day's weather report (specifically for fetching the rain data). Then it will notify us these data via SMS by using [Twilio](https://www.twilio.com/) Python rest client (You will need a Twilio API key and account_sid for this.)

First of all, let's set up our project folder a bit. In my case, my project folder looked like the following: 

**App.py** - this is where our main functions run

**Credentials.py** - this is where I store my secret credentials so that I'm not showing them during tutorial recording in my main script. (If you want, you can have this all in one .py file or save these secrets as environment variables. )

Also in order for us to have a more Pythonic API interface to work with Open Weather Map, we will use a Python wrapper module called [PYOWM](https://pyowm.readthedocs.io/en/latest/) to interact with open weather map rest API. 

## Write the main script and test it locally

Let's import necessary modules:


```python
from pyowm import OWM ## import Open Weather Map api wrapper
from twilio.rest import Client ## import twilio rest Python client
```

then we should import our credentials stored in Credentials.py:


```python
from credentials import (my_twilio_number, account_sid, 
                         auth_token, my_phone_number)
```

Instantiate an OWM object with your [Open Weather API key](https://home.openweathermap.org/api_keys)


```python
# Instantiate an owm object

owm = OWM('your Open Weather Map API KEY')


# Construct a forecast 

forecast = owm.weather_at_place("City, Country") # (London, GB)

# Get the weather object to fetch specific data.

weather = forecast.get_weather()
```

we define a function umbrellaNotRequired() that returns True if there's no rain. Otherwise, this function will return False. 


```python
def umbrellaNotRequired():
    
    # Use get_rain() method from weather object.
    rain = weather.get_rain()
    status = weather.get_status().lower().strip()

    if len(rain) == 0 or status == "clear":

        return True
    else:
        return False
```

Now we are making a function mainly for constructing a Twilio rest client to send SMS meanwhile validating umbrellaNotRequired() to send custom notifications. Learn more about how to use Python Twilio API [here](https://frankdu.co/tutorial/send_sms_with_twilio_api_using_python/)


```python
def send_weather_sms():

    # Make a Twilio rest client with api token and account_sid
    client = Client(account_sid, auth_token)

    # Check if the OWM API is onine. 
    if owm.is_API_online:

        if umbrellaNotRequired():

            # Get temp 
            temperature = weather.get_temperature("celsius")["temp"]
            
            # Get the humidity
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
                body="Hey, you got an umbrella warning!!!")

    else:
        
        client.messages.create(
            from_=my_twilio_number,
            to=my_phone_number,
            body='''Hey, weather service not available and check it out by yourself
                    ''')
```

Run the function. 


```python
if __name__ == '__main__':
    
    send_weather_sms()

```
