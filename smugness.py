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
results = Geocoder.geocode("Tian'anmen, Beijing")
here = results[0].coordinates
here = (51.2330, -0.2859)
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
    loc2 = sydney

    # find current weather, icon + temp of loc1
    current1, icon1, temp1 = single_location(loc1)

    # find current weather, icon + temp of loc2
    # smugness is the ratio of weather indices
    current2, smugness, icon2, temp2 = compare_locations(current1, loc2)

    # find weather index of current location
    index = weather_index(current1)
    here_goodness = 1.
    here_rank = here_goodness*index

    # rank locations according to current weather, taking usual weather into account
    ranked_locs = rank_locations([sydney, new_york, tokyo, riodj], loc_strs)
    ranks = ranked_locs
    ranks = 'Nowhere'
#     for loc_tuple in ranked_locs:
#         if loc_tuple[1] > here_rank:
#             ranks = loc_tuple[0]
    ranks = ranked_locs[0][0]

    text1, text2 = compass(loc1)
    temp1 = "%s%sC" %(int(temp1), u'\N{DEGREE SIGN}')
    temp2 = "%s%sC" %(int(temp2), u'\N{DEGREE SIGN}')

#     print loc1[0], loc1[1]
#     word_location = Geocoder.reverse_geocode(loc1[0], loc1[1])
#     print word_location

    description = "That's not so good, but don't worry -"
    if here_rank > 10:
        description = "That's pretty nice, AND"

    return render_template('smug.html', text1=text1, text2=text2, \
            text3=current1.summary, text4=smug, temp1=temp1, temp2=temp2, \
            img_name1=icon1, img_name2=icon2, ranks=ranks, text5=current2.summary, \
            description=description)

if __name__ == '__main__':
    app.run(debug=True)

