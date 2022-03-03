import requests
import config

API_KEY = config.api_key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

city = input('Enter a city name: ')
request_url = f'{BASE_URL}?appid={API_KEY}&q={city}'
response = requests.get(request_url)

if response.status_code == 200:
    data = response.json()
    weather = data['weather'][0]['description']
    temperature = round(data['main']['temp'] - 273.15)
    print(weather)
    print(f'{temperature}°C')
else:
    print('An error occurred')

