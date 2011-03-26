#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Command's module    
'''
import os
from subprocess import Popen, PIPE, STDOUT
# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))
import ponyguruma as onig
from ponyguruma.constants import OPTION_CAPTURE_GROUP
from prymatex.bundles.base import PMXBundleItem
from prymatex.bundles.snippet import PMXSnippet
from prymatex.bundles.utils import ensureShellScript, ensureEnvironment, makeExecutableTempFile, deleteFile

onig_compile = onig.Regexp.factory(flags = OPTION_CAPTURE_GROUP)

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
            if not input: return "", u""
            if input == 'document':
                return 'document', document
            if input == 'line':
                return 'line', environment['TM_CURRENT_LINE']
            if input == 'character':
                return 'character', character
            if input == 'scope':
                return 'scope', environment['TM_SCOPE']
            if input == 'selection' and 'TM_SELECTED_TEXT' in environment:
                return 'selection', environment['TM_SELECTED_TEXT']
            if input == 'word':
                return 'word', environment['TM_CURRENT_WORD']
            return "", u""
        input, text = switch(self.input)
        if not text:
            input, text = switch(self.fallbackInput)
        if not text:
            input, text = switch(self.standardInput)
        return input, text.encode("utf-8")

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
        def discard(input, text):
            print 'discard', input, text
        return 'discard', discard
    
    def buildOutputArgument(self, output, text):
        if output == 'insertAsSnippet':
            snippet = PMXSnippet({ 'content': text})
            snippet.bundle = self.bundle
            return snippet
        elif output == 'showAsTooltip':
            return text.strip().decode('utf-8')
        else:
            return text.decode('utf-8')
        
    def resolve(self, document, character, environment = {}):
        self.input_current, self.input_text = self.getInputText(document, character, environment)
        if self.input_current == 'world':
            environment['TM_INPUT_START_LINE_INDEX'] = environment['TM_CURRENT_WORD_INDEX'] 
        command = ensureShellScript(self.getSystemCommand())
        self.temp_command_file = makeExecutableTempFile(command)  
        self.command_process = Popen([  self.temp_command_file],
                                        stdin=PIPE, stdout=PIPE, stderr=STDOUT, 
                                        env = ensureEnvironment(environment))
    
    def execute(self, output_functions):
        self.command_process.stdin.write(self.input_text)
        self.command_process.stdin.close()
        text = self.command_process.stdout.read()
        self.command_process.stdout.close()
        exit_code = self.command_process.wait()
        
        type, function = self.getOutputFunction(exit_code, output_functions)
        print self.bundle.name, self.name, self.temp_command_file, type, text
        function(self.input_current, self.buildOutputArgument(type, text))
        
        #Podria borrar este archivo cuando de borra el objeto
        #deleteFile(self.temp_command_file)