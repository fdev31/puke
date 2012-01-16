#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, os.path, shutil, logging, sys, filecmp, stat, re, time


from puke.FileList import *
from puke.Console import *
from scss import Scss
from puke.FileSystem import *
from puke.Compress import *
from puke.Std import *
from puke.ToolsExec import *



from puke.Cache import *
import System





CSS_COMPRESSOR = sys.argv[0] + '.css.compress'
JS_COMPRESSOR = sys.argv[0] + '.js.compress'
JS_RUNNER = sys.argv[0] + '.js.runner'

def combine(in_files, out_file, verbose=False, replace = None):

    in_files = FileList.check(in_files)
         
    builddir = os.path.dirname(out_file)

    makedir(builddir)

    temp_file = os.path.join(builddir, '.temp')

    console.header( "- Combining files :")

    isCSS = False
    combined = ""

    for f in in_files:
        if not __get_ext(f) in ['css', 'scss']:
            continue

        isCSS = True
        combined = "@option compress: no;"
    

    for f in in_files:

        fh = open(f)
        data = fh.read() + '\n'

        if replace:
            data = __replace(data, replace)

        fh.close()
   
        console.info('  + %s ' % (__pretty(f)))

        combined += data
        
    
    if isCSS:
        combined = __parse_scss(combined)

    console.confirm( "  Generating %s" % out_file)
    writefile(out_file, combined)

def minify(in_file, out_file = None, verbose=False):

    System.check_package('java')

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

    #avoid division by zero
    if not new_size:
        console.fail('Compression fail')

    
    console.info('  ~ Original: %.2f kB' % (org_size / 1024.0))
    console.info('  ~ Compressed: %.2f kB' % (new_size / 1024.0))
    console.confirm('  %s ( Reduction : %.1f%% )' % (out_file, (float(org_size - new_size) / org_size * 100)))


def jslint(files, fix = False, relax = False, fail = True):
    System.check_package('java')

    files = FileList.check(files)

    options = []
    command = ""

    options.append('--jslint_error=optional_type_marker')
    options.append('--jslint_error=blank_lines_at_top_level')
    options.append('--jslint_error=indentation')
    options.append('--custom_jsdoc_tags=homepage,version,ignore,returns,example,function,requires,name,namespace,property,static,constant,default,location,copyright,memberOf,lends,fileOverview')


    if fix == True:
        header = "Fix JS lint"
        command = "fixjsstyle %s %s "  % (  ' '.join(options) , ' '.join(files))
    else:
        header = "JS lint"
        command = "gjslint %s %s "  % (  ' '.join(options) , ' '.join(files))
    
    if relax == True:
        command += ' | grep -v "Line too long"'
    result = sh(command, header = "%s (%s files)" % (header, len(files)) )

    error = re.search('Found\s([0-9]+)\serrors', result)

    if fail and error:
        console.fail( ' :puke:\n' + error.group())


def jsdoc(files, folder, template = None, fail = True):
    System.check_package('java')

    files = FileList.check(files)

    if not template:
        template = "%s/templates/gris_taupe" % jsdoc

    jsdoc =  os.path.join(__get_datas_path(), 'jsdoc-toolkit')
    output = sh("java -jar %s/jsrun.jar %s/app/run.js -d=%s -t=%s -a  %s" % (jsdoc, jsdoc, folder, template, ' '.join(files)), header = "Generating js doc", output = True)

    if fail and output:
        console.fail(output)
    
    console.confirm('  Doc generated in "%s"' % folder)

def patch(dir, patch, p=0):
    # patch -p0 -N <

    output = sh(['cd %s' % dir, 'patch -p%s -N -r pukepatch.rej < %s' % (p, patch)], output = False)
    console.header(' - Patching %s with %s' % (dir, patch))
    lines = output.split('\n')
    for line in lines:
        if 'can\'t find file to patch' in line:
            console.fail('Path : can\'t find file to patch')
            return False
        
        if line.startswith('patching'):
            console.confirm('    ' + line)
        elif 'ignored' in line:
            console.warn('    ' + line)
        else:
            console.info('    ' + line)
    
    try:
        remove(join(dir, 'pukepatch.rej'))
    except:
        pass


def prompt(message, default = ''):
    console.warn(message)
    result = sh('read toto && echo $toto', header = None, output=False)
    result = result.strip()
    if not result:
        result = default
    
    return result


def deepcopy(file_list, folder, replace = None):

    file_list = FileList.check(file_list, True)

    stat = 0
    console.header( "- copy to %s (%s files)" % (folder, len(file_list)))


    #Check if Sed changed
    forceRefresh = False
    if replace:
        filesId = FileList.getSignature(file_list)
        sedID = replace.getSignature()
        filesInfo = Cache.read("sed-%s" % filesId)

        sedUpdated = True

        if filesInfo:
            lastSed = filesInfo.split('\n')[-1]
            lastSed = lastSed.split(':')[0]

            if lastSed == sedID:
                sedUpdated = False
            
            filesInfo += "\n"
        else:
            filesInfo = ""



        if sedUpdated:
            forceRefresh = True
            Cache.write("sed-%s" % (filesId), "%s%s:%s" % (filesInfo, sedID, int(time.time())))

    
        
    
    for (file, basepath) in file_list:
        
        if basepath:
            dst_file = __pretty(file).replace(basepath, '').strip(os.sep)
            dst_file = os.path.join(folder,dst_file)
        else:
            dst_file = os.path.join(folder,os.path.basename(__pretty(file)))

        #console.warn("File : " + file +  " dest " + dst_file)

        if not forceRefresh:
            res = copyfile(file, dst_file, force = True)
        else:
            copyfile(file, dst_file)
            res = True
        

        if res and replace:

            fh = open(dst_file)
            data = fh.read()
        
            data = __replace(data, replace)

            fh.close()
            writefile(dst_file, data)
            


        if res:
            console.info(' + %s' % __pretty(file))
            stat += 1
    
    console.confirm( "  %s files updated" % (stat))

    


def stats(file_list, title = ""):
    file_list = FileList.check(file_list)

    if not title:
        title = "Stats on files"

    console.header(" - %s :" % title)

    if len(file_list) == 0:
        console.info(  "   No files ")
        return False

    size = __exec("du -k  %s | cut  -f1 |(tr '\n' '+'; echo 0) | bc" % ' '.join(file_list))
    
    try:
        size = int(size)
    except Exception:
        return 0
    
    size = size * 1024

    lines = __exec("wc -l %s | tail -1" % ' '.join(file_list))
    lines =  re.findall(r'\d+(?:\.\d+)?', lines)
    if len(lines):
        try:
            lines = int(lines.pop(0))
        except:
            lines = 0
    else:
        lines = 0
    
    
    console.info(  "   ~ Files : %s" % len(file_list))
    console.info(  "   ~ Lines : %s  (%s per file)" % (lines, (lines / len(file_list))))
    console.info(  "   ~ Size : %s (%s per file)" % (hsizeof(size), hsizeof((size / len(file_list)))))
    console.info("")

    return (len(file_list), lines, size)



def pack (file_list, output):

    file_list = FileList.check(file_list)

    console.header( "- Packing files to %s (%s files)" % (output, len(file_list)))

    comp = Compress.open(output, "w")
     
    for file in file_list:
        console.info(' * %s' % __pretty(file))
        comp.add(file)

    comp.close()

    console.confirm(" %s packed" % output)

def unpack (pack_file, output, extract = None, verbose=True):
    
    console.header( "- Unpacking %s to %s " % (pack_file, output))

    if not Compress.check(pack_file):
        console.error(" %s is not a valid pack" % output)
        raise PukeError('%s is not a valid pack' % output)
        return

    comp = Compress.open(pack_file, "r")
    
    

    count = 0
    for fname in comp:
        if extract and extract not in fname:
            continue

        (data, infos) = comp.extract(fname)
        
       
        #folder
        if not data:
            continue
        
        output_file = os.path.join(output, fname)


        if exists(output_file) and os.path.getmtime(output_file) == infos.mtime:
            continue
        
        if verbose == True:
            console.info(' + %s' % __pretty(output_file))
        
        writefile(output_file, data, mtime=infos.mtime)

        if infos.mode:
            chmod(output_file, infos.mode)

        count += 1
    
    comp.close()
    console.confirm(" %s unpacked in %s (%s files)" % (pack_file, output, count))

### WIP
def __jasmine(files):

    System.check_package('java')

    files = [files]

    envjs =  os.path.join(__get_datas_path(), 'envjs')
    output = sh("cd %s && java -jar %s -opt -1 %s/envjs.bootstrap.js %s" % (envjs, JS_RUNNER, envjs, " ".join(files)) , header = None, output = False)

    lines = output.split('\n')

    hasFailed = False

    for line in lines:
        if "Envjs" in line:
            continue

        if "Loading" in line:
            console.info('  * ' + line)
        elif "FAILED" in line:
            hasFailed = True
            console.error('  ' + line + '  ')
        elif "Suite" in line:
            console.log(' • ' + line)
        elif "Spec" in line or "Error" in line:
            console.info('   ' + line)
        elif "Passed:" in line:
            console.log(' ' + '-'*40)
            console.log('  '+ line)
        elif "Failed:" in line:
            console.log('  ' + line)
        elif "Total" in line:
            console.log('  ' + line)
            console.log(' ' + '-'*40)
        else:
            console.info('  ' + line)
    
    if not hasFailed: 
        console.confirm('  Tests success')
    else:
        console.fail("  Tests failure")
    
def __replace(data, replace):
    for k in replace.keys():
        data = re.sub(k, replace.get(k), data)

    return data


def __pretty(filename):
    if filename.startswith('.pukecache'):
        return Cache.getInfo(filename.split(os.sep).pop())
    
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

