from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.ui.editorstatus import Ui_CodeEditorStatus

class PMXCodeEditorStatus(QtGui.QWidget, Ui_CodeEditorStatus, PMXObject):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.currentEditor = None
        
        self.setupUi(self)
        self.goToLine.setVisible(False)
        self.findReplace.setVisible(False)
        self.setupSyntaxMenu()
        
    def disconnectEditor(self, editor):
        editor.cursorPositionChanged.disconnect(self.updateCursorPosition)
        editor.syntaxChanged.disconnect(self.updateSyntax)
        
    def connectEditor(self, editor):
        editor.cursorPositionChanged.connect(self.updateCursorPosition)
        editor.syntaxChanged.connect(self.updateSyntax)
        
    def setCurrentEditor(self, editor):
        if self.currentEditor is not None:
            self.disconnectEditor(self.currentEditor)
        self.connectEditor(editor)
        self.updateCursorPosition(editor)
        self.updateSyntax(editor)
        self.currentEditor = editor
    
    def setupSyntaxMenu(self):
        tableView = QtGui.QTableView(self)
        tableView.setModel(self.application.supportManager.syntaxProxyModel)
        tableView.resizeColumnsToContents()
        tableView.resizeRowsToContents()
        tableView.verticalHeader().setVisible(False)
        tableView.horizontalHeader().setVisible(False)
        tableView.setShowGrid(False)
        tableView.setMinimumWidth(tableView.horizontalHeader().length() + 25)
        tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        tableView.setAutoScroll(False)
        self.syntaxMenu.setModel(self.application.supportManager.syntaxProxyModel);
        self.syntaxMenu.setModelColumn(0)
        self.syntaxMenu.setView(tableView)
    
    @QtCore.pyqtSlot(int)
    def on_syntaxMenu_currentIndexChanged(self, index):
        model = self.syntaxMenu.model()
        node = model.mapToSource(model.createIndex(index, 0))
        if self.currentEditor is not None:
            self.currentEditor.syntax = node.internalPointer()
            
    def updateCursorPosition(self, editor = None):
        editor = editor or self.currentEditor
        cursor = editor.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.labelLineColumn.setText("Line: %5d Column: %5d" % (line, column))
        
    def updateSyntax(self, editor = None):
        editor = editor or self.currentEditor
        model = self.syntaxMenu.model()
        index = model.findItemIndex(editor.syntax)
        self.syntaxMenu.blockSignals(True)
        self.syntaxMenu.setCurrentIndex(index)
        self.syntaxMenu.blockSignals(False)
