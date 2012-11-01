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
        
        self.extraSelectionCursors = {}
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
        self.extraSelectionCursors.setdefault(scope, []).extend(cursors)
        
    def updateExtraSelectionCursors(self, extraSelectionCursors):
        for scope, cursors in extraSelectionCursors.iteritems():
            self.extendExtraSelectionCursors(scope, cursors)
        
    def updateExtraSelections(self):
        extraSelections = []
        for scope, cursors in self.extraSelectionCursors.iteritems():
            extraSelections.extend(self.buildExtraSelections(scope, cursors))
        self.setExtraSelections(extraSelections)

    def searchExtraSelectionCursors(self, scope):
        cursors = filter(lambda (s, _): s.startswith(scope), self.extraSelectionCursors.iteritems())
        return reduce(lambda c1, (_, c2): c1 + c2, cursors, [])    
    
    def clearExtraSelectionCursors(self, scope, applyExtraSelections = True):
        del self.extraSelectionCursors[scope]
        if applyExtraSelections:
            self.updateExtraSelections()
        
    def clearExtraSelections(self, applyExtraSelections = True):
        self.extraSelectionCursors.clear()
        if applyExtraSelections:
            self.updateExtraSelections()
        
    def buildExtraSelections(self, scope, cursors):
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
