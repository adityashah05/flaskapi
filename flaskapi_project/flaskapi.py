"""
This is the main module of the API which creates a flask object and registers the endpoints using blueprint
Unit Test Module: test_flaskapi.py
"""

from flask import Flask
from flaskapi_blueprint import apiBluePrint
import os

app = Flask(__name__)

# to Keep the response order intact
app.config['JSON_SORT_KEYS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eshop_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(apiBluePrint)
