# encoding: utf-8
'''
This module contains the main window status bar definition and widgets.
Some of the widgets defined here are:
    * The line counter
    * Syntax selector
    * 
'''
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.utils.translation import ugettext as _

class PWMStatusLabel(QtGui.QLabel):
    '''
    A label which fires a menu when it's clicked. When an action is 
    '''
    valueChanged = QtCore.pyqtSignal(object)
    
    def __init__(self, text, parent, default = 0, *options):
        QtGui.QLabel.__init__(self, text, parent)
        self.setToolTip(text)
        self.menu = QtGui.QMenu(self)
        
        self.menu.triggered[QtGui.QAction].connect(self.indentModeChangedFromMenu)
        actions = []
        for name, value in options:
            action = self.menu.addAction(name)
            action.value = value
            actions.append(action)
        if actions:
            actions[default].trigger()
        
    def mouseReleaseEvent(self, event):
        if self.menu.actions():
            self.menu.popup( event.globalPos() ) #self.menu.exec_()
    
    def indentModeChangedFromMenu(self, action):
        self.setText(action.text())
        self.valueChanged.emit(action.value)

class PMXCursorPositionLabel(QtGui.QWidget):
    
    FORMAT = "Line: %5d Col: %5d"
    def __init__(self, parent):
        super(PMXCursorPositionLabel, self).__init__(parent)
        self.__text_format = self.trUtf8(self.FORMAT)
        layout = QtGui.QHBoxLayout()
        #self.label = QLabel(self.trUtf8('Pos:'))
        #layout.addWidget(self.label)
        self.postionLabel = QtGui.QLabel(self.text_format % (0, 0))
        fm = self.fontMetrics()
        self.postionLabel.setMinimumWidth(fm.width('0') * len(self.text_format) + 3 )
        layout.addWidget(self.postionLabel)
        self.setLayout(layout)

    @property
    def text_format(self):
        return unicode(self.__text_format)
        
    def update(self, col, line):
        self.postionLabel.setText(self.text_format % (line, col))

class PMXSymbolBox(QtGui.QComboBox):
    # TODO: Implement SymbolBox
    def __init__(self, parent):
        super(PMXSymbolBox, self).__init__(parent)        
            
class PMXStatusBar(QtGui.QStatusBar, PMXObject):
    '''
    Main Window status bar, declares some widgets
    '''
    syntaxChanged = QtCore.pyqtSignal(object)
    
    def __init__(self, parent ):
        QtGui.QStatusBar.__init__(self, parent)
        
        self.lineColLabel = PMXCursorPositionLabel(self)

        self.comboIndentMode = PWMStatusLabel(_("Indent Mode"),
                                                 self, True,
                                                (_('Soft Tabs'), True),
                                                (_('Hard Tabs'), False),
                                                 )
        
        self.comboIndentMode.valueChanged.connect(self.setIndentMode)
        
        self.comboIndentWidth = PWMStatusLabel(_("Intendt width"), self,
                                                  -1,
                                                  ('1', 1),
                                                  ('2', 2),
                                                  ('3', 3),
                                                  ('4', 4),
                                                  ('8', 8),
                                                  )
        
        self.comboIndentWidth.valueChanged.connect(self.setIndentWidth)
        
        
        self.syntaxMenu = QtGui.QComboBox(self)
        self.syntaxMenu.setModel(self.pmxApp.supportManager.syntaxProxyModel)
            
        self.addPermanentWidget(self.syntaxMenu)
        self.addPermanentWidget(self.lineColLabel)    
        self.addPermanentWidget(self.comboIndentMode)
        self.addPermanentWidget(self.comboIndentWidth)
        
        self.connectSignals()
        
        self.mainWindow.tabWidget.currentEditorChanged.connect(self.syncToEditor)
    
    def mostrar(self, index):
        print self._combo.model()[index, 'item']
        print self._combo.model()[index, 'path']
    
    def setIndentMode(self, value):
        self.mainWindow.currentEditorWidget.codeEdit.softTabs = value 
    
    def setIndentWidth(self, value):
        self.warn("Tab Width %d" % value)
        self.mainWindow.currentEditorWidget.codeEdit.tabWidth = value
        
    def connectSignals(self):
        self.syntaxMenu.currentIndexChanged[int].connect(self.syntaxMenuIndexChanged)
    
    def syncToEditor(self, widget):
        editor = widget
        self.debug("Widget changed to %s", editor)
        
        try:
            codeEdit = widget.codeEdit
        except AttributeError:
            self.warn("Tab doen't seem to be a code edit")
            return
        
        # Update labels
        syn = codeEdit.syntax
        if syn:
            self.updateSyntax(syn)
    
    def syntaxMenuIndexChanged(self, index):
        model = self.syntaxMenu.model()
        node = model.mapToSource(model.createIndex(index, 0))
        syntax = node.internalPointer()
        self.syntaxChanged.emit(syntax)
        
    def updateStatus(self, status):
        self.lineColLabel.update(status['column'], status['line'])
    
    def updateSyntax(self, syntax):
        model =  self.syntaxMenu.model() # Proxy
        index = model.findItemIndex(syntax)
        self.syntaxMenu.setCurrentIndex(index)
        