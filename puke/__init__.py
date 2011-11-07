#
# puke - JavaScript Tooling Framework
# Copyright 2010-2011 Sebastian Werner
#

from puke.Error import *
from puke.Task  import *
from puke.Tools  import *
from puke.FileList import *
from puke.Sed import *
from puke.Console import *

VERSION = 0.1

__all__ = ["main", "VERSION"]

import sys, logging, os
from optparse import OptionParser

from colorama import *



def run():
    """ Main routine which should be called on startup """

    #
    # Parse options
    #

    parser = OptionParser()
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", help="don't print status messages to stdout")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="print more detailed status messages to stdout")
    parser.add_option("-l", "--log", dest="logfile", help="Write debug messages to given logfile")
    parser.add_option("-f", "--file", dest="file", help="Use the given build script")

    (options, args) = parser.parse_args()


    #
    # Configure logging
    # 

    if options.logfile:
        logging.basicConfig(filename=options.logfile, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
        logging.getLogger().setLevel(logging.DEBUG)
    elif not logging.root.handlers:
        if options.verbose is True:
            logging.getLogger().setLevel(logging.DEBUG)
        elif options.verbose is False:
            logging.getLogger().setLevel(logging.WARN)
        else:
            logging.getLogger().setLevel(logging.INFO)
    
    # Define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()

    if options.verbose is True:
        console.setLevel(logging.DEBUG)
    elif options.verbose is False:
        console.setLevel(logging.WARN)
    else:
        console.setLevel(logging.INFO)
        
    console.setFormatter(logging.Formatter( ' %(message)s' + Style.RESET_ALL, '%H:%M:%S'))
    logging.getLogger().addHandler(console)


    #
    # Find and execute build script
    #
    
    pukefiles = ["pukefile", "pukeFile", "pukefile", "pukefile.py", "pukeFile.py", "pukefile.py"]
    
    script = None
    if options.file:
        if os.path.isfile(options.file):
            script = options.file
    else:
        for name in pukefiles:
            if os.path.isfile(name):
                script = name

    if script is None:
        if options.file:
            raise PukeError("No generate file '%s' found!" % options.file)
        else:
            raise PukeError("No generate file found!")

    retval = execfile(script)

    #
    # Execute tasks
    #
    
    if not args:
        logging.error("No tasks to execute. Please choose from: ")
        printTasks()
        sys.exit(1)

    for name in args:
        if not os.path.basename(name) in pukefiles:
            executeTask(name)
        
        

def main():
    try:
        run()

    except Exception as error:
        sys.stderr.write("!!! %s\n" % error)
        raise error
        sys.exit(1)
        
    except KeyboardInterrupt:
        sys.stderr.write("Build interrupted!\n")
        sys.exit(2)
        
    sys.exit(0)