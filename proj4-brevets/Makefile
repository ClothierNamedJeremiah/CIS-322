#
# Project 4:  Brevet calculator
#
# Gnu make and bash are required. 
#


# Many recipes need to be run in the virtual environment, 
# so run them as $(INVENV) command
INVENV = . env/bin/activate ;

##
##  Virtual environment
##     
env:
	python3 -m venv env
	($(INVENV) pip install -r requirements.txt )

## Installation
install: env credentials

credentials: brevets/credentials.ini

brevets/credentials.ini: 
	echo "You must manually create credentials.ini"


##
## Start, stop, test
##

start:	env credentials
	bash start.sh

stop: 	env credentials
	bash stop.sh

test:	env
	($(INVENV) cd brevets; nosetests) 


##
## Preserve virtual environment for git repository
## to duplicate it on other targets
##
dist:	env
	$(INVENV) pip freeze >requirements.txt


# 'clean' and 'veryclean' are typically used before checking 
# things into git.  'clean' should leave the project ready to 
# run, while 'veryclean' may leave project in a state that 
# requires re-running installation and configuration steps
# 
clean:
	rm -f *.pyc */*.pyc
	rm -rf __pycache__ */__pycache__

veryclean:
	make clean
	rm -rf env



