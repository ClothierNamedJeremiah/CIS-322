#! /bin/bash
#
# Kill all current instances of flask_brevets on this machine
#
#

# Grep for all running processes containing flask_brevets in description
# EXCEPT the grep command itself; turn them into 'kill' commands and
# execute the commands with bash
#
ps -x | grep flask_brevets | grep -v grep | \
    awk '{print "kill " $1}' | bash


