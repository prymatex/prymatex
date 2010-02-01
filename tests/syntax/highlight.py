#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.Qt import *
import sys, re

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



class Resaltador(QSyntaxHighlighter):
    '''
    Resaltador de sintaxis basado en QSyntaxHighlighter de Qt4.

    Con cada edición de texto se invoca a la función highlightBlock

    '''
    def __init__(self, doc):
        QSyntaxHighlighter.__init__(self, doc)


        self.formatos = {} # Acá vamos a guardar los patrones 
        # Crear el formato
        formato = QTextCharFormat()
        formato.setFontWeight(QFont.Bold)
        formato.setForeground(Qt.darkMagenta)
        patron = '|'.join(C_KEYWORDS)
        patron = re.compile(patron)
        self.formatos[patron] = formato

    def highlightBlock(self, texto):
        # Fuerza bruta
        for patron, formato in self.formatos.iteritems():
            
            for match in patron.finditer(texto):
                inicio, longitud = match.span()
                #print inicio, longitud
                inivio, cant = match.start(), match.end() - match.start()
                self.setFormat(inicio, cant, formato)
                
            
            

def main(argv = sys.argv):
    app = QApplication(argv)
    win = QMainWindow() # Creamos la ventana de edición
    text_edit = QTextEdit()
    text_edit.setFontFamily("Consolas")
    win.setCentralWidget(text_edit)
    sintaxis = Resaltador(text_edit.document())
    
    win.show()
    return app.exec_()
    

if __name__ == "__main__":
    sys.exit(main())