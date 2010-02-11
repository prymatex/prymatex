from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData

from prymatex.lib.textmate.syntax import TMSyntaxProcessor 

class PMXToken(object):
    def __init__(self, begin, end, scopes):
        self.begin, self.end, self.scopes = begin, end, scopes

    def __str__(self):
        return '<token: Position: (%d, %d) Scopes: "%s...">' % (self.begin, self.end, self.scopes)

class PMXUserData(QTextBlockUserData):
    def __init__(self, tokens):
        QTextBlockUserData.__init__(self)
        self.tokens = tokens
    
    def __str__(self):
        return ' '.join(map(str, self.tokens))
    
    def get_scope_at(self, pos):
        tokens = filter(lambda t: t.begin <= pos <= t.end, self.tokens)
        if not tokens:
            #TODO: Rtornar la syntax
            return 'No scope' 
        elif len(tokens) > 1:
            raise Exception("Multiples scopes :S")
        return tokens[0].scopes
        

class PMXSyntaxProcessor(QSyntaxHighlighter, TMSyntaxProcessor):
    def __init__(self, doc, syntax, style):
        QSyntaxHighlighter.__init__(self, doc)
        self.syntax = syntax
        self.style = style
    
    def highlightBlock(self, texto):
        stack = [[self.syntax, None]]
        self.tokens = []
        self.scopes = []
        self.current_position = None
        self.syntax.parse_line(stack, unicode(texto), self)
        self.setCurrentBlockUserData(PMXUserData(self.tokens))

    def open_tag(self, name, position):
        self.scopes.append(name)
        if self.current_position != None:
            self.add_token(self.current_position, position, self.scopes[:])
        self.current_position = position

    def close_tag(self, name, position):
        if self.current_position == None or name != self.scopes[-1]:
            raise Exception('Error al parsear un token.')
        self.add_token(self.current_position, position, self.scopes[:])
        self.scopes.pop()
        self.current_position = position
    
    def add_token(self, begin, end, scopes):
        self.tokens.append(PMXToken(begin, end, " ".join(scopes)))
        print "%s, %s, %s" % (begin, end - begin, " ".join(scopes))
        self.setFormat(begin, end - begin, self.style.get_format(scopes[-1]))
