#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QColorDialog

class AcceptableColorDialog(QColorDialog):
    def __init__(self, *largs):
        super(AcceptableColorDialog, self).__init__(*largs)
        
    __isAccepted = False
    @property
    def isAccepted(self):
        return self.__isAccepted
    
    @isAccepted.setter
    def isAccepted(self, value):
        assert type(value) is bool
        self.__isAccepted = value
    
    def accept(self, *largs):
        self.isAccepted = True
        super(AcceptableColorDialog, self).accept(*largs)
    
class PMXColorDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, options, index):
        editor = AcceptableColorDialog(parent)
        editor.setOptions(QtGui.QColorDialog.ShowAlphaChannel)
        return editor
    
    def setModelData(self, colorDialog, model, index):
        if colorDialog.isAccepted:
            color = colorDialog.currentColor()
            model.setData(index, color)
    
    def setEditorData(self, colorDialog, index):
        variant = index.data()
        if variant.canConvert(QtCore.QVariant.Color):
            colorDialog.setCurrentColor(QtGui.QColor(variant))
