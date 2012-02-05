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
    
BASH_SCRIPT = '''#!/bin/bash
source %s/lib/bash_init.sh
%s'''

ENV_SCRIPT = '''#!%s/bin/shebang.sh %s
%s'''

def has_shebang(text):
    line = text.split()[0]
    return line.startswith("#!")

def is_bash_shebang(text):
    line = text.split()[0]
    #TODO: Regexp
    return line.startswith("#!/bin/bash") or line.startswith("#!/bin/sh")

def is_env_shebang(text):
    line = text.split()[0]
    return line.startswith("#!/usr/bin/env")

def ensureShellScript(script, supportPath):
    if not has_shebang(script) or is_bash_shebang(script):
        if sys.platform == "win32":
            supportPath = supportPath.replace("\\",'/')
        script = BASH_SCRIPT % (supportPath, script)
    elif is_env_shebang(script):
        lines = script.splitlines()
        shebang = lines[0].split()
        script = ENV_SCRIPT % (supportPath, " ".join(shebang[1:]), "\n".join(lines[1:])) 
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
    file = os.fdopen(descriptor, 'w+')
    file.write(content.encode('utf-8'))
    file.close()
    os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
    return name

def prepareShellScript(script, environment):
    environment = ensureEnvironment(environment)
    assert 'PMX_SUPPORT_PATH' in environment, "PMX_SUPPORT_PATH is not in the environment"
    script = ensureShellScript(script, environment['PMX_SUPPORT_PATH'])
    file = makeExecutableTempFile(script, environment.get('PMX_LOG_PATH'))
    if sys.platform == "win32":
        #FIXME: re trucho pero por ahora funciona para mi :)
        command = "c:\\cygwin\\bin\\env %s" % file
    else:
        command = file
    return command, environment

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
