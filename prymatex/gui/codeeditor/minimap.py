#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from prymatex.qt import QtGui, QtCore

from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.codeeditor.sidebar import SideBarWidgetAddon

class MiniMapAddon(QtGui.QPlainTextEdit, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignRight
    WIDTH = 100
    MINIMAP_MAX_OPACITY = 0.8
    MINIMAP_MIN_OPACITY = 0.1
    
    @pmxConfigPorperty(default = True)
    def showMiniMap(self, value):
        self.setVisible(value)
    
    def __init__(self, parent):
        QtGui.QPlainTextEdit.__init__(self, parent)

        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)
        self.setCenterOnScroll(True)
        self.setMouseTracking(True)
        self.viewport().setCursor(QtCore.Qt.PointingHandCursor)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        self.lines_count = 0
        self.goe = QtGui.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.goe)
        self.goe.setOpacity(self.MINIMAP_MIN_OPACITY)
        self.animation = QtCore.QPropertyAnimation(self.goe, "opacity")
        
        self.slider = SliderArea(self)
        self.slider.show()
        self.setFixedWidth(self.WIDTH)

    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        editor.themeChanged.connect(self.on_editor_themeChanged)
        editor.highlightChanged.connect(self.on_editor_highlightChanged)
        editor.document().contentsChange.connect(self.on_document_contentsChange)
        editor.updateRequest.connect(self.update_visible_area)
        
        # Setup font
        font = editor.document().defaultFont()
        font.setPointSize(int(self.width() / editor.marginLineSize))
        self.setFont(font)

        # TODO El ancho del tabulador
        self.setTabStopWidth(editor.tabStopWidth())
        
        self.on_editor_themeChanged()
    
    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "rightGutter" or "leftGutter"
        menuEntry = {
            'name': 'miniMap',
            'text': "Minimap",
            'toggled': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return { baseMenu: menuEntry }
    
    def on_editor_themeChanged(self):
        #Editor colours
        appStyle = """QPlainTextEdit {background-color: %s;
        color: %s;
        border: 0px;
        selection-background-color: %s; }""" % (
            self.editor.colours['background'].name(), 
            self.editor.colours['foreground'].name(), 
            self.editor.colours['selection'].name())
        self.setStyleSheet(appStyle)
        self.slider.setStyleSheet("background: %s;" % self.editor.colours['selection'].name())

    def on_editor_highlightChanged(self):
        block = self.editor.document().begin()
        length = 0
        while block.isValid():
            miniBlock = self.document().findBlockByNumber(block.blockNumber())
            miniBlock.layout().setAdditionalFormats(block.layout().additionalFormats())
            length += block.length()
            block = block.next()

        self.document().markContentsDirty(0, length)
    
    def on_document_contentsChange(self, position, charsRemoved, charsAdded):
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(position)
        if charsRemoved:
            cursor.setPosition(position + charsRemoved, QtGui.QTextCursor.KeepAnchor)
        text = self.editor.document().toPlainText()[position: position + charsAdded]
        cursor.insertText(text)
        block = self.editor.document().findBlock(position)
        miniBlock = self.document().findBlock(position)
        miniBlock.layout().setAdditionalFormats(block.layout().additionalFormats())
        self.document().markContentsDirty(miniBlock.position(), miniBlock.length())
    
    def update_visible_area(self):
        if not self.slider.pressed:
            line_number = self.editor.firstVisibleBlock().blockNumber()
            block = self.document().findBlockByLineNumber(line_number)
            cursor = self.textCursor()
            cursor.setPosition(block.position())
            rect = self.cursorRect(cursor)
            line_height = self.editor.cursorRect().height()
            if line_height:
                self.lines_count = self.editor.viewport().height() / line_height
            self.setTextCursor(cursor)
            self.slider.move_slider(rect.y())
            self.slider.update_position()

    def enterEvent(self, event):
        self.animation.setDuration(300)
        self.animation.setStartValue(self.MINIMAP_MIN_OPACITY)
        self.animation.setEndValue(self.MINIMAP_MAX_OPACITY)
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setDuration(300)
        self.animation.setStartValue(self.MINIMAP_MAX_OPACITY)
        self.animation.setEndValue(self.MINIMAP_MIN_OPACITY)
        self.animation.start()

    def mousePressEvent(self, event):
        QtGui.QPlainTextEdit.mousePressEvent(self, event)
        cursor = self.cursorForPosition(event.pos())
        self.editor.goToBlock(cursor.block())

    def resizeEvent(self, event):
        QtGui.QPlainTextEdit.resizeEvent(self, event)
        self.slider.update_position()

    def scroll_area(self, pos_parent, pos_slider):
        pos_parent.setY(pos_parent.y() - pos_slider.y())
        cursor = self.cursorForPosition(pos_parent)
        self.editor.verticalScrollBar().setValue(cursor.blockNumber())

    def wheelEvent(self, event):
        QtGui.QPlainTextEdit.wheelEvent(self, event)
        self.editor.wheelEvent(event)

    def scroll(self, *largs):
        pass
            
class SliderArea(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setMouseTracking(True)
        self.setCursor(QtCore.Qt.OpenHandCursor)

        self.goe = QtGui.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.goe)
        self.goe.setOpacity(parent.MINIMAP_MAX_OPACITY / 2)

        self.pressed = False
        self.__scroll_margins = None

    def update_position(self):
        line_height = self.parent().cursorRect().height()
        height = self.parent().lines_count * line_height
        self.setFixedHeight(height)
        self.setFixedWidth(self.parent().width())
        self.__scroll_margins = (height, self.parent().height() - height)

    def move_slider(self, y):
        self.move(0, y)

    def mousePressEvent(self, event):
        QtGui.QFrame.mousePressEvent(self, event)
        self.pressed = True
        self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        QtGui.QFrame.mouseReleaseEvent(self, event)
        self.pressed = False
        self.setCursor(QtCore.Qt.OpenHandCursor)
    
    def wheelEvent(self, event):
        self.parent().wheelEvent(event)

    def mouseMoveEvent(self, event):
        QtGui.QFrame.mouseMoveEvent(self, event)
        if self.pressed:
            pos = self.mapToParent(event.pos())
            y = pos.y() - (self.height() / 2)
            if y < 0:
                y = 0
            if y < self.__scroll_margins[0]:
                self.parent().verticalScrollBar().setSliderPosition(
                    self.parent().verticalScrollBar().sliderPosition() - 2)
            elif y > self.__scroll_margins[1]:
                self.parent().verticalScrollBar().setSliderPosition(
                    self.parent().verticalScrollBar().sliderPosition() + 2)
            self.move(0, y)
            self.parent().scroll_area(pos, event.pos())
