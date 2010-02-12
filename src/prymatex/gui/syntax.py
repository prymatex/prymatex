from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData

from prymatex.lib.textmate.syntax import TMSyntaxProcessor 

class PMXToken(object):
    def __init__(self, begin, end, scopes):
        self.begin, self.end, self.scopes = begin, end, scopes

    def __str__(self):
        return '<token: Position: (%d, %d) Scopes: "%s...">' % (self.begin, self.end, self.scopes)

class PMXBlockUserData(QTextBlockUserData):
    def __init__(self, tokens):
        QTextBlockUserData.__init__(self)
        self.tokens = tokens
    
    def __str__(self):
        return ' '.join(map(str, self.tokens))
    
    def get_scope_at(self, pos):
        if len(self.tokens) == 1:
            return self.tokens[0].scopes
        tokens = filter(lambda t: t.begin < pos <= t.end, self.tokens)
        return tokens[0].scopes
        

class PMXSyntaxProcessor(QSyntaxHighlighter, TMSyntaxProcessor):
    def __init__(self, doc, syntax, style):
        QSyntaxHighlighter.__init__(self, doc)
        self.syntax = syntax
        self.style = style
    
    def highlightBlock(self, texto):
        print self.syntax.parse(unicode(texto), self)
        self.setCurrentBlockUserData(PMXBlockUserData(self.tokens))

    def start_parsing(self, scope, position):
        self.current_position = position
        self.tokens = []
        self.scopes = [ scope ]

    def end_parsing(self, scope, position):
        self.add_token(self.current_position, position, self.scopes[:])
        self.scopes.pop()

    def open_tag(self, scope, position):
        if self.current_position < position:
            self.add_token(self.current_position, position, self.scopes[:])
        self.scopes.append(scope)
        self.current_position = position

    def close_tag(self, scope, position):
        self.add_token(self.current_position, position, self.scopes[:])
        self.scopes.pop()
        self.current_position = position
    
    def add_token(self, begin, end, scopes):
        self.tokens.append(PMXToken(begin, end, " ".join(scopes)))
        print "%s, %s, %s" % (begin, end, " ".join(scopes))
        self.setFormat(begin, end - begin, self.style.get_format(scopes[-1]))


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
