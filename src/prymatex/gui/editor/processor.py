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
    def setFormatter(self, syntax):
        self.__formatter =  syntax
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
        if not self.syntax:
            return
        text = unicode(text)
        if self.previousBlockState() == self.MULTI_LINE:
            text = self.collectPreviousText(text)
            self.discard_lines = len(text)
            text = "\n".join( text )
        else:  
            self.discard_lines = 0
        self.syntax.parse(text, self)
    
    def addToken(self, end):
        begin = self.line_position
        if self.discard_lines == 0:
            scopes = " ".join(self.scopes)
            self.userData.addScope(begin, end, scopes)
            if self.formatter != None:
                if scopes not in self.FORMAT_CACHE:
                    self.FORMAT_CACHE[scopes] = self.formatter.getStyle(scopes).QTextFormat
                self.setFormat(begin, end - begin, self.FORMAT_CACHE[scopes])
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
    @property
    def document(self):
        return unicode(self.editor.toPlainText())
        
    @property
    def line(self):
        return self.environment['TM_CURRENT_LINE']
        
    @property
    def character(self):
        cursor = self.editor.textCursor()
        return cursor.document().characterAt(cursor.position()).toAscii()
        
    @property
    def scope(self):
        return self.environment['TM_SCOPE']
        
    @property
    def selection(self):
        if 'TM_SELECTED_TEXT' in self.environment:
            index = self.environment['TM_LINE_INDEX'] - len(self.environment['TM_SELECTED_TEXT'])
            index = index >= 0 and index or 0
            self.environment['TM_INPUT_START_COLUMN'] = self.environment['TM_CURRENT_LINE'].find(self.environment['TM_SELECTED_TEXT'], index)
            self.environment['TM_INPUT_START_LINE'] = self.environment['TM_LINE_NUMBER']
            self.environment['TM_INPUT_START_LINE_INDEX'] = self.environment['TM_CURRENT_LINE'].find(self.environment['TM_SELECTED_TEXT'], index)
            return self.environment['TM_SELECTED_TEXT']
        
    @property
    def selectedText(self):
        return self.selection
    
    @property
    def word(self):
        if 'TM_CURRENT_WORD' in self.environment:
            index = self.environment['TM_LINE_INDEX'] - len(self.environment['TM_CURRENT_WORD'])
            index = index >= 0 and index or 0
            self.environment['TM_INPUT_START_COLUMN'] = self.environment['TM_CURRENT_LINE'].find(self.environment['TM_CURRENT_WORD'], index)
            self.environment['TM_INPUT_START_LINE'] = self.environment['TM_LINE_NUMBER']
            self.environment['TM_INPUT_START_LINE_INDEX'] = self.environment['TM_CURRENT_LINE'].find(self.environment['TM_CURRENT_WORD'], index)
            return self.environment['TM_CURRENT_WORD']

    @property
    def environment(self):
        return self.__env
    
    def startCommand(self, command):
        self.command = command
        
        env = command.buildEnvironment()
        env.update(self.editor.buildEnvironment())
        #env.update(self.editor.mainwindow._meta.settings['static_variables'])
        self.__env = env

    #beforeRunningCommand
    def saveModifiedFiles(self):
        return self.editor.mainwindow.on_actionSaveAll_triggered()
    
    def saveActiveFile(self):
        return self.editor.mainwindow.on_actionSave_triggered()
    
    # deleteFromEditor
    def deleteWord(self):
        cursor = self.editor.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        cursor.removeSelectedText()
        
    def deleteSelection(self):
        cursor = self.editor.textCursor()
        cursor.removeSelectedText()

    def deleteCharacter(self):
        cursor = self.editor.textCursor()
        cursor.deleteChar()
        
    # Outpus function
    def discard(self, text):
        pass
        
    def replaceSelectedText(self, text):
        cursor = self.editor.textCursor()
        position = cursor.selectionStart()
        cursor.insertText(text)
        cursor.setPosition(position, position + len(text))
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
        self.editor.insertBundleItem(snippet, indent = False)
            
    def showAsHTML(self, text):
        self.editor.mainwindow.paneBrowser.setHtml(text, self.command)
        self.editor.mainwindow.paneBrowser.show()
        
    def showAsTooltip(self, text):
        cursor = self.editor.textCursor()
        point = self.editor.viewport().mapToGlobal(self.editor.cursorRect(cursor).bottomRight())
        QToolTip.showText(point, text.strip(), self.editor, self.editor.rect())
        
    def createNewDocument(self, text):
        print "Nuevo documento", text

# Macro
class PMXMacroProcessor(PMXMacroProcessor):
    def __init__(self, editor):
        super(PMXMacroProcessor, self).__init__()
        self.editor = editor
