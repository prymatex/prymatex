from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.ui.editorstatus import Ui_CodeEditorStatus

class PMXCodeEditorStatus(QtGui.QWidget, Ui_CodeEditorStatus, PMXObject):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.editor = None
        
        self.setupUi(self)
        #self.widgetGoToLine.setVisible(False)
        #self.widgetFindReplace.setVisible(False)
        #self.widgetCommand.setVisible(False)
        self.setupWidgetStatus()
        self.setupWidgetCommand()
        self.setupWidgetFindReplace()
    
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
        self.comboBoxOutput.setCurrentIndex(3)
    
    def setupWidgetFindReplace(self):
        #TODO: Constantes
        self.comboBoxFindMode.addItem("Plain text", 0)
        self.comboBoxFindMode.addItem("Whole word only", 1)
        self.comboBoxFindMode.addItem("Escape sequences", 2)
        self.comboBoxFindMode.addItem("Regular expressions", 3)
        
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
    
    @QtCore.pyqtSlot()
    def on_lineEditCommand_returnPressed(self):
        command = self.lineEditCommand.text()
        self.lineEditCommand.clear()
        input = self.comboBoxInput.itemData(self.comboBoxInput.currentIndex())
        output = self.comboBoxOutput.itemData(self.comboBoxOutput.currentIndex())
        self.editor.insertCommand(command, input, output)
    
    #============================================================
    # AutoConnect GoToLine widget signals
    #============================================================
    @QtCore.pyqtSlot()
    def on_pushButtonGoToLineClose_pressed(self):
        self.widgetGoToLine.setVisible(False)
    
    @QtCore.pyqtSlot(int)
    def on_spinBoxGoToLine_valueChanged(self, lineNumber):
        self.editor.goToLine(lineNumber)

    #============================================================
    # AutoConnect FindReplace widget signals
    #============================================================    
    @QtCore.pyqtSlot()
    def on_pushButtonFindReplaceClose_pressed(self):
        self.widgetFindReplace.setVisible(False)
    
    @QtCore.pyqtSlot()
    def on_pushButtonFindNext_pressed(self):
        caseSensitively = 0 if not self.checkBoxFindCaseSensitively.isChecked() else QtGui.QTextDocument.FindCaseSensitively
        wholeWords = 0
        match = self.lineEditFind.text()
        mode = self.comboBoxFindMode.itemData(self.comboBoxFindMode.currentIndex())
        if mode == 1:
            wholeWords = QtGui.QTextDocument.FindWholeWords
        elif mode == 2:
            pass
        elif mode == 3:
            match = QtCore.QRegExp(QtCore.QRegExp.escape(match))  
        flags = caseSensitively + wholeWords
        self.editor.findMatch(match, flags, True)

    @QtCore.pyqtSlot()
    def on_pushButtonFindPrevious_pressed(self):
        '''
        s = 0 if not self._searchWidget._checkSensitive.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self._searchWidget._checkWholeWord.isChecked() \
            else QTextDocument.FindWholeWords
        flags = 1 + s + w
        '''
        flags = 1 + QtGui.QTextDocument.FindWholeWords + QtGui.QTextDocument.FindCaseSensitively
        self.editor.findMatch(self.lineEditFind.text(), flags)
    
    #============================================================
    # AutoConnect IFind widget signals
    #============================================================    
    @QtCore.pyqtSlot()
    def on_pushButtonIFindClose_pressed(self):
        self.widgetIFind.setVisible(False)
    
    @QtCore.pyqtSlot(str)
    def on_lineEditIFind_textChanged(self, text):
        flags = QtGui.QTextDocument.FindFlags()
        if not self.checkBoxIFindCaseSensitively.isChecked():
            flags |= QtGui.QTextDocument.FindCaseSensitively
        self.editor.findMatch(text, flags)
    
    @QtCore.pyqtSlot()
    def on_pushButtonIFindNext_pressed(self):
        flags = QtGui.QTextDocument.FindFlags()
        if self.checkBoxIFindCaseSensitively.isChecked():
            flags |= QtGui.QTextDocument.FindCaseSensitively
        self.editor.findMatch(self.lineEditIFind.text(), flags, True)

    @QtCore.pyqtSlot()
    def on_pushButtonIFindPrevious_pressed(self):
        flags = QtGui.QTextDocument.FindFlags()
        flags |= QtGui.QTextDocument.FindBackward
        if self.checkBoxIFindCaseSensitively.isChecked():
            flags |= QtGui.QTextDocument.FindCaseSensitively
        self.editor.findMatch(self.lineEditFind.text(), flags)
    
    #============================================================
    # Control de eventos
    #============================================================
    def eventFilter(self, obj, event):
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
