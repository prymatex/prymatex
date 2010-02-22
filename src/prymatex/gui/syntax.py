from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData, QTextCharFormat, QColor, QFont
from prymatex.lib.textmate.syntax import TMSyntaxProcessor, TMScoreManager
from prymatex.lib.textmate.theme import TM_THEMES

class PMXSyntaxFormater(object):
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
        ss = PMXSyntaxFormater()
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
    SINGLE_LINE = 0
    MULTI_LINE = 1
    
    def __init__(self, doc, syntax, formater):
        QSyntaxHighlighter.__init__(self, doc)
        self.syntax = syntax
        self.formater = formater
        self.discard_lines = 0
    
    def collect_previous_text(self):
        self.discard_lines = 1
        text_blocks = []
        
        block = self.currentBlock().previous()
        while block.userState() == self.MULTI_LINE:
            text_blocks.insert(0, unicode(block.text()))
            self.discard_lines += 1
            block = block.previous()
        return '\n'.join(text_blocks)
    
    def highlightBlock(self, text):
        self.tokens = []
        self.scopes = []
        text = unicode(text)
        if self.previousBlockState() == self.MULTI_LINE:
            previous = self.collect_previous_text()
            text = previous + '\n' + text
            print text
            self.syntax.parse(text, self)
        else:
            self.syntax.parse(text, self)
    
    def add_token(self, begin, end, scope):
        if self.discard_lines == 0:
            self.tokens.append(PMXBlockToken(begin, end, scope))
            self.setFormat(begin, end - begin, self.formater.get_format(scope))
    
    def new_line(self, line):
        self.current_position = 0
        if self.discard_lines:
            self.discard_lines -= 1

    # Arranca el parser
    def start_parsing(self, scope):
        self.scopes.append(scope)

    # En cada oportunidad de se abre un tag
    def open_tag(self, scope, position):
        self.add_token(self.current_position, position, " ".join(self.scopes))
        self.current_position = position
        self.scopes.append(scope)

    def close_tag(self, scope, position):
        self.add_token(self.current_position, position, " ".join(self.scopes))
        self.current_position = position
        self.scopes.pop()

    def end_parsing(self, scope, closed):
        if closed:
            self.setCurrentBlockState(self.SINGLE_LINE)
        else:
            self.setCurrentBlockState(self.MULTI_LINE)
            self.add_token(self.current_position, self.currentBlock().length(), " ".join(self.scopes))
        self.setCurrentBlockUserData(PMXBlockUserData(self.tokens))
