from flask import Blueprint, request, jsonify, abort
from flaskapi_project.analytics import ShopDataAnalytics
from flaskapi_project.api_def import get_data_by_date
import json
from http import HTTPStatus
import logging, logging.config, yaml
import pathlib

filepath = pathlib.Path(__file__).parent.resolve()

# defining log files for errors and info
logging.config.dictConfig(yaml.load(open(filepath+'logging.conf')))
errorfile = logging.getLogger('logfile1')
infofile = logging.getLogger('logfile2')


# defining custom error codes
ERROR_CODE_404 = {'Error': 'Invalid URL, Correct format is /?date=YYYY-MM-DD'}
ERROR_CODE_400 = {'Error': 'Missing date parameter in the URL, please use /?date=YYYY-MM-DD'}
ERROR_CODE_500 = {'Error': 'Something went wrong in the API, please contact support at adityahshahit@gmail.com'}


apiBluePrint = Blueprint('flaskapi_blueprint', __name__)


# defining the root end point
@apiBluePrint.route("/")
def event():
    """
    The root Endpoint which accepts a date argument and returns the shop data analytics for that date.
    If the parameter is missing or if there is no data for the given date, it raises the appropriate errors
    :param: date
    """

    date = request.args.get('date', default=None)
    if date:
        try:
            result = get_data_by_date(date)
            # using json.dumps to format the response with an indent(new line for every key) to make it more readable)
            from flaskapi_project.flaskapi import app
            infofile.info(request.url)
            infofile.info(result)
            return app.response_class(
                json.dumps(result, indent=2, sort_keys=False),
                mimetype=app.config['JSONIFY_MIMETYPE'])
        except Exception as e:
            errorfile.debug(e, extra={'stack': True})
            abort(HTTPStatus.INTERNAL_SERVER_ERROR.value)
    else:
        abort(HTTPStatus.BAD_REQUEST.value)


# error handler for HTTP 404, Invalid URL
# NOTE: use app_errorhandler method to handle 404
@apiBluePrint.app_errorhandler(HTTPStatus.NOT_FOUND.value)
def not_found(e):
    """
    A Custom error handler, to educate the user if an invalid url is provided.
    """

    errorfile.debug(request.url)
    errorfile.debug(ERROR_CODE_404)
    resp = jsonify(ERROR_CODE_404)
    return resp, HTTPStatus.NOT_FOUND.value


# error handler for HTTP 400, bad request if the date parameter is missing
@apiBluePrint.errorhandler(HTTPStatus.BAD_REQUEST.value)
def not_found(e):
    """
    A Custom error handler to educate the user to pass date as an argument
    """

    errorfile.debug(request.url)
    errorfile.debug(ERROR_CODE_400)
    resp = jsonify(ERROR_CODE_400)
    return resp, HTTPStatus.BAD_REQUEST.value

# error handler for HTTP 500, API Failure
@apiBluePrint.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR.value)
def not_found(e):
    """
    A Custom error handler if somethings goes wrong in the API code.
    """
    errorfile.debug(request.url)
    errorfile.debug(ERROR_CODE_500)
    resp = jsonify(ERROR_CODE_500)
    return resp, HTTPStatus.INTERNAL_SERVER_ERROR.value
