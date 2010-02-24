# -*- coding: utf-8 -*-
from PyQt4.Qt import QSyntaxHighlighter, QTextBlockUserData, QTextCharFormat, QColor, QFont
from prymatex.lib.textmate.syntax import TMSyntaxProcessor, TMScoreManager
from prymatex.lib.textmate.theme import TM_THEMES

class PMXSyntaxFormatter(object):
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
        ss = PMXSyntaxFormatter()
        ss.default = cls.build_format_from_style(theme.default)
        for scope, style in theme.items():
            ss.add_format(scope, cls.build_format_from_style(style))
        return ss

class PMXBlockToken(object):
    def __init__(self, begin, end, scopes):
        self.begin = begin
        self.end = end
        self.scopes = scopes

    def __str__(self):
        return '<token: Position: (%d, %d) Scopes: "%s...">' % (self.begin, self.end, self.scopes)

class PMXBlockUserData(QTextBlockUserData):
    def __init__(self, root):
        QTextBlockUserData.__init__(self)
        self.root = root
        self.tokens = []
    
    def __str__(self):
        return ' '.join(map(str, self.tokens))
    
    def add_token(self, token):
        self.tokens.append(token)
        
    def get_scope_at(self, pos):
        tokens = filter(lambda t: t.begin < pos <= t.end, self.tokens)
        if not tokens:
            return self.root
        if len(tokens) == 1:
            return self.root + " " + tokens[-1].scopes
        else:
            raise Exception("WTF? muchos tokens")
        
class PMXSyntaxProcessor(QSyntaxHighlighter, TMSyntaxProcessor):
    SINGLE_LINE = 0
    MULTI_LINE = 1
    
    def __init__(self, doc, syntax, formatter):
        QSyntaxHighlighter.__init__(self, doc)
        self.syntax = syntax
        self.formatter = formatter
    
    def collect_all_text(self, current):
        text = [ current ]
        block = self.currentBlock().previous()
        
        while block.userState() == self.MULTI_LINE:
            text.append(unicode(block.text()))
            block = block.previous()
        text.reverse()
        return text
    
    def highlightBlock(self, text):
        text = unicode(text)
        if self.previousBlockState() == self.MULTI_LINE:
            text = self.collect_all_text(text)
            self.discard_lines = len(text)
            text = "\n".join( text )
        else:  
            self.discard_lines = 0
        self.syntax.parse(text, self)
    
    def add_token(self, begin, end):
        if self.discard_lines == 0:
            scopes = " ".join(self.scopes)
            self.user_data.add_token(PMXBlockToken(begin, end, scopes))
            self.setFormat(begin, end - begin, self.formatter.get_format(scopes))
    
    def new_line(self, line):
        self.current_position = 0
        if self.discard_lines:
            self.discard_lines -= 1

    # Arranca el parser
    def start_parsing(self, scope):
        self.scopes = []
        self.user_data = PMXBlockUserData(scope)

    # En cada oportunidad de se abre un tag
    def open_tag(self, scope, position):
        self.add_token(self.current_position, position)
        self.current_position = position
        self.scopes.append(scope)

    def close_tag(self, scope, position):
        if self.scopes[-1] != scope:
            raise Exception('Bad scope close "%s"' % scope)
        self.add_token(self.current_position, position)
        self.current_position = position
        self.scopes.pop()

    def end_parsing(self, scope):
        if len(self.scopes) == 0:
            self.setCurrentBlockState(self.SINGLE_LINE)
        else:
            self.setCurrentBlockState(self.MULTI_LINE)
            self.add_token(self.current_position, self.currentBlock().length())
        self.setCurrentBlockUserData(self.user_data)
