#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Command's module    
'''
import os, stat, tempfile
from subprocess import Popen, PIPE, STDOUT
# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))
import ponyguruma as onig
from ponyguruma.constants import OPTION_CAPTURE_GROUP
from prymatex.bundles.base import PMXBundleItem
from prymatex.core.config import settings
'''
These functions only work when the initial output option is not set as "Show as HTML". The list of functions is as follows:
input:
    document
    line
    word
    character
    scope
output:
200 exit_discard
201 exit_replace_text
202 exit_replace_document
203 exit_insert_text
204 exit_insert_snippet
205 exit_show_html
206 exit_show_tool_tip
207 exit_create_new_document
    showAsHTML
    showAsTooltip
    insertAsSnippet
    replaceSelectedText
    replaceDocument
'''

onig_compile = onig.Regexp.factory(flags = OPTION_CAPTURE_GROUP)

class PMXShell(Popen):
    INIT_SCRIPT = settings.PMX_SUPPORT_PATH + '/lib/bash_init.sh'
    FUNCTIONS = [  'exit_discard', 'exit_replace_text', 'exit_replace_document', 'exit_insert_text', 'exit_insert_snippet',
               'exit_show_html', 'exit_show_tool_tip', 'exit_create_new_document', 'require_cmd', 'rescan_project', 'pre']
    def __init__(self, environment):
        super(PMXShell, self).__init__(["/bin/bash"], stdin=PIPE, stdout=PIPE, stderr=STDOUT, env = environment)
        self.execute("source " + self.INIT_SCRIPT)
        for function in self.FUNCTIONS:
            self.execute("export -f  %s" % function)
        
    def execute(self, command):
        self.stdin.write(command + "\n")

    def read(self):
        self.stdin.close()
        value = self.stdout.read()
        self.stdout.close()
        return (self.wait(), value)
        
    @staticmethod
    def makeExecutableTempFile(content):
        descriptor, name = tempfile.mkstemp(prefix='pmx')
        file = os.fdopen(descriptor, 'w+')
        file.write(content.encode('utf8'))
        file.close()
        os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        return name

    @staticmethod
    def deleteFile(file):
        return os.unlink(file)
        
class PMXCommand(PMXBundleItem):
    path_patterns = ['Commands/*.tmCommand', 'Commands/*.plist']
    bundle_collection = 'commands'
    def __init__(self, hash, name_space = "default", path = None):
        super(PMXCommand, self).__init__(hash, name_space, path)
        for key in [    'input', 'fallbackInput', 'standardInput', 'output', 'standardOutput',  #I/O
                        'command', 'winCommand', 'linuxCommand',                                #System based Command
                        'capturePattern', 'fileCaptureRegister',
                        'columnCaptureRegister', 'inputFormat', 'disableOutputAutoIndent',
                        'lineCaptureRegister', 'dontFollowNewOutput',
                        'beforeRunningCommand', 'autoScrollOutput', 'captureFormatString', 'beforeRunningScript' ]:
            value = hash.get(key, None)
            if value != None and key in [    'capturePattern' ]:
                value = onig_compile( value )
            setattr(self, key, value)
        self.value = u""
        
    def __unicode__(self):
        return self.value
    
    def resolve(self, document, character, environment = {}):
        file = PMXShell.makeExecutableTempFile(self.command)
        shell = PMXShell(environment)
        shell.execute(file)
        if self.input == 'document':
            shell.stdin.write(document)
        if self.input == 'line':
            shell.stdin.write(environment['TM_CURRENT_LINE'])
        if self.input == 'character':
            shell.stdin.write(character)
        if self.input == 'scope':
            shell.stdin.write(environment['TM_SCOPE'])
        if self.input == 'word':
            shell.stdin.write(environment['TM_CURRENT_WORD'])
        exit_code, self.value = shell.read()
        print exit_code, self.value
        PMXShell.deleteFile(file)
    
    def execute(self, parent):
        if self.output != None and self.output == 'showAsTooltip':
            parent.showTooltip(self.value)
        if self.output != None and self.output == 'showAsHTML':
            parent.showHtml(self.value)
    