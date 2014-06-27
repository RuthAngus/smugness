import forecastio
import numpy as np
from api_key import key

from flask import Flask, render_template

app = Flask(__name__)

api_key = key()

lat = 51.2330
lng = 0.2859

@app.route('/')
def index():

    forecast = forecastio.load_forecast(api_key, lat, lng)
    current = forecast.currently()

    return render_template('index.html', text1=lat, text2=lng, text3=current.summary)

if __name__ == '__main__':
    app.run(debug=True)
