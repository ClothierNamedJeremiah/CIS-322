#! /bin/bash
# 
# Test the trivial web server.  
# Usage:  tests.sh http://the.IP.address:port/path
# Example: tests.sh http://127.0.0.1:5000/sample.html
#
URLbase=$1

# Test cases for the body 
# 

function expect_body() {
    # Args
    path=$1
    expect=$2
    curl --silent ${URLbase}/${path} >/tmp/,$$
    if grep -q ${expect} /tmp/,$$ ; then 
	echo "Pass --  found ${expect} in ${path}"
    else
        echo "*** FAIL *** expecting ${expect} in  ${URLbase}/${path}"
    fi
}

function expect_status() {
    # Args
    path=$1
    expect=$2
    curl --silent -i ${URLbase}/${path} >/tmp/,$$
    if grep -q ${expect} /tmp/,$$ ; then 
	echo "Pass --  found ${expect} in ${URLbase}/${path} "
    else
        echo "*** FAIL *** expecting status ${expect} in ${URLbase}/${path} "
    fi
}


expect_body trivia.html  "Seriously"
expect_status nosuch.html "404"
expect_status there/theybe.html 404
expect_status there//theybe.html "403"
expect_status there.xxx "403" 
