#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Code Editor Widget.
'''
import os, re, sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, Qt, pyqtSignal, QTimer
from PyQt4.QtGui import QFont, QMessageBox, QFileDialog, QColor, QIcon, QWidget, QAction, QMenu, QKeySequence, qApp, QFocusEvent

from prymatex import resources
from prymatex.support import PMXSyntax
from prymatex.gui.main.widget import PMXBaseWidget
from os.path import join
from prymatex.core.exceptions import APIUsageError
from prymatex.ui.editorwidget import Ui_EditorWidget

class PMXEditorWidget(PMXBaseWidget, Ui_EditorWidget):
    '''
    It implements the logic needed for gui defined in ui_files/editorwidget.ui
    This logic includes Go To Line and Find action behaviour.
    '''
    #===========================================================================
    # Signals
    #===========================================================================
    fileStatusModified = QtCore.pyqtSignal(object)
    fileStatusSynced = QtCore.pyqtSignal(object)
    fileStatusOutOfSync = QtCore.pyqtSignal(object)
    fileStatusDeleted = QtCore.pyqtSignal(object)
    
    def __init__(self, parent = None):
        super(PMXEditorWidget, self).__init__(parent)
        
        self.setupUi(self)
        self.setupFindReplaceWidget()
        self.setupGoToLineWidget()
    
    @classmethod
    def factoryMethod(cls, fileInfo = None, parent = None):
        return cls(parent)
    
    def setFileInfo(self, fileInfo):
        self.fileInfo = fileInfo
        self.tabStatusChanged.emit()
    
    def getTitle(self):
        return self.file.baseName()
    
    def getIcon(self):
        if self.codeEdit.document().isModified():
            return resources.ICONS["save"]
        else:
            return self.application.fileManager.getFileIcon(self.file)
    
    def setContent(self, content):
        return self.codeEdit.setPlainText(content)
    
    
    def focusInEvent(self, event):
        self.codeEdit.setFocus(Qt.MouseFocusReason)
    
    def fileSaved(self):
        self.codeEdit.document().setModified(False)
        self.fileTitleUpdate.emit()
    
    def on_codeEdit_modificationChanged(self, modified):
        self.tabStatusChanged.emit()
    
    @property
    def index(self):
        return self.parent().indexOf(self)
    
    @property
    def tabwidget(self):
        # This is very ugly :(
        from prymatex.gui.tabwidget import PMXTabWidget
        w = self.parent()
        while not isinstance(w, PMXTabWidget):
            w = w.parent()
        return w
        
    def isModified(self):
        return self.codeEdit.document().isModified()
    
    #===========================================================================
    # Factory methods
    #===========================================================================
    
    @classmethod
    def registerEditor(cls, editor_cls):
        '''
        Register an edior class.
        '''
        raise NotImplementedError("No implemented")

    def showFindWidget(self):
        '''
        Find start point
        '''
        self.setReplaceWidgetsShown(False)
        self.findReplaceWidget.show()
        
        text = self.codeEdit.textCursor().selectedText()
        if text.length():
            self.comboFind.setEditText(text)
            
        self.comboFind.setFocus(Qt.MouseFocusReason)


    def showReplaceWidget(self):
        '''
        Replace start point
        '''
        self.setReplaceWidgetsShown(True)
        self.findReplaceWidget.show()
        if self.comboFind.currentText().length() == 0:
            self.comboFind.setFocus(Qt.MouseFocusReason)
        else:
            self.comboReplace.setFocus()
        
    def goToLine(self):
        '''
        Show Go To Line widget
        '''
        self.goToLineWidget.show()
        self.findreplaceWidget.hide()
        self.spinLineNumbers.setFocus(Qt.MouseFocusReason)
        
    def setReplaceWidgetsShown(self, show):
        self.labelReplaceWith.setShown(show)
        self.comboReplace.setShown(show)
        self.pushReplaceAll.setShown(show)
        self.pushReplaceAndFindNext.setShown(show)
        self.pushReplaceAndFindPrevious.setShown(show)
        
    def setupFindReplaceWidget(self):
        
        self.findReplaceWidget.hide()
        self.actionRegex = QAction(self.trUtf8("Use &regular expressions"), self)
        self.actionRegex.setCheckable(True)
        
        self.actionWholeWord = QAction(self.trUtf8("Find &whole word only"), self)
        self.actionWholeWord.setCheckable(True)

        self.actionCaseSensitive = QAction(self.trUtf8("Case &Sensitive"), self)
        self.actionCaseSensitive.setCheckable(True)

        self.menuOptions = QMenu()
        self.menuOptions.addAction(self.actionRegex)
        self.menuOptions.addAction(self.actionWholeWord)
        self.menuOptions.addAction(self.actionCaseSensitive)

        self.pushOptions.setMenu(self.menuOptions)
        
        self.comboFind.editionFinished.connect(self.findReplaceWidget.hide)
        self.comboReplace.editionFinished.connect(self.findReplaceWidget.hide)
        
        # Find/Replace Widget logic
        #self.comboFind.setTextEdit(self.codeEdit)
        self.findReplaceWidget.setTextEdit(self.codeEdit)
        self.comboFind.findRequested.connect(self.findReplaceWidget.findFirstTime)
        self.comboFind.findNextRequested.connect(self.findReplaceWidget.findNext)
        self.findReplaceWidget.findMatchCountChanged.connect(self.comboFind.findMatchCountChanged)
        self.findReplaceWidget.searchFlagsChanged.connect(self.comboFind.optionsChanged)
        self.findReplaceWidget.findMatchCountChanged.connect(self.updateMatchLabel)
        
        self.actionCaseSensitive.toggled.connect(self.findReplaceWidget.setCaseSensitive)
        self.actionRegex.triggered.connect(self.findReplaceWidget.setUseRegex)
        self.actionWholeWord.toggled.connect(self.findReplaceWidget.setWholeWord)

        self.pushFindNext.pressed.connect(self.findReplaceWidget.findNext)
        self.pushFindPrevious.pressed.connect(self.findReplaceWidget.findPrevious)
        
        
        # Replace
        
        self.comboReplace.replaceTextRequested.connect(self.findReplaceWidget.replace)
        self.findReplaceWidget.focusFindBox.connect(self.comboFind.setFocus)
    
    def setupGoToLineWidget(self):
        self.goToLineWidget.hide()
        self.codeEdit.blockCountChanged.connect(self.blockCountChanged)
        linecount = self.codeEdit.blockCount()
        self.goToLineWidget.showed.connect(self.syncGoToLinePosition)
        self.spinLineNumbers.setMaximum(linecount)
        self.spinLineNumbers.valueChanged.connect(self.moveCursorToLine)
        self.spinLineNumbers.editionFinished.connect(self.goToLineWidget.hide)
        

    def on_pushCloseFindreplace_pressed(self):
        self.findreplaceWidget.hide()

    
    def setSyntax(self):
        syntax = PMXSyntax.findSyntaxByFileType(self.path)
        self.codeEdit.setSyntax(syntax)
        
    @property
    def modfified(self):
        return self.codeEdit.document().isModified()
    
    def blockCountChanged(self, new_count):
        self.spinLineNumbers.setMaximum(new_count)
        
    def moveCursorToLine(self, line):
        self.codeEdit.goToLine(line)
        self.codeEdit.ensureCursorVisible()
    
    def syncGoToLinePosition(self):
        lineno = self.codeEdit.textCursor().blockNumber()
        self.spinLineNumbers.setValue(lineno + 1)
    
    def updateMatchLabel(self, match_count):
        label_text = unicode(self.trUtf8("%d matches")) % match_count
        self.labelMatchCounter.setText(label_text)
    
    #===========================================================================
    # Callbacks
    #===========================================================================
    
    def afterInsertionCallback(self):
        ''' Callback when the tab is inserted '''
        QTimer.singleShot(0, self.fileTitleUpdate.emit)
    
    def afterRemoveCallback(self):
        self.file.references -= 1


if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QFont, QWidget, QVBoxLayout
    from PyQt4.QtGui import QPushButton
    app = QApplication(sys.argv)
    app.logger = {}
    win = PMXEditorWidget(None) # No Parent
    win.show()
    sys.exit(app.exec_())

