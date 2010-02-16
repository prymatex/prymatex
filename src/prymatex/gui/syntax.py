from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData

from prymatex.lib.textmate.syntax import TMSyntaxProcessor 

class PMXBlockToken(object):
    def __init__(self, begin, end, scopes):
        self.begin, self.end, self.scopes = begin, end, scopes

    def __str__(self):
        return '<token: Position: (%d, %d) Scopes: "%s...">' % (self.begin, self.end, self.scopes)

class PMXBlockUserData(QTextBlockUserData):
    def __init__(self, tokens, scopes = [], stack = None):
        QTextBlockUserData.__init__(self)
        self.tokens = tokens
        self.scopes = scopes
        self.stack = stack
    
    def __str__(self):
        return ' '.join(map(str, self.tokens))
    
    def get_scope_at(self, pos):
        if len(self.tokens) == 1:
            return self.tokens[0].scopes
        tokens = filter(lambda t: t.begin < pos <= t.end, self.tokens)
        return tokens[0].scopes
        

class PMXSyntaxProcessor(QSyntaxHighlighter, TMSyntaxProcessor):
    NO_STATE_SET = -1
    SINGLE_LINE = 0
    MULTI_LINE = 1
    def __init__(self, doc, syntax, style):
        QSyntaxHighlighter.__init__(self, doc)
        self.syntax = syntax
        self.style = style
    
    def highlightBlock(self, texto):
        self.tokens = []
        if self.previousBlockState() == self.NO_STATE_SET or self.previousBlockState() == self.SINGLE_LINE:
            self.scopes = []
            self.syntax.parse(unicode(texto), self)
        elif self.previousBlockState() == self.MULTI_LINE:
            user_data = self.currentBlock().previous().userData()
            self.scopes = user_data.scopes
            self.syntax.parse(unicode(texto), self, user_data.stack)

    # Arranca el parser
    def start_parsing(self, scope, position, stack):
        self.current_position = position
        if len(stack) == 1:
            self.scopes.append(scope)

    # En cada oportunidad de se abre un tag
    def open_tag(self, scope, position):
        # TODO: Validar
        print self.current_position, position
        self.tokens.append(PMXBlockToken(self.current_position, position, " ".join(self.scopes)))
        self.current_position = position
        self.scopes.append(scope)

    def close_tag(self, scope, position):
        # TODO: Validar
        print self.current_position, position
        self.tokens.append(PMXBlockToken(self.current_position, position, " ".join(self.scopes)))
        self.current_position = position
        self.scopes.pop()

    def end_parsing(self, scope, position, stack):
        # TODO: Validar
        self.tokens.append(PMXBlockToken(self.current_position, position, " ".join(self.scopes)))
        print stack
        if len(stack) > 1:
            user_data = PMXBlockUserData(self.tokens, self.scopes[:], stack[:])
            self.setCurrentBlockState(self.MULTI_LINE)
        else:
            user_data = PMXBlockUserData(self.tokens)
            self.setCurrentBlockState(self.SINGLE_LINE)
            self.scopes.pop()
        self.setCurrentBlockUserData(user_data)

class TMDebugSyntaxProcessor(TMSyntaxProcessor):
    def __init__(self):
        self.line_number = 0
        self.printable_line = ''

    def pprint(self, line, string, position = 0):
        line = line[:position] + string + line[position:]
        return line

    def open_tag(self, name, position):
        print self.pprint( '', '{ %s' % name, position + len(self.line_marks))

    def close_tag(self, name, position):
        print self.pprint( '', '} %s' % name, position + len(self.line_marks))

    def new_line(self, line):
        self.line_number += 1
        self.line_marks = '[%04s] ' % self.line_number
        print '%s%s' % (self.line_marks, line)
