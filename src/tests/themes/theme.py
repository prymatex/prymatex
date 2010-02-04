#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, sys, glob, plistlib
from pprint import pprint
from PyQt4.Qt import *
import ipdb

THEMES = {}

C_KEYWORDS = """
auto    double  int     struct
break   else    long    switch
case    enum    register        typedef
char    extern  return  union
const   float   short   unsigned
continue        for     signed  void
default goto    sizeof  volatile
do      if      static  while
""".split()

class ThemeItem(object):
    def __init__(self, name, scope, settings):
        self.name = name
        self.scope = scope
        self.format = QTextCharFormat()
        if 'fontStyle' in settings:
            self.format.setFontWeight(QFont.Light)
        if 'foreground' in settings:
            self.format.setForeground(QColor(settings['foreground']))
        if 'background' in settings:
            self.format.setBackground(QColor(settings['background']))

class PrymatexSyntaxTheme(QSyntaxHighlighter):
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
        for format in settings:
            if 'scope' in format:
                format = ThemeItem(**format)
                self.formats[format.scope] = format

    def highlightBlock(self, texto):
        patron = '|'.join(C_KEYWORDS)
        patron = re.compile(patron)
        for match in patron.finditer(texto):
            inicio, cant = match.start(), match.end() - match.start()
            self.setFormat(inicio, cant, self.formats.values()[0].format)
        
def main(argv = sys.argv):
    app = QApplication(argv)
    win = QMainWindow() # Creamos la ventana de edición
    text_edit = QTextEdit()
    text_edit.setFontFamily('Consolas')
    win.setCentralWidget(text_edit)

    #Leer los temas
    paths = glob.glob('./Themes/*.tmTheme')
    for path in paths:
        data = plistlib.readPlist(os.path.abspath(path))
        theme = PrymatexSyntaxTheme(win, **data)
        THEMES[theme.name] = theme

    theme = THEMES.values()[7]
    sintaxis = theme.setDocument(text_edit.document())
    
    win.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())

