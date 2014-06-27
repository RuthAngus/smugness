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
new_york = (40.7127, -74.0059)
tokyo = (35.6895, -139.6917)
riodj = (22.9083, 43.1964)

@app.route('/')
def index():

    loc1 = here
    loc2 = new_york

    current1, icon1, temp1 = single_location(loc1)
    current2, smugness, icon2, temp2 = \
            compare_locations(current1, loc2)

    smug = "no. Haha I'm sooooo smug!"
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
    text2 = '%s%s %s' %(abs(loc1[1]), u'\N{DEGREE SIGN}', compass)
    temp1 = "%s%sC" %(int(temp1), u'\N{DEGREE SIGN}')
    temp2 = "%s%sC" %(int(temp2), u'\N{DEGREE SIGN}')

    return render_template('index.html', text1=text1, text2=text2, \
            text3=current1.summary, text4=smug, temp1=temp1, temp2=temp2, \
            img_name1=icon1, img_name2=icon2)

# returns current forecast of one location
def single_location(loc1):
    lat1, lng1 = loc1
    forecast1 = forecastio.load_forecast(api_key, lat1, lng1)
    current1 = forecast1.currently()
    return current1, current1.icon, current1.temperature

# compares the weather index of two locations
# if > 1, loc1 is better than loc2.
def compare_locations(current1, loc2):
    lat2, lng2 = loc2
    forecast2 = forecastio.load_forecast(api_key, lat2, lng2)
    current2 = forecast2.currently()

    index1 = weather_index(current1)
    index2 = weather_index(current2)
    return current2, index1/index2, current2.icon, current2.temperature

def rank_locations(current1, otherlocs):

    # calculate index for current location
    indices = np.empty(len(otherlocs)+1)
    indices[0] = weather_index(current1)

    # calculate current indices for all other locations
    # change this so it updates every hour to save on api calls
    for i, loc in enumerate(otherlocs):
        forecast = forecastio.load_forecast(api_key, loc[0], loc[1])
        current = forecast.currently()
        indices[i] = weather_index(current)

    # weight by average goodness
    # average goodness could be 'learnt' or could take data from NOAO
    # for now I'm going to make average goodness up
    i_sydney = .8
    i_tokyo = .5
    i_riodj = .9
    i_here = .4
    i_new_york = .7
    return

# order locations by longitude
def order(otherlocs):
    return

# calculates a weather index for a location, based on its current forecast
# currently uses temperature only
def weather_index(current):
    temp = current.temperature
    feels_like = current.apparentTemperature
    humidity = current.humidity*100
    precip = current.precipIntensity
    precipProb = current.precipProbability
    windspeed = current.windSpeed
    cloudcover = current.cloudCover
    if current.precipIntensity != 0:
        precipType = current.precipType
    return temp

def remove_space(phrase):
    return phrase.replace(' ', '').replace('-','').lower()

if __name__ == '__main__':
    app.run(debug=True)
