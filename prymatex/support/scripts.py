#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import os
import stat
import tempfile
import codecs

from prymatex.utils import six
from prymatex.utils import encoding

RE_SHEBANG = re.compile("^#!(.*)$")
RE_SHEBANG_ENVKEY = re.compile("(\w+)_SHEBANG")

PMX_CYGWIN_PATH = "c:\\cygwin"

PMX_SHEBANG = "#!%s/bin/shebang.sh"
PMX_BASHINIT = "%s/lib/bash_init.sh"
SHELL_BASH = "/bin/bash"

"""
Working with shebangs
http://en.wikipedia.org/wiki/Shebang_(Unix)

In memory of Dennis Ritchie
http://en.wikipedia.org/wiki/Dennis_Ritchie
"""

def getSupportPath(environment):
    return environment["PMX_SUPPORT_PATH"]

def getShellShebang(environment):
    return "#!%s" % environment.get("SHELL", SHELL_BASH)

def buildShellScript(script, environment, shebang = None):
    shellScript = [ getShellShebang(environment) ] if shebang is None else [ shebang ]
    supportPath = getSupportPath(environment)
    
    bashInit = PMX_BASHINIT % supportPath
    shellScript.append('source "%s"' % bashInit)
    shellScript.append(script)
    return "\n".join(shellScript)

def buildEnvScript(script, command, environment):
    supportPath = getSupportPath(environment)

    shebang = PMX_SHEBANG % supportPath
    envScript = [ "%s %s" % (shebang, command) ]
    envScript.append(script)
    return "\n".join(envScript)
    
def has_shebang(line):
    return line.startswith("#!")

def is_shell_shebang(line):
    return os.path.basename(line) in [ "bash", "sh", "csh", "zsh" ]

def is_env_shebang(line):
    return os.path.basename(line) == "env"

def shebang_patch(shebang, environment):
    shebangParts = shebang.split()
    if shebangParts[0].startswith("#!/usr/bin/env") and len(shebangParts) > 1:
        envKey = shebangParts[1].upper()
        patchValue = environment.get("TM_%s" % envKey, environment.get( "PMX_%s" % envKey))
        if patchValue:
            shebang = "%s %s %s" % ("#!/usr/bin/env", patchValue, " ".join(shebangParts[2:]))
    else:
        #No portable shebang
        for key, value in environment.items():
            match = RE_SHEBANG_ENVKEY.match(key)
            if match:
                shebangKey = match.group(1).lower()
                splitIndex = shebang.find(shebangKey)
                if splitIndex != -1:
                    splitIndex += len(shebangKey)
                    shebang = value + shebang[splitIndex:]
    return shebang

def shebang_command(shebang, environment):
    shebangParts = shebang.split()
    if is_env_shebang(shebangParts[0]) and len(shebangParts) > 1:
        envKey = shebangParts[1].upper()
        patchValue = environment.get("TM_%s" % envKey, environment.get( "PMX_%s" % envKey))
        if patchValue:
            return "%s %s" % (patchValue, " ".join(shebangParts[2:]))
    else:
        #No portable shebang
        for key, value in environment.items():
            for prefix in [ "TM_", "PMX_" ]:
                if key.startswith(prefix) and key[len(prefix):].lower() in shebang:
                    return ("%s %s") % (value, " ".join(shebangParts[1:]))
    return " ".join(shebangParts[1:])

def ensureShellScript(script, environment):
    scriptLines = script.splitlines()
    scriptFirstLine = scriptLines[0]
    scriptContent = "\n".join(scriptLines[1:])
    
    #shebang analytics for build executable script
    if not has_shebang(scriptFirstLine):
        script = buildShellScript(script, environment)
    elif is_shell_shebang(scriptFirstLine):
        script = buildShellScript(scriptContent, environment, shebang = scriptFirstLine)
    else:
        command = shebang_command(scriptFirstLine, environment)
        script = buildEnvScript(scriptContent, command, environment)
    return script


#============================
# UINX
#============================
def ensureUnixEnvironment(environment):
    return dict(map(lambda item: (encoding.force_str(item[0]), encoding.force_str(item[1])), environment.items()))

def prepareUnixShellScript(script, environment):
    script = ensureShellScript(script, environment)
    tmpFile = makeExecutableTempFile(script, environment.get('PMX_TMP_PATH'))
    return tmpFile, ensureUnixEnvironment(environment), tmpFile
    
#============================
# WINDOWS
#============================
def ensureWindowsEnvironment(environment):
    return dict(map(lambda item: (encoding.to_fs(item[0]), encoding.to_fs(item[1])), environment.items()))

def prepareWindowsShellScript(script, environment):
    environment = ensureWindowsEnvironment(environment)
    script = ensureShellScript(script, environment)
    tmpFile = makeExecutableTempFile(script, environment.get('PMX_TMP_PATH'))
    return tmpFile, environment, tmpFile
    
#============================
# CYGWIN
#============================
def ensureCygwinPath(path):
    import win32api
    if os.path.exists(path):
        path = win32api.GetShortPathName(path)
        path = path.replace("\\", "/")
    return path

def ensureCygwinEnvironment(environment):
    return dict(map(lambda item: (encoding.to_fs(item[0]), ensureCygwinPath(encoding.to_fs(item[1]))), environment.items()))

def prepareCygwinShellScript(script, environment):
    cygwinPath = environment.get("PMX_CYGWIN_PATH", PMX_CYGWIN_PATH)
    environment = ensureCygwinEnvironment(environment)

    script = ensureShellScript(script, environment)
    tmpFile = makeExecutableTempFile(script, environment.get("PMX_TMP_PATH"))
    command = '%s\\bin\\env.exe "%s"' % (cygwinPath, tmpFile)
    return command, environment, tmpFile

def prepareShellScript(script, variables):
    #Aca entran las variables de prymatex, tengo que armar el environment con os.environ
    assert 'PMX_SUPPORT_PATH' in variables, "PMX_SUPPORT_PATH is not in the environment"
    
    # Build final environment
    environment = os.environ.copy()
    environment.update(variables)
    
    if sys.platform == "win32" and "PMX_CYGWIN_PATH" in environment:
        return prepareCygwinShellScript(script, environment)
    elif sys.platform == "win32":
        return prepareWindowsShellScript(script, environment)
    return prepareUnixShellScript(script, environment)

def makeExecutableTempFile(content, directory):
    # TODO: Mejorara la generacion de temp, se borra no se borra que onda
    #tempFile = tempfile.NamedTemporaryFile(prefix='pmx', dir = directory)
    descriptor, name = tempfile.mkstemp(prefix='pmx', dir = directory)
    tempFile = os.fdopen(descriptor, 'w+')
    tempFile.write(six.PY3 and content or encoding.to_fs(content))
    tempFile.close()
    os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
    return name

def deleteFile(filePath):
    os.unlink(filePath)

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
    """Return a safe path, ensure not exists"""
    if suffix == 0 and not os.path.exists(path % name):
        return path % name
    else:
        newPath = path % (name + "_" + six.u(suffix))
        if not os.path.exists(newPath):
            return newPath
        else:
            return ensurePath(path, name, suffix + 1)

if __name__ == '__main__':
    #http://en.wikipedia.org/wiki/Shebang_(Unix)
    environment = {
        "TM_PYTHON": "python2",
        "PMX_PHP": "php4",
        "TM_RUBY": "ruby1.8",
        "TM_BASH": "zsh",
        "PYTHON_SHEBANG": "#!/usr/bin/python2",
        "RUBY_SHEBANG": "#!/usr/local/bin/ruby1.8",
        "BASH_SHEBANG": "#!/bin/sh"
    }
    print(shebang_patch("#!/usr/bin/env python", environment))
    print(shebang_patch("#!/usr/bin/env python -s", environment))
    print(shebang_patch("#!/usr/bin/env ruby -w -u", environment))
    print(shebang_patch("#!/bin/ruby -uw --other", environment))
    print(shebang_patch("#!/usr/bin/python", environment))
    print(shebang_patch("#!/usr/bin/env bash", environment))
    print(shebang_patch("#!/usr/bin/bash", environment))
    print(shebang_command("#!/usr/bin/env python", environment))
    print(shebang_command("#!/usr/bin/env python -s", environment))
    print(shebang_command("#!/usr/bin/env ruby -w -u", environment))
    print(shebang_command("#!/bin/ruby -uw --other", environment))
    print(shebang_command("#!/bin/php -uw --other", environment))
    print(shebang_command("#!/usr/bin/python", environment))
    print(shebang_command("#!/usr/bin/env bash", environment))
    print(shebang_command("#!/usr/bin/env php", environment))
    print(shebang_command("#!/usr/bin/bash", environment))