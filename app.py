import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#################################################
# Database Setup
#################################################
# reflect an existing database into a new model

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Legalization_data.sqlite"

db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
State_Usedata = Base.classes.mjuse_compare
State_Arrest = Base.classes.arrest_prispop_data

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(State_Arrest).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])


@app.route("/metadata/<State>")
def mjuse_compare(State):
    """Return the MetaData for a given sample."""
    sel = [
        State_Usedata.State,
        State_Usedata.age1217_89,
        State_Usedata.age1217_1617,
        State_Usedata.age1825_89,
        State_Usedata.age1825_1617,
        State_Usedata.age26_89,
        State_Usedata.age26_1617,
    ]

    results = db.session.query(*sel).filter(State_Usedata.State == State).all()

    # Create a dictionary entry for each row of metadata information
    mjuse_compare = {}
    for result in results:
        mjuse_compare["State"] = result[0]
        mjuse_compare["age1217_89"] = result[1]
        mjuse_compare["age1217_1617"] = result[2]
        mjuse_compare["age1825_89"] = result[3]
        mjuse_compare["age1825_1617"] = result[4]
        mjuse_compare["BBTYPE"] = result[5]
        mjuse_compare["age26_89"] = result[6]
        mjuse_compare["age26_1617"] = result[7]

    print(mjuse_compare)
    return jsonify(mjuse_compare)


@app.route("/arrest_prispop_data/<State>")
def arrest_prispop_data(State):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(State_Arrest).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    state_data = df.loc[df[State] > 0, ["dt_ids", "dt_information", State]]

    # Sort by sample
    state_data.sort_values(by= State, ascending=False, inplace=True)

    # Format the data to send as json
    data = {
        "dt_ids": state_data.dt_id.values.tolist(),
        "state_values": state_data[State].values.tolist(),
        "dt_information": state_data.dt_information.tolist(),
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run()

