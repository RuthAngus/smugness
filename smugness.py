# -*- coding: utf-8 -*-
import forecastio
import numpy as np
from api_key import key
from pygeocoder import Geocoder
from farm import *
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
sydney = (-33.86, -151.2094)
new_york = (40.7127, -74.0059)
tokyo = (35.6895, -139.6917)
riodj = (22.9083, 43.1964)
loc_strs = ['Sydney', 'New York', 'Tokyo', 'Rio de Janeiro']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<latlong>')
def show_latlong(latlong):

    try:
        here = map(float, latlong.split(','))
    except ValueError:
        return flask.abort(404)

    if len(here) != 2:
        return flask.abort(404)

    loc1 = here
    lat, lng = compass(loc1)

    # find current weather, icon + temp of loc1
    current1, icon1, temp1 = single_location(loc1)
    temp1 = "%s%sC" %(int(temp1), u'\N{DEGREE SIGN}')

    # find weather index of current location
    wthr_ind = weather_index(current1)
    here_gdnss = .4
    here_smg = (1./wthr_ind)*here_gdnss

    # rank locations according to current weather, taking usual weather into account
    ranked_locs = rank_locations([sydney, new_york, tokyo, riodj], loc_strs)
    if ranked_locs[-1][1] > here_smg:
        loc2_string = ranked_locs[-1][0]
        there_smg = ranked_locs[-1][1]
    else: description = "Nowhere has worse weather"

    # find current weather, icon + temp of loc2
    # smugness is the ratio of weather indices
    results = Geocoder.geocode(loc2_string)
    loc2 = results[0].coordinates
    current2, smugness, icon2, temp2 = compare_locations(current1, loc2)
    temp2 = "%s%sC" %(int(temp2), u'\N{DEGREE SIGN}')

    print loc1[0], loc1[1]
    word_location = Geocoder.reverse_geocode(loc1[0], loc1[1])
    print word_location

    description = "Don't worry though, it could be worse -"

    return render_template('smug.html', text1=lat, text2=lng, \
            text3=current1.summary, temp1=temp1, temp2=temp2, \
            img_name1=icon1, img_name2=icon2, text5=current2.summary, \
            description=description, loc2_string=loc2_string, \
            word_loc=str(word_location))

if __name__ == '__main__':
    app.run(debug=True)

