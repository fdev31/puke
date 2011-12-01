import os, time
import shutil
from puke.Console import *

def makedir(dirname):
    """ Creates missing hierarchy levels for given directory """
    
    if dirname == "":
        return
    
    if exists(dirname) and isfile(dirname):
        raise FileSystemError("%s is a file. Cannot create a directory" % dirname)
        
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except Exception as e:
            raise FileSystemError("Error creating %s : %s" % (dirname, e) )

def readfile(file):
    data = None
    try:
        fh = open(file)
        data = fh.read()
        fh.close()
    except Exception as e:
        raise FileSystemError(e)
    finally:
        if fh:
            fh.close()


    return data

def remove(file):

    if not file or file in ['./', '/', '~/', '~', '.', '..', '../']:
        raise FileSystemError('Invalid path %s' % file)
    
    try:
        if os.path.isfile(file):
            os.remove(file)
        else:
            shutil.rmtree(file)
    except Exception as e:
        raise FileSystemError( "Error removing %s : %s" % (file , e))
    

def copyfile(src, dst, force = False):
    """ Copy src file to dst file. Both should be filenames, not directories. """
    
    if not os.path.isfile(src):
        raise FileSystemError("No such file: %s" % src)
    

    try:
        dst_mtime = os.path.getmtime(dst)
        src_mtime = os.path.getmtime(src)
        
        # Only accecpt equal modification time as equal as copyfile()
        # syncs over the mtime from the source.
        if force and src_mtime == dst_mtime:
            return False
        
    except OSError:
        # destination file does not exist, so mtime check fails
        pass

    # First test for existance of destination directory
    makedir(os.path.dirname(dst))
    
    # Finally copy file to directory
    try:
        shutil.copy2(src, dst)
    except IOError as ex:
        raise FileSystemError("Could not write file %s: %s" % (dst, ex))
        
    return True
    
def exists(src):
    if not os.path.exists(src):
        return False

    return True
    
def isfile(src):
    if not exists(src):
        raise FileSystemError('isfile error : %s not found' % src)

    if not os.path.isfile(src):
        return False

    return True

def isdir(dirname):
    if not exists(dirname):
        raise FileSystemError('isdir error : %s not found' % dirname)

    if not os.path.isdir(dirname):
        return False

    return True


def writefile(dst, content, mtime = None):
    # First test for existance of destination directory
    makedir(os.path.dirname(dst))
    
    # Open file handle and write
    try:
        handle = open(dst, mode="w")
        handle.write(content)
        handle.close()
    except Exception as e:
        raise FileSystemError("Error writing file %s : %s" % (dst, e))

    if mtime:
        os.utime(dst, (time.time(), mtime))

def join(*args):
    return os.path.join(*args)

def abspath(path):
    return os.path.abspath(path)



class FileSystemError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)