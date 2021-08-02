"""
This module starts the flask server
"""

from flaskapi_project.flaskapi import app

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
