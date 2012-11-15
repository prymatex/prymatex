#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseStatusBar

from prymatex import resources
from prymatex.gui.codeeditor.editor import CodeEditor
from prymatex.ui.codeeditor.status import Ui_CodeEditorStatus

class PMXCodeEditorStatus(QtGui.QWidget, Ui_CodeEditorStatus, PMXBaseStatusBar):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXBaseStatusBar.__init__(self)
        self.currentEditor = None
        
        self.setupUi(self)
        self.widgetGoToLine.setVisible(False)
        self.widgetFindReplace.setVisible(False)
        self.widgetCommand.setVisible(False)
        self.setupWidgetStatus()
        self.setupWidgetCommand()
        self.setupWidgetFindReplace()
        self.setupEvents()
    
    def hideAllWidgets(self):
        map(lambda widget: widget.setVisible(False), [self.widgetGoToLine, self.widgetFindReplace, self.widgetCommand, self.widgetIFind])

    #============================================================
    # Setup Events
    #============================================================    
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
        self.comboBoxSyntaxes.setView(tableView)
        self.comboBoxSyntaxes.setModelColumn(0)
        
        #Connect tab size context menu
        self.labelTabSize.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.labelTabSize.customContextMenuRequested.connect(self.showTabSizeContextMenu)
        
        #Create bundle menu
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
        
    #============================================================
    # Handle editors
    #============================================================
    def acceptEditor(self, editor):
        return isinstance(editor, CodeEditor)
    
    def disconnectEditor(self, editor):
        editor.cursorPositionChanged.disconnect(self.on_cursorPositionChanged)
        editor.syntaxChanged.disconnect(self.on_syntaxChanged)
        editor.modeChanged.disconnect(self.on_modeChanged)
        
    def connectEditor(self, editor):
        editor.cursorPositionChanged.connect(self.on_cursorPositionChanged)
        editor.syntaxChanged.connect(self.on_syntaxChanged)
        editor.modeChanged.connect(self.on_modeChanged)
        
    def setCurrentEditor(self, editor):
        if self.currentEditor is not None:
            self.disconnectEditor(self.currentEditor)
        #Change currentEditor
        self.currentEditor = editor
        self.hideAllWidgets()
        if self.currentEditor is not None:
            self.connectEditor(self.currentEditor)
            self.comboBoxSymbols.setModel(self.currentEditor.symbolListModel)
            self.on_cursorPositionChanged(self.currentEditor)
            self.on_syntaxChanged(self.currentEditor.getSyntax())
            self.on_modeChanged(self.currentEditor)
            self.setTabSizeLabel(self.currentEditor)
        
    #============================================================
    # Status Widget
    #============================================================
    # AutoConnect signals----------------------------------------
    @QtCore.pyqtSlot(int)
    def on_comboBoxSyntaxes_activated(self, index):
        if self.currentEditor is not None:
            model = self.comboBoxSyntaxes.model()
            node = model.node(model.createIndex(index, 0))
            self.currentEditor.setSyntax(node)

    @QtCore.pyqtSlot(int)
    def on_comboBoxTabSize_activated(self, index):
        data = self.comboBoxTabSize.itemData(index)
    
    @QtCore.pyqtSlot(int)
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
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        selection = cursor.selectionEnd() - cursor.selectionStart()
        self.labelLineColumn.setText("Line: %5d Column: %5d Selection: %5d" % (line, column, selection))
        #Set index of current symbol
        self.comboBoxSymbols.setCurrentIndex(self.comboBoxSymbols.model().findBlockIndex(cursor.block()))
        
    def on_syntaxChanged(self, syntax):
        model = self.comboBoxSyntaxes.model()
        index = model.findItemIndex(syntax)
        self.comboBoxSyntaxes.setCurrentIndex(index)

    def on_modeChanged(self, editor = None):
        editor = editor or self.currentEditor
        self.pushButtonMultiCursor.setEnabled(editor.multiCursorMode.isActive())
        self.pushButtonSnippet.setEnabled(editor.snippetMode.isActive())
        self.pushButtonOverwrite.setEnabled(editor.overwriteMode())
        
    def showTabSizeContextMenu(self, point):
        editor = self.currentEditor
        #Setup Context Menu
        menu = QtGui.QMenu(self)
        menu.setObjectName('tabSizeMenu')
        
        for size in [2, 4, 8]:
            action = menu.addAction("%d" % size, lambda size = size: self.setCurrentEditorTabSize(size))
            action.setCheckable(True)
            action.setChecked(editor.tabStopSize == size)
        
        if editor.tabStopSize not in [2,4,8]:
            action = menu.addAction("Other (%d)" % editor.tabStopSize)
            action.setCheckable(True)
            action.setChecked(True)
        else:
            action = menu.addAction("Other")
            action.setCheckable(True)
        
        menu.addSeparator()
        action = menu.addAction("Soft Tabs (Spaces)", lambda soft = not editor.tabStopSoft: self.setCurrentEditorTabSoft(soft))
        action.setCheckable(True)        
        action.setChecked(editor.tabStopSoft == True)
        menu.popup(self.labelTabSize.mapToGlobal(point))
    
    def setCurrentEditorTabSoft(self, soft):
        self.currentEditor.tabStopSoft = soft
        
    def setCurrentEditorTabSize(self, size):
        self.currentEditor.tabStopSize = size
        self.setTabSizeLabel(self.currentEditor)
        
    def setTabSizeLabel(self, editor):
        #Tab Size
        self.labelTabSize.setText("Soft Tab: %d" % editor.tabStopSize if editor.tabStopSoft else "Hard Tab: %d" % editor.tabStopSize)
        
    #============================================================
    # AutoConnect Command widget signals
    #============================================================
    @QtCore.pyqtSlot()
    def on_pushButtonCommandClose_pressed(self):
        self.widgetCommand.setVisible(False)
    
    @QtCore.pyqtSlot()
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
    
    #============================================================
    # AutoConnect GoToLine widget signals
    #============================================================
    @QtCore.pyqtSlot()
    def on_pushButtonGoToLineClose_pressed(self):
        self.widgetGoToLine.setVisible(False)
    
    @QtCore.pyqtSlot(int)
    def on_spinBoxGoToLine_valueChanged(self, lineNumber):
        self.currentEditor.goToLine(lineNumber)

    def showGoToLine(self):
        self.hideAllWidgets()
        self.widgetGoToLine.setVisible(True)
        self.spinBoxGoToLine.setFocus()
        
    #============================================================
    # FindReplace widget
    #============================================================
    # AutoConnect Signals ---------------------------------------
    @QtCore.pyqtSlot()
    def on_pushButtonFindReplaceClose_pressed(self):
        self.widgetFindReplace.setVisible(False)
    
    @QtCore.pyqtSlot()
    def on_pushButtonFindNext_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        self.currentEditor.findMatch(match, flags, True)

    @QtCore.pyqtSlot()
    def on_pushButtonFindPrevious_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        flags |= QtGui.QTextDocument.FindBackward
        self.currentEditor.findMatch(match, flags)
    
    @QtCore.pyqtSlot()
    def on_pushButtonReplace_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        replace = self.lineEditReplace.text()
        self.currentEditor.replaceMatch(match, replace, flags)
        self.currentEditor.findMatch(match, flags)
    
    @QtCore.pyqtSlot()
    def on_pushButtonReplaceAll_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        replace = self.lineEditReplace.text()
        if len(match) == 0 and len(replace) == 0:
            self.currentEditor.replaceMatch(match, replace, flags, False)
        else:
            self.currentEditor.replaceMatch(match, replace, flags, True)

    @QtCore.pyqtSlot()
    def on_pushButtonFindAll_pressed(self):
        match, flags = self.getFindMatchAndFlags()
        self.currentEditor.findAll(match, flags)
        
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
        
    #============================================================
    # IFind widget
    #============================================================
    # AutoConnect Signals ---------------------------------------
    @QtCore.pyqtSlot()
    def on_pushButtonIFindClose_pressed(self):
        self.widgetIFind.setVisible(False)
        self.currentEditor.setFocus()
    
    @QtCore.pyqtSlot(str)
    def on_lineEditIFind_textChanged(self, text):
        if text:
            _, flags = self.getIFindMatchAndFlags()
            match = self.currentEditor.findMatch(text, flags)
            self.lineEditIFind.setStyleSheet(match and resources.FIND_MATCH_STYLE or resources.FIND_NO_MATCH_STYLE)
        else:
            #TODO: Buscar un clean style
            self.lineEditIFind.setStyleSheet('')
    
    @QtCore.pyqtSlot()
    def on_pushButtonIFindNext_pressed(self):
        match, flags = self.getIFindMatchAndFlags()
        self.currentEditor.findMatch(match, flags, True)

    @QtCore.pyqtSlot()
    def on_pushButtonIFindPrevious_pressed(self):
        match, flags = self.getIFindMatchAndFlags()
        flags |= QtGui.QTextDocument.FindBackward
        self.currentEditor.findMatch(match, flags)
    
    @QtCore.pyqtSlot(int)
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

    #===========================================================================
    # Menus
    #===========================================================================
    # Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls, addonClasses):
        edit = {
            'items': [
                '-',
                {'text': "Find",
                 'shortcut': "Ctrl+F",
                 'callback': cls.showIFind
                },
                {'text': "Replace",
                 'shortcut': "Ctrl+R",
                 'callback': cls.showFindReplace
                }
            ]}
        text = {
            'items': [
                {'text': 'Filter Through Command',
                 'callback': cls.showCommand
                 }
            ]}
        navigation = {
            'items': [
                {'text': 'Go To &Line',
                 'callback': cls.showGoToLine,
                 'shortcut': 'Meta+Ctrl+Shift+L',
                 }
            ]}
        return { "Edit": edit, "Navigation": navigation, "Text": text }