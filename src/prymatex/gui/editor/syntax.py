# -*- coding: utf-8 -*-
from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData, QTextCharFormat, QColor, QFont
from prymatex.bundles.processor import PMXSyntaxProcessor

class PMXBlockToken(object):
    def __init__(self, begin, end, scopes):
        self.begin = begin
        self.end = end
        self.scopes = scopes

    def __str__(self):
        return '<token: Position: (%d, %d) Scopes: "%s...">' % (self.begin, self.end, self.scopes)

class PMXBlockUserData(QTextBlockUserData):
    FOLDING_NONE = 0
    FOLDING_START = 1
    FOLDING_STOP = -1
    
    def __init__(self):
        QTextBlockUserData.__init__(self)
        self.tokens = []
        self.folding = self.FOLDING_NONE
    
    def __str__(self):
        return ' '.join(map(str, self.tokens))
    
    def add_token(self, token):
        self.tokens.append(token)
        
    def getScopeAtPosition(self, pos):
        tokens = filter(lambda t: t.begin <= pos < t.end, self.tokens)
        if len(tokens) == 1:
            return tokens[-1].scopes
        else:
            raise Exception("WTF? muchos tokens")
        
class PMXSyntaxProcessor(QSyntaxHighlighter, PMXSyntaxProcessor):
    SINGLE_LINE = 0
    MULTI_LINE = 1
    
    def __init__(self, doc, syntax = None, formatter = None):
        QSyntaxHighlighter.__init__(self, doc)
        self.syntax = syntax
        self.formatter = formatter
    
    def collect_previous_text(self, current):
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
            text = self.collect_previous_text(text)
            self.discard_lines = len(text)
            text = "\n".join( text )
        else:  
            self.discard_lines = 0
        self.syntax.parse(text, self)
    
    def set_syntax(self, syntax):
        self.syntax =  syntax
        self.rehighlight()
    
    def add_token(self, end):
        begin = self.line_position
        if self.discard_lines == 0:
            scopes = " ".join(self.scopes)
            self.user_data.add_token(PMXBlockToken(begin, end, scopes))
            self.setFormat(begin, end - begin, self.formatter.getStyle(scopes).QTextFormat)
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

    def folding_marker(self):
        if hasattr(self.syntax, 'foldingStartMarker') and self.syntax.foldingStartMarker.match(unicode(self.currentBlock().text())):
            self.user_data.folding = self.user_data.FOLDING_START
        elif hasattr(self.syntax, 'foldingStopMarker') and self.syntax.foldingStopMarker.match(unicode(self.currentBlock().text())):
            self.user_data.folding = self.user_data.FOLDING_STOP
        else: 
            self.user_data.folding = self.user_data.FOLDING_NONE
        
    #END
    def end_parsing(self, scope):
        if self.scopes[-1] == scope:
            self.setCurrentBlockState(self.SINGLE_LINE)
        else:
            self.setCurrentBlockState(self.MULTI_LINE)
        self.add_token(self.currentBlock().length())
        self.scopes.pop()
        self.folding_marker()
        self.setCurrentBlockUserData(self.user_data)
