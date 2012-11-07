#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

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
        color = index.data()
        if color is not None:
            colorDialog.setCurrentColor(color)
            
    def paint(self, painter, option, index):
        data = index.data()
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
        self.buttonBold.setMaximumWidth(30)
        
        self.buttonItalic = QtGui.QPushButton("I")
        self.buttonItalic.setCheckable(True)
        font = QtGui.QFont()
        font.setItalic(True)
        self.buttonItalic.setFont(font)
        self.buttonItalic.setMaximumWidth(30)
        
        self.buttonUnderline = QtGui.QPushButton("U")
        self.buttonUnderline.setCheckable(True)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.buttonUnderline.setFont(font)
        self.buttonUnderline.setMaximumWidth(30)
        
        layout.addWidget(self.buttonBold)
        layout.addWidget(self.buttonItalic)
        layout.addWidget(self.buttonUnderline)
        self.setLayout(layout)
        
class PMXFontStyleDelegate(QtGui.QStyledItemDelegate):
    
    def __init__(self, parent):
        # Store the widget and update it acordigly
        super(PMXFontStyleDelegate, self).__init__(parent)
        
    def createEditor(self, parent, option, index):
        return PMXFontStyleWidget(parent)
        
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
        flags = index.data()
        widget.buttonBold.setChecked('bold' in flags)
        widget.buttonItalic.setChecked('italic' in flags)
        widget.buttonUnderline.setChecked('underline' in flags)
    
    def getWidgetForIndex(self, index):
        indexTuple = index.column(), index.row()
        widget = PMXFontStyleWidget()
        self.setEditorData(widget, index)
        return widget
    
    def paint(self, painter, option, index):
        widget = self.getWidgetForIndex(index)
        #widget.resize(option.rect.size())
        painter.save()
        painter.translate(option.rect.topLeft())
        widget.render(painter)
        painter.restore()