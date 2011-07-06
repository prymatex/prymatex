#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class AcceptableColorDialog(QtGui.QColorDialog):
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

class PMXWidgetDelegate(QtGui.QStyledItemDelegate):
    # Taken from http://www.qtcentre.org/threads/26916-inserting-custom-Widget-to-listview?p=155774#post155774
    def __init__(self, parent, widget = QtGui.QLabel("Change ME!")):
        super(PMXWidgetDelegate, self).__init__(parent)
        self.widget = widget
        
    def paint(self, painter, option, index):
        
        self.widget.resize(option.rect.size())
        #
        #       Here update the witem with some method with the real item data
        #       Update labels, icons, and so on
        #       */
                
        painter.save()
        painter.translate(option.rect.topLeft())
        self.widget.render(painter)
        painter.restore()
        
class PMXFontStyleDelegate(PMXWidgetDelegate):
    def __init__(self, parent):
        widget = self.createWidget()
        super(PMXFontStyleDelegate, self).__init__(parent, widget)
        
    def createWidget(self):
        widget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        self.buttonBold = QtGui.QPushButton("B")
        self.buttonBold.setCheckable(True)
        font = QtGui.QFont()
        font.setWeight(QtGui.QFont.Bold)
        self.buttonBold.setFont(font)
        font = QtGui.QFont()
        font.setItalic(True)
        self.buttonItalic = QtGui.QPushButton("I")
        self.buttonItalic.setCheckable(True)
        self.buttonItalic.setFont(font)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.buttonUnderline = QtGui.QPushButton("U")
        self.buttonUnderline.setCheckable(True)
        self.buttonUnderline.setFont(font)
        layout.addWidget(self.buttonBold)
        layout.addWidget(self.buttonItalic)
        layout.addWidget(self.buttonUnderline)
        widget.setLayout(layout)
        return widget
    
    def createEditor(self, parent, option, index):
        widget = self.createWidget()
        widget.setParent(parent)
        return widget
        
        
        