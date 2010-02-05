#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, sys, glob, plistlib
from pprint import pprint
from PyQt4.Qt import *
from bundles import syntax
from xml.parsers.expat import ExpatError

class PMXSyntaxProcessor(QSyntaxHighlighter, syntax.TMSyntaxProcessor):
    def __init__(self):
        pass
    
    def highlightBlock(self, texto):
        parser = syntax.TM_SYNTAXES['HTML']['text.html.basic']
        stack = [[parser, None]] 
        parser.parse_line(stack, unicode(texto), self)
        pprint(stack)
        #for match in patron.finditer(texto):
        #    inicio, cant = match.start(), match.end() - match.start()
        #    self.setFormat(inicio, cant, self.formats.values()[0].format)

    def open_tag(self, name, position):
        print "open: %s in %d" % (name, position)

    def close_tag(self, name, position):
        print "close: %s in %d" % (name, position)

    def new_line(self, line):
        self.line_number += 1
        self.line_marks = '[%04s] ' % self.line_number
        print '%s%s' % (self.line_marks, line)

    def start_parsing(self, name):
        self.line_number = 0
        print '{ %s' % name

    def end_parsing(self, name):
        print '} %s' % name
        
def main(argv = sys.argv):
    app = QApplication(argv)
    win = QMainWindow() # Creamos la ventana de edición
    text_edit = QTextEdit()
    text_edit.setFontFamily('Consolas')
    win.setCentralWidget(text_edit)

    #Leer los temas
    paths = glob.glob('./bundles/Themes/*.tmTheme')
    for path in paths:
        try:
            data = plistlib.readPlist(os.path.abspath(path))
            theme = SyntaxThemeProcessor(win, **data)
            THEMES[theme.name] = theme
        except ExpatError:
            pass

    theme = THEMES.values()[7]
    sintaxis = theme.setDocument(text_edit.document())
    
    win.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
