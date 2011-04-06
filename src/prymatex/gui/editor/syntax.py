# -*- coding: utf-8 -*-
from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData
from PyQt4.QtGui import qApp
from prymatex.bundles.processor import PMXSyntaxProcessor

from logging import getLogger
logger = getLogger(__file__)


class PMXBlockUserData(QTextBlockUserData):
    FOLDING_NONE = 0
    FOLDING_START = -1
    FOLDING_STOP = -2
    
    def __init__(self):
        QTextBlockUserData.__init__(self)
        self.scopes = []
        self.folding = self.FOLDING_NONE
    
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
    
    if qApp.instance().options.profile_enabled:
        entries = qApp.instance().options.profile_entries 
        try:
            from prymatex.lib.profilehooks import profile
        except ImportError, e:
            logger.debug("Profile enabled but could not be imported")
            logger.info("Error was: %s", unicode(e))
        else:
            highlightBlock = profile(highlightBlock, entries = entries)
    
    def add_token(self, end):
        begin = self.line_position
        if self.discard_lines == 0:
            scopes = " ".join(self.scopes)
            self.user_data.addScope(begin, end, scopes)
            if self.formatter != None:
                if scopes not in self.FORMAT_CACHE:
                    self.FORMAT_CACHE[scopes] = self.formatter.getStyle(scopes).QTextFormat
                self.setFormat(begin, end - begin, self.FORMAT_CACHE[scopes])
        self.line_position = end
    
    def new_line(self, line):
        self.line_position = 0
        if self.discard_lines:
            self.discard_lines -= 1

    #START
    def start_parsing(self, scope):
        self.line_position = 0
        self.scopes = [ scope ]
        self.user_data = PMXBlockUserData()

    #OPEN
    def open_tag(self, scope, position):
        self.add_token(position)
        self.scopes.append(scope)

    #CLOSE
    def close_tag(self, scope, position):
        self.add_token(position)
        self.scopes.pop()

    def foldingMarker(self):
        line = unicode(self.currentBlock().text()).encode('utf-8')
        if self.syntax.foldingStartMarker != None and self.syntax.foldingStartMarker.match(line):
            self.user_data.folding = PMXBlockUserData.FOLDING_START
        elif self.syntax.foldingStopMarker != None and self.syntax.foldingStopMarker.match(line):
            if line.strip() == "":
                block = self.currentBlock().previous()
                while block.userData() != None and block.userData().folding == PMXBlockUserData.FOLDING_NONE:
                    block = block.previous()
                if block.userData() != None and block.userData().folding != PMXBlockUserData.FOLDING_STOP:
                    self.user_data.folding = PMXBlockUserData.FOLDING_STOP
            else:
                self.user_data.folding = PMXBlockUserData.FOLDING_STOP
    #END
    def end_parsing(self, scope):
        if self.scopes[-1] == scope:
            self.setCurrentBlockState(self.SINGLE_LINE)
        else:
            self.setCurrentBlockState(self.MULTI_LINE)
        self.add_token(self.currentBlock().length())
        self.scopes.pop()
        self.foldingMarker()
        self.setCurrentBlockUserData(self.user_data)
