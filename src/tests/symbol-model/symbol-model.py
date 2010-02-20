# -*- coding: utf-8 -*-
'''
Mockup de sábado a la mañana.
Este modelo debería ser propiedad del textdocument o el editor.
Su utiliad podria ser:

    - folding
    - guardar estado de la pila del formateador
    - búsqueda de simbolos símil Ctrl+O en eclipse
    - visualización gerarquica de símbolos (no muy útil pero algo bonito)

La API es muy beta, pero la idea es que sea una especie de autómata
de pila

'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from cgi import escape

class SymbolItem(QStandardItem):
     
    def __init__(self, parentSymbol):
        QStandardItem.__init__(self)
        self.parentSymbol = parentSymbol # setChild api not apropiate :(
        self.setEditable(False)
        self._startLine = self._endLine = 0
        self._startColumn = self._endColumn = 0
    
    def startLine(): #@NoSelf
        doc = """Start Line""" #@UnusedVariable
       
        def fget(self):
            return self._startLine
           
        def fset(self, value):
            self._startLine = value
            self.updateToolTip()
        
        return locals()
       
    startLine = property(**startLine())
    
    def endLine(): #@NoSelf
        doc = """End Line""" #@UnusedVariable
       
        def fget(self):
            return self._endLine
           
        def fset(self, value):
            self._endLine = value
        return locals()
       
    endLine = property(**endLine())
    
    def startColumn(): #@NoSelf
        doc = """Start Column""" #@UnusedVariable
       
        def fget(self):
            return self._startColumn
           
        def fset(self, value):
            self._startColumn = value
           
        return locals()
       
    startColumn = property(**startColumn())
    
    def endColumn(): #@NoSelf
        doc = """Docstring""" #@UnusedVariable
       
        def fget(self):
            return self._endColumn
           
        def fset(self, value):
            self._endColumn = value
        return locals()
       
    endColumn = property(**endColumn())
    
    def updateToolTip(self):
        self.setToolTip('<b>%s</b><br/>Line: %d' % (escape(self.text()), 
                                                    self.startLine))
    
    @property
    def startPos(self):
        return self.startLine, self.startColumn

    @property
    def endPos(self):
        return self.endLine, self.endColumn
        

    def __str__(self):
        return "<%s %s" % (self.__class__.__name__, self.text())

    
class SymbolModel(QStandardItemModel):
    
    __currentSymbol = None
    
    def __init__(self, parent):
        QStandardItemModel.__init__(self, parent)
        self.currentSymbol = self # Root
        self.currentLine = 0
        self.currentColumn = 0

    def currentSymbol(): #@NoSelf
        def fget(self):
            return self.__currentSymbol
        def fset(self, val):
            assert val is self or isinstance(val, SymbolItem)
            #print (val) #Debug
            self.__currentSymbol = val
        doc = ''' Current symbol '''
        return locals()
    currentSymbol = property(**currentSymbol())

    
    def openSymbol(self, symbol_name, symbol_type = None, cursorPos = None):
        '''

        @param symbol_type: Podría servir para el icono :)
        Cada vez que se entra en un símbolo
        '''
        symbol = SymbolItem(self.currentSymbol) # Pass root
        symbol.setText(symbol_name) # Text
        symbol.startLine = symbol.endLine = self.currentLine
        symbol.startColumn = symbol.endColumn = self.currentColumn

        self.currentSymbol.appendRow(symbol) # Add to the tree
        self.currentSymbol = symbol
        return symbol


    def feedLine(self):
        self.currentLine += 1
        self.currentSymbol.endLine += 1

    def closeSymbol(self):
        self.currentSymbol = self.currentSymbol.parentSymbol

    def goUpTo(self, to = None):
        if not to:
            to = self
        if self.currentSymbol == self or to == self.currentSymbol:
            return
        while self.currentSymbol != to:
            print self.currentSymbol
            self.closeSymbol()

    def goRoot(self):
        self.goUpTo()
        
    def oneLineSymbol(self, symbol_name, symbol_type = None, cursorPosStart = None, cursorPosEnd = None):
        s = self.openSymbol(symbol_name, symbol_type, cursorPosStart)
        self.feedLine()
        self.closeSymbol()
        return s

    def lookupByCurPos(self, lineNo, cloumnNo):
        '''
        Serviría para ubicar un combo en el símbolo adecuado, textmate lo tiene en la barra de estado
        '''
        pass

    def lookupByLine(self, lineNo):
        ''' Helper '''
        return self.lookupByCurPos(lineNo, 0)


    def currentNodeStr(self):
        ''' Debug '''
        l = []
        n = self.currentSymbol
        if n == self:
            return "Root"
        while n != self:
            l.append(unicode(n.text()))
            n = n.parentSymbol
        return '->'.join(l)
        
class SymbolViewer(QTreeView):
    '''
    Un visor de símbolos es un visor de un modelo de una columna
    '''
    def __init__(self, parent = None):
        QTreeView.__init__(self, parent)
        model = SymbolModel(self)
        self.setModel(model)


def main(argv = sys.argv):
    app = QApplication(argv)
    win = QWidget()
    win.setWindowTitle("Symbol Model Mockup")
    win.setLayout(QVBoxLayout())
    splitter = QSplitter()
    win.layout().addWidget(splitter)
    editor = QTextEdit()
    editor.setPlainText("TODO")
    symbolTree = SymbolViewer()
    model = symbolTree.model()
    
    model.oneLineSymbol('import X')
    model.oneLineSymbol('import Y')
    model.openSymbol('class Persona(object)')
    model.feedLine()
    model.openSymbol('def __init__(self, args):')
    model.feedLine()
    model.openSymbol('self.args')
    model.feedLine()
    print(model.currentNodeStr())
    model.goRoot()
    model.openSymbol('class Pepe(object):')
    model.feedLine()
    model.openSymbol('class Pepa:')
    model.feedLine()
    model.goRoot()
    print model.currentNodeStr()
    # API alternativa?
    r = model.openSymbol('<html>')
    model.feedLine()
    print r
    model.openSymbol('<head>')
    model.feedLine()
    model.openSymbol('<title>')
    model.feedLine()
    model.goUpTo(r)
    model.openSymbol('<body>')
    model.feedLine()
    model.openSymbol('<div id="wrapper">')
    
    
    symbolTree.expandAll()
    splitter.addWidget(symbolTree)
    splitter.addWidget(editor)
    combo = QComboBox()
    combo.setToolTip(u"Solo aparecen los del nivel raíz, falta un proxymodel, pero la idea está :)")
    combo.setModel(model)
    win.layout().addWidget(combo)
    win.setGeometry(60,60,500,460)
    win.show()
    
    return app.exec_()
if __name__ == "__main__":
    sys.exit(main())