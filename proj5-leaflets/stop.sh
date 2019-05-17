#! /bin/bash
#
# Kill all current instances of flask_leaflets on this machine
#
#

# Grep for all running processes containing flask_leaflets in description
# EXCEPT the grep command itself; turn them into 'kill' commands and
# execute the commands with bash
#
ps -x | grep flask_leaflets | grep -v grep | \
    awk '{print "kill " $1}' | bash


