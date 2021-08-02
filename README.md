# flaskapi
Flask API for shop data analysis

Usage
-----

Clone the repo:

    git clone https://github.com/adityashah05/flaskapi.git
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

 http://localhost:5000/?date=2019-08-01

How to run the test cases

    1) make sure the flask server is running
    2) open a new terminal window
    3) go to the project directory
    3) activate the virtula env like we did before
        source venv/bin/activate
    4) go to the test folder 
        cd test
    5) run the test file
        python test_flaskapi.py
    
License
-------

MIT, see LICENSE file
