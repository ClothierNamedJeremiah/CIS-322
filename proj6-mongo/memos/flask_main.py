"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates:
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will
   - User input/output is in local (to the server) time.
"""

import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

import sys

# Date handling
import arrow
from dateutil import tz  # For interpreting local times

# Mongo database
import pymongo
from pymongo import MongoClient

import config
CONFIG = config.configuration()

import update_db


MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
    CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST,
    CONFIG.DB_PORT,
    CONFIG.DB)


print("Using URL '{}'".format(MONGO_CLIENT_URL))


###
# Globals
###

app = flask.Flask(__name__)
app.secret_key = CONFIG.SECRET_KEY

####
# Database connection per server process
###

try:
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, CONFIG.DB)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)


###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    g.memos = update_db.list_memos(collection)
    for memo in g.memos:
        app.logger.debug("Memo: " + str(memo))
    return flask.render_template('index.html',request=request)

@app.route("/create", methods=['POST','GET'])
def create():
    app.logger.debug("Create")
    if request.method == 'POST':
      date = request.form['memo_date']
      text = request.form['memo_text']
      update_db.add_to_db(collection,date,text)
      return flask.redirect(url_for('create')) # display the new memos

    return flask.render_template('create.html',request=request)

@app.route("/delete",methods=['POST'])
def delete():
  update_db.delete_from_db(collection,request)
  return flask.redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################


@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
    """
    Date is internal UTC ISO format string.
    Output: "today", "yesterday", "in 5 days", etc.
    """
    return update_db.humanize_date(date)

if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")
