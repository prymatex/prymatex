#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.gui import utils
from prymatex.support.processor import PMXCommandProcessor

#Este es un processor de commands para la Main Window
class MainWindowCommandProcessor(PMXCommandProcessor):
    def __init__(self, mainWindow):
        super(PMXCommandProcessor, self).__init__()
        self.mainWindow = mainWindow

    def environment(self, command):
        environment = command.buildEnvironment()
        environment.update(self.mainWindow.buildEnvironment())
        environment.update(self.baseEnvironment)
        return environment

    def configure(self, settings):
        self.asynchronous = settings.get("asynchronous", True)
        self.baseEnvironment = settings.get("environment", {})
        self.errorCommand = settings.get("errorCommand", False)

    #beforeRunningCommand
    def saveModifiedFiles(self):
        ret = True
        for editor in self.mainWindow.editors():
            if editor.isModified():
                self.mainWindow.saveEditor(editor = editor)
                ret = ret and not editor.isModified()
            if ret == False:
                break
        return ret
    
    def saveActiveFile(self):
        editor = self.mainWindow.currentEditor()
        if editor is not None:
            self.mainWindow.saveEditor(editor = editor)
            return not (editor.isModified() or editor.isNew())
        return True
    
    # Outpus function
    def error(self, context):
        #TODO: Mover esto a un lugar donde no dependa del processor mostrar un error en el borwser, quiza a la mainWindow
        #para poder llamarlos como showErrorInBrowser o algo asi :)
        if self.errorCommand:
            #Prevenir la entrada recursiva
            raise Exception(context.errorValue)
        from prymatex.support.utils import makeHyperlinks
        from prymatex.utils import html
        commandScript = '''
            source "$TM_SUPPORT_PATH/lib/webpreview.sh" 
            
            html_header "An error has occurred while executing command %(name)s"
            echo -e "<pre>%(output)s</pre>"
            echo -e "<p>Exit code was: %(exitcode)d</p>"
            html_footer
        ''' % {'output': html.escape(context.errorValue),
               'name': html.escape(context.description()),
               'exitcode': context.outputType}
        command = self.mainWindow.application.supportManager.buildAdHocCommand(commandScript, context.bundleItem.bundle,
            name = "Error runing %s" % context.description(),
            commandOutput = 'showAsHTML')
        self.mainWindow.insertBundleItem(command, errorCommand = True)
        
    def showAsHTML(self, context):
        self.mainWindow.browser.setRunningContext(context)

    timespanFactor = 1
    def showAsTooltip(self, context):
        # Chicho's sense of statistics
        linesToRead = context.outputValue.count('\n') or context.outputValue.count('<br')
        if linesToRead > 10:
            timeout = 8000
        else:
            timeout = linesToRead * 700
            
        #TODO: Una mejor forma de mostrar en html la salida 
        cursor = self.mainWindow.textCursor()
        point = self.mainWindow.cursorRect(cursor).bottomRight()
        html = """
            <span>%s</span><hr>
            <div style='text-align: right; font-size: small;'><a href='copy'>Copy</a>
            </div>""" % context.outputValue.strip().replace('\n', '<br/>').replace(' ', '&nbsp;')
        timeout = timeout * self.timespanFactor
        callbacks = {
                   'copy': lambda s = context.outputValue: QtGui.qApp.instance().clipboard().setText(s)
        }
        pos = (point.x() + 30, point.y() + 5)
        timeout = timeout * self.timespanFactor
        
        self.mainWindow.showMessage(html, timeout = timeout, pos = pos, hrefCallbacks = callbacks)
        
    def createNewDocument(self, context):
        editor = self.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)
        
    def openAsNewDocument(self, context):
        editor = self.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)