"""
Flask web site with vocabulary matching game
(identify vocabulary words that can be made
from a scrambled string)
"""

import flask
import logging

# Our own modules
from letterbag import LetterBag
from vocab import Vocab
from jumble import jumbled
import config

###
# Globals
###
app = flask.Flask(__name__)

CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY  # Should allow using session variables

#
# One shared 'Vocab' object, read-only after initialization,
# shared by all threads and instances.  Otherwise we would have to
# store it in the browser and transmit it on each request/response cycle,
# or else read it from the file on each request/responce cycle,
# neither of which would be suitable for responding keystroke by keystroke.

WORDS = Vocab(CONFIG.VOCAB)

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    """The main page of the application"""
    flask.g.vocab = WORDS.as_list()
    flask.session["target_count"] = min(
        len(flask.g.vocab), CONFIG.SUCCESS_AT_COUNT)
    flask.session["jumble"] = jumbled(
        flask.g.vocab, flask.session["target_count"])
    flask.session["matches"] = []
    app.logger.debug("Session variables have been set")
    assert flask.session["matches"] == []
    assert flask.session["target_count"] > 0
    app.logger.debug("At least one seems to be set correctly")
    return flask.render_template('vocab.html')


@app.route("/keep_going")
def keep_going():
    """
    After initial use of index, we keep the same scrambled
    word and try to get more matches
    """
    flask.g.vocab = WORDS.as_list()
    return flask.render_template('vocab.html')


@app.route("/success")
def success():
    return flask.render_template('success.html')

#######################
# Form handler.
# CIS 322 note:
#   You'll need to change this to a
#   a JSON request handler
#######################


@app.route("/_check")
def check():
    """
    User has submitted the form with a word ('attempt')
    that should be formed from the jumble and on the
    vocabulary list.  We respond depending on whether
    the word is on the vocab list (therefore correctly spelled),
    made only from the jumble letters, and not a word they
    already found.
    """
    app.logger.debug("Entering check")

    # The data we need, from form and from cookie
    text = flask.request.args.get("text",type = str) # current text in #attempt input field
    letter = flask.request.args.get("letr",type = str) # most recently pressed key
    jumble = flask.session["jumble"].upper() # use .upper() to prevent case sensitive issues
    matches = flask.request.args.get("spelt", type=str).split("\n") # list of spelled words for current game

    # Is it good?
    in_jumble = LetterBag(jumble).contains(letter)
    matched = WORDS.has(text)

    rslt = {
    "have_letter": in_jumble, 
    "valid_word":  matched and in_jumble and not (text in matches),
    "is_playing": len(matches)-1 < CONFIG.SUCCESS_AT_COUNT,
    "msg" : ""
    }

    # Respond appropriately
    if rslt["valid_word"]:
        # Cool, they found a new word
        matches.append(text)
        flask.session["matches"] = matches
        if (len(matches)-1 == CONFIG.SUCCESS_AT_COUNT):
            # Game Over
            rslt["is_playing"] = False
        else:
            rslt["is_playing"] = True
            rslt["msg"] = "Only {} words remaining".format(CONFIG.SUCCESS_AT_COUNT - len(matches)+1)
    elif text in matches:
        # they've already found this word
        rslt["msg"] = "You already found {}".format(text)
    elif not matched:
        # the word they've entered doesn't exist
        rslt["msg"] = "{} isn't in the list of words".format(text)
    elif not in_jumble:
        # The word they've spelled cannot be made
        rslt["msg"] = '"{}"can\'t be made from the letters {}'.format(text, jumble)

    return flask.jsonify(result=rslt)

###############
# AJAX request handlers
#   These return JSON, rather than rendering pages.
###############


@app.route("/_example")
def example():
    """
    Example ajax request handler
    """
    app.logger.debug("Got a JSON request")
    rslt = {"key": "value"}
    return flask.jsonify(result=rslt)


#################
# Functions used within the templates
#################

@app.template_filter('filt')
def format_filt(something):
    """
    Example of a filter that can be used within
    the Jinja2 code
    """
    return "Not what you asked for"

###################
#   Error handlers
###################


@app.errorhandler(404)
def error_404(e):
    app.logger.warning("++ 404 error: {}".format(e))
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    app.logger.warning("++ 500 error: {}".format(e))
    assert not True  # I want to invoke the debugger
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def error_403(e):
    app.logger.warning("++ 403 error: {}".format(e))
    return flask.render_template('403.html'), 403


####

if __name__ == "__main__":
    if CONFIG.DEBUG:
        app.debug = True
        app.logger.setLevel(logging.DEBUG)
        app.logger.info(
            "Opening for global access on port {}".format(CONFIG.PORT))
        app.run(port=CONFIG.PORT, host="0.0.0.0")
