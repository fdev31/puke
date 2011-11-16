# Building: puke it right

## Technology

We are using python, and a homemade system named "puke". It's quite similar to rake, jake, jasy, scons, etc, except:

* it doesn't suck ass, unlike ruby
* it installs painless, unlike ruby
* it's extremely straightforward and does just a couple of simple things, avoiding both bloat and indigest documentation
* it's python, so it's cool and sexy, unlike ruby

## Features

Basic file manipulation, js linting via closure, minification via closure and YUI, scss parser, js documentation via jsdoctoolkit.


## Install

Use brew (https://github.com/mxcl/homebrew) and get yourself a fresh python if you don't want to mess up your lovely Lion system.

<pre>brew install python</pre>

Update your .profile PATH if you're a new brew user.

<pre>export PATH="/usr/local/bin:/usr/local/share/python:$PATH"</pre>

Get pip.

<pre>/usr/local/share/python/easy_install pip</pre>

<pre>/usr/local/share/python/pip install --upgrade distribute</pre>

Then get puke.

<pre>pip install puke</pre>

That's it. You're ready

Whenever you want to upgrade to the latest version, just 

<pre>pip install puke --upgrade</pre>

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

<pre>jslint(list, strict=False, nojsdoc=False, fix=False, relax=False)</pre>


### Using jsdoctoolkit (see [documenting javascript](Javascript-documentation) for more):

<pre>jsdoc(list, "docdestination", [template = "templatepath"])</pre>

### Clear puke cache

<pre>
$ puke -c
 
 Spring time, cleaning all the vomit around ...
 ...
 You're good to go !
</pre> 


## Guidelines

Nope.

## Gotcha

Don't puke on yourself!
