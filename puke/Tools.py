import os, os.path, shutil, logging, sys, filecmp, stat
from puke.FileList import *
from scss import Scss

CSS_COMPRESSOR = sys.argv[0] + '.css.compress'
JS_COMPRESSOR = sys.argv[0] + '.js.compress'


def combine(in_files, out_file, verbose=False):
    
    if isinstance(in_files, FileList):
        in_files = in_files.get()
    elif isinstance(in_files, str):
        in_files = [in_files]
         
    builddir = os.path.dirname(out_file)

    makedir(builddir)

    temp_file = os.path.join(builddir, '.temp')

    logging.info( "- Combining files :")

    temp = open(temp_file, 'w')
    for f in in_files:
        infos = ""

        fh = open(f)
        data = fh.read() + '\n'
        fh.close()

        if __get_ext(f) == 'scss':
            data = __parse_scss(data)
            infos = "SCSS OK"

        temp.write(data)

        if infos:
            infos = "(%s)" % infos

        logging.info('  + %s %s' % (f, infos))

    temp.close()
    logging.info( "  Generating %s" % out_file)
    copyfile(temp_file, out_file)
    os.remove(temp_file)

def minify(in_file, out_file = None, verbose=False):

    if not isinstance(in_file, str):
        raise Exception("Minify : single file only")

    if not out_file:
        out_file = in_file
    
    in_type = __get_ext(out_file)

    org_size = os.path.getsize(in_file)

    logging.info('- Minifying %s (%.2f kB)' % (in_file, org_size / 1024.0))

    if in_type == 'js':
        __minify_js(in_file, out_file + '.tmp', verbose)
    else:
        __minify_css(in_file, out_file + '.tmp', verbose)
    
    copyfile(out_file + '.tmp', out_file)
    os.remove(out_file + '.tmp')

    new_size = os.path.getsize(out_file)

    
    logging.info('  Original: %.2f kB' % (org_size / 1024.0))
    logging.info('  Compressed: %.2f kB' % (new_size / 1024.0))
    logging.info('  Reduction: %.1f%%' % (float(org_size - new_size) / org_size * 100))
    logging.info('=> %s' % out_file)

def jslint(files):
    if isinstance(files, FileList):
        files = files.get()
    elif isinstance(files, str):
        files = [files]

    sh("gjslint " + ' '.join(files))

def sh (command):
    os.system(command)

def __minify_js(in_file, out_file, verbose):
    options = ['--js %s' % in_file,
               '--js_output_file %s' % out_file,
               '--warning_level QUIET']

    os.system('java -jar "%s" %s' % (JS_COMPRESSOR,
                                          ' '.join(options)))

def __minify_css(in_file, out_file, verbose):
    options = ['-o "%s"' % out_file,
               '--type css']

    if verbose:
        options.append('-v')

    os.system('java -jar "%s" %s %s' % (CSS_COMPRESSOR,
                                          ' '.join(options), in_file))

def __get_ext(filename):
    return filename.split('.')[-1]


def __parse_scss(payload):
    css = Scss()
    return css.compile(payload)


def makedir(dirname):
    """ Creates missing hierarchy levels for given directory """
    
    if dirname == "":
        return
        
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    
def copyfile(src, dst):
    """ Copy src file to dst file. Both should be filenames, not directories. """
    
    if not os.path.isfile(src):
        raise Exception("No such file: %s" % src)

    # First test for existance of destination directory
    makedir(os.path.dirname(dst))
    
    # Finally copy file to directory
    try:
        shutil.copy2(src, dst)
    except IOError as ex:
        logging.error("Could not write file %s: %s" % (dst, ex))
        
    return True
    
    
def updatefile(src, dst):
    """ Same as copyfile() but only do copying when source file is newer than target file """
    
    if not os.path.isfile(src):
        raise Exception("No such file: %s" % src)
    
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


def writefile(dst, content):
    # First test for existance of destination directory
    makedir(os.path.dirname(dst))
    
    # Open file handle and write
    handle = open(dst, mode="w", encoding="utf-8")
    handle.write(content)
    handle.close()