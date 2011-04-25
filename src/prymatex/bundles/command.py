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

    @property
    def systemCommand(self):
        if self.winCommand != None and 'Window' in os.environ['OS']:
            return self.winCommand
        elif self.linuxCommand != None:
            return self.linuxCommand
        else:
            return self.command
    
    def getInputText(self, processor):
        def switch(input):
            if not input: return None, None
            return input, getattr(processor, input)
        input, value = switch(self.input)
        if not value:
            input, value = switch(self.fallbackInput)
        if not value:
            input, value = switch(self.standardInput)
        return input, unicode(value).encode("utf-8")

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
        
    def getOutputHandler(self, code):
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
            return type
        return 'discard'
    
    def execute(self, processor):
        processor.startCommand(self)
        input_type, input_value = self.getInputText(processor)
        command = ensureShellScript(self.systemCommand)
        temp_file = makeExecutableTempFile(command)
        process = Popen([  temp_file], stdin=PIPE, stdout=PIPE, stderr=STDOUT, env = ensureEnvironment(processor.environment))
        
        process.stdin.write(input_value)
        process.stdin.close()
        output_value = process.stdout.read()
        process.stdout.close()
        output_type = process.wait()
        output_handler = self.getOutputHandler(output_type)
        
        #handle input_type in editor, remove word, remove character, remove selection
        
        text = output_value.decode('utf-8')
        function = getattr(processor, output_handler)
        function(text)
        
        processor.endCommand(self)
        
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