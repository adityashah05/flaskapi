"""
This is the test module of the flaskapi.py, the test cases check the following:
1) The API is returning expected data for a valid request
2) The API is returning expected data for a invalid valid request, eg http://localhost:5000/xxxx
3) The API is returning expected data for a date for which there is no data, http://localhost:5000/?date=2021-08-01
Module: flaskapi.py
"""

import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

import unittest
from flaskapi_project.flaskapi import app
import requests
from flask import abort


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_valid_response(self):
        response = requests.get('http://localhost:5000/?date=2019-08-01')
        self.assertEqual(response.json(), {
                                          "customers": 9,
                                          "total_discount_amount": 130429980.26,
                                          "items": 2895,
                                          "order_total_avg": 1182286.1,
                                          "discount_rate_avg": 0.13,
                                          "commissions": {
                                            "promotions": {
                                              "2": 188049.4,
                                              "5": 1153804.8
                                            },
                                            "total": 20833236.94,
                                            "order_average": 2314804.1
                                          }
                                        })

    def test_invalid_response(self):
        response = requests.get('http://localhost:5000/xxxx')
        self.assertEqual(response.json(), {'Error': 'Invalid URL, Correct format is /?date=YYYY-MM-DD'})

    def test_invalid_range_response(self):
        response = requests.get('http://localhost:5000/?date=2021-08-01')
        self.assertEqual(response.json(), {"Error": "No data found for the given date"})


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_flaskapi(self):
        response = self.app.get('/')


if __name__ == "__main__":
    unittest.main()
