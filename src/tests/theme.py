#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, sys, glob, plistlib
from pprint import pprint
from PyQt4.Qt import *
from bundles import syntax

THEMES = {}

class SyntaxThemeProcessor(QSyntaxHighlighter, syntax.SyntaxProcessor):
    def __init__(self, parent, uuid, name, settings, author = '', comment = ''):
        QSyntaxHighlighter.__init__(self, parent)
        self.uuid = uuid
        self.name = name
        self.author = author
        default = settings.pop(0)
        self.default = QTextCharFormat()
        if 'foreground' in default:
            self.default.setForeground(QColor(default['foreground']))
        if 'background' in default:
            self.default.setBackground(QColor(default['background']))
        self.formats = {}
        for setting in settings:
            if 'scope' not in setting:
                continue
            format = QTextCharFormat()
            if 'fontStyle' in setting:
                format.setFontWeight(QFont.Light)
            if 'foreground' in setting:
                format.setForeground(QColor(setting['foreground']))
            if 'background' in setting:
                format.setBackground(QColor(setting['background']))
            setting['format'] = format
            self.formats[setting['scope']] = setting

    def highlightBlock(self, texto):
        syntax.SYNTAXES['PHP']['source.php'].parse(unicode(texto), self)
        #for match in patron.finditer(texto):
        #    inicio, cant = match.start(), match.end() - match.start()
        #    self.setFormat(inicio, cant, self.formats.values()[0].format)

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

    def start_parsing(self, name):
        self.line_number = 0
        print '{%s' % name

    def end_parsing(self, name):
        print '}%s' % name
        
def main(argv = sys.argv):
    app = QApplication(argv)
    win = QMainWindow() # Creamos la ventana de edición
    text_edit = QTextEdit()
    text_edit.setFontFamily('Consolas')
    win.setCentralWidget(text_edit)

    #Leer los temas
    paths = glob.glob('./bundles/Themes/*.tmTheme')
    for path in paths:
        data = plistlib.readPlist(os.path.abspath(path))
        theme = SyntaxThemeProcessor(win, **data)
        THEMES[theme.name] = theme

    theme = THEMES.values()[7]
    sintaxis = theme.setDocument(text_edit.document())
    
    win.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
