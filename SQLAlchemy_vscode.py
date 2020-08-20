#################################################
# Imports
#################################################
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Unit_10_HW_Resources_hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# Home page. List all routes that are available.
@app.route("/")
def Welcome():
    #List all available api routes.
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )


# Convert the query results to a dictionary using date as the key and prcp as the value. Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    new_dict = {}
    for row in results:
        new_dict[row.date]=row.prcp
    print(new_dict)

    session.close()

    return jsonify(new_dict)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query precipitation
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station = list(np.ravel(results))

    return jsonify(station)

# # Query the dates and temperature observations of the most active station for the last year of data. Return a JSON list of temperature observations (TOBS) for the previous year
@app.route("/api/v1.0/tobs")
def tobs_active():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_day = dt.date(2017, 8, 23)
    one_year_ago = last_day - dt.timedelta(days=365)
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).filter(Measurement.station == 'USC00519281').all()

    # Convert list of tuples into normal list
    temp = list(np.ravel(tobs_results))

    return jsonify(temp)


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# @app.route("/api/v1.0/<start>", "/api/v1.0/<start>/<end>")


if __name__ == '__main__':
    app.run(debug=True, port=5001)

## Reference 10.3 Activity 10