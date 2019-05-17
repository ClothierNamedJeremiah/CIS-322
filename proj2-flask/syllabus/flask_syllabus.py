"""
Very simple Flask web site, with one page
displaying a course schedule.  We pre-process the
input file to set correct dates and highlight the
current week (if the academic term is in session).

"""


import flask
import logging
import arrow      # Replacement for datetime, based on moment.js

# Our own modules
import pre        # Preprocess schedule file
import config     # Configure from configuration files or command line


###
# Globals
###
app = flask.Flask(__name__)
if __name__ == "__main__":
    configuration = config.configuration()
else:
    # If we aren't main, the command line doesn't belong to us
    configuration = config.configuration(proxied=True)

if configuration.DEBUG:
    app.logger.setLevel(logging.DEBUG)

# Pre-processed schedule is global, so be careful to update
# it atomically in the view functions.
#
schedule = pre.process(open(configuration.SYLLABUS))


###
# Pages
# Each of these transmits the default "200/OK" header
# followed by html from the template.
###

@app.route("/")
@app.route("/index")
def index():
    """Main application page; most users see only this"""
    app.logger.debug("Main page entry")
    flask.g.schedule = schedule  # To be accessible in Jinja2 on page
    return flask.render_template('syllabus.html')


@app.route("/refresh")
def refresh():
    """Admin user (or debugger) can use this to reload the schedule."""
    app.logger.debug("Refreshing schedule")
    global schedule
    schedule = pre.process(open(configuration.SYLLABUS))
    return flask.redirect(flask.url_for("index"))

### Error pages ###
#   Each of these transmits an error code in the transmission
#   header along with the appropriate page html in the
#   transmission body


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.g.linkback = flask.url_for("index")
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def i_am_busted(error):
    app.logger.debug("500: Server error")
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def no_you_cant(error):
    app.logger.debug("403: Forbidden")
    return flask.render_template('403.html'), 403


#################
#
# Functions used within the templates
#
#################

@app.template_filter('fmtdate')
def format_arrow_date(date):
    try:
        normal = arrow.get(date)
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"


#
# If run as main program (not under gunicorn), we
# turn on debugging.  Connects to anything (0.0.0.0)
# so that we can test remote connections.
#
if __name__ == "__main__":
    app.run(port=configuration.PORT, host="0.0.0.0")
