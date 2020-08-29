import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base #to pull in the tables in the sqllite db
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify #for pulling out endpoints and display in browser

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True) #use inspector, here, you should be very familiar with data in database

# Save reference to the tables
Measurements = Base.classes.measurement #assuming know there is this table
Stations = Base.classes.station

# Initialize your Flask app
app = Flask(__name__)

# Flask Routes

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/measurement'>measurement</a>"
        f"<a href='/api/v1.0/station'>station</a>"
    )

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results = session.query(stations.station).all() #to get the name column

    session.close() # good housekeeping to close session
    # print(results)
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     return jsonify(precip)


# * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# * Return the JSON representation of your dictionary.
# * Return a JSON list of stations from the dataset.
# * Query the dates and temperature observations of the most active station for the last year of data.
# * Return a JSON list of temperature observations (TOBS) for the previous year.
# *`/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
# * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
# ## Hints
# * You will need to join the station and measurement tables for some of the queries.
# * Use Flask `jsonify` to convert your API data into a valid JSON response object.

# #not quite working yet, did it not work because above was not quite done?
# @app.route("/api/v1.0/justice-league/<name>")
# def justice_league_name(name):
#     """Return the name of super hero"""
#     for x in justice_league_members:
#         if x['superhero'] == name:
#             superhero = x
#             print(superhero)
#     return (superhero)

#she entered /api/v1.0/justice-league/Flash and it returned Flash's real name

if __name__ == "__main__":
    # Create your app.run statement here
        app.run(debug=True)

