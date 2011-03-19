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
    exit_codes = {
                  200: 'discard',
                  201: 'replaceSelectedText',
                  202: 'replaceDocument',
                  203: 'insertText',
                  204: 'insertAsSnippet',
                  205: 'showAsHTML',
                  206: 'showAsTooltip',
                  207: 'createNewDocument'
                  }
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

    def getSystemCommand(self):
        if self.winCommand != None and 'Window' in os.environ['OS']:
            return self.winCommand
        elif self.linuxCommand != None and 'Window' not in os.environ['OS']:
            return self.linuxCommand
        else:
            return self.command
    
    def getInputText(self, document, character, environment):
        def switch(input):
            if not input: return ""
            if input == 'document':
                return document
            if input == 'line':
                return environment['TM_CURRENT_LINE']
            if input == 'character':
                return character
            if input == 'scope':
                return environment['TM_SCOPE']
            if input == 'selection':
                return environment['TM_SELECTED_TEXT']
            if input == 'word':
                return environment['TM_CURRENT_WORD']
            return ""
        return switch(self.input) or switch(self.fallbackInput) or switch(self.standardInput)

    def getOutputFunction(self, code, functions):
        ''' showAsHTML
            showAsTooltip
            insertAsSnippet
            replaceSelectedText
            replaceDocument
        '''
        type = ''
        if self.output != 'showAsHTML' and code != 0 and code in self.exit_codes:
            type = self.exit_codes[code]
        else:
            type = self.output
        if type in functions:
            return type, functions[type]
        def discard(text):
            print 'discard', text
        return 'discard', discard
    
    def buildOutputArgument(self, output, text):
        from prymatex.bundles.snippet import PMXSnippet
        if output == 'insertAsSnippet':
            snippet = PMXSnippet({ 'content': text})
            snippet.bundle = self.bundle
            return snippet
        else:
            return text.strip()
        
    def __del__(self):
        PMXShell.deleteFile(self.temp_command_file)
        
    def resolve(self, document, character, environment = {}):
        self.temp_command_file = PMXShell.makeExecutableTempFile(self.getSystemCommand())
        self.shell_interpreter = PMXShell(environment)
        self.input_text = self.getInputText(document, character, environment)
    
    def execute(self, output_functions):
        self.shell_interpreter.execute(self.temp_command_file)
        if self.input_text != "":
            self.shell_interpreter.stdin.write(self.input_text)
        exit_code, text = self.shell_interpreter.read()

        type, function = self.getOutputFunction(exit_code, output_functions)
        function(self.buildOutputArgument(type, text))
        
        #Podria borrar este archivo cuando de borra el objeto
        #PMXShell.deleteFile(self.temp_command_file)