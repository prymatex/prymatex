#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from functools import reduce

from prymatex.qt import QtCore, QtGui, Qt

from prymatex.core import config
from prymatex.models.support import BundleItemTreeNode

# ===================================
# Completer
# ===================================
class CodeEditorCompleter(QtGui.QCompleter):
    def __init__(self, editor):
        super(CodeEditorCompleter, self).__init__(parent = editor)
        self.editor = editor
        self.editor.registerKeyPressHandler(QtCore.Qt.Key_Enter, 
            self.__insert_completion, important = True)
        self.editor.registerKeyPressHandler(QtCore.Qt.Key_Return, 
            self.__insert_completion, important = True)
        self.editor.registerKeyPressHandler(QtCore.Qt.Key_Tab, 
            self.__insert_completion, important = True)

        self._start_position = 0
        # Models
        self.completionModels = [ ]

        self.completerTasks = [ ]
        
        # Role
        self.setCompletionRole(QtCore.Qt.MatchRole)
        
        # Popup table view
        self.setPopup(QtGui.QTableView(self.editor))
        self.popup().setAlternatingRowColors(True)
        self.popup().verticalHeader().setVisible(False)
        self.popup().horizontalHeader().setStretchLastSection(True)
        self.popup().horizontalHeader().setVisible(False)
        self.popup().setShowGrid(False)
        self.popup().setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.popup().setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.popup().setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.activated[QtCore.QModelIndex].connect(self.activatedCompletion)
        self.highlighted[QtCore.QModelIndex].connect(self.highlightedCompletion)

        self.setWidget(self.editor)
    
    def __insert_completion(self, event):
        if self.isVisible():
            event.ignore()
            return True
        return False

    def completionPrefixRange(self):
        prefix = self.completionPrefix()
        return prefix, self._start_position, self._start_position + len(prefix) + 1
        
    def startPosition(self):
        return self._start_position

    def setPalette(self, palette):
        self.popup().setPalette(palette)
        self.popup().viewport().setPalette(palette)

    def isVisible(self):
        return self.completionMode() == QtGui.QCompleter.PopupCompletion and self.popup().isVisible()

    def hide(self):
        if self.completionMode() == QtGui.QCompleter.PopupCompletion:
            self.popup().hide()

    def fixPopupView(self):
        if self.completionMode() == QtGui.QCompleter.PopupCompletion:
            self.popup().resizeColumnsToContents()
            self.popup().resizeRowsToContents()
            width = self.popup().verticalScrollBar().sizeHint().width()
            for columnIndex in range(self.model().columnCount()):
                width += self.popup().columnWidth(columnIndex)
            self.popup().setMinimumWidth(width > 212 and width or 212)
            height = self.popup().rowHeight(0) * self.completionCount()
            self.popup().setMinimumHeight(height > 343 and 343 or height)

    def activatedCompletion(self, index):
        self.model().activatedCompletion(self.completionModel().mapToSource(index))
        
    def highlightedCompletion(self, index):
        self.model().highlightedCompletion(self.completionModel().mapToSource(index))
        
    def setCurrentRow(self, index):
        if not QtGui.QCompleter.setCurrentRow(self, index):
            return False
        cIndex = self.completionModel().index(index, 0)
        if self.completionMode() == QtGui.QCompleter.PopupCompletion:
            self.popup().setCurrentIndex(cIndex)
        return self.model().setCurrentRow(
            self.completionModel().mapToSource(cIndex), self.completionCount())

    def setCompletionPrefix(self, prefix):
        self._start_position = self.editor.textCursor().position() - len(prefix or "")
        for model in self.completionModels:
            model.setCompletionPrefix(prefix)
        QtGui.QCompleter.setCompletionPrefix(self, prefix)
        if self.model() is not None:
            self.fixPopupView()
    
    def setModel(self, model):
        # Esto esta bueno pero cuando cambias de modelo tenes que hacer algo mas
        #self.setModelSorting(model.modelSorting())
        #self.setCaseSensitivity(model.caseSensitivity())
        QtGui.QCompleter.setModel(self, model)

    def trySetModel(self, model):
        current_model = self.model()
        if model not in self.completionModels:
            return False
        self.setModel(model)
        if self.setCurrentRow(0):
            self.fixPopupView()
        else:
            self.setModel(current_model)
        return self.model() != current_model
        
    def registerModel(self, completionModel):
        self.completionModels.append(completionModel)
        completionModel.setEditor(self.editor)
    
    def unregisterModel(self, completionModel):
        self.completionModels.remove(completionModel)
        completionModel.setEditor(None)

    def trySetNextModel(self):
        current = model = self.model() or self.completionModels[-1]
        while True:
            index = (self.completionModels.index(model) + 1) % len(self.completionModels)
            model = self.completionModels[index]
            if model.isReady() and self.trySetModel(model):
                return True
            if current == model:
                break
        return False

    def runCompleter(self, rect, model = None):
        if self.isVisible():
            if model != self.model() and self.trySetModel(model):
                self.complete(rect)
        elif not self.isVisible():
            for completerTask in self.completerTasks:
                completerTask.cancel()
            self.setModel(None)
            def _go(model):
                # First win
                if self.model() is None and self.trySetModel(model):
                    self.complete(rect)
            if model is not None:
                _go(model)
            self.completerTasks = self.editor.application().schedulerManager.tasks(
                lambda model: model.fillModel(_go), self.completionModels)
