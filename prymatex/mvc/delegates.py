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
    
class PMXColorDelegate(QtGui.QStyledItemDelegate):
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
            
    def paint(self, painter, option, index):
        data = index.data().toPyObject()
        if isinstance(data, QtGui.QColor):
            painter.save()
            #Con un pixmap lindo
            #pixmap = QtGui.QPixmap(16, 16)
            #pixmap.fill(data)
            #painter.translate(option.rect.topLeft())
            #painter.drawPixmap(0, 0, pixmap)
            #Pintando todo
            brush = QtGui.QBrush(data)
            painter.fillRect(option.rect, brush)
            painter.restore()
            return
        super(PMXColorDelegate, self).paint(painter, option, index)
    
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
        
class PMXFontStyleDelegate(QtGui.QStyledItemDelegate):
    
    def __init__(self, parent):
        # Store the widget and update it acordigly
        super(PMXFontStyleDelegate, self).__init__(parent)
        self.widgetDict = {}
        
    def createWidget(self):
        widget = PMXFontStyleWidget()
        return widget
    
    def createEditor(self, parent, option, index):
        widget = self.createWidget()
        widget.setParent(parent)
        return widget
        
    def setModelData(self, editedWidget, model, index):
        flags = set()
        widgetToPaint = self.getWidgetForIndex(index)
        widgetToPaint.buttonBold.setChecked(editedWidget.buttonBold.isChecked())
        if editedWidget.buttonBold.isChecked():
            flags.add('bold')
        
        widgetToPaint.buttonItalic.setChecked(editedWidget.buttonItalic.isChecked())    
        if editedWidget.buttonItalic.isChecked():
            flags.add('italic')
            
        widgetToPaint.buttonUnderline.setChecked(editedWidget.buttonUnderline.isChecked())
        if editedWidget.buttonUnderline.isChecked():
            flags.add('underline')
            
        model.setData(index, flags)
    
    def setEditorData(self, widget, index):
        flags = index.data().toPyObject()
        widget.buttonBold.setChecked('bold' in flags)
        widget.buttonItalic.setChecked('italic' in flags)
        widget.buttonUnderline.setChecked('underline' in flags)
    
    def getWidgetForIndex(self, index):
        indexTuple = index.column(), index.row()
        
        if not indexTuple in self.widgetDict:
            widget = self.createWidget()
            self.setEditorData(widget, index)
            self.widgetDict[indexTuple] = widget
            
        return self.widgetDict[indexTuple]
    
    def paint(self, painter, option, index):
        widget = self.getWidgetForIndex(index)
        widget.resize(option.rect.size())
        #
        #       Here update the witem with some method with the real item data
        #       Update labels, icons, and so on
        #       */
                
        painter.save()
        painter.translate(option.rect.topLeft())
        widget.render(painter)
        painter.restore()