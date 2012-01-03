#!/usr/bin/env python
# -*- coding: utf8 -*-

import platform

if platform.system() == 'Windows':
    from compat import *

from puke.Error import *
from puke.Task  import *
from puke.Tools  import *
from puke.ToolsExec  import *
from puke.FileList import *
from puke.Sed import *
from puke.Console import *
from puke.Env import *
from puke.Cache import *
from puke.Require import *
from puke.Yak import *
from puke.VirtualEnv import *
from puke.Std import *
import puke.System
import puke.FileSystem
import puke.Utils


VERSION = 0.1
__all__ = [
            "main", "VERSION", "Error", "FileList", "Sed", "Std", "Env", "Require", "Yak", "VirtualEnv", "System", "FileSystem", "Utils",
            "combine", "sh", "minify", "jslint", "jsdoc", "patch", "prompt", "deepcopy", "stats", "pack", "unpack", "hsizeof", "console"
         ]


import sys, logging, os, traceback
import pkg_resources
from optparse import OptionParser

from colorama import *



try:
    sys.path.insert(1, os.getcwd())
except:
    pass

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
    parser.add_option("-p", "--patch",action="store_true",  dest="patch", help="Patch closure")
    parser.add_option("-i", "--info",action="store_true",  dest="info", help="puke task --info show task informations")

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



     #Patch closure

    try:
        closure = pkg_resources.get_distribution('closure_linter').location
        closure_lock = os.path.join(closure, 'closure_linter', 'puke.lock')
        
        if options.patch or not os.path.isfile(closure_lock):
            closure = os.path.join(closure, 'closure_linter', 'ecmalintrules.py')
            
            try:
                handle = source = destination = None
                import shutil
                shutil.move( closure, closure+"~" )
                destination= open( closure, "w" )
                source= open( closure+"~", "r" )
                
                content = source.read()
                content = content.replace('MAX_LINE_LENGTH = 80', 'MAX_LINE_LENGTH = 120')
                destination.write(content)

                source.close()
                destination.close()

                os.remove(closure+"~" )


                handle = file(closure_lock, 'a')
                handle.close

                if options.patch:
                    console.confirm('Patch successful')
                    sys.exit(0)
            except Exception as e:
                console.warn(">>> you should consider running \"sudo puke --patch\"")
                if handle:
                    handle.close()
                if source:
                    source.close()
                if destination:
                    destination.close()
                
                if options.patch:
                    sys.exit(0)


    except Exception as e:
        console.error('Closure linter not found %s' % e)


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
        console.confirm("Please choose from: ")
        printTasks()
        sys.exit(0)

   

    
    if options.clearcache:
        console.header("Spring time, cleaning all the vomit around ...")
        console.log("...")
        if Cache.clean():
            console.confirm("You're good to go !\n")
        else:
            console.confirm("Your room is already tidy, good boy :-) \n")
        sys.exit(0)
    
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

    else:
        name = args.pop(0)

        if options.info:
            printHelp(name.strip())
        else:
            executeTask(name.strip(), *args)
                


def gettraceback(level = 0):
    trace = ""
    exception = ""
    exc_list = traceback.format_exception_only (sys.exc_type, sys.exc_value)

    reverse = -1 - level
    for entry in exc_list:
        exception += entry
    tb_list = traceback.format_tb(sys.exc_info()[2])
    for entry in tb_list[reverse]:
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