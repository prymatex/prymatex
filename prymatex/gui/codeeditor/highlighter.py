import re
from PyQt4 import QtGui

from prymatex.gui.codeeditor.processors import PMXSyntaxProcessor
from prymatex.gui.codeeditor.userdata import PMXBlockUserData
from prymatex.support.syntax import PMXSyntax

WHITESPACE = re.compile(r'^(?P<whitespace>\s+)', re.UNICODE)
def whiteSpace(text):
    match = WHITESPACE.match(text)
    try:
        ws = match.group('whitespace')
        return ws
    except AttributeError:
        return ''

class PMXSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    NO_STATE = -1
    SINGLE_LINE = 0
    MULTI_LINE = 1
    FORMAT_CACHE = {}
    
    def __init__(self, editor, syntax, theme = None):
        super(PMXSyntaxHighlighter, self).__init__(editor.document())
        assert syntax is not None, "Syntax cannot be None"
        self.editor = editor
        self.processor = PMXSyntaxProcessor()
        self.syntax = syntax
        self.theme = theme

    def setTheme(self, theme):
        PMXSyntaxHighlighter.FORMAT_CACHE = {}
        self.theme = theme
    
    def hasTheme(self):  
        return self.theme is not None
    
    def _analyze_all_text(self, text):
        self.syntax.parse(text, self.processor)
        for index, data in enumerate(self.processor.lines):
            block = self.document().findBlockByNumber(index)
            userData, state = self.buildBlockUserData(block, data)
            block.setUserData(userData)
            block.setUserState(state)
    
    def applyFormat(self, userData):
        for scope, start, end in userData.getAllScopes():
            format = self.getFormat(scope)
            if format is not None:
                self.setFormat(start, end - start, format)
    
    def setupBlockUserData(self, text, userData, data):
        state = self.SINGLE_LINE
        userData.setScopes(data[0])
        if data[1] is not None:
            state = self.MULTI_LINE
            userData.setStackAndScopes(*data[1])
        
        #1 Update Indent
        userData.indent = whiteSpace(text)
        
        #2 Update Folding
        foldingMark = self.syntax.folding(text)
        if userData.foldingMark != foldingMark:
            userData.foldingMark = foldingMark
            if userData.foldingMark == None:
                self.editor.folding.removeFoldingBlock(self.currentBlock())
            else:
                self.editor.folding.addFoldingBlock(self.currentBlock())

        #3 Update Symbols
        preferences = map(lambda (scope, start, end): (self.editor.getPreference(scope), start, end), userData.getAllScopes())
        
        symbolRange = filter(lambda (preference, start, end): preference.showInSymbolList == 1, preferences)
        if symbolRange:
            symbol = text[symbolRange[0][1]:symbolRange[-1][2]]
            symbol = symbolRange[0][0].transformSymbol(symbol)
        else:
            symbol = None

        if userData.symbol != symbol:
            userData.symbol = symbol
            if userData.symbol == None:
                self.editor.symbols.removeSymbolBlock(self.currentBlock())
            else:
                self.editor.symbols.addSymbolBlock(self.currentBlock())

        #4 Save the hash the text, scope and state
        userData.textHash = hash(text) + hash(self.syntax.scopeName) + state

        return state

    def highlightBlock(self, text):
        userData = self.currentBlock().userData()
        if userData is not None and userData.textHash == hash(text) + hash(self.syntax.scopeName) + self.previousBlockState():
            self.applyFormat(userData)
        else:
            self.processor.startParsing(self.syntax.scopeName)
            if self.previousBlockState() == self.MULTI_LINE:
                #Recupero una copia del stack y los scopes del user data
                stack, scopes = self.currentBlock().previous().userData().getStackAndScopes()
                self.processor.setScopes(scopes)
            else:
                #Creo un stack y scopes nuevos
                stack = [[self.syntax.grammar, None]]
    
            # A parserar mi amor, vamos a parsear mi amor
            self.syntax.parseLine(stack, text, self.processor)
            
            data = self.processor.lines[-1]
            if userData is None:
                userData = PMXBlockUserData()
                self.setCurrentBlockUserData(userData)

            oldSymbol = userData.symbol
            oldFoldingMark = userData.foldingMark

            state = self.setupBlockUserData(text, userData, data)
            self.setCurrentBlockState(state)

            self.applyFormat(userData)

    def getFormat(self, scope):
        if self.theme is None:
            return None
        if scope not in PMXSyntaxHighlighter.FORMAT_CACHE: 
            format = QtGui.QTextCharFormat()
            settings = self.theme.getStyle(scope)
            if 'foreground' in settings:
                format.setForeground(settings['foreground'])
            if 'background' in settings:
                format.setBackground(settings['background'])
            if 'fontStyle' in settings:
                if 'bold' in settings['fontStyle']:
                    format.setFontWeight(QtGui.QFont.Bold)
                if 'underline' in settings['fontStyle']:
                    format.setFontUnderline(True)
                if 'italic' in settings['fontStyle']:
                    format.setFontItalic(True)
            PMXSyntaxHighlighter.FORMAT_CACHE[scope] = format 
        return PMXSyntaxHighlighter.FORMAT_CACHE[scope]
