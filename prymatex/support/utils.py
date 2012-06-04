#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, os, stat, tempfile
try:
    from ponyguruma import sre
except Exception, e:
    sre = re

RE_SHEBANG = re.compile("^#!(.*)$")
RE_SHEBANG_ENVKEY = re.compile("(\w+)_SHEBANG")
RE_ABSPATH_LINENO = re.compile('''
    (?P<text>(?P<path>/[\w\d\/\.]+)(:(?P<line>\d+))?)
''', re.VERBOSE)

PMX_CYGWIN_PATH = "c:\\cygwin"

PMX_SHEBANG = "#!%s/bin/shebang.sh"
PMX_BASHINIT = "%s/lib/bash_init.sh"
SHELL_SHEBANG = "#!/bin/bash"

"""
Working with shebangs
http://en.wikipedia.org/wiki/Shebang_(Unix)

In memory of Dennis Ritchie
http://en.wikipedia.org/wiki/Dennis_Ritchie
"""

def getSupportPath(environment):
    supportPath = environment["PMX_SUPPORT_PATH"]
    if (supportPath[0] == '"' and supportPath[-1] == '"') or \
    (supportPath[0] == "'" and supportPath[-1] == "'"):
        supportPath = supportPath[1:-1]
    return supportPath

def buildShellScript(script, environment):
    #TODO: Tomar del environment la shell por defecto
    shellScript = [SHELL_SHEBANG]
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

def is_bash_shebang(line):
    return line.startswith("#!/bin/bash") or line.startswith("#!/bin/sh")

def is_env_shebang(line):
    return line.startswith("#!/usr/bin/env")

def shebang_patch(shebang, environment):
    shebangParts = shebang.split()
    if shebangParts[0].startswith("#!/usr/bin/env") and len(shebangParts) > 1:
        envKey = shebangParts[1].upper()
        patchValue = environment.get("TM_%s" % envKey, environment.get( "PMX_%s" % envKey))
        if patchValue:
            shebang = "%s %s %s" % ("#!/usr/bin/env", patchValue, " ".join(shebangParts[2:]))
    else:
        #No portable shebang
        for key, value in environment.iteritems():
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
        for key, value in environment.iteritems():
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
    elif is_bash_shebang(scriptFirstLine):
        script = buildShellScript(scriptContent, environment)
    else:
        command = shebang_command(scriptFirstLine, environment)
        script = buildEnvScript(scriptContent, command, environment)
    return script

#============================
# UINX
#============================
def ensureUnixEnvironment(environment):
    codingenv = {}
    for key, value in os.environ.iteritems():
        codingenv[key] = value[:]
    for key, value in environment.iteritems():
        codingenv[unicode(key).encode('utf-8')] = unicode(value).encode('utf-8')
    return codingenv

def prepareUnixShellScript(script, environment):
    environment = ensureUnixEnvironment(environment)
    script = ensureShellScript(script, environment)
    tmpFile = makeExecutableTempFile(script, environment.get('PMX_TMP_PATH'))
    return tmpFile, environment, tmpFile
    
#============================
# WINDOWS
#============================
def ensureWindowsEnvironment(environment):
    codingenv = {}
    for key, value in os.environ.iteritems():
        codingenv[key] = value[:]
    for key, value in environment.iteritems():
        codingenv[unicode(key).encode('utf-8')] = unicode(value).encode('utf-8')
    return codingenv

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
    codingenv = {}
    for key, value in os.environ.iteritems():
        codingenv[key] = ensureCygwinPath(value)
    for key, value in environment.iteritems():
        key = unicode(key).encode('utf-8')
        value = unicode(value).encode('utf-8')
        codingenv[key] = ensureCygwinPath(value)
    return codingenv

def prepareCygwinShellScript(script, environment):
    cygwinPath = environment.get("PMX_CYGWIN_PATH", PMX_CYGWIN_PATH)
    environment = ensureCygwinEnvironment(environment)

    script = ensureShellScript(script, environment)
    tmpFile = makeExecutableTempFile(script, environment.get("PMX_TMP_PATH"))
    command = '%s\\bin\\env.exe "%s"' % (cygwinPath, tmpFile)
    return command, environment, tmpFile

def prepareShellScript(script, environment):
    assert 'PMX_SUPPORT_PATH' in environment, "PMX_SUPPORT_PATH is not in the environment"
    if sys.platform == "win32" and "PMX_CYGWIN_PATH" in environment:
        return prepareCygwinShellScript(script, environment)
    elif sys.platform == "win32":
        return prepareWindowsShellScript(script, environment)
    return prepareUnixShellScript(script, environment)

def makeExecutableTempFile(content, directory):
    descriptor, name = tempfile.mkstemp(prefix='pmx', dir = directory)
    tempFile = os.fdopen(descriptor, 'w+')
    tempFile.write(content.encode('utf-8'))
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
    """
    Return a safe path, ensure not exists
    """
    if suffix == 0 and not os.path.exists(path % name):
        return path % name
    else:
        newPath = path % (name + "_" + unicode(suffix))
        if not os.path.exists(newPath):
            return newPath
        else:
            return ensurePath(path, name, suffix + 1)
            
def pathToLink(match):
    path = match.group('path')
    attrs = {}
    attrs['url'] = 'file://%s' % match.group('path')
    attrs['line'] = match.group('line')
    #attrs['column'] = match.group('column')
    
    final_attrs = '?%s' % '?'.join(['%s=%s' % (k, v) for k, v in attrs.iteritems() if v ])
    text = match.group('text')
    
    data = dict(attrs= final_attrs, text= text)
    link = '<a href="txmt://open/%(attrs)s">%(text)s</a>' % data 
    return link

def makeHyperlinks(text):
    return re.sub(RE_ABSPATH_LINENO, pathToLink, text)

def compileRegexp(string):
    #Muejejejeje
    try:
        restring = string.replace('?i:', '(?i)')
        return re.compile(unicode(restring))
    except:
        try:
            return sre.compile(unicode(string))
        except:
            #Mala leche
            pass

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
    print shebang_patch("#!/usr/bin/env python", environment)
    print shebang_patch("#!/usr/bin/env python -s", environment)
    print shebang_patch("#!/usr/bin/env ruby -w -u", environment)
    print shebang_patch("#!/bin/ruby -uw --other", environment)
    print shebang_patch("#!/usr/bin/python", environment)
    print shebang_patch("#!/usr/bin/env bash", environment)
    print shebang_patch("#!/usr/bin/bash", environment)
    print shebang_command("#!/usr/bin/env python", environment)
    print shebang_command("#!/usr/bin/env python -s", environment)
    print shebang_command("#!/usr/bin/env ruby -w -u", environment)
    print shebang_command("#!/bin/ruby -uw --other", environment)
    print shebang_command("#!/bin/php -uw --other", environment)
    print shebang_command("#!/usr/bin/python", environment)
    print shebang_command("#!/usr/bin/env bash", environment)
    print shebang_command("#!/usr/bin/env php", environment)
    print shebang_command("#!/usr/bin/bash", environment)
