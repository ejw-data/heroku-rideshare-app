# Dependencies
from flask import Flask, render_template, jsonify, request, redirect, url_for
from inputs import ride_share_calcs

app = Flask(__name__)


@app.route('/')    # removed:  , methods=['GET']
def index():

    start_location =""
    end_location=""

    return render_template("index.html", start_location=start_location, end_location=end_location)

@app.route('/submit', methods=['POST'])
def submit_fare():

    if request.method == 'POST':
        start_location = request.form['startLoc']
        end_location = request.form['endLoc']
       

        if start_location == '' or end_location == '':
            return render_template('index.html', message='Please complete all sections of the form', start_location=start_location, end_location=end_location)
        elif start_location != '' and end_location != '':
            fare_estimate = ride_share_calcs(start_location, end_location, '2019-12-11 00:00:00')
            return render_template('index.html', estimator=fare_estimate, start_location=start_location, end_location=end_location)
        else:
            return render_template('index.html', estimator='', start_location=start_location, end_location=end_location)

    # Mapquest and mapbox:  https://www.mapquestapi.com/directions/v2/route?key=6aMCYSpGBo4Eg20Lw7RljQ0nXcUGsA5S&from=Denver%2C+CO&to=Boulder%2C+CO&outFormat=json&ambiguities=ignore&routeType=fastest&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false
    return render_template('index.html', estimator='')

@app.route('/visual') 
def graphics():


    return render_template('visual.html')


if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=False)




