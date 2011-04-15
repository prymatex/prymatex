# -*- coding: utf-8 -*-
from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData
from prymatex.bundles import PMXSyntaxProcessor, PMXSyntax, PMXPreferenceSettings, PMXBundle

from logging import getLogger
logger = getLogger(__file__)


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
        self.indent = self.INDENT_NONE
        self.indentLevel = 0
    
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

    def indentMarker(self, line, scope):
        settings = PMXBundle.getPreferenceSettings(scope)
        self.userData.indent = settings.indent(line)
        self.userData.indentLevel = self.editor.indentationWhitespace(line)

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
