#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtWidgets

from prymatex.core import config

# ===================================
# Completer Base Model
# ===================================
class CompletionBaseModel(QtCore.QAbstractTableModel):
    suggestionsReady = QtCore.Signal()
    def __init__(self, **kwargs):
        super(CompletionBaseModel, self).__init__(**kwargs)
        self.editor = None
        self._prefix = None
        self._priority = 0

    def priority(self):
        return self._priority
        
    def setPriority(self, priority):
        self._priority = priority

    def completionPrefix(self):
        return self._prefix
        
    def setCompletionPrefix(self, prefix):
        self._prefix = prefix

    def setEditor(self, editor):
        self.editor = editor

    def setCurrentRow(self, index, completion_count):
        return False
    
    def modelSorting(self):
        #QCompleter.UnsortedModel
        #QCompleter.CaseSensitivelySortedModel
        #QCompleter.CaseInsensitivelySortedModel
        return QtWidgets.QCompleter.UnsortedModel

    def caseSensitivity(self):
        #QtCore.Qt.CaseInsensitive
        #QtCore.Qt.CaseSensitive
        return QtCore.Qt.CaseSensitive

    def filterMode(self):
        #QtCore.Qt.MatchStartsWith
        #QtCore.Qt.MatchContains
        #QtCore.Qt.MatchEndsWith 
        return QtCore.Qt.MatchStartsWith
        
    def fill(self):
        raise NotImplemented
    
    def isReady(self):
        raise NotImplemented
    
    def activatedCompletion(self, index):
        raise NotImplemented

    def highlightedCompletion(self, index):
        raise NotImplemented

# ===================================
# Custom completer models
# ===================================
class WordsCompletionModel(CompletionBaseModel):
    def __init__(self, **kwargs):
        super(WordsCompletionModel, self).__init__(**kwargs)
        self.suggestions = set()

    # ----------- Setup completer
    def modelSorting(self):
        return QtWidgets.QCompleter.CaseInsensitivelySortedModel

    def caseSensitivity(self):
        return QtCore.Qt.CaseInsensitive
    
    def filterMode(self):
        return QtCore.Qt.MatchContains

    def fill(self):
        # TODO Hacer las palabras con un timer
        # TODO Palabras mas proximas al cursor o mas utilizadas
        self.suggestions = set()
        block = self.editor.document().begin()
        # TODO: No usar la linea actual, quiza algo de niveles de anidamiento
        while block.isValid():
            user_data = self.editor.blockUserData(block)
            all_words = map(lambda token: config.RE_WORD.findall(token.chunk),
                user_data.tokens[::-1])
            for words in all_words:
                self.suggestions.update(words)
            block = block.next()

        self.suggestions.update(self.editor.preferenceSettings().completions)
        self.suggestions.discard(self.completionPrefix())
        if self.suggestions:
            self.suggestions = sorted(list(self.suggestions))
            self.suggestionsReady.emit()

    def isReady(self):
        return bool(self.suggestions)

    def activatedCompletion(self, index):
        suggestion = self.suggestions[index.row()]
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end)
        cursor.insertText(suggestion)
        
    def highlightedCompletion(self, index):
        suggestion = self.suggestions[index.row()]

    # -------------- Model overrite methods
    def columnCount(self, parent = None):
        return 1

    def rowCount(self, parent = None):
        return len(self.suggestions)

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.suggestions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()
            
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return suggestion
        elif role == QtCore.Qt.ToolTipRole:
            return suggestion
        elif role == QtCore.Qt.MatchRole:
            #return text.fuzzy_match(self.prefix, suggestion) and self.prefix or suggestion
            return suggestion

    def setCurrentRow(self, index, completion_count):
        suggestion = self.suggestions[index.row()]
        return completion_count > 1 or self.completionPrefix() != suggestion

class TabTriggerItemsCompletionModel(CompletionBaseModel):
    def __init__(self, **kwargs):
        super(TabTriggerItemsCompletionModel, self).__init__(**kwargs)
        self.triggers = []

    def caseSensitivity(self):
        return QtCore.Qt.CaseSensitive
        
    def fill(self):
        leftScope, rightScope = self.editor.scope(self.editor.textCursor())
        self.triggers = self.editor.application().supportManager.getAllTabTriggerItemsByScope(leftScope, rightScope)
        if self.triggers:
            self.suggestionsReady.emit()
    
    # -------------- Model overrite methods
    def columnCount(self, parent = None):
        return 2

    def rowCount(self, parent = None):
        return len(self.triggers)

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.triggers):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.triggers[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            #Es un bundle item
            if index.column() == 0:
                return suggestion.tabTrigger
            elif index.column() == 1:
                return suggestion.name
        elif role == QtCore.Qt.DecorationRole and index.column() == 0:
            return suggestion.icon()
        elif role == QtCore.Qt.ToolTipRole:
            return suggestion.name
        elif role == QtCore.Qt.MatchRole:
            return suggestion.tabTrigger

    def isReady(self):
        return bool(self.triggers)

    def activatedCompletion(self, index):
        trigger = self.triggers[index.row()]
        currentWord, start, end = self.editor.currentWord()
        cursor = self.editor.newCursorAtPosition(start, end)
        cursor.removeSelectedText()
        self.editor.insertBundleItem(trigger, textCursor = cursor)

    def highlightedCompletion(self, index):
        trigger = self.triggers[index.row()]
        
    def setCurrentRow(self, index, completion_count):
        return completion_count > 0

class SuggestionsCompletionModel(CompletionBaseModel):
    #display The title to display in the suggestions list
    #insert Snippet to insert after selection
    #image An image name, see the :images option
    #match Typed text to filter on (defaults to display)

    def __init__(self, **kwargs):
        super(SuggestionsCompletionModel, self).__init__(**kwargs)
        self.suggestions = []
        self.completionCallback = None

    def setSuggestions(self, suggestions):
        self.modelAboutToBeReset.emit()
        self.suggestions = suggestions
        self.modelReset.emit()

    def setCompletionCallback(self, callback):
        self.completionCallback = callback

    # -------------- Model overrite methods
    def columnCount(self, parent = None):
        return 1

    def rowCount(self, parent = None):
        return len(self.suggestions)

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.suggestions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        suggestion = self.suggestions[index.row()]
        if role == QtCore.Qt.DisplayRole:
            if 'display' in suggestion:
                return suggestion['display']
            elif 'title' in suggestion:
                return suggestion['title']
        elif role == QtCore.Qt.EditRole:
            if 'match' in suggestion:
                return suggestion['match']
            elif 'display' in suggestion:
                return suggestion['display']
            elif 'title' in suggestion:
                return suggestion['title']
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0 and 'image' in suggestion:
                return self.editor.resources().get_icon(suggestion['image'])
        elif role == QtCore.Qt.ToolTipRole:
            if 'tooltip' in suggestion:
                if 'tooltip_format' in suggestion:
                    print(suggestion["tooltip_format"])
                return suggestion['tooltip']
        elif role == QtCore.Qt.MatchRole:
            return suggestion['display']

    def fill(self):
        pass

    def isReady(self):
        return bool(self.suggestions)

    def activatedCompletion(self, index):
        self.completionCallback(self.suggestions[index.row()])

    def highlightedCompletion(self, index):
        suggestion = self.suggestions[index.row()]
        if 'tooltip' in suggestion and suggestion['tooltip']:
            self.editor.showTooltip(suggestion['tooltip'])
            
    def setCurrentRow(self, index, completion_count):
        suggestion = self.suggestions[index.row()]
        return suggestion.get('insert') != self.completionPrefix()
