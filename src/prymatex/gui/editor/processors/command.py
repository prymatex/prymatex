#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.support.processor import PMXCommandProcessor

class PMXCommandProcessor(PMXCommandProcessor):
    def __init__(self, editor):
        super(PMXCommandProcessor, self).__init__()
        self.editor = editor

    #Inputs
    def document(self, format = None):
        if format == "xml":
            result = u""
            block = self.editor.document().firstBlock()
            while block.isValid():
                text = unicode(block.text())
                for scope, start, end in block.userData().getAllScopes():
                    ss = scope.split()
                    result += "".join(map(lambda scope: "<" + scope + ">", ss))
                    result += text[start:end]
                    ss.reverse()
                    result += "".join(map(lambda scope: "</" + scope + ">", ss))
                result += "\n"
                block = block.next()
            return result
        else:
            return unicode(self.editor.document().toPlainText())
        
    def line(self, format = None):
        return self.environment['TM_CURRENT_LINE']
        
    def character(self, format = None):
        cursor = self.editor.textCursor()
        return cursor.document().characterAt(cursor.position()).toAscii()
        
    def scope(self, format = None):
        return self.environment['TM_SCOPE']
    
    def selection(self, format = None):
        if 'TM_SELECTED_TEXT' in self.environment:
            index = self.environment['TM_LINE_INDEX'] - len(self.environment['TM_SELECTED_TEXT'])
            index = index >= 0 and index or 0
            self.environment['TM_INPUT_START_COLUMN'] = self.environment['TM_CURRENT_LINE'].find(self.environment['TM_SELECTED_TEXT'], index)
            self.environment['TM_INPUT_START_LINE'] = self.environment['TM_LINE_NUMBER']
            self.environment['TM_INPUT_START_LINE_INDEX'] = self.environment['TM_CURRENT_LINE'].find(self.environment['TM_SELECTED_TEXT'], index)
            if format == "xml":
                cursor = self.editor.textCursor()
                bstart, bend = self.editor.getSelectionBlockStartEnd()
                result = u""
                if bstart == bend:
                    text = unicode(bstart.text())
                    scopes = bstart.userData().getAllScopes(start = cursor.selectionStart() - bstart.position(), end = cursor.selectionEnd() - bstart.position())
                    for scope, start, end in scopes:
                        ss = scope.split()
                        result += "".join(map(lambda scope: "<" + scope + ">", ss))
                        result += text[start:end]
                        ss.reverse()
                        result += "".join(map(lambda scope: "</" + scope + ">", ss))
                else:
                    block = bstart
                    while True:
                        text = unicode(block.text())
                        if block == bstart:
                            scopes = block.userData().getAllScopes(start = cursor.selectionStart() - block.position())
                        elif block == bend:
                            scopes = block.userData().getAllScopes(end = cursor.selectionEnd() - block.position())
                        else:
                            scopes = block.userData().getAllScopes()
                        for scope, start, end in scopes:
                            ss = scope.split()
                            result += "".join(map(lambda scope: "<" + scope + ">", ss))
                            result += text[start:end]
                            ss.reverse()
                            result += "".join(map(lambda scope: "</" + scope + ">", ss))
                        result += "\n"
                        block = block.next()
                        if block == bend:
                            break
                return result
            else:
                return self.environment['TM_SELECTED_TEXT']
        
    def selectedText(self, format = None):
        return self.selection
    
    def word(self, format = None):
        if 'TM_CURRENT_WORD' in self.environment:
            index = self.environment['TM_LINE_INDEX'] - len(self.environment['TM_CURRENT_WORD'])
            index = index >= 0 and index or 0
            self.environment['TM_INPUT_START_COLUMN'] = self.environment['TM_CURRENT_LINE'].find(self.environment['TM_CURRENT_WORD'], index)
            self.environment['TM_INPUT_START_LINE'] = self.environment['TM_LINE_NUMBER']
            self.environment['TM_INPUT_START_LINE_INDEX'] = self.environment['TM_CURRENT_LINE'].find(self.environment['TM_CURRENT_WORD'], index)
            return self.environment['TM_CURRENT_WORD']
    
    @property
    def environment(self, format = None):
        return self.__env
    
    #Interface
    def startCommand(self, command):
        self.command = command
        self.disableAutoIndent = True
        
        env = command.buildEnvironment()
        print env
        env.update(self.editor.buildEnvironment())
        self.__env = env

    #beforeRunningCommand
    def saveModifiedFiles(self):
        print "saveModifiedFiles"
        results = [self.editor.mainWindow.tabWidgetEditors.widget(i).reqquest_save() for i in range(0, self.editor.mainWindow.tabWidgetEditors.count())]
        return all(results)
    
    def saveActiveFile(self):
        print "saveActiveFile"
        value = self.editor.mainWindow.current_editor_widget.request_save()
        print value
        return value
    
    # deleteFromEditor
    def deleteWord(self):
        self.disableAutoIndent = False
        word, index = self.editor.getCurrentWordAndIndex()
        print word, index
        cursor = self.editor.textCursor()
        for _ in xrange(index):
            cursor.deletePreviousChar()
        for _ in xrange(len(word) - index):
            cursor.deleteChar()
        
    def deleteSelection(self):
        cursor = self.editor.textCursor()
        cursor.removeSelectedText()

    def deleteCharacter(self):
        cursor = self.editor.textCursor()
        cursor.deleteChar()
    
    def deleteDocument(self):
        self.editor.document().clear()
        
    # Outpus function
    def commandError(self, text, code):
        from prymatex.utils.pathutils import make_hyperlinks
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
        ''' % {'output': make_hyperlinks(text), 
               'name': self.command.name,
               'exit_code': code}
        self.showAsHTML(html)
        
    def discard(self, text):
        pass
        
    def replaceSelectedText(self, text):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            position = cursor.selectionStart()
            cursor.insertText(text)
            cursor.setPosition(position, position + len(text))
        else:
            cursor.insertText(text)
        self.editor.setTextCursor(cursor)
        
    def replaceDocument(self, text):
        self.editor.document().setPlainText(text)
        
    def insertText(self, text):
        cursor = self.editor.textCursor()
        cursor.insertText(text)
        
    def afterSelectedText(self, text):
        cursor = self.editor.textCursor()
        position = cursor.selectionEnd()
        cursor.setPosition(position)
        cursor.insertText(text)
        
    def insertAsSnippet(self, text):
        snippet = PMXSnippet("internal", hash = { 'content': text})
        snippet.bundle = self.command.bundle
        self.editor.insertBundleItem(snippet, disableIndent = self.disableAutoIndent)
            
    def showAsHTML(self, text):
        self.editor.mainWindow.paneBrowser.setHtml(text, self.command)
        self.editor.mainWindow.paneBrowser.show()
        
    def showAsTooltip(self, text):
        cursor = self.editor.textCursor()
        point = self.editor.viewport().mapToGlobal(self.editor.cursorRect(cursor).bottomRight())
        QToolTip.showText(point, text.strip(), self.editor, self.editor.rect())
        
    def createNewDocument(self, text):
        print "Nuevo documento", text
        
    def openAsNewDocument(self, text):
        editor_widget = self.editor.mainWindow.currentTabWidget.appendEmptyTab()
        editor_widget.codeEdit.setPlainText(text)