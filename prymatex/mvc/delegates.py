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
        
class PMXFontStyleWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(PMXFontStyleWidget, self).__init__(parent)
        self.setupUi()
        
    def setupUi(self):
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
        self.setLayout(layout)
        
class PMXFontStyleDelegate(PMXWidgetDelegate):
    
    def __init__(self, parent):
        # Store the widget and update it acordigly
        self.widgetToPaint = self.createWidget()
        super(PMXFontStyleDelegate, self).__init__(parent, self.widgetToPaint)
        
    def createWidget(self):
        widget = PMXFontStyleWidget()
        return widget
    
    def createEditor(self, parent, option, index):
        widget = self.createWidget()
        widget.setParent(parent)
        return widget
        
    def setModelData(self, widget, model, index):
        flags = set()
        self.widgetToPaint.buttonBold.setChecked(widget.buttonBold.isChecked())
        if widget.buttonBold.isChecked():
            flags.add('bold')
        
        self.widgetToPaint.buttonItalic.setChecked(widget.buttonItalic.isChecked())    
        if widget.buttonItalic.isChecked():
            flags.add('italic')
            
        self.widgetToPaint.buttonUnderline.setChecked(widget.buttonUnderline.isChecked())
        if widget.buttonUnderline.isChecked():
            flags.add('underline')
            
        modelString = ','.join(flags)
        #print "setModelData", modelString
        model.setData(index, modelString)
    
    def setEditorData(self, widget, index):
        flags = index.data().toString().split(',')
        widget.buttonBold.setChecked('bold' in flags)
        widget.buttonItalic.setChecked('italic' in flags)
        widget.buttonUnderline.setChecked('underline' in flags)
            
        