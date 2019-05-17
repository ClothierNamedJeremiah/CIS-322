import logging
import flask
from flask import render_template, jsonify

# Our own modules
import config 		# Configure from configuration files or command line

##
## Globals
##
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
# Set key as config
app.config['GOOGLEMAPS_KEY'] = CONFIG.API_KEY

##
## Pages
##
@app.route("/")
def fullmap():
	app.logger.debug("Main page entry")
	return render_template('map.html')

##
## AJAX: Processes Points of Interest
##
@app.route("/_full_map")
def _full_map():
	result = {"markers": []}
	with open("data/points.txt","r") as f:
		line = f.readline().strip()
		while line:
			if line[0] is not "#":
				temp_list = line.strip().split(",")
				# Convert Latitude, Longitude and Rating to floats
				for i in range(1,4):
					temp_list[i] = float(temp_list[i])
				result["markers"].append(temp_list)
			line = f.readline()
	app.logger.debug("RESULT SENT TO CLIENT {}".format(result))
	return jsonify(result=result)


##############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")