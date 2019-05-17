"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    distance = request.args.get('distance',type=str)
    begin_date = request.args.get('begin_date',type=str)
    begin_time = request.args.get('begin_time',type=str)

    # app.logger.debug("km={}%n".format(km))
    # app.logger.debug("distance={}%n".format(distance))
    # app.logger.debug("begin_date={}%n".format(begin_date))
    # app.logger.debug("begin_time={}%n".format(begin_time))
    # app.logger.debug("request.args: {}%n".format(request.args))

    begin_time_formatted = arrow.get(begin_date + " " +begin_time,"YYYY-MM-DD HH:mm")
    begin_time_formatted = begin_time_formatted.replace(tzinfo='utc').isoformat()
    # app.logger.debug("Formatted Time: {}".format(begin_time_formatted))
    open_time = acp_times.open_time(int(km),int(distance),begin_time_formatted)
    close_time = acp_times.close_time(int(km),int(distance),begin_time_formatted)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
