# Make sure directory is correct to run file
import os
os.chdir(os.path.dirname(__file__))

# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite").connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome! <br/>"
        f"<br/>"
        f"Please enter start/end dates in YYYY-MM-DD format. <br/>"
        f"Start/end dates can range from 2010-01-01 to 2017-08-23 <br/>"
        f"<br/>"
        f"Available routes are the following: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    # Query for date and precipitation over prior year 
    last_date = dt.date(2017, 8, 23)

    year_prior = last_date - dt.timedelta(days=365)

    precipitation_query = session.query(measurement.date, measurement.prcp)\
        .filter(measurement.date >= year_prior).all()
    
    # Reformat data in order to jsonify
    precipitation_dates = []
    for date, precipitation in precipitation_query:
        prcp_date_dict = {}
        prcp_date_dict["date"] = date
        prcp_date_dict["prcp"] = precipitation
        precipitation_dates.append(prcp_date_dict)

    # Close our session
    session.close()
    
    return jsonify(precipitation_dates)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    # Query
    station_query = session.query(station.id, station.station, station.name,\
                station.latitude, station.longitude, station.elevation).all()

    # Reformat data in order to jsonify
    station_data = []
    for id, stat, name, lat, lng, elev in station_query:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = stat
        station_dict["name"] = name
        station_dict["latitude"] = lat
        station_dict["longitude"] = lng
        station_dict["elevation"] = elev
        station_data.append(station_dict)

    # Close our session
    session.close()
    
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    # Query for date and TOBs over prior year at most-active station
    last_date = dt.date(2017, 8, 23)

    year_prior = last_date - dt.timedelta(days=365)
    
    tobs_query = session.query(measurement.date, measurement.tobs)\
        .filter(measurement.date >= year_prior)\
        .filter(measurement.station == "USC00519281").all()
    
    # Reformat data in order to jsonify
    tobs_dates = []
    for date, tobs in tobs_query:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dates.append(tobs_dict)

    # Close our session
    session.close()
    
    return jsonify(tobs_dates)

@app.route("/api/v1.0/<start>")
def date_start(start):
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    # Query for min, max, avg temps from start date onwards    
    start_query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs))\
    .filter(measurement.station == "USC00519281").filter(measurement.date >= start).all()

    # Reformat data in order to jsonify
    start_list = []
    for min, max, avg in start_query:
        start_dict = {}
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg
        start_list.append(start_dict)

    # Close our session
    session.close()

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def date_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    # Query for min, max, avg temps from start date to end date
    start_query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs))\
    .filter(measurement.station == "USC00519281").filter(measurement.date >= start).filter(measurement.date <= end).all()

    # Reformat data in order to jsonify
    start_end_list = []
    for min, max, avg in start_query:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["max"] = max
        start_end_dict["avg"] = avg
        start_end_list.append(start_end_dict)

    # Close our session
    session.close()

    return jsonify(start_end_list)


if __name__ == "__main__":
    app.run(debug=True)