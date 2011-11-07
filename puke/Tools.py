import os, os.path, shutil, logging, sys, filecmp, stat, re
from puke.FileList import *
from puke.Console import *
from scss import Scss

CSS_COMPRESSOR = sys.argv[0] + '.css.compress'
JS_COMPRESSOR = sys.argv[0] + '.js.compress'


def combine(in_files, out_file, verbose=False, replace = None):

    if isinstance(in_files, FileList):
        in_files = in_files.get()
    elif isinstance(in_files, str):
        in_files = [in_files]
         
    builddir = os.path.dirname(out_file)

    makedir(builddir)

    temp_file = os.path.join(builddir, '.temp')

    console.header( "- Combining files :")

    temp = open(temp_file, 'w')
    for f in in_files:
        infos = ""

        fh = open(f)
        data = fh.read() + '\n'

        if replace:
            for k in replace.keys():
                data = data.replace(k, replace.get(k))

        fh.close()

        if __get_ext(f) == 'scss':
            data = __parse_scss(data)
            infos = "SCSS OK"

        temp.write(data)

        if infos:
            infos = "(%s)" % infos

        console.info('  + %s %s' % (f, infos))

    temp.close()
    console.confirm( "  Generating %s" % out_file)
    copyfile(temp_file, out_file)
    os.remove(temp_file)

def minify(in_file, out_file = None, verbose=False):

    if not isinstance(in_file, str):
        raise Exception("Minify : single file only")

    if not out_file:
        out_file = in_file
    
    in_type = __get_ext(out_file)

    org_size = os.path.getsize(in_file)

    console.header('- Minifying %s (%.2f kB)' % (in_file, org_size / 1024.0))

    if in_type == 'js':
        __minify_js(in_file, out_file + '.tmp', verbose)
    else:
        __minify_css(in_file, out_file + '.tmp', verbose)
    
    copyfile(out_file + '.tmp', out_file)
    os.remove(out_file + '.tmp')

    new_size = os.path.getsize(out_file)

    
    console.info('  ~ Original: %.2f kB' % (org_size / 1024.0))
    console.info('  ~ Compressed: %.2f kB' % (new_size / 1024.0))
    console.confirm('  %s ( Reduction : %.1f%% )' % (out_file, (float(org_size - new_size) / org_size * 100)))


def jslint(files, fix = False, strict = False, nojsdoc = False, relax = False):
    if isinstance(files, FileList):
        files = files.get()
    elif isinstance(files, str):
        files = [files]

    options = []
    command = ""

    if strict == True:
        options.append('--strict')
    
    if nojsdoc == True:
        options.append('--nojsdoc')
    
    


    if fix == True:
        command = "fixjsstyle %s %s "  % (  ' '.join(options) , ' '.join(files))
    else:
        command = "gjslint %s %s "  % (  ' '.join(options) , ' '.join(files))
    
    if relax == True:
        command += ' | grep -v "Line too long" | grep -v "Invalid JsDoc tag"'
    
    sh(command)

def jsdoc(files, folder):
    if isinstance(files, FileList):
        files = files.get()
    elif isinstance(files, str):
        files = [files]

    jsdoc =  os.path.join(__get_datas_path(), 'jsdoc-toolkit')
    output = sh("java -jar %s/jsrun.jar %s/app/run.js -d=%s -t=%s/templates/puke -a  %s" % (jsdoc, jsdoc, folder, jsdoc, ' '.join(files)), header = "Generating js doc", output = False)

    if output:
        console.fail(output)
    
    console.confirm('  Doc generated in "%s"' % folder)

def sh (command, header = None, output = True):
    if not header:
        header = 'exec "%s" ' % command
    else:
        console.debug(command)

    console.header(' - '+header)
    
    result = ""
    p = os.popen(command)
    for line in p.readlines():

        result += line + '\n'

        if output:
            console.info( '   ' +line)
   
    p.close()
    return result

def makedir(dirname):
    """ Creates missing hierarchy levels for given directory """
    
    if dirname == "":
        return
        
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def deepcopy(file_list, folder):

    if isinstance(file_list, FileList):
        file_list = file_list.get()
    elif isinstance(file_list, str):
        file_list = [file_list]

    stat = 0
    console.header( "- copy to %s (%s files)" % (folder, len(file_list)))
    for file in file_list:
        dst_file = os.path.join(folder,os.path.basename(file))
        res = updatefile(file, dst_file)

        if res:
            console.info(' + %s' % file)
            stat += 1
    
    console.confirm( "  %s files updated" % (stat))

    
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


def writefile(dst, content):
    # First test for existance of destination directory
    makedir(os.path.dirname(dst))
    
    # Open file handle and write
    handle = open(dst, mode="w", encoding="utf-8")
    handle.write(content)
    handle.close()

def stats(file_list, title = ""):
    if isinstance(file_list, FileList):
        file_list = file_list.get()
    elif isinstance(file_list, str):
        file_list = [file_list]

    size = __exec("du %s | cut  -f1 |(tr '\n' '+'; echo 0) | bc" % ' '.join(file_list))

    try:
        size = int(size)
    except Exception:
        return 0

    lines = __exec("wc -l %s | tail -1" % ' '.join(file_list))
    lines =  re.findall(r'\d+(?:\.\d+)?', lines)
    if len(lines):
        lines = int(lines.pop())
    else:
        lines = 0
    
    if not title:
        title = "Stats on files"

    console.header(" - %s :" % title)
    console.info(  "   ~ Files : %s" % len(file_list))
    console.info(  "   ~ Lines : %s  (%s per file)" % (lines, (lines / len(file_list))))
    console.info(  "   ~ Size : %s (%s per file)" % (hsizeof(size), hsizeof((size / len(file_list)))))
    console.info("")


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

def __minify_js(in_file, out_file, verbose):
    options = ['--js %s' % in_file,
               '--js_output_file %s' % out_file,
               '--warning_level QUIET']

    os.system('java -jar "%s" %s' % (JS_COMPRESSOR,
                                          ' '.join(options)))

def __get_datas_path():
    return os.path.join(os.path.dirname( __file__ ), 'datas')


def __exec(command):
    result = ""
    p = os.popen(command)
    for line in p.readlines():
        result += line + '\n'
   
    p.close()

    return result

def hsizeof(num):
    try:
        num = int(num)
    except Exception:
        return 0
    
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

