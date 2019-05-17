#Spew 

This is a tiny application that demonstrates a few things: 

- Using config.py to combine a command-line argument with an argument supplied in the configuration file app.ini.  Try 

~~~~
python3 spew.py -R .. README.md
python3 spew.py trivia.css   # should look in ../pages
python3 spew.py README.md    # should fail
python3 spew.py              # should describe usage
python3 spew.py -h           # Usage in more detail
~~~~
- Creating a file search path with os.path.join

- Using a *with* block to open a file and make sure it is closed whether the block is exited normally or with an exception

- Catching OSError in case opening a file fails

##Why?
This is pointless as an application.  The Unix command `cat` or the Windows command `type` provide a superset of the functionality of spew, aside from the configurable search path.  The only purpose of this program is to provide you some example code to copy or learn from. 

This is based on code I wrote in my sample solution to the simple web server project.  It is intended to help you get through the project a little quicker.  While we may refine the handling of configuration files in future projects, we will be doing something like this (combining potentially multiple configuration files together with command line arguments) 

###License
Licensed under the *why bother* open source license:  Sure, do whatever you want.  