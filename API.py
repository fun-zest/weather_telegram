import requests
from datetime import datetime

API_KEY = 'fad08c806652d09d5962cb101133a89a'

def get_coords(city_name):
    url = 'http://api.openweathermap.org/geo/1.0/direct?'
    params = {
        'q': city_name,
        'appid': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()[0]
    return data['lat'], data['lon']

def get_weather(city_name):
    coords = get_coords(city_name)

    url = 'https://api.openweathermap.org/data/2.5/weather?'
    params = {
        'lat': coords[0],
        'lon': coords[1],
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }

    response = requests.get(url, params=params)
    data = response.json()
    main = data['main']
    description = data['weather'][0]['description']
    wind = data['wind']
    sunrise = data['sys']['sunrise']
    sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M:%S')
    sunset = data['sys']['sunset']
    sunset_time = datetime.fromtimestamp(sunset).strftime('%H:%M:%S')
    return (f"Температура {main['temp']}°C, {description}",
            f"Ощущается как {main['feels_like']}°C",
            f"Ветер {wind['speed']} м/с",
            f"Влажность {main['humidity']}%",
            f"Восход в {sunrise_time}",
            f"Закат в {sunset_time}")

def weather_on_day(city_name, date):
    coords = get_coords(city_name)
    

    url = 'https://api.openweathermap.org/data/3.0/onecall/day_summary?'
    params = {
        'lat': coords[0],
        'lon': coords[1],
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru',
        'date': date
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    main = data['main']
    description = data['weather'][0]['description']
    wind = data['wind']
    sunrise = data['sys']['sunrise']
    sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M:%S')
    sunset = data['sys']['sunset']
    sunset_time = datetime.fromtimestamp(sunset).strftime('%H:%M:%S')
    return (f"Температура {main['temp']}°C, {description}",
            f"Ощущается как {main['feels_like']}°C",
            f"Ветер {wind['speed']} м/с",
            f"Влажность {main['humidity']}%",
            f"Восход в {sunrise_time}",
            f"Закат в {sunset_time}")


if __name__ == "__main__":
    print(weather_on_day('Москва', '2024-05-24'))
