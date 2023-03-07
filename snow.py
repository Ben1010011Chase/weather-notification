import os
import requests
import yaml
from datetime import datetime, timedelta
from send_email import send_email

snow_threshold = 1  # in cm

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
weather_api_key = config['WEATHER_API_KEY']
lat = config['LATITUDE']
lon = config['LONGITUDE']

# Make a request to the OpenWeatherMap API to retrieve forecast weather data
url = ('https://api.openweathermap.org/data/2.5/'
        f'forecast?lat={lat}&lon={lon}&units=metric'
        f'&cnt=5&appid={weather_api_key}')
response = requests.get(url)

# Check if the response was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON to get the weather data
    weather_data = response.json()

    # Get the current date and time
    now = datetime.now()
    
    # calculate start and end times for the overnight period
    start_time = now.replace(hour=18, minute=0)
    end_time = start_time + timedelta(hours=15)

    # Extract the weather data for overnight (from 6pm to 9am)
    overnight_data = [data for data in
                      weather_data['list'] if start_time <= 
                      datetime.fromisoformat(data['dt_txt']) < end_time]

    # Calculate snow accumulation from overnight data if available,
    # otherwise set to 0
    snow_accumulation = sum(data['snow']['3h'] if 'snow' in data and
                            '3h' in data['snow'] else 0 for data in
                            overnight_data)

    # Display a notification if it's going to snow more than the 
    # threshold overnight
    if snow_accumulation > snow_threshold:
        os.system("osascript -e 'display notification \"Snow expected"
                  f" overnight! Accumulation: {snow_accumulation}cm\" with"
                  " title \"Snow Removal\" ' ")
        send_email('Snow Removal', 'Snow expected overnight!' 
                    f'Accumulation: {snow_accumulation}cm', 
                    config['BEN_CELL'], config['JENIKA_CELL'] )
else:
    os.system("osascript -e 'display notification \"Status code:" 
              f" {response.status_code}\" with title \"Error"
              " retrieving weather data\" ' ")
    send_email('Error retrieving weather data for snow removal', 
               f'Status code: {response.status_code}', 
               config['BEN_CELL'] )
