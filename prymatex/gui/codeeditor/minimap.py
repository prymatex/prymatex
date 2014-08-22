#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from prymatex.qt import QtGui, QtCore

from prymatex.core.settings import ConfigurableItem
from prymatex.gui.codeeditor.sidebar import SideBarWidgetAddon

class MiniMapAddon(SideBarWidgetAddon, QtGui.QPlainTextEdit):
    ALIGNMENT = QtCore.Qt.AlignRight
    WIDTH = 100
    MAX_OPACITY = 0.8
    MIN_OPACITY = 0.2
    
    @ConfigurableItem(default = True)
    def showMiniMap(self, value):
        self.setVisible(value)
    
    def __init__(self, **kwargs):
        super(MiniMapAddon, self).__init__(**kwargs)

        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)
        self.setCenterOnScroll(True)
        self.setMouseTracking(True)
        self.viewport().setCursor(QtCore.Qt.PointingHandCursor)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        self.lines_count = 0
        self.goe = QtGui.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.goe)
        self.goe.setOpacity(self.MIN_OPACITY)
        self.animation = QtCore.QPropertyAnimation(self.goe, "opacity")
        
        self.slider = SliderArea(self)
        self.slider.show()
        self.setFixedWidth(self.WIDTH)

    def initialize(self, **kwargs):
        super(MiniMapAddon, self).initialize(**kwargs)
        self.editor.highlightChanged.connect(self.on_editor_highlightChanged)
        self.editor.document().contentsChange.connect(self.on_document_contentsChange)
        self.editor.updateRequest.connect(self.update_visible_area)
        
    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter"
        menuEntry = {
            'text': "Minimap",
            'toggled': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return { baseMenu: menuEntry }
    
    def setPalette(self, palette):
        super(MiniMapAddon, self).setPalette(palette)
        appStyle = """QPlainTextEdit {background-color: %s;
color: %s;
border: 0;
selection-background-color: %s; }""" % (
            palette.color(QtGui.QPalette.Base).name(),
            palette.color(QtGui.QPalette.Text).name(),
            palette.color(QtGui.QPalette.HighlightedText).name())
        self.setStyleSheet(appStyle)
        self.slider.setPalette(palette)

    def setFont(self, font):
        font = QtGui.QFont(font)
        font.setPointSize(1)
        super(MiniMapAddon, self).setFont(font)
        
    def _apply_aditional_formats(self, block, line_count):
        position = block.position()
        length = 0
        while block.isValid() and line_count:
            miniBlock = self.document().findBlockByNumber(block.blockNumber())
            miniBlock.layout().setAdditionalFormats(
                block.layout().additionalFormats())
            length += block.length()
            block = block.next()
            line_count -= 1

        self.document().markContentsDirty(position, length)

    def on_editor_highlightChanged(self):
        block = self.editor.document().begin()
        line_count = self.editor.document().lineCount()
        self._apply_aditional_formats(block, line_count)
        
    def on_document_contentsChange(self, position, charsRemoved, charsAdded):
        cursor = QtGui.QTextCursor(self.document())
        print("te tengo")
        cursor.setPosition(position)
        print("sii")
        if charsRemoved:
            cursor.setPosition(position + charsRemoved, QtGui.QTextCursor.KeepAnchor)
        text = self.editor.document().toPlainText()[position: position + charsAdded]
        cursor.insertText(text)
        block = self.editor.document().findBlock(position)
        self._apply_aditional_formats(block, len(text.split()))
    
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
        self.animation.setStartValue(self.MIN_OPACITY)
        self.animation.setEndValue(self.MAX_OPACITY)
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setDuration(300)
        self.animation.setStartValue(self.MAX_OPACITY)
        self.animation.setEndValue(self.MIN_OPACITY)
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

        self.goe = QtGui.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.goe)
        self.goe.setOpacity(parent.MAX_OPACITY / 2)

        self.pressed = False
        self.__scroll_margins = None

    def setPalette(self, palette):
        super(SliderArea, self).setPalette(palette)
        self.setStyleSheet("background: %s;" % palette.color(QtGui.QPalette.HighlightedText).name())

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
