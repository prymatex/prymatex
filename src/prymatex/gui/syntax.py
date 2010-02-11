from PyQt4.Qt import QSyntaxHighlighter

from prymatex.lib.textmate.syntax import TMSyntaxProcessor 

class Token(object):
    def __init__(self, begin, end, scopes):
        self.begin, self.end, self.scopes = begin, end, scopes

    def __str__(self):
        return '<token: Position: (%d, %d) Scopes: "%s...">' % (self.begin, self.end, ', '.join(self.scopes))

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
        self.tokens = Token(begin, end, scopes)
        print "%s, %s, %s" % (begin, end - begin, " ".join(scopes))
        self.setFormat(begin, end - begin, self.style.get_format(scopes[-1]))
