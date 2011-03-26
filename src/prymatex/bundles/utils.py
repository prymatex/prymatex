import os, stat, tempfile
from prymatex.core.config import settings

DIALOG = settings.PMX_SUPPORT_PATH + '/bin/CocoaDialog.app/Contents/MacOS/CocoaDialog'

BASH_SCRIPT = '''#!/bin/bash
source %s/lib/bash_init.sh
%%s''' % settings.PMX_SUPPORT_PATH

ENV_SCRIPT = '''#!%s/bin/shebang %%s
%%s''' % settings.PMX_SUPPORT_PATH

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
        tokens = text.splitlines()[0].split()
        if len(tokens) > 2:
            text = ENV_SCRIPT % (" ".join(tokens[1:]), text) 
    return text

def makeExecutableTempFile(content):
    descriptor, name = tempfile.mkstemp(prefix='pmx')
    file = os.fdopen(descriptor, 'w+')
    file.write(content.encode('utf-8'))
    file.close()
    os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
    return name
    
def deleteFile(file):
    return os.unlink(file)

def ensureEnvironment(environment):
    codingenv = { 'DIALOG': DIALOG }
    for key, value in os.environ.iteritems():
        codingenv[key] = value[:]
    for key, value in environment.iteritems():
        codingenv[key] = value.encode('utf-8')
    return codingenv