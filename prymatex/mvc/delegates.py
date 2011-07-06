#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class PMXColorDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtGui.QColorDialog(parent)
        editor.setOptions(QtGui.QColorDialog.ShowAlphaChannel)
        return editor
    
    def setModelData(self, colorDialog, model, index):
        color = colorDialog.currentColor()
        model.setData(index, color)
    
    def setEditorData(self, colorDialog, index):
        variant = index.data()
        if variant.canConvert(QtCore.QVariant.Color):
            colorDialog.setCurrentColor(QtGui.QColor(variant))