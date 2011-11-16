import os, time
import shutil
from puke.Console import *

def makedir(dirname):
    """ Creates missing hierarchy levels for given directory """
    
    if dirname == "":
        return
        
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def readfile(file):
    fh = open(file)
    data = fh.read()
    fh.close()

    return data

def rm(file):
    shutil.rmtree(file)

def copyfile(src, dst):
    """ Copy src file to dst file. Both should be filenames, not directories. """
    
    if not os.path.isfile(src):
        console.error("No such file: %s" % src)
        return False

    # First test for existance of destination directory
    makedir(os.path.dirname(dst))
    
    # Finally copy file to directory
    try:
        shutil.copy2(src, dst)
    except IOError as ex:
        console.error("Could not write file %s: %s" % (dst, ex))
        
    return True
    
    
def updatefile(src, dst):
    """ Same as copyfile() but only do copying when source file is newer than target file """
    
    if not os.path.isfile(src):
        console.error("No such file: %s" % src)
        return False
    
    try:
        dst_mtime = os.path.getmtime(dst)
        src_mtime = os.path.getmtime(src)
        
        # Only accecpt equal modification time as equal as copyfile()
        # syncs over the mtime from the source.
        if src_mtime == dst_mtime:
            return False
        
    except OSError:
        # destination file does not exist, so mtime check fails
        pass
        
    return copyfile(src, dst)

def fileexists(src):
    if not os.path.isfile(src):
        return False

    return True

def writefile(dst, content, mtime = None):
    # First test for existance of destination directory
    makedir(os.path.dirname(dst))
    
    # Open file handle and write
    handle = open(dst, mode="w")
    handle.write(content)
    handle.close()

    if mtime:
        os.utime(dst, (time.time(), mtime))