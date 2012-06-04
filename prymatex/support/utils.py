#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, os, stat, tempfile
try:
    from ponyguruma import sre
except Exception, e:
    sre = re

ABSPATH_LINENO_RE = re.compile('''
    (?P<text>(?P<path>/[\w\d\/\.]+)(:(?P<line>\d+))?)
''', re.VERBOSE)

#TODO: Tomar del environment la shell por defecto    
BASH_SCRIPT = '''#!/bin/bash
source %s/lib/bash_init.sh
%s'''

ENV_SCRIPT = '''#!%s/bin/shebang.sh %s
%s'''

"""
Working with shebangs
http://en.wikipedia.org/wiki/Shebang_(Unix)

In memory of Dennis Ritchie
http://en.wikipedia.org/wiki/Dennis_Ritchie
"""

RE_SHEBANG = re.compile("^#!(.*)$")
RE_SHEBANG_ENVKEY = re.compile("(\w+)_SHEBANG")

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
    supportPath = environment['PMX_SUPPORT_PATH']
    
    #shebang analytics for build executable script
    if not has_shebang(scriptFirstLine):
        script = BASH_SCRIPT % (supportPath, script)
    elif is_bash_shebang(scriptFirstLine):
        script = BASH_SCRIPT % (supportPath, scriptContent)
    else:
        command = shebang_command(scriptFirstLine, environment)
        script = ENV_SCRIPT % (supportPath, command, scriptContent) 
    return script

def ensureEnvironment(environment):
    codingenv = {}
    for key, value in os.environ.iteritems():
        codingenv[key] = value[:]
    for key, value in environment.iteritems():
        codingenv[unicode(key).encode('utf-8')] = unicode(value).encode('utf-8')
    return codingenv

def makeExecutableTempFile(content, directory):
    descriptor, name = tempfile.mkstemp(prefix='pmx', dir = directory)
    tempFile = os.fdopen(descriptor, 'w+')
    tempFile.write(content.encode('utf-8'))
    tempFile.close()
    os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
    return name

def deleteFile(filePath):
    os.unlink(filePath)
    
def prepareShellScript(script, environment):
    environment = ensureEnvironment(environment)
    assert 'PMX_SUPPORT_PATH' in environment, "PMX_SUPPORT_PATH is not in the environment"
    script = ensureShellScript(script, environment)
    tempFile = makeExecutableTempFile(script, environment.get('PMX_TMP_PATH'))
    if sys.platform == "win32":
        #FIXME: re trucho pero por ahora funciona para mi :)
        command = "c:\\cygwin\\bin\\env %s" % self.tempFile
    else:
        command = tempFile
    return command, environment, tempFile

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
    return re.sub(ABSPATH_LINENO_RE, pathToLink, text)

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
