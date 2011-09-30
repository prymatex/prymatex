from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.ui.editorstatus import Ui_CodeEditorStatus

class PMXCodeEditorStatus(QtGui.QWidget, Ui_CodeEditorStatus, PMXObject):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.editor = None
        
        self.setupUi(self)
        self.widgetGoToLine.setVisible(False)
        self.widgetFindReplace.setVisible(False)
        #self.widgetCommand.setVisible(False)
        self.setupWidgetStatus()
        self.setupWidgetCommand()
    
    #============================================================
    # Setup Widgets
    #============================================================
    def setupWidgetStatus(self):
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
        self.comboBoxSyntaxes.setModel(self.application.supportManager.syntaxProxyModel);
        self.comboBoxSyntaxes.setModelColumn(0)
        self.comboBoxSyntaxes.setView(tableView)
    
    def setupWidgetCommand(self):
        #Install event filter for capture Return key
        self.lineEditCommand.installEventFilter(self)
        self.comboBoxInput.addItem("None", "none")
        self.comboBoxInput.addItem("Selection", "selection") #selectedText
        self.comboBoxInput.addItem("Document", "document")
        self.comboBoxOutput.addItem("Discard", "discard")
        self.comboBoxOutput.addItem("Replace Selection", "replaceSelectedText")
        self.comboBoxOutput.addItem("Replace Document", "replaceDocument")
        self.comboBoxOutput.addItem("Insert as Text", "insertText")
        self.comboBoxOutput.addItem("Insert as Snippet", "insertAsSnippet")
        self.comboBoxOutput.addItem("Show as HTML", "showAsHTML")
        self.comboBoxOutput.addItem("Show as Tool Tip", "showAsTooltip")
        self.comboBoxOutput.addItem("Create New Document", "createNewDocument")
    
    #============================================================
    # AutoConnect Status signals
    #============================================================
    @QtCore.pyqtSlot(int)
    def on_comboBoxSyntaxes_currentIndexChanged(self, index):
        model = self.comboBoxSyntaxes.model()
        node = model.mapToSource(model.createIndex(index, 0))
        if self.editor is not None:
            self.editor.syntax = node.internalPointer()
    
    #============================================================
    # AutoConnect Command widget signals
    #============================================================
    @QtCore.pyqtSlot()
    def on_pushButtonCommandClose_pressed(self):
        self.widgetCommand.setVisible(False)
    
    @QtCore.pyqtSlot(int)
    def on_comboBoxInput_currentIndexChanged(self, index):
        value = self.comboBoxInput.itemData(index)
        self.debug(value)
    
    @QtCore.pyqtSlot(int)
    def on_comboBoxOutput_currentIndexChanged(self, index):
        value = self.comboBoxOutput.itemData(index)
        self.debug(value)
    
    #============================================================
    # Control de eventos
    #============================================================
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Return and obj == self.lineEditCommand:
            command = self.lineEditCommand.text()
            self.lineEditCommand.clear()
            self.debug("Correr comando %s" % command)
            return True
        return QtGui.QWidget.eventFilter(self, obj, event)
    
    def disconnectEditor(self, editor):
        editor.cursorPositionChanged.disconnect(self.updateCursorPosition)
        editor.syntaxChanged.disconnect(self.updateSyntax)
        
    def connectEditor(self, editor):
        editor.cursorPositionChanged.connect(self.updateCursorPosition)
        editor.syntaxChanged.connect(self.updateSyntax)
        
    def setEditor(self, editor):
        if self.editor is not None:
            self.disconnectEditor(self.editor)
        self.connectEditor(editor)
        self.updateCursorPosition(editor)
        self.updateSyntax(editor)
        self.editor = editor
    
    def updateCursorPosition(self, editor = None):
        editor = editor or self.editor
        cursor = editor.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.labelLineColumn.setText("Line: %5d Column: %5d" % (line, column))
        
    def updateSyntax(self, editor = None):
        editor = editor or self.editor
        model = self.comboBoxSyntaxes.model()
        index = model.findItemIndex(editor.syntax)
        self.comboBoxSyntaxes.blockSignals(True)
        self.comboBoxSyntaxes.setCurrentIndex(index)
        self.comboBoxSyntaxes.blockSignals(False)
