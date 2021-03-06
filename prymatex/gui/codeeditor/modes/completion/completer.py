#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from functools import reduce

from prymatex.qt import QtCore, QtGui, Qt, QtWidgets, API

from prymatex.core import config
from prymatex.models.support import BundleItemTreeNode

# ===================================
# Completer
# ===================================
class CodeEditorCompleter(QtWidgets.QCompleter):
    def __init__(self, editor):
        super(CodeEditorCompleter, self).__init__(parent = editor)
        self.editor = editor

        # Models
        self.completion_models = [ ]

        # Role
        self.setCompletionRole(QtCore.Qt.MatchRole)
        
        # Popup table view
        self.setPopup(QtWidgets.QTableView(self.editor))
        self.popup().setAlternatingRowColors(True)
        self.popup().verticalHeader().setVisible(False)
        self.popup().horizontalHeader().setStretchLastSection(True)
        self.popup().horizontalHeader().setVisible(False)
        self.popup().setShowGrid(False)
        self.popup().setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.popup().setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.popup().setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.activated[QtCore.QModelIndex].connect(self.activatedCompletion)
        self.highlighted[QtCore.QModelIndex].connect(self.highlightedCompletion)

        self.setWidget(self.editor)
    
    # ------------------- Register models
    def registerModel(self, completionModel):
        self.completion_models.append(completionModel)
        completionModel.suggestionsReady.connect(self.on_model_suggestionsReady)
        completionModel.setEditor(self.editor)
        completionModel.setPriority(len(self.completion_models))
    
    def unregisterModel(self, completionModel):
        self.completion_models.remove(completionModel)
        completionModel.setEditor(None)
        completionModel.suggestionsReady.disconnect(self.on_model_suggestionsReady)

    def setPalette(self, palette):
        self.popup().setPalette(palette)
        self.popup().viewport().setPalette(palette)

    def isVisible(self):
        return self.completionMode() == QtWidgets.QCompleter.PopupCompletion and self.popup().isVisible()

    def hide(self):
        if self.completionMode() == QtWidgets.QCompleter.PopupCompletion:
            self.popup().hide()

    def activatedCompletion(self, index):
        self.model().activatedCompletion(self.completionModel().mapToSource(index))
        
    def highlightedCompletion(self, index):
        self.model().highlightedCompletion(self.completionModel().mapToSource(index))
        
    def setCurrentRow(self, index):
        if super(CodeEditorCompleter, self).setCurrentRow(index):
            cIndex = self.completionModel().index(index, 0)
            if self.completionMode() == QtWidgets.QCompleter.PopupCompletion:
                self.popup().setCurrentIndex(cIndex)
            return self.model().setCurrentRow(
                self.completionModel().mapToSource(cIndex), self.completionCount())

    def setCompletionPrefix(self, prefix):
        for model in self.completion_models:
            model.setCompletionPrefix(prefix)
        QtWidgets.QCompleter.setCompletionPrefix(self, prefix)
    
    def complete(self, rect):
        width = 0
        for index in range(self.model().columnCount()):
            width += self.popup().sizeHintForColumn(index)
        rect.setWidth(width + self.popup().verticalScrollBar().sizeHint().width())
        super(CodeEditorCompleter, self).complete(rect)

    # ----------- Set or try to set model
    def setModel(self, model):
        super(CodeEditorCompleter, self).setModel(model)
        if model is not None:
            self.setModelSorting(model.modelSorting())
            self.setCaseSensitivity(model.caseSensitivity())
            if API == 'pyqt5':
                self.setFilterMode(model.filterMode())

    def trySetModel(self, model):
        current = self.model()
        prefix = self.completionPrefix()
        self.setModel(model)
        self.setCompletionPrefix(prefix)
        if self.setCurrentRow(0):
            return True
        self.setModel(current)
        return False

    def trySetNextModel(self):
        current = model = self.model() or self.completion_models[-1]
        while True:
            index = (self.completion_models.index(model) + 1) % len(self.completion_models)
            model = self.completion_models[index]
            if current == model:
                break
            if self.trySetModel(model):
                return True
        return False

    @QtCore.Slot()
    def on_model_suggestionsReady(self):
        model = self.sender()
        if not self.isVisible():
            alreadyTyped, start, end = self.editor.wordUnderCursor(direction="left", search = True)
            self.setCompletionPrefix(alreadyTyped)
        if (not self.isVisible() or self.model() is None or self.model().priority() <= model.priority()) and self.trySetModel(model):
            self.complete(self.editor.cursorRect())
        
    def runCompleter(self):
        self.setModel(None)
        for model in self.completion_models:
            model.fill()
