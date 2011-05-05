# -*- coding: utf-8 -*-
import re
from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData, QToolTip, QTextCursor
from prymatex.bundles import PMXSyntaxProcessor, PMXCommandProcessor, PMXMacroProcessor, PMXSnippet, PMXSyntax, PMXPreferenceSettings, PMXBundle

from logging import getLogger
logger = getLogger(__file__)

WHITESPACE = re.compile(r'^(?P<whitespace>\s+)', re.UNICODE)
def whiteSpace(text):
    match = WHITESPACE.match(text)
    try:
        ws = match.group('whitespace')
        return ws
    except AttributeError:
        return ''

# Syntax
class PMXBlockUserData(QTextBlockUserData):
    FOLDING_NONE = PMXSyntax.FOLDING_NONE
    FOLDING_START = PMXSyntax.FOLDING_START
    FOLDING_STOP = PMXSyntax.FOLDING_STOP
    INDENT_NONE = PMXPreferenceSettings.INDENT_NONE
    INDENT_INCREASE = PMXPreferenceSettings.INDENT_INCREASE
    INDENT_DECREASE = PMXPreferenceSettings.INDENT_DECREASE
    INDENT_NEXTLINE = PMXPreferenceSettings.INDENT_NEXTLINE
    UNINDENT = PMXPreferenceSettings.UNINDENT
    
    def __init__(self):
        QTextBlockUserData.__init__(self)
        self.scopes = []
        self.folding = self.FOLDING_NONE
        self.foldingLevel = 0
        #self.foldingPeer = None
        self.folded = False
        self.indentMark = self.INDENT_NONE
        self.indent = ""
    
    def __nonzero__(self):
        return bool(self.scopes)
    
    def getLastScope(self):
        return self.scopes[-1]
    
    def addScope(self, begin, end, scope):
        for pos in xrange(end - begin):
            self.scopes.insert(begin + pos, scope)
        
    def getScopeAtPosition(self, pos):
        return self.scopes[pos]
    
    def getAllScopes(self, start = 0, end = None):
        current = ( self.scopes[start], start )
        scopes = []
        for index, scope in enumerate(self.scopes[start:], start):
            if scope != current[0] or (end != None and index == end):
                scopes.append(( current[0], current[1], index ))
                current = ( scope, index )
                if end != None and index == end:
                    break
        return scopes
    
class PMXSyntaxProcessor(QSyntaxHighlighter, PMXSyntaxProcessor):
    SINGLE_LINE = 0
    MULTI_LINE = 1
    FORMAT_CACHE = {}
    
    def __init__(self, editor):
        QSyntaxHighlighter.__init__(self, editor.document())
        self.editor = editor
        self.__syntax = None
        self.__formatter = None

    def getSyntax(self):
        return self.__syntax
    def setSyntax(self, syntax):
        self.__syntax =  syntax
        self.rehighlight()
    syntax = property(getSyntax, setSyntax)
    
    def getFormatter(self):
        return self.__formatter
    def setFormatter(self, formatter):
        self.__formatter =  formatter
        #Deprecate cache
        self.__formatter.clearCache()
        PMXSyntaxProcessor.FORMAT_CACHE = {}
        self.rehighlight()
    formatter = property(getFormatter, setFormatter)

    def collectPreviousText(self, current):
        text = [ current ]
        block = self.currentBlock().previous()
        
        while block.userState() == self.MULTI_LINE:
            text.append(unicode(block.text()))
            block = block.previous()
        text.reverse()
        return text
    
    def highlightBlock(self, text):
        #block = self.currentBlock()
        text = unicode(text)
        if self.previousBlockState() == self.MULTI_LINE:
            text = self.collectPreviousText(text)
            self.discard_lines = len(text)
            text = "\n".join( text )
        else:  
            self.discard_lines = 0
        self.syntax.parse(text, self)

    def blockRange(self, block):
        first = self.editor.firstVisibleBlock()
        page_bottom = self.editor.viewport().height()
        viewport_offset = self.editor.contentOffset()
        first_position = self.editor.blockBoundingGeometry(first).topLeft() + viewport_offset
        block_position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
        return first_position.y() <= block_position.y() <= page_bottom

    def addToken(self, end):
        begin = self.line_position
        if self.discard_lines == 0:
            scopes = " ".join(self.scopes)
            self.userData.addScope(begin, end, scopes)
            if self.formatter != None:
                if scopes not in PMXSyntaxProcessor.FORMAT_CACHE:
                    PMXSyntaxProcessor.FORMAT_CACHE[scopes] = self.formatter.getStyle(scopes).QTextFormat
                self.setFormat(begin, end - begin, PMXSyntaxProcessor.FORMAT_CACHE[scopes])
        self.line_position = end
    
    def newLine(self, line):
        self.line_position = 0
        if self.discard_lines:
            self.discard_lines -= 1

    #START
    def startParsing(self, scope):
        self.line_position = 0
        self.scopes = [ scope ]
        self.userData = self.currentBlock().userData()
        if self.userData == None:
            self.setCurrentBlockUserData(PMXBlockUserData())
        self.userData = self.currentBlock().userData()

    #OPEN
    def openTag(self, scope, position):
        self.addToken(position)
        self.scopes.append(scope)

    #CLOSE
    def closeTag(self, scope, position):
        self.addToken(position)
        self.scopes.pop()

    def foldingMarker(self, line):
        self.userData.folding = self.syntax.folding(line)
        if self.syntax.indentSensitive and self.userData.folding == self.syntax.FOLDING_STOP and line.strip() == "":
            self.userData.folding = self.syntax.FOLDING_NONE

    def indentMarker(self, line, scope):
        settings = PMXBundle.getPreferenceSettings(scope)
        self.userData.indentMark = settings.indent(line)
        if self.syntax.indentSensitive and line.strip() == "":
            prev = self.currentBlock().previous()
            self.userData.indent = prev.userData().indent if prev.isValid() else ""
        else: 
            self.userData.indent = whiteSpace(line)

    #END
    def endParsing(self, scope):
        if self.scopes[-1] == scope:
            self.setCurrentBlockState(self.SINGLE_LINE)
        else:
            self.setCurrentBlockState(self.MULTI_LINE)
        self.addToken(self.currentBlock().length())
        self.scopes.pop()
        
        line = unicode(self.currentBlock().text())
        self.foldingMarker(line)
        self.indentMarker(line, scope)
        
        #self.setCurrentBlockUserData(self.userData)

# Command
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
                start, end = self.editor.getSelectionBlockStartEnd()
                print start, end
                result = u""
                if start == end:
                    text = unicode(start.text())
                    scopes = start.userData().getAllScopes(start = cursor.selectionStart() - start.position(), end = cursor.selectionEnd() - start.position())
                    for scope, start, end in scopes:
                        ss = scope.split()
                        result += "".join(map(lambda scope: "<" + scope + ">", ss))
                        result += text[start:end]
                        ss.reverse()
                        result += "".join(map(lambda scope: "</" + scope + ">", ss))
                else:
                    block = start
                    while True:
                        text = unicode(block.text())
                        if block == start:
                            print cursor.selectionStart() - block.position()
                            scopes = block.userData().getAllScopes(start = cursor.selectionStart() - block.position())
                        elif block == end:
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
                        if block == end or block == None:
                            print result
                            break
                print result
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
        env.update(self.editor.buildEnvironment())
        #env.update(self.editor.mainwindow._meta.settings['static_variables'])
        self.__env = env

    #beforeRunningCommand
    def saveModifiedFiles(self):
        print "saveModifiedFiles"
        results = [self.editor.mainwindow.tabWidgetEditors.widget(i).reqquest_save() for i in range(0, self.editor.mainwindow.tabWidgetEditors.count())]
        return all(results)
    
    def saveActiveFile(self):
        print "saveActiveFile"
        value = self.editor.mainwindow.current_editor_widget.request_save()
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
        snippet = PMXSnippet({ 'content': text})
        snippet.bundle = self.command.bundle
        self.editor.insertBundleItem(snippet, disableIndent = self.disableAutoIndent)
            
    def showAsHTML(self, text):
        self.editor.mainwindow.paneBrowser.setHtml(text, self.command)
        self.editor.mainwindow.paneBrowser.show()
        
    def showAsTooltip(self, text):
        cursor = self.editor.textCursor()
        point = self.editor.viewport().mapToGlobal(self.editor.cursorRect(cursor).bottomRight())
        QToolTip.showText(point, text.strip(), self.editor, self.editor.rect())
        
    def createNewDocument(self, text):
        print "Nuevo documento", text
        
    def openAsNewDocument(self, text):
        editor_widget = self.editor.mainwindow.currentTabWidget.appendEmptyTab()
        editor_widget.codeEdit.setPlainText(text)

# Macro
class PMXMacroProcessor(PMXMacroProcessor):
    def __init__(self, editor):
        super(PMXMacroProcessor, self).__init__()
        self.editor = editor
    
    # Move
    def moveRight(self):
        cursor = self.editor.textCursor()
        cursor.setPosition(cursor.position() + 1)
        self.editor.setTextCursor(cursor)
   
    def moveLeft(self):
        cursor = self.editor.textCursor()
        cursor.setPosition(cursor.position() - 1)
        self.editor.setTextCursor(cursor)
        
    def selectHardLine(self):
        cursor = self.editor.textCursor()
        block = cursor.block()
        start = block.position()
        next = block.next()
        end = next.position() if next.isValid() else start + block.length() - 1
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)
        
    def deleteBackward(self):
        self.editor.textCursor().deletePreviousChar()