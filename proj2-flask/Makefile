#
# Second app: Flask project Creates a date-sensitive course schedule
# (syllabus) that highlights the current week
# 

SHELL = /bin/bash
SRC = syllabus
SOURCES = $(SRC)/flask_syllabus.py $(SRC)/pre.py $(SRC)/credentials.ini


$(SRC)/credentials.ini:
	echo "You must create credentials.ini and save it in $(SRC)"

##
##  Virtual environment
##     
install:	env  $(SRC)/credentials.ini

env:
	python3 -m venv  env
	(source env/bin/activate; pip install -r requirements.txt)


##
## Preserve virtual environment
##
dist:
	pip freeze >requirements.txt

# 'make run' runs Flask's built-in test server, 
#  which may be configured with built-in debugging.
#  Runs in foreground; kill with control-C. 
# 
run:	$(SOURCES) env
	(source env/bin/activate; cd syllabus; \
	python3 flask_syllabus.py ) || true

## 
## Run as background service, under gunicorn
##'

# 'make start' starts the service in the background
#  and saves the process ID in file SERVICE_PID so that
#  it can be stopped. 'make stop' stops that service.
#  FIXME: I need control of ports 
# 
start:	env
	bash start.sh

stop:	SERVICE_PID
	bash stop.sh




# 'clean' and 'veryclean' are typically used before checking 
# things into git.  'clean' should leave the project ready to 
# run, while 'veryclean' may leave project in a state that 
# requires re-running installation and configuration steps
# 
clean:
	rm -f *.pyc */*.pyc
	rm -rf __pycache__

veryclean:
	make clean
	rm -rf env



