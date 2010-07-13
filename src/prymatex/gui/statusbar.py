# encoding: utf-8
'''
This module contains the main window status bar definition and widgets.
Some of the widgets defined here are:
    * The line counter
    * Syntax selector
    * 
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from prymatex.lib.i18n import ugettext as _
from prymatex.lib.textmate.syntax import TM_SYNTAXES

class QuickSyntaxSwitchDialog(QDialog):
    def __init__(self, parent = None):
        '''
        Una idea para seleccionar rápidamente la sintaxis
        '''
        QDialog.__init__(self, parent)
        self.setWindowTitle("Quick Syntax Switch")
        layout = QVBoxLayout()
        lineEdit = QLineEdit()
        completer = QCompleter(['python', 'python and django', 'C', 'C++'], lineEdit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        lineEdit.setCompleter(completer)
        layout.addWidget(QLabel("Select Syntax and press Intro"))
        layout.addWidget(lineEdit)
        
        self.setLayout(layout)
        
        

class PWMStatusLabel(QLabel):
    def __init__(self, text, parent, default = 0, *options):
        QLabel.__init__(self, text, parent)
        self.setToolTip(text)
        self.menu = QMenu(self)
        self.menu.setObjectName("menu")
        #print "COnexion", self.connect(self.menu, SIGNAL("triggered(QAction* action)"), self.selected)
        QMetaObject.connectSlotsByName(self)
        actions = []
        for name, value in options:
            action = self.menu.addAction(name)
            action.value = value
            actions.append(action)
        if actions:
            actions[default].trigger()
        
        
    def mouseReleaseEvent(self, event):
        if self.menu.actions():
            #self.menu.exec_()
            self.menu.popup( event.globalPos() )
    
    def on_menu_triggered(self, action):
        self.setText(action.text())
    
class PMXSyntaxMenu(QComboBox):
    # TODO: Seleccionar la última sintaxis utilizada
    def __init__(self, parent = None):
        QComboBox.__init__(self, parent)
        self.addItem("No syntax")
        self.connect(self, SIGNAL('currentIndexChanged(int)'), self.setSyntax)
    
    def setSyntax(self, index):
        syntax = self.itemData(index).toPyObject()
        print "Cambiando la syntax a ", syntax.name
        qApp.instance().current_editor.set_syntax(syntax)
    

class PMXStatusBar(QStatusBar):
    
    def __init__(self, parent ):
        QStatusBar.__init__(self, parent)
        self.lineLabel = PWMStatusLabel(_("Line: %6d", 0), self)
        self.columnLabel = PWMStatusLabel(_("Column: %6d", 0), self)
        self.langComboBox = PWMStatusLabel(_("Lang"), self)
        self.indentModeComboBox = PWMStatusLabel(_("Indent Mode"),
                                                 self, 0,
                                                (_('Soft Tabs'), 0),
                                                (_('Hard Tabs'), 1),
                                                 )
        
        self.indentWidthComboBox = PWMStatusLabel(_("Intendt width"), self,
                                                  -1,
                                                  ('1', 1),
                                                  ('2', 2),
                                                  ('4', 4),
                                                  ('8', 8),
                                                  )
        
        
        self.syntaxMenu = PMXSyntaxMenu(self)
        # TODO: Nueva iteracion
        for scope, syntax in TM_SYNTAXES['textmate'].items():
            
            self.syntaxMenu.addItem(syntax.name, userData=QVariant(syntax))
            
        self.addPermanentWidget(self.syntaxMenu)
        self.addPermanentWidget(self.lineLabel)
        self.addPermanentWidget(self.columnLabel)
        self.addPermanentWidget(self.langComboBox)
        self.addPermanentWidget(self.indentModeComboBox)
        self.addPermanentWidget(self.indentWidthComboBox)
    
    def updateCursorPos(self, col, row):
        '''  Called by the main window '''
        self.lineLabel.setText(_("Line: %6d", row))
        self.columnLabel.setText(_("Column: %6d", col))
        
        self.setStyleSheet('''
            QLabel { border-left: 1px solid #000;
                    font-family: Monospace; }
        ''')
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = QuickSyntaxSwitchDialog(None)
    dlg.exec_()
    