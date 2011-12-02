# Building: puke it right

<pre>
   .-'"'-.
  / `. ,' \
 |  ,' `.  |
 |   ___   |
  \ ( . ) /
   '-.:.-'
     .:.
     :::          
     :::
     ::.
     '::
      ' 
</pre>      

## Technology

We are using python, and a homemade system named "puke". It's quite similar to rake, jake, jasy, scons, etc, except:

* it doesn't suck ass, unlike ruby
* it installs painless, unlike ruby
* it's extremely straightforward and does just a couple of simple things, avoiding both bloat and indigest documentation
* it's python, so it's cool and sexy, unlike ruby

## Features

Basic file manipulation, js linting via closure, minification via closure and YUI, scss parser, js documentation via jsdoctoolkit, VirtualEnv creation with package installation, system package check.

## Changelog

### 1.3

 * Require.merge() makes now a deep merge
 * sh() can take now multiple commandes : sh(['cd somepath', 'do something'])
 * prompt('message', 'default') to prompt during the build
 * New FileSystem api
 * New System api
 * New Utils api
 * New VirtualEnv api
 * patch('dir/to/patch', patchfile) (Supports unix patch format only : man patch)
 * Task parameters (puke task arg1 arg2)
 * Task infos (puke task -i  docstring style)
 * few fixes
 

## Install

There is two ways to get there.

Either the recommended sandboxed way (using brew, for *MacOSX*), read 1a.

Or the "system" way (MacOSX and Linux), read 1b.

If you don't understand what I'm saying, you are on mac, so just follow 1a.
If you do, then you already have a working python + easy_install environment, right? Move on to step 2.

### 1. Sandboxed way

<pre>
# Install XCode:
http://developer.apple.com/technologies/xcode.html

# Install brew:
sudo mkdir /usr/local
sudo chmod g+rwx /usr/local
sudo chown root:staff local
/usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"

# Install python with brew:
brew install python

# Update your .profile so that the brew python is used
echo 'export PATH="/usr/local/share/python:/usr/local/bin:/usr/local/sbin:$PATH"' >> ~/.profile
source ~/.profile

# Double-check that the sandboxed python is used
which easy_install
# Should output/usr/local/share/python/easy_install
which python
# Should output /usr/local/bin/python
</pre>

Now go to step three.

### 2. The system way

You have nothing special to do, but you will need to be root in some of the following steps.

Go to step three now.

### 3. Install pip

If on Mac:

<pre>
easy_install pip
</pre>

If on Linux, just make sure you got pip:

<pre>
# If debian based...
sudo aptitude install python-pip
# or do it whatever way pleases you
</pre>


### 4. Install puke

<pre>
# Get some puke on you
pip install --upgrade puke
</pre>

Whenever you want to upgrade to the latest version, just do it again

<pre>pip install puke --upgrade</pre>

Yeah, that's it.

### Oh, did I mentioned the BIG FAT WARNING MANU BUG?

First time puke runs, it does patch some internal dependency (closure).
So, IN THE CASE YOU USED THE SYSTEM WAY, do this after install:
<pre>
sudo puke --patch
</pre>

Don't forget to do that (yet again, only if you installed puke as ROOT) every time you install.

That's it.


## Usage

You pretty much create a puke file, which is a very simple python script that describes build tasks for your project.
You may name it either "pukefile", or "pukefile.py".

Then you just call "puke someTaskName".

Help me puke :
<pre> 
$ puke --help
Usage: puke [options]

Options:
  -h, --help            show this help message and exit
  -c, --clear           Spring time, clean all the vomit
  -q, --quiet           don't print status messages to stdout
  -v, --verbose         print more detailed status messages to stdout
  -t, --tasks           list tasks
  -l LOGFILE, --log=LOGFILE
                        Write debug messages to given logfile
  -f FILE, --file=FILE  Use the given build script
  -p, --patch           Patch closure
</pre>

Can't remember your tasks ? Just puke it 

<pre>
$ puke --tasks
 No tasks to execute. Please choose from: 
 test: coin coin
 simple: Simple Test
 lint: lint
 doc: Documentation
 gate: Build gate package
</pre>

## Puke 10 seconds API reference 

### Header:

<pre>
#!/usr/bin/env puke
# -*- coding: utf8 -*-
</pre>


### Defining a simple task:
_Name your task "default" in order to have it executed by simply puke-ing_

<pre>
@task("Simple Test")
def simple():
   console.log("Do something")
</pre>

### import python script
<pre>
| pukefile.py
| helpers.py

=> helpers.py
from puke import *

def test():
  f = FileList('some/path')
  print "success"

=> pukefile.py
import helpers

helpers.test()
</pre>


### Calling a task from another task:

<pre>executeTask('simple')</pre>


### Defining "default" task:

<pre>
@task("")
def default():
   executeTask('simple')

@task("Simple Test")
def simple():
   console.log("Do something")

</pre>

### Executing tasks with args

Your pukefile
<pre>
@task('with args')
def test(required, optional = 'default'):
   """Python docstring style comment"""
   print "Required : %s" % required
   print "Optional : %s" % optional
</pre>

Execute puke
<pre>
puke test value
>>> Required : value
>>> Optional : default
</pre>

Need help with your params ?
<pre>
puke test --info
>>> -------------------------------------
>>> * Help test (task description) 
>>> -------------------------------------
>>> Help on function test in module puke:
>>>
>>> test(required, optional = 'default')
>>>    Python docstring style comment

</pre>


### Require (json / yaml)

<pre>
r = Require('global.yaml')
r.merge('build.yaml')
</pre>

Working with environment variables (Yaml example):

<pre>
params:
  #           envvar name | default
  build_dir: "${BUILD_DIR}|/usr/toto/build/"
  string: "toto"

</pre>

Yak it and make the puke easier!

<pre>
r = Require('global.yaml')
r.yak('params')

@task("Simple Test")
def simple():
   console.log("Easy to get my conf", Yak.build_dir, Yak.string)

#Check if your param exists
if 'build_dir' in Yak:
   print "yes"

</pre>

### Straight access to environment variables

<pre>
Env.get('BUILD_DIR', 'default')
</pre>


### Logging:

<pre>
# Info levels
console.info("info", arg2, ...)
console.confirm("confirm", arg2, ...)
console.log("log", arg2, ...)
console.debug("debug", arg2, ...)
console.warn("warn", arg2, ...)
console.error("error", arg2, ...)

console.header("header")
console.fail("fail")
</pre>

### Prompt :

<pre>
#prompt(message,default)
answer = prompt('How are you doing ?', 'fuck off')
</pre>

### Getting a FileList:

<pre>
list = FileList("foldername", filter = "*.js", exclude = "*.min.js")`

# multicriteria
list2 = FileList("src", filter = "*.css,*.scss")

#merge lists
list.merge(list2) 

</pre>

or

<pre>list = ["somefilepath", "someother", "http://example.com/something"]</pre>

**Note** that http:// urls are supported

**Note** that SCSS are automatically parsed


### Merging files into one:

<pre>combine(list, "build/test.js")</pre>


### Deep-copying (folder list):

<pre>deepcopy(list, 'build/copy/')</pre>


### Minifying (with closure for js, and yahoo ui for css):

<pre>minify("build/test.js", "build/test.min.js")</pre>

### Patch (unix patch format)
<pre>
patch('dir/to/patch', patchfile)
</pre>

### Pack/unpack (gz, zip)
Packing :

<pre>
#zip
pack(list, "folder/something.zip")

#gz
pack(list, "folder/something.tar.gz")
</pre>

Unpacking :
<pre>
#zip
unpack('folder/something.zip', 'folder/test-unpack/')

#gz
unpack('build/something.tar.gz', 'folder/test-unpack/')
</pre>


### Call system:

<pre>sh("pwd")</pre>
<pre>
#get output
pwd = sh("pwd")
#multiple commands
sh(['cd somepath', 'do something])
</pre>

### Get FileList stats:

<pre>stats(list, title = "JS Stats")</pre>

<pre>
 - JS stats :
   ~ Files : 65
   ~ Lines : 23477  (361 per file)
   ~ Size : 1.8KB (28.0bytes per file)
</pre>


### Perform in-file pattern replacement:

<pre>
sed = Sed()
sed.add('$TOTO$', 'troulute')
combine(list, "build/test.js", replace = sed)
deepcopy(list, "build/test.js", replace = sed)
</pre>


### Using jslint (see [linting](Javascript-linting) for more):

<pre>jslint(list, fix = False, relax = False, fail = True)</pre>


### Using jsdoctoolkit (see [documenting javascript](Javascript-documentation) for more):

<pre>jsdoc(list, "docdestination", [template = "templatepath"])</pre>

### Clear puke cache

<pre>
$ puke -c
 
 Spring time, cleaning all the vomit around ...
 ...
 You're good to go !
</pre> 

### FileSystem

Creates missing hierarchy levels for given directory
<pre>
FileSystem.makedir('somepath/to/dir')
</pre>

Get file content
<pre>
FileSystem.readfile('path/to/file')
</pre>

Remove file or dir (recursively)
<pre>
#With protection if you're trying to remove : './', '/', '~/', '~', '.', '..', '../'
FileSystem.remove('something')
</pre>

Copy a file
<pre>
#creates dirs if dst doesn't exist
#Does the copy only if the file doesn't exist or if the file has been modified
#To force to copy anyway, use  force = True
FileSystem.copyfile(src, dst)
</pre>

Create a file and write your content
<pre>
FileSystem.writefile('file', 'content')
</pre>

Check if the path exists
<pre>
FileSystem.exists('path')
</pre>

Check if the path is a file
<pre>
FileSystem.isfile('somefile')
</pre>

Check if the path is a dir
<pre>
FileSystem.path('somedir')
</pre>

Get an OS path  (eg : build/lib/folder on Unix)
<pre>
FileSystem.join('build', 'lib','folder')
</pre>

Get the absolute path
<pre>
FileSystem.abspath('./')
</pre>

Get file name
<pre>
FileSystem.basename('/path/to/toto.py')
>>> 'toto.py'
</pre>

### System

Check platform
<pre>
if System.OS == System.MACOS:
   #do something macos related
elif System.OS == System.LINUX:
   #do something linux related
elif System.OS == System.WINDOWS:
   #Achtung windows ...
</pre>

Get user login
<pre>
#Return None if something went wrong
System.LOGIN
</pre>

Check if a system package is here :
<pre>
System.check_package('nginx')
>>>   nginx is M.I.A
>>>     => "brew install nginx"
>>>   /!\ BUILD FAIL : nginx not installed

#Check version too (>= <= > < ==)
System.check_package('varnish', '>=3.0.1')
>>> varnish : INSTALLED (3.0.0 not >=3.0.1)
>>> * Continue anyway ? [Y/N default=Y]
>>> N
>>>  /!\ BUILD FAIL : Failed on version comp varnish 

#Only check on specific platform (System.LINUX, System.MACOS, System.LINUX, "all")
System.check_package('libcaca', platform=System.LINUX)
</pre>

Get package version
<pre>
System.get_package_version('uwsgi')
>>> "0.9.9"
</pre>

### VirtualEnv (Create and manage virtualenvs)

Create
<pre>
env = VirtualEnv()
env.create('path/to/create/env', python='python3|python|python2.7|...')
>>> * Creating env "test" ...
>>>   virtualenv : OK (1.6.4)
>>>   Python version : 3.2.2 ...
>>>   Env "test"  created 
</pre>

Load an existing virtualenv
<pre>
env = VirtualEnv()
env.load('test')
</pre>

install package
<pre>
env.install('webob')
>>> * Install "webob" in env "test" ...
>>>   Package "webob" is ready
</pre>

install package in a specific version
<pre>
env.install('webob', '1.1.1')
>>> * Install "webob" in env "test" ...
>>>   Package "webob" is ready
</pre>

install / force upgrade if installed
<pre>
env.install('webob', upgrade=True)
</pre>

upgrade package / all packages
<pre>
env.upgrade('webob')
env.upgrade('*')
</pre>

Check package / auto fix
<pre>
#check if the named package respect the version
env.check_package('webob', '>=1.1.1')

#check it and fix if the cond fails (make an install or upgrade or downgrade)
env.check_package('webob', '>=1.1.1', fix = True)
</pre>

List packages
<pre>
env.list()
>>>  * List packages (env "test")
>>>    - PIL (1.1.6)
>>>    - PyYAML (3.10)
>>>    - WebOb (1.2b2)
</pre>

Package info
<pre>
env.package_info('webob')
</pre>

Remove env
<pre>
env.remove()
</pre>

### Utils

Merge two deep dicts non-destructively
<pre>
a = {'a': 1, 'b': {1: 1, 2: 2}, 'd': 6}
b = {'c': 3, 'b': {2: 7}, 'd': {'z': [1, 2, 3]}}
Utils.deepmerge(a, b)
>>> {'a': 1, 'b': {1: 1, 2: 7}, 'c': 3, 'd': {'z': [1, 2, 3]}}
</pre>


## Guidelines

Nope.

## Gotcha

Don't puke on yourself!
