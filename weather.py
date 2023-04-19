# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com/geo/1.0/direct?q="


def search_city(query):
    '''
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    '''
    cities= requests.get(BASE_URI+"/geo/1.0/direct?", params= {'q': query, 'limit':5}).json()
    if not cities:
        print(f"Sorry, we don't have information about {query}!")
        return None
    if len(cities)==1:
        return cities[0]
    if len(cities)>1:
        print('Multiple matches found, which city did you mean?')
        for index, city in enumerate (cities):
            print(f"{index + 1}. {city['name']}, {city['country']}")
        index_chosen = int(input("Multiple matches found, which city did you mean?\n> "))-1
        return cities[index_chosen]
    return None



def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    url = urllib.parse.urljoin(BASE_URI, "/data/2.5/forecast")
    forecast= requests.get(url, params={'lat': lat,'lon':lon, 'units':'metric'}).json()['list']
    return forecast[:5]


def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)

    if city:
        daily_forecasts = weather_forecast(city['lat'], city['lon'])

        for forecast in daily_forecasts:
            max_temp = round(forecast['main']['temp_max'])
            print(f"{forecast['dt_txt'][:10]}: {forecast['weather'][0]['main']} ({max_temp}°C)")


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
