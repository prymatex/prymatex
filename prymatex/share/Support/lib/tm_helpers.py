#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
tm_helpers.py

A collection of useful helper functions and classes for writing
commands in Python for TextMate.
"""

import sys, os, tempfile, stat
from re import sub, compile as compile_
from os import popen, path, environ as env

from plistlib import writePlistToString, readPlistFromString

# alias the plistlib functions, we will replace these
# with PyObjC when it becomes available.
to_plist   = writePlistToString
from_plist = readPlistFromString

def current_word(pat, direction="both"):
    """ Return the current word from the environment.
    
        pat       – A regular expression (as a raw string) matching word characters.
                    Typically something like this:  r"[A-Za-z_]*".
        direction – One of "both", "left", "right".  The function will look in
                    the specified directions for word characters.
    """
    word = ""
    if "TM_SELECTED_TEXT" in env:
        word = env["TM_SELECTED_TEXT"]
    elif "TM_CURRENT_WORD" in env and env["TM_CURRENT_WORD"]:
        line, x = env["TM_CURRENT_LINE"], int(env["TM_LINE_INDEX"])
        # get text before and after the index.
        first_part, last_part = line[:x], line[x:]
        word_chars = compile_(pat)
        m = word_chars.match(first_part[::-1])
        if m and direction in ("left", "both"):
            word = m.group(0)[::-1]
        m = word_chars.match(last_part)
        if m and direction in ("right", "both"):
            word += m.group(0)
    return word

def selection_or_line():
    """Return selected text, the current line or None if there's a problme"""

    try:
        text = os.environ['TM_SELECTED_TEXT']
    except KeyError:
        text = os.environ.get('TM_CURRENT_LINE')
    return text

def makeTempFile():
    tempDir = os.environ.get("PMX_TMP_PATH")
    descriptor, name = tempfile.mkstemp(dir = tempDir, text=True)
    os.chmod(name, stat.S_IREAD | stat.S_IWRITE)
    return name

def save_current_document():
    doc, dst = sys.stdin.read(), os.environ.get('TM_FILEPATH')
    
    if dst:
        os.environ['TM_DISPLAYNAME'] = os.environ.get('TM_FILENAME')
        if os.path.exists(dst) and os.access(os.path.dirname(dst), os.W_OK):
            os.utime(dst, None)
        with open(dst) as fd:
            content = fd.read()
        if os.path.exists(dst) and content == doc:
            return
    else:
        os.environ['TM_FILEPATH']         = dst = makeTempFile()
        os.environ['TM_FILENAME']         = os.path.basename(dst)
        os.environ['TM_FILE_IS_UNTITLED'] = "true"
        os.environ['TM_DISPLAYNAME']      = 'untitled'
        os.chdir(os.path.dirname(os.environ["TM_FILEPATH"]))
    
    try:
        f = open(dst, 'w')
        f.write(doc)
        f.close()
    except:
        os.environ['TM_ORIG_FILEPATH']    = dst
        os.environ['TM_ORIG_FILENAME']    = os.path.basename(dst)
        os.environ['TM_FILEPATH']         = dst = makeTempFile()
        os.environ['TM_FILENAME']         = os.path.basename(dst)
        os.environ['TM_DISPLAYNAME']     += ' (M)'
    
def env_python():
    """ Return (python, version) from env.
    
        Checks for the environment variable TM_FIRST_LINE and parses
        it for a #!.  Failing that, checks for the environment variable
        TM_PYTHON.  Failing that, uses "/usr/bin/env python".
    """
    python = ""
    if "TM_FIRST_LINE" in env:
        first_line = env["TM_FIRST_LINE"]
        hash_bang = compile_(r"^#!(.*)$")
        m = hash_bang.match(first_line)
        if m:
            python = m.group(1)
            version_string = sh(python + " -S -V 2>&1")
            if version_string.startswith("-bash:"):
                python = ""
    if not python and "TM_PYTHON" in env:
        python = env["TM_PYTHON"]
    elif not python:
        python = "/usr/bin/env python"
    version_string = sh(python + " -S -V 2>&1")
    version = version_string.strip().split()[1]
    version = int(version[0] + version[2])
    return python, version

def sh(cmd):
    """ Execute `cmd` and capture stdout, and return it as a string. """
    result = ""
    pipe = None
    try:
        pipe   = popen(cmd)
        result = pipe.read()
    finally:
        if pipe: pipe.close()
    return result

def sh_escape(s):
    """ Escape `s` for the shell. """
    return sub(r"(?=[^a-zA-Z0-9_.\/\-\x7F-\xFF\n])", r'\\', s).replace("\n", "'\n'")

def exit_discard():
    sys.exit(200)

def exit_replace_text(out = None):
  if out: print out
  sys.exit(201)
  
def exit_replace_document(out = None):
  if out: print out
  sys.exit(202)

def exit_insert_text(out = None):
  if out: print out
  sys.exit(203)

def exit_insert_snippet(out = None):
  if out: print out
  sys.exit(204)

def exit_show_html(out = None):
  if out: print out
  sys.exit(205)

def exit_show_tool_tip(out = None):
  if out: print out
  sys.exit(206)

def exit_create_new_document(out = None):
  if out: print out
  sys.exit(207)