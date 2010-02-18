from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData, QTextCharFormat, QColor, QFont
from prymatex.lib.textmate.syntax import TMSyntaxProcessor, TMScoreManager
from prymatex.lib.textmate.theme import TM_THEMES

class PMXSyntaxStyle(object):
    def __init__(self):
        self.score = TMScoreManager()
        self.styles = {}
        self.default = None
        self.formats = {}
    
    def add_format(self, scope, format):
        self.styles[scope] = format
    
    def get_format(self, scope):
        if not (self.formats.has_key(scope)):
            self.formats[scope] = self.__search_format( scope )
        print scope, self.formats[scope]
        return self.formats[scope]
    
    def __search_format(self, reference_scope):
        score, format = 0, self.default 
        for search_scope in self.styles.keys():
            tmp_score, tmp_format = self.score.score(search_scope, reference_scope), self.styles[search_scope]
            if tmp_score > score:
                score, format = tmp_score, tmp_format
        return format
    
    @classmethod
    def build_format_from_style(cls, style):
        format = QTextCharFormat()
        if 'foreground' in style:
            format.setForeground(QColor(style['foreground']))
        if 'background' in style:
            format.setBackground(QColor(style['background']))
        if 'fontStyle' in style:
            if style['fontStyle'] == 'bold':
                format.setFontWeight(QFont.Bold)
            elif style['fontStyle'] == 'underline':
                format.setFontUnderline(True)
            elif style['fontStyle'] == 'italic':
                format.setFontItalic(True)
        return format
    
    @classmethod
    def load_from_textmate_theme(cls, theme_name):
        assert theme_name in TM_THEMES, 'No textmate theme for %s' % theme_name
        theme = TM_THEMES[theme_name] 
        ss = PMXSyntaxStyle()
        ss.default = cls.build_format_from_style(theme.default)
        for scope, style in theme.items():
            ss.add_format(scope, cls.build_format_from_style(style))
        return ss

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
        self.setFormat(self.current_position, position - self.current_position, self.style.get_format(" ".join(self.scopes)))
        self.current_position = position
        self.scopes.append(scope)

    def close_tag(self, scope, position):
        # TODO: Validar
        print self.current_position, position
        self.tokens.append(PMXBlockToken(self.current_position, position, " ".join(self.scopes)))
        self.setFormat(self.current_position, position - self.current_position, self.style.get_format(" ".join(self.scopes)))
        self.current_position = position
        self.scopes.pop()

    def end_parsing(self, scope, position, stack):
        # TODO: Validar
        self.tokens.append(PMXBlockToken(self.current_position, position, " ".join(self.scopes)))
        self.setFormat(self.current_position, position - self.current_position, self.style.get_format(" ".join(self.scopes)))
        print stack
        if len(stack) > 1:
            user_data = PMXBlockUserData(self.tokens, self.scopes[:], stack[:])
            self.setCurrentBlockState(self.MULTI_LINE)
        else:
            user_data = PMXBlockUserData(self.tokens)
            self.setCurrentBlockState(self.SINGLE_LINE)
            self.scopes.pop()
        self.setCurrentBlockUserData(user_data)
