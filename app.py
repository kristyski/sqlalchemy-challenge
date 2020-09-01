import numpy as np

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base #to pull in the tables from the sqllite db
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify #for pulling out endpoints and display in browser

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Initialize Flask app
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/station'>Stations</a><br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/tobs'>TOBS</a><br/>"
        f"<a href='/api/v1.0/<start>'>Start Date</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>Start Date / End Date</a><br/>"
        )

#################################################
# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/station")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results = session.query(Stations.station).all() #to get the station name column

    session.close()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#################################################
# * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# * Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all measurements"""
    # Query all precip
    results = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date >= '2016-08-23').all()
    print (results[0])
   
    precip = {date: prcp for date, prcp in results}

    return jsonify(precip)

    session.close()

#################################################
# * Query the dates and temperature observations of the most active station for the last year of data.
# * Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list for most active station for last year"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all
    results = session.query(Measurements.tobs).\
        filter(Measurements.date>='2016-08-23').\
        filter(Measurements.station == 'USC00519281').all()

    session.close()
    print(results)

# Convert list of tuples into normal list
    tobs = list(np.ravel(results))

# * Return a JSON list of stations from the dataset.
    return jsonify(tobs=tobs)

#################################################
# * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start):
# def stats(start=None, end=None):

#   Query min, avg, max temp for a start & end range
    session = Session(engine)
    
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)

    sel = [func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)]
    results = session.query(*sel).filter(Measurements.date >= start).filter(Measurements.date <= end).all()

    stats = list(np.ravel(results))
    
    return jsonify(stats=stats)

    session.close()

if __name__ == "__main__":
    # Create your app.run statement here
    app.run(debug=True)