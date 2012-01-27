#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, time, pwd, grp
import shutil, hashlib
from puke.Console import *
import Utils

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
    fh = None
    try:
        fh = open(file)
        data = fh.read()
        fh.close()
    except Exception as e:
        raise FileSystemError("%s : %s" % (e, file))
    finally:
        if fh:
            fh.close()


    return data

def checksum (file):
    block_size=2**20
    md5 = hashlib.md5()
    data = None
    fh = None
    try:
        fh = open(file, 'rb')
        while True:
            data = fh.read(block_size)
            if not data:
                break
            md5.update(data)

        fh.close()
    except Exception as e:
        raise FileSystemError(e)
    finally:
        if fh:
            fh.close()
    
    
    return md5.hexdigest()

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
        if force and src_mtime <= dst_mtime:
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


def writefile(dst, content, mtime = None, binary = False):
    # First test for existance of destination directory
    makedir(os.path.dirname(dst))
    
    # Open file handle and write
    if binary:
        mode = "wb"
    else:
        mode = "w"
    try:
        handle = open(dst, mode=mode)
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

def basename(path):
    return os.path.basename(path)

def dirname(path):
    return os.path.dirname(path)

def normpath(path):
    return os.path.normpath(path)

def sep():
    return os.sep

def chown(path, uname = None, gname = None):
    isfile(path)

    if not uname:
        uid = os.stat(path).st_uid

    if not gname:
        gid = os.stat(path).st_gid

    if not isinstance(uname, int) and uname != None:
        uid = getUid(uname)
    
    if not isinstance(gname, int) and gname != None:
        gid = getGid(gname)

    
    if uid == None or gid == None:
        raise FileSystemError('CHOWN %s : Invalid uname or gname (%s->%s:%s->%s)' % (path, uname, uid, gname, gid))

    return os.chown(path, uid, gid)

def chmod(path, mode):
    isfile(path)


    if not isinstance(mode, int):
        mode = Utils.octalmode(path, mode)
    else:
        mode = int("%s" % mode, 8)
    
    return os.chmod(path, mode)

def getUid(name):
    try:
        return pwd.getpwnam(name)[2]
    except:
        return None

def getGid(name):
    try:
        return grp.getgrnam(name)[2]
    except:
        return None



class FileSystemError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)