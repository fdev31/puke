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
from puke.FileSystem import *
from puke.Env import *
from puke.Cache import *
from puke.Require import *
from puke.Yak import *

VERSION = 0.1

__all__ = ["main", "VERSION"]

import sys, logging, os, traceback
from optparse import OptionParser

from colorama import *



def run():
    """ Main routine which should be called on startup """

    #
    # Parse options
    #

    parser = OptionParser()
    parser.add_option("-c", "--clear", action="store_true", dest="clearcache", help="Spring time, clean all the vomit")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", help="don't print status messages to stdout")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="print more detailed status messages to stdout")
    parser.add_option("-t", "--tasks",action="store_true",  dest="list_tasks", help="list tasks")
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
    consoleCfg = logging.StreamHandler()

    if options.verbose is True:
        consoleCfg.setLevel(logging.DEBUG)
    elif options.verbose is False:
        consoleCfg.setLevel(logging.WARN)
    else:
        consoleCfg.setLevel(logging.INFO)
    
    if os.environ.get("NOCOLOR"):
        consoleCfg.setFormatter(logging.Formatter( ' %(message)s' , '%H:%M:%S'))
    else:
        consoleCfg.setFormatter(logging.Formatter( ' %(message)s' + Style.RESET_ALL, '%H:%M:%S'))

    logging.getLogger().addHandler(consoleCfg)

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


    if options.list_tasks:
        logging.error("No tasks to execute. Please choose from: ")
        printTasks()
        sys.exit(1)

    
    if options.clearcache:
        console.header("Spring time, cleaning all the vomit around ...")
        console.log("...")
        if Cache.clean():
            console.confirm("You're good to go !\n")
        else:
            console.confirm("Your room is already tidy, good boy :-) \n")
        sys.exit(1)
    
    try:
        args = args.strip()
    except:
        pass

    if not args:
        if hasDefault():
            executeTask('default')
        else:
            logging.error("No tasks to execute. Please choose from: ")
            printTasks()
            sys.exit(1)

    for name in args:
        if not os.path.basename(name) in pukefiles:
            executeTask(name.strip())
        
def gettraceback():
    trace = ""
    exception = ""
    exc_list = traceback.format_exception_only (sys.exc_type, sys.exc_value)
    for entry in exc_list:
        exception += entry
    tb_list = traceback.format_tb(sys.exc_info()[2])
    for entry in tb_list[-1]:
        trace += entry  
    return trace  

def main():
    try:
        run()
    
    except Exception as error:

        console.fail("\n\n :puke: \n PUKE %s \n %s \n" % (error, gettraceback()))

        sys.exit(1)
        
    except KeyboardInterrupt:
        console.warn("\n\n :puke: \nBuild interrupted!\n")
        sys.exit(2)
        
    sys.exit(0)