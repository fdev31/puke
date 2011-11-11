import os, os.path, shutil, logging, sys, filecmp, stat, re, time
from puke.FileList import *
from puke.Console import *
from scss import Scss
from puke.FileSystem import *


CSS_COMPRESSOR = sys.argv[0] + '.css.compress'
JS_COMPRESSOR = sys.argv[0] + '.js.compress'


def combine(in_files, out_file, verbose=False, replace = None):

    in_files = FileList.check(in_files)
         
    builddir = os.path.dirname(out_file)

    makedir(builddir)

    temp_file = os.path.join(builddir, '.temp')

    console.header( "- Combining files :")

    isCSS = False
    combined = ""

    if len(in_files) > 0 and __get_ext(in_files[0]) in ['css', 'scss']:
        isCSS = True
        combined = "@option compress: no;"


    

    for f in in_files:

        fh = open(f)
        data = fh.read() + '\n'

        if replace:
            for k in replace.keys():
                data = data.replace(k, replace.get(k))

        fh.close()
   
        console.info('  + %s ' % (__pretty(f)))

        combined += data
        
    
    if isCSS:
        combined = __parse_scss(combined)

    console.confirm( "  Generating %s" % out_file)
    writefile(out_file, combined)

def minify(in_file, out_file = None, verbose=False):

    if not isinstance(in_file, str):
        raise Exception("Minify : single file only")

    if not out_file:
        out_file = in_file
    
    in_type = __get_ext(out_file)

    org_size = os.path.getsize(in_file)

    console.header('- Minifying %s (%.2f kB)' % (__pretty(in_file), org_size / 1024.0))

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
    in_files = FileList.check(in_files)

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
    in_files = FileList.check(in_files)

    jsdoc =  os.path.join(__get_datas_path(), 'jsdoc-toolkit')
    output = sh("java -jar %s/jsrun.jar %s/app/run.js -d=%s -t=%s/templates/gris_taupe -a  %s" % (jsdoc, jsdoc, folder, jsdoc, ' '.join(files)), header = "Generating js doc", output = False)

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


def deepcopy(file_list, folder, replace = None):

    if isinstance(file_list, FileList):
        file_list = file_list.get(True)
    elif isinstance(file_list, str):
        file_list = [(file_list, '')]
    else:
        result = []
        for f in file_list:
            result.append( ( f, ''))
        file_list = result
        del result

    stat = 0
    console.header( "- copy to %s (%s files)" % (folder, len(file_list)))
    for (file, basepath) in file_list:
        
        if basepath:
            dst_file = file.replace(basepath, '').strip('/')
            dst_file = os.path.join(folder,dst_file)
        else:
            dst_file = os.path.join(folder,os.path.basename(file))

        #console.warn("File : " + file +  " dest " + dst_file)

        res = updatefile(file, dst_file)


        if res and replace:

            fh = open(dst_file)
            data = fh.read()
        
            for k in replace.keys():
                data = data.replace(k, replace.get(k))

            fh.close()
            writefile(dst_file, data, os.path.getmtime(file))
            


        if res:
            console.info(' + %s' % __pretty(file))
            stat += 1
    
    console.confirm( "  %s files updated" % (stat))

    


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

def __pretty(filename):
    if filename.startswith('.pukecache'):
        return PukeBuffer.getInfo(filename.split('/').pop())
    
    return filename

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

