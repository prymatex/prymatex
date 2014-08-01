#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import sys
import os
import stat
import tempfile
import codecs

from prymatex.utils import encoding
from prymatex.utils import osextra
from prymatex.utils import programs

RE_SHEBANG = re.compile("^#!(.*)$")
RE_SHEBANG_ENVKEY = re.compile("(\w+)_SHEBANG")

ENV = programs.find_program("env")
SH = programs.find_program("sh")
CYGWIN = programs.find_program("cygwin")

"""
Working with shebangs
http://en.wikipedia.org/wiki/Shebang_(Unix)

In memory of Dennis Ritchie
http://en.wikipedia.org/wiki/Dennis_Ritchie
"""

def getShellShebang(environment):
    return "#!/bin/bash"
    return "#!%s" % environment.get("SHELL", SH)

def has_shebang(line):
    return line.startswith("#!")

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
    print(shebangParts)
    if shebangParts[0].startswith("env") and len(shebangParts) > 1:
        envKey = shebangParts[1].upper()
        patchValue = environment.get("TM_%s" % envKey, environment.get( "PMX_%s" % envKey))
        if patchValue:
            return "%s %s" % (patchValue, " ".join(shebangParts[2:]))
    else:
        # No portable shebang
        for key, value in environment.items():
            for prefix in ( "TM_", "PMX_" ):
                if key.startswith(prefix) and key[len(prefix):].lower() in shebang:
                    return ("%s %s") % (value, " ".join(shebangParts[2:]))
    return " ".join(shebangParts[1:])

def prepareShellScript(script, environment, variables):
    scriptLines = script.splitlines()
    
    # Shebang
    shellScript = [ getShellShebang(environment) ]
    
    # Agregar las variables
    for variable in variables:
        shellScript.append('export %s="%s"' % variable)
    
    # Agregar bash_init
    shellScript.append(". $TM_SUPPORT_PATH/lib/bash_init.sh")
    
    if has_shebang(scriptLines[0]):
        # Build fake shebang
        shellScript.append('exec %s $@' % ENV)
        shebang = makeExecutableTempFile(
            "\n".join(shellScript),
            environment.get('PMX_TMP_PATH'),
            prefix="shebang"
        )
        command = shebang_command(scriptLines[0], environment)
        #shellScript.append("%(env)s %(command)s <( <<'SCRIPT'" % {"env": ENV, "command": command})
        shellScript = [ "#!%(shebang)s %(command)s" % { 
            "shebang": shebang,
            "command": command } ]

        shellScript.extend(scriptLines[1:])
        
        #shellScript.append("SCRIPT")
        #shellScript.append(")")
    else:
        shellScript.extend(scriptLines)
    return "\n".join(shellScript)
    
#============================
# UINX
#============================
def ensureUnixEnvironment(environment):
    return dict(map(lambda item: (encoding.force_str(item[0]), encoding.force_str(item[1])), environment.items()))

def prepareUnixShellScript(script, environment, variables):
    script = prepareShellScript(script, environment, variables)
    scriptFile = makeExecutableTempFile(script, environment.get('PMX_TMP_PATH'))
    return scriptFile
    
#============================
# WINDOWS
#============================
def ensureWindowsEnvironment(environment):
    return dict(map(lambda item: (encoding.to_fs(item[0]), encoding.to_fs(item[1])), environment.items()))

def prepareWindowsShellScript(script, environment, variables):
    script = prepareShellScript(script, environment, variables)
    scriptFile = makeExecutableTempFile(script, environment.get('PMX_TMP_PATH'))
    return scriptFile
    
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

def prepareCygwinShellScript(script, environment, variables):
    cygwinPath = environment.get("PMX_CYGWIN_PATH", PMX_CYGWIN_PATH)

    script = prepareShellScript(script, environment, variables)
    scriptFile = makeExecutableTempFile(script, environment.get("PMX_TMP_PATH"))
    #TODO: Ver de pasarle en env correcto al script
    command = '%s\\bin\\env.exe "%s"' % (cygwinPath, scriptFile)
    return scriptFile

def buildShellScriptContext(script, environment, variables):
    scriptEnvironment = os.environ.copy()
    scriptEnvironment.update(environment)
    
    if sys.platform == "win32" and "PMX_CYGWIN_PATH" in scriptEnvironment:
        scriptEnvironment = ensureCygwinEnvironment(scriptEnvironment)
        scriptFile = prepareCygwinShellScript(
                        script, 
                        scriptEnvironment,
                        variables)
        return scriptFile, scriptEnvironment
    elif sys.platform == "win32":
        scriptEnvironment = ensureWindowsEnvironment(scriptEnvironment)
        scriptFile = prepareWindowsShellScript(
                    script,
                    scriptEnvironment,
                    variables)
        return scriptFile, scriptEnvironment
    scriptEnvironment = ensureUnixEnvironment(scriptEnvironment)
    scriptFile = prepareUnixShellScript(
        script, 
        scriptEnvironment,
        variables)
    return scriptFile, scriptEnvironment

def makeExecutableTempFile(content, directory, prefix="script"):
    # TODO: Mejorara la generacion de temp, se borra no se borra que onda
    #tempFile = tempfile.NamedTemporaryFile(prefix='pmx', dir = directory)
    descriptor, name = tempfile.mkstemp(prefix=prefix, dir = directory)
    tempFile = os.fdopen(descriptor, 'w+')
    tempFile.write(encoding.to_fs(content))
    tempFile.close()
    os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
    return name

def deleteFile(filePath):
    return
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
        newPath = path % ("%s_%s" % (name, suffix))
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
