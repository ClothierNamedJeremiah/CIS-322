The 'tests' directory is where we keep a few 
automated tests for the page server. 

These tests use 'curl', a Unix utility for fetching data from 
a server.  It's like requesting a URL with a browser, but without
the browser.  This allows us to run more tests, more quickly, 
and ore often than we could by hand.  You should also do a 
little bit of manual testing using a browser, just to be sure 
there isn't some bug that affects interactive use but is not
triggered by these test scripts. 

To test:  You will need to be running your server in 
one window, and running these tests in another window 
(ideally on a different machine).  
