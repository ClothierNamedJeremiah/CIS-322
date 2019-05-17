"""
Spew the contents of a file to standard output. 
Similar to Unix command 'cat' or Windows command 'type'
for a single file.  

The file given on the command line is interpreted relative to 
a path that may be specified on the command line as -D path 
or in the configuration file as DOCROOT.
"""

import config
import os
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.DEBUG)

log = logging.getLogger(__name__)
DOCROOT = "."   # Overridden by configuration

def spew(file_name):
    """Spew contents of 'source' to standard output. 
    Source should be a file or file-like object.
    """
    source_path = os.path.join(DOCROOT, file_name)
    log.debug("Source path: {}".format(source_path))
    try: 
        with open(source_path, 'r', encoding='utf-8') as source:
            for line in source:
                print(line.strip())
    except OSError as error:
        log.warn("Failed to open or read file")
        log.warn("Requested file was {}".format(source_path))
        log.warn("Exception: {}".format(error))

def main():
    global DOCROOT
    options = config.configuration()
    assert options.DOCROOT, "Document root must be specified in " \
      + "configuration file credentials.ini or on command line"
    DOCROOT = options.DOCROOT
    assert options.input, "You must specify an input file on the command line"
    infile = options.input
    spew(infile)

if __name__ == "__main__":
    main()

