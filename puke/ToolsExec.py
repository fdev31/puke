import os, sys

import subprocess
import signal, platform
from puke.Console import *
from puke.Std import *
from puke.SSH import SSH



class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm


def sh (command, header = None, output = True, timeout = None, std = None, ssh=None):

    isWouinWouin = (platform.system() == 'Windows')

    if isinstance(command, list):
        command = " \n ".join(command)

    
    if ssh and not isinstance(ssh, SSH):
        console.fail('Bad ssh param. See SSH.')


    if header == None:
        header = 'exec "%s" ' % command
    else:
        console.debug(command)
    
    if output and header != False:
        console.header(' - '+header)


    stdErrMarker = "XXXERRORXXX"
    
    result = ""

    if timeout and not isWouinWouin:
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(timeout)  # 5 seconds
    

    try:

        if not ssh:
            executable = '/bin/bash'
            command = "export PYTHONIOENCODING=utf-8;" + command


            if isWouinWouin:
                executable = None
                command = "bash.exe -c '" + command.replace("'", "\\'") + "'"
            

            cProcess = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True, stderr= subprocess.PIPE, executable=executable, env=os.environ)
            (rStdout, rStderr) = cProcess.communicate()
            code = cProcess.returncode
        else:
            isWouinWouin == False

            (rStdout, rStderr, code) = ssh.execute(command)

        if not isWouinWouin:
            signal.alarm(0)

    except Alarm:
        console.debug('taking too long (%s)' % command)
        cProcess.kill()
        rStdout = rStderr = ''
        code = 0
    
    if std and isinstance(std, Std):
        std.set(rStdout, rStderr, code)

    rStdout = "%s\n%s\n%s" % (rStdout if rStdout else '', stdErrMarker if rStderr else '', rStderr if rStderr else '')

    lines = rStdout.split('\n')
    for line in lines:
        if not line:
            continue

        if output == True and stdErrMarker in line:
            console.error("")
            console.error('Std error :')
            line = ""
        

        result += line
        
        if not line.endswith('\n'):
            result += '\n'

        if output == True:
            console.info( '   ' +line)
   
    return result