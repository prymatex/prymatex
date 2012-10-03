#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtGui, QtCore

from prymatex.gui.codeeditor.sidebar import SideBarWidgetAddon

class MiniMapAddon(QtGui.QPlainTextEdit, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignRight
    
    def __init__(self, parent):
        QtGui.QPlainTextEdit.__init__(self, parent)
        font = self.document().defaultFont()
        font.setPixelSize(1)
        self.document().setDefaultFont(font)
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)
        self.setCenterOnScroll(True)
        self.setMouseTracking(True)
        self.viewport().setCursor(QtCore.Qt.PointingHandCursor)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        self.editor = None
        self.highlighter = None
        self.lines_count = 0

        self.goe = QtGui.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.goe)
        self.goe.setOpacity(50)
        self.animation = QtCore.QPropertyAnimation(self.goe, "opacity")

        self.slider = SliderArea(self)
        self.slider.show()

    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.editor = editor
        editor.textChanged.connect(self.updateDocumentText)
        editor.themeChanged.connect(self.on_editor_themeChanged)
        
    def on_editor_themeChanged(self):
        #Editor colours
        appStyle = """QPlainTextEdit {background-color: %s;
        color: %s;
        border: 0px;
        selection-background-color: %s; }""" % (self.editor.colours['background'].name(), self.editor.colours['foreground'].name(), self.editor.colours['selection'].name())
        self.setStyleSheet(appStyle)
        self.setOpacity(50)

    def updateDocumentText(self):
        text = self.parent().toPlainText()
        self.setPlainText(text)
        
    def updateOverlay(self):
        parentRect = self.parent().viewport().rect()
        
        x = parentRect.width() - 100
        self.setGeometry(x, 0, 150, parentRect.height())
        self.slider.update_position()
        self.update_visible_area()
    
    def __calculate_max(self):
        line_height = self.editor.cursorRect().height()
        if line_height > 0:
            self.lines_count = self.editor.viewport().height() / line_height
        self.slider.update_position()
        self.update_visible_area()

    def set_code(self, source):
        self.highlighter.highlight_function = self.highlighter.open_highlight
        self.setPlainText(source)
        self.__calculate_max()
        self.highlighter.async_highlight()

    def adjust_to_parent(self):
        self.setFixedHeight(self.editor.height())
        self.setFixedWidth(self.editor.width() * 10)
        x = self.editor.width() - self.width()
        self.move(x, 0)
        fontsize = int(self.width() / 20)
        if fontsize < 1:
            fontsize = 1
        font = self.document().defaultFont()
        font.setPointSize(fontsize)
        self.setFont(font)
        self.__calculate_max()

    def update_visible_area(self):
        if not self.slider.pressed:
            line_number = self.editor.firstVisibleBlock().blockNumber()
            block = self.document().findBlockByLineNumber(line_number)
            cursor = self.textCursor()
            cursor.setPosition(block.position())
            rect = self.cursorRect(cursor)
            self.setTextCursor(cursor)
            self.slider.move_slider(rect.y())

    def enterEvent(self, event):
        self.animation.setDuration(300)
        self.animation.setStartValue(50)
        self.animation.setEndValue(50)
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setDuration(300)
        self.animation.setStartValue(50)
        self.animation.setEndValue(50)
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

class SliderArea(QtGui.QFrame):

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self._parent = parent
        self.setMouseTracking(True)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setStyleSheet("background: red;")
        self.goe = QtGui.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.goe)
        self.goe.setOpacity(50 / 2)

        self.pressed = False
        self.__scroll_margins = None

    def update_position(self):
        font_size = QtGui.QFontMetrics(self._parent.font()).height()
        height = self._parent.lines_count * font_size
        self.setFixedHeight(height)
        self.setFixedWidth(self._parent.width())
        self.__scroll_margins = (height, self._parent.height() - height)

    def move_slider(self, y):
        self.move(0, y)

    def mousePressEvent(self, event):
        QtGui.QFrame.mousePressEvent(self, event)
        self.pressed = True
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        QtGui.QFrame.mouseReleaseEvent(self, event)
        self.pressed = False
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        QtGui.QFrame.mouseMoveEvent(self, event)
        if self.pressed:
            pos = self.mapToParent(event.pos())
            y = pos.y() - (self.height() / 2)
            if y < 0:
                y = 0
            if y < self.__scroll_margins[0]:
                self._parent.verticalScrollBar().setSliderPosition(
                    self._parent.verticalScrollBar().sliderPosition() - 2)
            elif y > self.__scroll_margins[1]:
                self._parent.verticalScrollBar().setSliderPosition(
                    self._parent.verticalScrollBar().sliderPosition() + 2)
            self.move(0, y)
            self._parent.scroll_area(pos, event.pos())