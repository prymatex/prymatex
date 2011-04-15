# encoding: utf-8
'''
This module contains the main window status bar definition and widgets.
Some of the widgets defined here are:
    * The line counter
    * Syntax selector
    * 
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from prymatex.bundles.syntax import PMXSyntax
from prymatex.core.base import PMXObject
from prymatex.lib.i18n import ugettext as _
        
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

class PMXCursorPositionLabel(QWidget):
    FORMAT = "Line: %d Col: %d"
    def __init__(self, parent):
        super(PMXCursorPositionLabel, self).__init__(parent)
        self.__text_format = self.trUtf8(self.FORMAT)
        layout = QHBoxLayout()
        #self.label = QLabel(self.trUtf8('Pos:'))
        #layout.addWidget(self.label)
        self.postionLabel = QLabel(self.text_format % (0, 0))
        fm = self.fontMetrics()
        self.postionLabel.setMinimumWidth(fm.width('0') * len(self.text_format) + 3 )
        layout.addWidget(self.postionLabel)
        self.setLayout(layout)

    @property
    def text_format(self):
        return unicode(self.__text_format)
        
    def update(self, col, line):
        self.postionLabel.setText(self.text_format % (line, col))

class PMXSymbolBox(QComboBox):
    def __init__(self, parent):
        super(PMXSymbolBox, self).__init__(parent)        
            
class PMXStatusBar(QStatusBar, PMXObject):
    
    def __init__(self, parent ):
        QStatusBar.__init__(self, parent)
        
        self.lineColLabel = PMXCursorPositionLabel(self)

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
        
        
        self.syntaxMenu = QComboBox(self)
        
        #No syntax
        self.syntaxMenu.addItem("No syntax")
        for name in PMXSyntax.getSyntaxesNames(sort = True):
            self.syntaxMenu.addItem(name)
            
        self.addPermanentWidget(self.syntaxMenu)
        self.addPermanentWidget(self.lineColLabel)
        
        self.addPermanentWidget(self.indentModeComboBox)
        self.addPermanentWidget(self.indentWidthComboBox)
        self.declareEvents()
        self.setSignals()
            
    def setSignals(self):
        #External events
        self.connect(self.mainwindow, SIGNAL('editorCursorPositionChangedEvent'), self.updatePosition )
        self.connect(self.mainwindow, SIGNAL('editorSetSyntaxEvent'), self.updateSyntax )
        self.connect(self.mainwindow, SIGNAL('tabWidgetEditorChangedEvent'), self.updateEditor )
        
        #Internal signals
        self.connect(self.syntaxMenu, SIGNAL('currentIndexChanged(QString)'), self.sendStatusBarSyntaxChanged)
        
    def declareEvents(self):
        self.declareEvent('statusBarSytnaxChangedEvent()')
    
    def sendStatusBarSyntaxChanged(self, name):
        syntax = PMXSyntax.getSyntaxByName(str(name))
        self.statusBarSytnaxChangedEvent(syntax)
        
    def updatePosition(self, source, line, col):
        self.lineColLabel.update(col, line)
    
    def updateEditor(self, source, editor):
        self.updateSyntax(source, editor.syntax)
    
    def updateSyntax(self, source, syntax):
        if syntax != None:
            index = self.syntaxMenu.findText(syntax.name, Qt.MatchExactly)
            self.syntaxMenu.setCurrentIndex(index)
        else:
            self.syntaxMenu.setCurrentIndex(0)
