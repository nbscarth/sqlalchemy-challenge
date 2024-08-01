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
        f"Welcome!<br/>"
        f"Available routes are the following:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
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
    
    # Close our session
    session.close()
    
    return jsonify()

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    # Query
    station_query = session.query(station).all()

    # Close our session
    session.close()
    
    return jsonify()

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
    
    # Close our session
    session.close()
    
    return jsonify()

@app.route("/api/v1.0/<start>")
def date_start():
    return

@app.route("/api/v1.0/<start>/<end>")
def date_start_end():
    return


if __name__ == "__main__":
    app.run(debug=True)