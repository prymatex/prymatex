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
        elif self.linuxCommand != None:
            return self.linuxCommand
        else:
            return self.command
    
    def getInputText(self, document, character, environment):
        def switch(input):
            if not input: return "", ""
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
            if input == 'word' and 'TM_CURRENT_WORD' in environment:
                return 'word', environment['TM_CURRENT_WORD']
            return "", ""
        input, text = switch(self.input)
        if not text:
            input, text = switch(self.fallbackInput)
        if not text:
            input, text = switch(self.standardInput)
        return input, unicode(text).encode("utf-8")


    def formatError(self, output, exit_code):
        from prymatex.lib.pathutils import make_hyperlinks
        html = '''
            <html>
                <head>
                    <title>Error</title>
                    <style>
                        body {
                            background: #999;
                            
                        }
                        pre {
                            border: 1px dashed #222;
                            background: #ccc;
                            text: #000;
                            padding: 2%%;
                        }
                    </style>
                </head>
                <body>
                <h3>An error has occurred while executing command "%(name)s"</h3>
                <pre>%(output)s</pre>
                <p>Exit code was: %(exit_code)d</p>
                </body>
            </html>
        ''' % {'output': make_hyperlinks(output), 
               'name': self.name,
               'exit_code': exit_code}
        #html.replace()
        return html
        
    def getOutputFunction(self, code, functions):
        ''' showAsHTML
            showAsTooltip
            insertAsSnippet
            replaceSelectedText
            replaceDocument
        '''
        type = ''
        if self.output != 'showAsHTML' and code in self.exit_codes:
            type = self.exit_codes[code]
        else:
            type = self.output
        if type in functions:
            return type, functions[type]
        def discard(text, **kwargs):
            print 'discard', text, kwargs
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
        #TODO: Terminar la logica para los inputs
        if self.input_current == 'word':
            index = environment['TM_LINE_INDEX'] - len(environment['TM_CURRENT_WORD'])
            index = index >= 0 and index or 0
            environment['TM_INPUT_START_COLUMN'] = environment['TM_CURRENT_LINE'].find(environment['TM_CURRENT_WORD'],index)
            environment['TM_INPUT_START_LINE'] = environment['TM_LINE_NUMBER']
            environment['TM_INPUT_START_LINE_INDEX'] = environment['TM_CURRENT_LINE'].find(environment['TM_CURRENT_WORD'],index)
        elif self.input_current == 'selection':
            index = environment['TM_LINE_INDEX'] - len(environment['TM_SELECTED_TEXT'])
            index = index >= 0 and index or 0
            environment['TM_INPUT_START_COLUMN'] = environment['TM_CURRENT_LINE'].find(environment['TM_SELECTED_TEXT'],index)
            environment['TM_INPUT_START_LINE'] = environment['TM_LINE_NUMBER']
            environment['TM_INPUT_START_LINE_INDEX'] = environment['TM_CURRENT_LINE'].find(environment['TM_SELECTED_TEXT'],index)
        
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
        
        kwargs = {'command': self}
        if self.input_current:
            kwargs['input'] = self.input_current
            
        function(self.buildOutputArgument(type, text), **kwargs)
        
        #Podria borrar este archivo cuando de borra el objeto
        #deleteFile(self.temp_command_file)

class PMXDragCommand(PMXCommand):
    path_patterns = ['DragCommands/*.tmCommand', 'DragCommands/*.plist']
    def __init__(self, hash, name_space = "default", path = None):
        super(PMXDragCommand, self).__init__(hash, name_space, path)
        for key in [    'draggedFileExtensions' ]:
            setattr(self, key, hash.get(key, None))

    def buildEnvironment(self, directory = "", name = ""):
        env = super(PMXDragCommand, self).buildEnvironment()
        # TM_DROPPED_FILE � relative path of the file dropped (relative to the document directory, which is also set as the current directory).
        env['TM_DROPPED_FILE'] = os.path.join(directory)
        #TM_DROPPED_FILEPATH � the absolute path of the file dropped.
        env['TM_DROPPED_FILEPATH'] = os.path.join(directory)
        #TM_MODIFIER_FLAGS � the modifier keys which were held down when the file got dropped.
        #This is a bitwise OR in the form: SHIFT|CONTROL|OPTION|COMMAND (in case all modifiers were down).
        env['TM_MODIFIER_FLAGS'] = directory
        return env
        
    def setBundle(self, bundle):
        super(PMXDragCommand, self).setBundle(bundle)
        bundle.DRAGS.append(self)