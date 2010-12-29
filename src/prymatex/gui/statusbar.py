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
from prymatex.lib.textmate.syntax import TM_SYNTAXES, TMSyntaxNode
from prymatex.core.base import PMXObject

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
    syntaxChange = pyqtSignal(TMSyntaxNode)
    
    def __init__(self, parent = None):
        QComboBox.__init__(self, parent)
        self.addItem("No syntax", userData=QVariant(None))
        self.connect(self, SIGNAL('currentIndexChanged(int)'), self.setSyntax)
    
    def setSyntax(self, index):
        syntax = self.itemData(index).toPyObject()
        if syntax:
            syntax.syntax_menu_index = index
        self.syntaxChange.emit(syntax)
        
    def on_current_editor_changed(self, editor):
        # TODO: Enable
        #syntax = editor.syntax_processor.syntax
        syntax = None
        if syntax != None:
            self.setCurrentIndex(syntax.syntax_menu_index)
        else:
            self.setCurrentIndex(0)
            
class PMXStatusBar(QStatusBar, PMXObject):
    
    def __init__(self, parent ):
        QStatusBar.__init__(self, parent)
        #self.lineLabel = PWMStatusLabel(_("Line: %6d", 0), self)
        self.lineLabel = QLabel("Line %d %d", self)
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
        
        syntaxes = []
        for name_space in TM_SYNTAXES.values():
            syntaxes.extend(name_space.values())
        
        syntaxes = sorted(syntaxes, lambda a, b: cmp(a.name, b.name))
        for syntax in syntaxes:
            self.syntaxMenu.addItem(syntax.name, userData=QVariant(syntax))
            
        self.addPermanentWidget(self.syntaxMenu)
        self.addPermanentWidget(self.lineLabel)
        self.addPermanentWidget(self.columnLabel)
        self.addPermanentWidget(self.langComboBox)
        self.addPermanentWidget(self.indentModeComboBox)
        self.addPermanentWidget(self.indentWidthComboBox)
        
        self.connect(self.root, SIGNAL('cursorPositionChangedEvent'),
                     self.updatePosition )
    
    def updatePosition(self, *largs, **kwargs):
        print "updatePosition", largs, kwargs 
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
    