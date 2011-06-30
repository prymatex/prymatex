#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, stat, tempfile
try:
    from prymatex.core.config import PMX_SUPPORT_PATH
except:
    PMX_SUPPORT_PATH = "/"

DIALOG = PMX_SUPPORT_PATH + '/bin/CocoaDialog.app/Contents/MacOS/CocoaDialog'

BASH_SCRIPT = '''#!/bin/bash
source %s/lib/bash_init.sh
%%s''' % PMX_SUPPORT_PATH

ENV_SCRIPT = '''#!%s/bin/shebang.sh %%s
%%s''' % PMX_SUPPORT_PATH

def has_shebang(text):
    line = text.split()[0]
    return line.startswith("#!")

def is_bash_shebang(text):
    line = text.split()[0]
    return line.startswith("#!/bin/bash")

def is_env_shebang(text):
    line = text.split()[0]
    return line.startswith("#!/usr/bin/env")

def ensureShellScript(text):
    if not has_shebang(text) or is_bash_shebang(text):
        text = BASH_SCRIPT % text
    elif is_env_shebang(text):
        lines = text.splitlines()
        shebang = lines[0].split()
        text = ENV_SCRIPT % (" ".join(shebang[1:]), "\n".join(lines[1:])) 
    return text

def ensureEnvironment(environment):
    codingenv = { 'DIALOG': DIALOG }
    for key, value in os.environ.iteritems():
        codingenv[key] = value[:]
    for key, value in environment.iteritems():
        codingenv[unicode(key).encode('utf-8')] = unicode(value).encode('utf-8')
    return codingenv

def makeExecutableTempFile(content):
    descriptor, name = tempfile.mkstemp(prefix='pmx')
    file = os.fdopen(descriptor, 'w+')
    file.write(content.encode('utf-8'))
    file.close()
    os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
    return name
    
def deleteFile(file):
    return os.unlink(file)

def sh(cmd):
    """ Execute cmd and capture stdout, and return it as a string. """
    result = ""
    pipe = None
    try:
        pipe   = os.popen(cmd)
        result = pipe.read()
    finally:
        if pipe: pipe.close()
    return result

def ensurePath(path, name, suffix = 0):
    '''
        Return a safe path, ensure not exists
    '''
    print path, name
    if suffix == 0 and not os.path.exists(path % name):
        return path % name
    else:
        newPath = path % (name + "_" + unicode(suffix))
        if not os.path.exists(newPath):
            return newPath
        else:
            return ensurePath(path, name, suffix + 1)