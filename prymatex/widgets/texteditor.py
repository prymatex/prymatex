#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import re

from prymatex.qt import QtGui, QtCore

class TextEditWidget(QtGui.QPlainTextEdit):
    RE_MAGIC_FORMAT_BUILDER = re.compile(r"textCharFormat_([A-Za-z]+)_builder", re.UNICODE)
    def __init__(self, parent = None):
        QtGui.QPlainTextEdit.__init__(self, parent)
        
        # TODO: Buscar sobre este atributo en la documnetación
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.scopedExtraSelections = {}
        self.textCharFormatBuilders = {}
        self.registerTextCharFormatBuildersByName()

    #------ Extra selections
    def registerTextCharFormatBuildersByName(self):
        for method in dir(self):
            match = self.RE_MAGIC_FORMAT_BUILDER.match(method)
            if match:
                self.registerTextCharFormatBuilder("%s" % match.group(1), getattr(self, method))

    def registerTextCharFormatBuilder(self, scope, formatBuilder):
        self.textCharFormatBuilders[scope] = formatBuilder
    
    def defaultTextCharFormatBuilder(self, scope):
        return QtGui.QTextCharFormat()

    def extendExtraSelectionCursors(self, scope, cursors):
        self.scopedExtraSelections.setdefault(scope, []).extend(self.__build_extra_selections(scope, cursors))

    def setExtraSelectionCursors(self, scope, cursors):
        self.scopedExtraSelections[scope] = self.__build_extra_selections(scope, cursors)
    
    def updateExtraSelectionCursors(self, cursorsDict):
        map(lambda (scope, cursors): self.setExtraSelectionCursors(scope, cursors), cursorsDict.iteritems())
    
    def updateExtraSelections(self, order = []):
        extraSelections = []
        for scope in order:
            extraSelections.extend(self.scopedExtraSelections[scope])
        for scope, extra in self.scopedExtraSelections.iteritems():
            if scope not in order:
                extraSelections.extend(extra)
        self.setExtraSelections(extraSelections)

    def searchExtraSelections(self, scope):
        cursors = filter(lambda (s, _): s.startswith(scope), self.scopedExtraSelections.iteritems())
        return reduce(lambda c1, (_, c2): c1 + c2, cursors, [])    
    
    def clearExtraSelectionCursors(self, scope):
        del self.scopedExtraSelections[scope]
        
    def clearExtraSelections(self):
        self.scopedExtraSelections.clear()
        self.updateExtraSelections()
        
    def __build_extra_selections(self, scope, cursors):
        extraSelections = []
        for cursor in cursors:
            selection = QtGui.QTextEdit.ExtraSelection()
            if scope in self.textCharFormatBuilders:
                # TODO: un FORMAT_CACHE
                selection.format = self.textCharFormatBuilders[scope]()
            else:
                selection.format = self.defaultTextCharFormatBuilder(scope)
            selection.cursor = cursor
            extraSelections.append(selection)
        return extraSelections
