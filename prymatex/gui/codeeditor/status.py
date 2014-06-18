#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core import PrymatexStatusBar

from prymatex import resources
from prymatex.gui.codeeditor.editor import CodeEditor
from prymatex.ui.codeeditor.status import Ui_CodeEditorStatus

class CodeEditorStatus(PrymatexStatusBar, Ui_CodeEditorStatus, QtGui.QWidget):
    def __init__(self, **kwargs):
        super(CodeEditorStatus, self).__init__(**kwargs)

        self.currentEditor = None
        
        self.setupUi(self)
        self.widgetGoToLine.setVisible(False)
        self.widgetFindReplace.setVisible(False)
        self.widgetCommand.setVisible(False)
        self.setupWidgetStatus()
        self.setupWidgetCommand()
        self.setupWidgetFindReplace()
        self.setupEvents()
    
    def initialize(self, **kwargs):
        super(CodeEditorStatus, self).initialize(**kwargs)
        self.hideAllWidgets()

    def hideAllWidgets(self):
        for widget in [self.widgetGoToLine, self.widgetFindReplace, self.widgetCommand, self.widgetIFind]:
            widget.setVisible(False)

    # --------------- Setup Events
    def setupEvents(self):
        self.lineEditIFind.installEventFilter(self)
        self.comboBoxCommand.installEventFilter(self)
        self.lineEditFind.installEventFilter(self)
        self.lineEditReplace.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if obj is self.lineEditIFind:
                if event.key() == QtCore.Qt.Key_Escape:
                    self.pushButtonIFindClose.click()
                    return True
                elif event.key() == QtCore.Qt.Key_Return and event.modifiers() == QtCore.Qt.ShiftModifier:
                    self.pushButtonIFindPrevious.click()
                    return True
                elif event.key() == QtCore.Qt.Key_Return:
                    self.pushButtonIFindNext.click()
                    return True
            elif obj is self.comboBoxCommand:
                if event.key() == QtCore.Qt.Key_Escape:
                    self.pushButtonCommandClose.click()
                    return True
            elif obj is self.lineEditFind:
                if event.key() == QtCore.Qt.Key_Escape:
                    self.pushButtonFindReplaceClose.click()
                    return True
                elif event.key() == QtCore.Qt.Key_Return and event.modifiers() == QtCore.Qt.ShiftModifier:
                    self.pushButtonFindPrevious.click()
                    return True
                elif event.key() == QtCore.Qt.Key_Return:
                    self.pushButtonFindNext.click()
                    return True
            elif obj is self.lineEditReplace:
                if event.key() == QtCore.Qt.Key_Escape:
                    self.pushButtonFindReplaceClose.click()
                    return True
                elif event.key() == QtCore.Qt.Key_Return:
                    self.pushButtonReplace.click()
                    return True
        return QtGui.QWidget.eventFilter(self, obj, event)

    # -------------- Setup Widgets
    def setupWidgetStatus(self):
        # Custom Table view for syntax combo
        self.comboBoxSyntaxes.setView(QtGui.QTableView(self))
        self.comboBoxSyntaxes.setModel(
            self.application.supportManager.syntaxProxyModel);
        self.comboBoxSyntaxes.setModelColumn(0)
        self.comboBoxSyntaxes.view().resizeColumnsToContents()
        self.comboBoxSyntaxes.view().resizeRowsToContents()
        self.comboBoxSyntaxes.view().verticalHeader().setVisible(False)
        self.comboBoxSyntaxes.view().horizontalHeader().setVisible(False)
        self.comboBoxSyntaxes.view().setShowGrid(False)
        self.comboBoxSyntaxes.view().setMinimumWidth(
            self.comboBoxSyntaxes.view().horizontalHeader().length() + 25)
        self.comboBoxSyntaxes.view().setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.comboBoxSyntaxes.view().setSelectionMode(
            QtGui.QAbstractItemView.SingleSelection)
        self.comboBoxSyntaxes.view().setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.comboBoxSyntaxes.view().setAutoScroll(False)
        
        # Connect tab size context menu
        self.labelIndentation.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.labelIndentation.customContextMenuRequested.connect(self.showTabSizeContextMenu)
        
        # Create bundle menu
        self.menuBundle = QtGui.QMenu(self)
        self.application.supportManager.appendMenuToBundleMenuGroup(self.menuBundle)
        self.toolButtonMenuBundle.setMenu(self.menuBundle)
        
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
        self.comboBoxCommand.lineEdit().returnPressed.connect(self.on_comboBoxCommand_returnPressed)
    
    def setupWidgetFindReplace(self):
        #TODO: Constantes
        self.comboBoxFindMode.addItem("Plain text", 0)
        self.comboBoxFindMode.addItem("Whole word only", 1)
        self.comboBoxFindMode.addItem("Escape sequences", 2)
        self.comboBoxFindMode.addItem("Regular expressions", 3)

    # --------------- Handle editors
    def acceptEditor(self, editor):
        return isinstance(editor, CodeEditor)

    def disconnectEditor(self, editor):
        editor.cursorPositionChanged.disconnect(self.on_cursorPositionChanged)
        editor.syntaxChanged.disconnect(self.on_syntaxChanged)

    def connectEditor(self, editor):
        editor.cursorPositionChanged.connect(self.on_cursorPositionChanged)
        editor.syntaxChanged.connect(self.on_syntaxChanged)

    def setCurrentEditor(self, editor):
        if self.currentEditor is not None:
            self.disconnectEditor(self.currentEditor)
        #Change currentEditor
        self.currentEditor = editor
        if self.currentEditor is not None:
            self.connectEditor(self.currentEditor)
            self.comboBoxSymbols.setModel(self.currentEditor.symbolListModel)
            self.on_cursorPositionChanged(self.currentEditor)
            self.on_syntaxChanged(self.currentEditor.syntax())
            self.setTabSizeLabel(self.currentEditor)

    # ---------------- AutoConnect Status Widget signals
    @QtCore.Slot(int)
    def on_comboBoxSyntaxes_activated(self, index):
        if self.currentEditor is not None:
            model = self.comboBoxSyntaxes.model()
            node = model.node(model.createIndex(index, 0))
            self.currentEditor.insertBundleItem(node)

    @QtCore.Slot(int)
    def on_comboBoxTabSize_activated(self, index):
        data = self.comboBoxTabSize.itemData(index)

    @QtCore.Slot(int)
    def on_comboBoxSymbols_activated(self, pos):
        model = self.comboBoxSymbols.model()
        index = model.index(pos)
        if index.isValid():
            block = index.internalPointer()
            self.currentEditor.goToBlock(block)
            self.currentEditor.setFocus()

    def on_cursorPositionChanged(self, editor = None):
        editor = editor or self.currentEditor
        cursor = editor.textCursor()
        self.labelPosition.setText("Line: %5d Column: %5d Selection: %5d" % (
            cursor.blockNumber() + 1, cursor.columnNumber() + 1, 
            cursor.selectionEnd() - cursor.selectionStart()))
        #Set index of current symbol
        self.comboBoxSymbols.setCurrentIndex(self.comboBoxSymbols.model().findBlockIndex(cursor))

    def on_syntaxChanged(self, syntax):
        model = self.comboBoxSyntaxes.model()
        index = model.nodeIndex(syntax).row()
        self.comboBoxSyntaxes.setCurrentIndex(index)

    def showTabSizeContextMenu(self, point):
        editor = self.currentEditor
        #Setup Context Menu
        menuIndentation = self.mainWindow.findChild(QtGui.QMenu, "menuIndentation")
        menuIndentation.popup(self.labelIndentation.mapToGlobal(point))

    def setCurrentEditorTabSoft(self, soft):
        self.currentEditor.indentUsingSpaces = soft

    def setCurrentEditorTabSize(self, size):
        self.currentEditor.tabWidth = size
        self.setTabSizeLabel(self.currentEditor)

    def setTabSizeLabel(self, editor):
        #Tab Size
        if editor.indentUsingSpaces:
            self.labelIndentation.setText("Spaces: %d" % editor.indentationWidth)
        else:
            self.labelIndentation.setText("Tab width: %d" % editor.tabWidth)

    # -------------- AutoConnect Command widget signals
    @QtCore.Slot()
    def on_pushButtonCommandClose_pressed(self):
        self.widgetCommand.setVisible(False)

    @QtCore.Slot()
    def on_comboBoxCommand_returnPressed(self):
        command = self.comboBoxCommand.lineEdit().text()
        input = self.comboBoxInput.itemData(self.comboBoxInput.currentIndex())
        output = self.comboBoxOutput.itemData(self.comboBoxOutput.currentIndex())
        self.currentEditor.executeCommand(command, input, output)
        self.comboBoxCommand.lineEdit().clear()

    def showCommand(self):
        self.hideAllWidgets()
        self.widgetCommand.setVisible(True)
        self.comboBoxCommand.setFocus()

    # ------------ AutoConnect GoToLine widget signals
    @QtCore.Slot()
    def on_pushButtonGoToLineClose_pressed(self):
        self.widgetGoToLine.setVisible(False)

    @QtCore.Slot(int)
    def on_spinBoxGoToLine_valueChanged(self, lineNumber):
        self.currentEditor.goToLine(lineNumber)

    def showGoToLine(self):
        self.hideAllWidgets()
        self.widgetGoToLine.setVisible(True)
        self.spinBoxGoToLine.setFocus()

    # --------- AutoConnect FindReplace widget Signals
    @QtCore.Slot()
    def on_pushButtonFindReplaceClose_pressed(self):
        self.widgetFindReplace.setVisible(False)

    @QtCore.Slot()
    def on_pushButtonFindNext_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        self.currentEditor.findMatch(match, flags, True)

    @QtCore.Slot()
    def on_pushButtonFindPrevious_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        flags |= QtGui.QTextDocument.FindBackward
        self.currentEditor.findMatch(match, flags)

    @QtCore.Slot()
    def on_pushButtonReplace_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        replace = self.lineEditReplace.text()
        if match and replace:
            self.currentEditor.replaceMatch(match, replace, flags)
            self.currentEditor.findMatch(match, flags)

    @QtCore.Slot()
    def on_pushButtonReplaceAll_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        replace = self.lineEditReplace.text()
        if match and replace:
            self.currentEditor.replaceMatch(match, replace, flags, allText = True)
        # TODO: mensaje de cuantos remplazo

    @QtCore.Slot()
    def on_pushButtonFindAll_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        cursors = self.currentEditor.findAll(match, flags)
        self.currentEditor.setExtraSelectionCursors("selection", cursors)
        self.currentEditor.updateExtraSelections()
        # TODO: mensaje de cuantos encontro y ver que queremos hacer con ellos

    def getFindMatchAndFlags(self):
        flags = QtGui.QTextDocument.FindFlags()
        if self.checkBoxFindCaseSensitively.isChecked():
            flags |= QtGui.QTextDocument.FindCaseSensitively
        match = self.lineEditFind.text()
        mode = self.comboBoxFindMode.itemData(self.comboBoxFindMode.currentIndex())
        if mode == 1:
            flags |= QtGui.QTextDocument.FindWholeWords
        elif mode == 2:
            pass
        elif mode == 3:
            match = QtCore.QRegExp(match)
        return match, flags

    def showFindReplace(self):
        self.hideAllWidgets()
        self.widgetFindReplace.setVisible(True)
        self.lineEditFind.setFocus()

    # -------------- AutoConnect IFind widget Signals
    @QtCore.Slot()
    def on_pushButtonIFindClose_pressed(self):
        self.widgetIFind.setVisible(False)
        self.currentEditor.setFocus()

    @QtCore.Slot(str)
    def on_lineEditIFind_textChanged(self, text):
        if text:
            _, flags = self.getIFindMatchAndFlags()
            match = self.currentEditor.findMatch(text, flags, cyclicFind = True)
            self.lineEditIFind.setStyleSheet(match and resources.FIND_MATCH_STYLE or resources.FIND_NO_MATCH_STYLE)
        else:
            #TODO: Buscar un clean style
            self.lineEditIFind.setStyleSheet('')

    @QtCore.Slot()
    def on_pushButtonIFindNext_pressed(self):
        match, flags = self.getIFindMatchAndFlags()
        self.currentEditor.findMatch(match, flags, findNext = True)

    @QtCore.Slot()
    def on_pushButtonIFindPrevious_pressed(self):
        match, flags = self.getIFindMatchAndFlags()
        flags |= QtGui.QTextDocument.FindBackward
        self.currentEditor.findMatch(match, flags)

    @QtCore.Slot(int)
    def on_checkBoxIFindCaseSensitively_stateChanged(self, value):
        match, flags = self.getIFindMatchAndFlags()
        if self.currentEditor.findMatch(match, flags):
            self.lineEditIFind.setStyleSheet(resources.FIND_MATCH_STYLE)
        else:
            self.lineEditIFind.setStyleSheet(resources.FIND_NO_MATCH_STYLE)

    def getIFindMatchAndFlags(self):
        flags = QtGui.QTextDocument.FindFlags()
        if self.checkBoxIFindCaseSensitively.isChecked():
            flags |= QtGui.QTextDocument.FindCaseSensitively
        return self.lineEditIFind.text(), flags

    def showIFind(self):
        self.hideAllWidgets()
        cursor = self.currentEditor.textCursor()
        if cursor.hasSelection():
            word = cursor.selectedText()
        else: 
            word, _, _ = self.currentEditor.currentWord()
        self.lineEditIFind.setText(word)        
        self.widgetIFind.setVisible(True)
        self.lineEditIFind.selectAll()
        self.lineEditIFind.setFocus()

    # ------------- Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls):
        menu = {}
        menu["edit"] = [
                '-',
                {'text': "Find",
                 'sequence': resources.get_sequence("StatusBar", "Find", "Find"),
                 'triggered': cls.showIFind
                },
                {'text': "Replace",
                 'sequence': resources.get_sequence("StatusBar", "Replace", "Replace"),
                 'triggered': cls.showFindReplace
                }
            ]
        menu["text"] = [
                {'text': 'Filter through command',
                 'triggered': cls.showCommand
                 }
            ]
        menu["navigation"] = [
                {'text': 'Go to &line',
                 'triggered': cls.showGoToLine,
                 'sequence': resources.get_sequence("StatusBar", "GoToLine", 'Meta+Ctrl+Shift+L'),
                 }
            ]
        return menu
