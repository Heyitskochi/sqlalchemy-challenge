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
    return ( f"these are the available routes...<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route('/api/v1.0/precipitation') 
def precip():
    precip_obj = session.query(measurement.date, measurement.prcp).all()
    precip_obj = dict(precip_obj)
    return jsonify(precip_obj)

@app.route('/api/v1.0/stations')
def stations():
    new_stations = session.query(func.distinct(station.station)).all()
    return jsonify(new_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    twelve_months2 = session.query(measurement.date, measurement.tobs).filter(measurement.date > year_ago).filter(measurement.station == "USC00519281").all()
    twelve_months2 = list(twelve_months2)
    return jsonify(twelve_months2)

@app.route('/api/v1.0/<start>')
def start(start):
    date_time = dt.datetime.strptime(start, '%Y-%m-%d')
    year_ago2 = date_time - dt.timedelta(days=365)
    tmin = session.query(func.min(measurement.tobs)).filter(measurement.date > year_ago2).all()
    tmax = session.query(func.max(measurement.tobs)).filter(measurement.date > year_ago2).all()
    tavg = session.query(func.avg(measurement.tobs)).filter(measurement.date > year_ago2).all()
    return jsonify(f"the min was {tmin}, the max was {tmax}, and the avg was {tavg} for all dates after {date_time}")

@app.route('/api/v1.0/<start>/<end>')
def startend(start, end):
    date_time1 = dt.datetime.strptime(start, '%Y-%m-%d')
    date_time2 = dt.datetime.strptime(end, '%Y-%m-%d')
    tmin = session.query(func.min(measurement.tobs)).filter(measurement.date > date_time1).filter(measurement.date < date_time2).all()
    tmax = session.query(func.max(measurement.tobs)).filter(measurement.date > date_time1).filter(measurement.date < date_time2).all()
    tavg = session.query(func.avg(measurement.tobs)).filter(measurement.date > date_time1).filter(measurement.date < date_time2).all()
    return jsonify(f"the min was {tmin}, the max was {tmax}, and the avg was {tavg} for all dates between {date_time1} and {date_time2}")

if __name__ == "__main__":
    app.run(debug=True)
