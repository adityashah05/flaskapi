# flaskapi
Flask API for shop data analysis

Usage
-----

Clone the repo:

    git clone https://github.com/adityashah05/flaskapi
    cd flaskapi

Create virtualenv:
    python3 -m virtualenv venv
    
    If virtual env not found (don't run if the top command is successful) : 
        python3 -m pip install --user --upgrade pip
        python3 -m pip --version
        python3 -m pip install --user virtualenv
    
    source venv/bin/activate
    pip install -r requirements.txt
    python setup.py install

Run the sample server

    python server.py

Try the endpoints:

 http://localhost:5000/date?=2019-08-01


License
-------

MIT, see LICENSE file
