import forecastio
import numpy as np
from api_key import key

from flask import Flask, render_template

app = Flask(__name__)

api_key = key()

lat = 51.2330
lng = 0.2859

# Some locations:
here = (lat, lng)
sydney = (-33.86, -151.2094)
new_york = (40.7127, 74.0059)
tokyo = (35.6895, -139.6917)
riodj = (22.9083, 43.1964)

@app.route('/')
def index():
    forecast = forecastio.load_forecast(api_key, lat, lng)
    current = forecast.currently()
    current1, current2, index_ratio = compare_locations(here, new_york)
    return render_template('index.html', text1=lat, text2=lng, text3=current.summary)

# compares the weather index of two locations
# if > 1, loc1 is better than loc2.
def compare_locations(loc1, loc2):
    lat1, lng1 = loc1
    lat2, lng2 = loc2

    forecast1 = forecastio.load_forecast(api_key, lat1, lng1)
    current1 = forecast1.currently()
    index1 = weather_index(current1)

    forecast2 = forecastio.load_forecast(api_key, lat2, lng2)
    current2 = forecast2.currently()
    index2 = weather_index(current2)
    return current1, current2, index1/index2

# calculates a weather index for a location, based on its current forecast
# currently uses temperature only
def weather_index(current):
    temp = current.temperature
    feels_like = current.apparentTemperature
    humidity = current.humidity*100
    precip = current.precipIntensity
    precipProb = current.precipProbability
    if current.precipIntensity != 0:
        precipType = current.precipType
    return temp

if __name__ == '__main__':
    app.run(debug=True)

# Can't get a google maps API key until we have a URL!
# from googlemaps import GoogleMaps
# gmaps = GoogleMaps(api_key)
# address = 'Constitution Ave NW & 10th St NW, Washington, DC'
# lat, lng = gmaps.address_to_latlng(address)
# print lat, lng
