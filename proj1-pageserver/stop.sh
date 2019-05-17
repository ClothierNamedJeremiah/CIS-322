#! /bin/bash
# 
# Stop server started with start.sh
# (Run from same directory as start.sh so that 
#  path to ,pid is the same)
#
pid=`cat ,pypid`
kill ${pid}
echo "${pid} should be dead now"
