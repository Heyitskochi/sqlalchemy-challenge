from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

app = Flask(__name__)

#SQL Alchemy connections
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement=Base.classes.measurement
station=Base.classes.station
session = Session(engine)

@app.route('/') 
def showroutes():
    return "hi"
# HELP

@app.route('/api/v1.0/precipitation') 
def precip():
    precip_obj = session.query(measurement.date, measurement.prcp).all()
    precip_obj = dict(precip_obj)
    return jsonify(precip_obj)

@app.route('/api/v1.0/stations')
def stations():
    new_stations = session.query(func.distinct(station.station)).all()
    new_stations = list(new_stations)
    return jsonify(new_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    twelve_months2 = session.query(measurement.date, measurement.tobs).filter(measurement.date > year_ago).filter(measurement.station == "USC00519281").all()
    twelve_months2 = list(twelve_months2)
    return jsonify(twelve_months2)

@app.route('/api/v1.0/<start>')
def start():
    return 'hi'

@app.route('/api/v1.0/<start>/<end>')
def startend():
    return 'hi'

if __name__ == "__main__":
    app.run(debug=True)
