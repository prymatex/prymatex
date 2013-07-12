#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

class ColorDelegate(QtGui.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtGui.QColorDialog(parent)
        editor.setOptions(QtGui.QColorDialog.ShowAlphaChannel)
        return editor

    def setModelData(self, editedWidget, model, index):
        if editedWidget.result() == QtGui.QDialog.Accepted:
            color = editedWidget.currentColor()
            model.setData(index, color)

    def setEditorData(self, editedWidget, index):
        color = index.data()
        if color is not None:
            editedWidget.setCurrentColor(color)
            
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

class FontStyleDelegate(QtGui.QStyledItemDelegate):
    
    def buildFontLayout(self, index, parent = None):
        flags = index.data()
        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        
        buttons = [ QtGui.QPushButton("B"), QtGui.QPushButton("I"), QtGui.QPushButton("U") ]
        
        font = buttons[0].font()
        font.setWeight(QtGui.QFont.Bold)
        buttons[0].setFont(font)
        
        font = buttons[1].font()
        font.setItalic(True)
        buttons[1].setFont(font)
        
        font = buttons[2].font()
        font.setUnderline(True)
        buttons[2].setFont(font)
        
        for button in buttons:
            button.setCheckable(True)
            button.setMaximumWidth(30)
            layout.addWidget(button)
        
        buttons[0].setChecked('bold' in flags)
        buttons[1].setChecked('italic' in flags)
        buttons[2].setChecked('underline' in flags)
        
        layout.buttons = buttons
        return layout
    
    def createEditor(self, parent, option, index):
        dialog = QtGui.QDialog(parent)
        dialog.setLayout(self.buildFontLayout(index, dialog))      
        return dialog
        
    def setModelData(self, editedWidget, model, index):
        flags = set()
        buttons = editedWidget.layout().buttons
        if buttons[0].isChecked():
            flags.add('bold')
        
        if buttons[1].isChecked():
            flags.add('italic')
            
        if buttons[2].isChecked():
            flags.add('underline')
            
        model.setData(index, flags)
    
    def paint(self, painter, option, index):
        widget = QtGui.QWidget()
        widget.setLayout(self.buildFontLayout(index))
        painter.save()
        painter.translate(option.rect.topLeft())
        widget.render(painter)
        painter.restore()