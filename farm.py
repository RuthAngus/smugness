# -*- coding: utf-8 -*-
import numpy as np
import forecastio
from api_key import key
from pygeocoder import Geocoder

api_key = key()

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

def rank_locations(latlongs, names):
    # calculate current indices for all other locations
    # change this so it updates every hour to save on api calls
    indices = np.empty(len(names))
    for i, loc in enumerate(latlongs):
        forecast = forecastio.load_forecast(api_key, loc[0], loc[1])
        current = forecast.currently()
        indices[i] = weather_index(current)
    # weight by goodness
    # goodness could be 'learnt' or could take data from NOAO
    # for now I'm going to make it up
    #sydney, tokyo, riodj, new_york
    goodness = [.8, .5, .9, .7]
    goodness = [1., 1., 1., 1.]
    likelihood = indices*goodness
    tuples = zip(names, likelihood)
    ranked = sorted(tuples, key=lambda x: x[1])
    return ranked

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
