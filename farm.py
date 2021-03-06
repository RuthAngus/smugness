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

def rank_locations(latlongs, place_names):
    # calculate current indices for all other locations
    # change this so it updates every hour to save on api calls
    wthr_inds = np.empty(len(place_names))
    for i, loc in enumerate(latlongs):
        forecast = forecastio.load_forecast(api_key, loc[0], loc[1])
        current = forecast.currently()
        wthr_inds[i] = weather_index(current)
    # weight by goodness
    # goodness could be 'learnt' or could take data from NOAO
    # for now I'm going to make it up
    #sydney, tokyo, riodj, new_york
    gdnss = [.8, .5, .9, .7] #the higher the gdnss, the better the average wthr
    smg = (1./wthr_inds)*gdnss #higher smg = more likely to appear
    # FIXME: equal weighting of wthr_inds and gdnss
    tuples = zip(place_names, smg)
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

def compass(loc):
    # add N, S, E, W
    compass = 'S'
    if loc[0] > 0:
        compass = 'N'
    text1 = '%s %s %s' %(abs(loc[0]), u'\N{DEGREE SIGN}', compass)
    compass = 'W'
    if loc[1] > 0:
        compass = 'E'
    text2 = '%s%s %s' %(abs(loc[1]), u'\N{DEGREE SIGN}', compass)
    return text1, text2
