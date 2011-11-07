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

`brew install python`

Update your .profile PATH if you're a new brew user.

`export PATH="/usr/local/bin:/usr/local/share/python:$PATH"`

Get pip.

`/usr/local/share/python/easy_install pip`

`/usr/local/share/python/pip install --upgrade distribute`

Then get puke.

`pip install puke`

That's it. You're ready

Whenever you want to upgrade to the latest version, just 

`pip install puke --upgrade`

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
  -q, --quiet           don't print status messages to stdout
  -v, --verbose         print more detailed status messages to stdout
  -l LOGFILE, --log=LOGFILE
                        Write debug messages to given logfile
  -f FILE, --file=FILE  Use the given build script
</pre>

Can't remember your tasks ? Just puke it 

<pre>
$ puke
 No tasks to execute. Please choose from: 
 test: coin coin
 simple: Simple Test
 lint: lint
 doc: Documentation
 gate: Build gate package
</pre>

## Puke 10 seconds API reference 

Header:

<pre>
#!/usr/bin/env puke
# -*- coding: utf8 -*-
</pre>


Defining a simple task:

<pre>
@task("Simple Test")
def simple():
   console.log("Do something")
</pre>

Calling a task from another task:

`executeTask('simple')`

Logging:

<pre>
# Info levels
console.info("info")
console.confirm("confirm")
console.header("header")
console.log("log")
console.debug("debug")
console.warn("warn")
console.error("error")
console.fail("fail")
</pre>

Getting a FileList:

<pre>
list = FileList("foldername", filter = "*.js", exclude = "*.min.js")`

# multicriteria
list = FileList("src", filter = "*.css,*.scss")
</pre>

or

`list = ["somefilepath", "someother"]`



Merging files into one:

`combine(list, "build/test.js")`

Deep-copying (folder list):

`deepcopy(list, 'build/copy/')`

Minifying (with closure for js, and yahoo ui for css):

`minify("build/test.js")`

Call system:

`sh("pwd")`

Get FileList stats:

`stats(list, title = "JS Stats")`

<pre>
 - JS stats :
   ~ Files : 65
   ~ Lines : 23477  (361 per file)
   ~ Size : 1.8KB (28.0bytes per file)
</pre>

Perform in-file pattern replacement:

<pre>
sed = Sed()
sed.add('$TOTO$', 'troulute')
combine(list, "build/test.js", replace = sed)
</pre>

Using jslint (see [linting](Javascript-linting) for more):

`jslint(list, strict=False, nojsdoc=False, fix=False, relax=False)`

Using jsdoctoolkit (see [documenting javascript](Javascript-documentation) for more):

`jsdoc(list, "docdestination")`

## Guidelines

Nope.

## Gotcha

Don't puke on yourself!
