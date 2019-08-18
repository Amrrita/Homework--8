    
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hello these are all your routes<br><br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/'start'<br>"
        f"/api/v1.0/'start'/'end'<br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return all date and prcp"""

    session = Session(engine)

    precipitation = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    prcp = []
    for i in np.arange(0,len(precipitation)):
        row = {}
        row[str(precipitation[i][0])] = precipitation[i][1]
        prcp.append(row)

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return list of stations"""

    session = Session(engine)
    station = session.query(Station.station,Station.name).all()

    return jsonify(station)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperatures from the last year"""

    session = Session(engine)
    Last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)

    precipitation = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=year_ago).order_by(Measurement.date).all()
    prcp = []
    for i in np.arange(0,len(precipitation)):
        row = {}
        row[str(precipitation[i][0])] = precipitation[i][1]
        prcp.append(row)

    return jsonify(prcp)

@app.route("/api/v1.0/<start>")
def starting(start):
    """Return temps from start to end"""
    session = Session(engine)
    temps = [func.min(Measurement.tobs),\
        func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)]
    tm = session.query(*temps).filter(Measurement.date >= start).all()
    return jsonify(tm[0])

@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start,end):
    """Return temps from start to specified end"""
    session = Session(engine)
    temps = [func.min(Measurement.tobs),\
        func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)]
    tm = session.query(*temps).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(tm[0])

if __name__ == '__main__':
    app.run(debug=True)