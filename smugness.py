# -*- coding: utf-8 -*-

import forecastio
import numpy as np
from api_key import key

from flask import Flask, render_template

app = Flask(__name__)

api_key = key()

# Can't get a google maps API key until we have a URL!
# from googlemaps import GoogleMaps
# gmaps = GoogleMaps(api_key)
# address = 'Constitution Ave NW & 10th St NW, Washington, DC'
# lat, lng = gmaps.address_to_latlng(address)
# print lat, lng

# Some locations:
here = (51.2330, 0.2859)
sydney = (-33.86, -151.2094)
new_york = (40.7127, 74.0059)
tokyo = (35.6895, -139.6917)
riodj = (22.9083, 43.1964)

@app.route('/')
def index():

    loc1 = sydney
    loc2 = new_york

    current1, current2, smugness = compare_locations(loc1, loc2)
#     current1 = single_location(here)

    smug = 'no'
    if smugness < 1:
        smug = 'yes (obv)'

    # add N, S, E, W
    compass = 'S'
    if loc1[0] > 0:
        compass = 'N'
    text1 = '%s %s %s' %(abs(loc1[0]), u'\N{DEGREE SIGN}', compass)
    compass = 'E'
    if loc1[1] > 0:
        compass = 'W'
    text2 = '%s %s %s' %(abs(loc1[1]), u'\N{DEGREE SIGN}', compass)

    return render_template('index.html', text1=text1, text2=text2, text3=current1.summary, text4=smug)

# returns current forecast of one location
def single_location(loc1):
    lat1, lng1 = loc1
    forecast1 = forecastio.load_forecast(api_key, lat1, lng1)
    current1 = forecast1.currently()
    return current1

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
