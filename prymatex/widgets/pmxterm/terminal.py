#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is based on AjaxTerm/Web-Shell which included a fairly complete
# vt100 implementation as well as a stable process multiplexer.
# I made some small fixes, improved some small parts and added a Session class
# which can be used by the widget.
# License: GPL2

import sys
import time

from prymatex.qt import QtCore, QtGui, QtWidgets, API

from .backend import constants
from .schemes import ColorScheme

DEBUG = False

class TerminalWidget(QtWidgets.QWidget):
    keymap = {
       QtCore.Qt.Key_Backspace: chr(127),
       QtCore.Qt.Key_Escape: chr(27),
       QtCore.Qt.Key_AsciiTilde: "~~",
       QtCore.Qt.Key_Up: "~A",
       QtCore.Qt.Key_Down: "~B",
       QtCore.Qt.Key_Left: "~D", 
       QtCore.Qt.Key_Right: "~C", 
       QtCore.Qt.Key_PageUp: "~1", 
       QtCore.Qt.Key_PageDown: "~2", 
       QtCore.Qt.Key_Home: "~H", 
       QtCore.Qt.Key_End: "~F", 
       QtCore.Qt.Key_Insert: "~3",
       QtCore.Qt.Key_Delete: "~4", 
       QtCore.Qt.Key_F1: "~a",
       QtCore.Qt.Key_F2: "~b", 
       QtCore.Qt.Key_F3:  "~c", 
       QtCore.Qt.Key_F4:  "~d", 
       QtCore.Qt.Key_F5:  "~e", 
       QtCore.Qt.Key_F6:  "~f", 
       QtCore.Qt.Key_F7:  "~g", 
       QtCore.Qt.Key_F8:  "~h", 
       QtCore.Qt.Key_F9:  "~i", 
       QtCore.Qt.Key_F10:  "~j", 
       QtCore.Qt.Key_F11:  "~k", 
       QtCore.Qt.Key_F12:  "~l", 
    }

    sessionClosed = QtCore.Signal()

    def __init__(self, session, scheme = None, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent().setTabOrder(self, self)
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setAutoFillBackground(False)
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, True)
        self.setCursor(QtCore.Qt.IBeamCursor)
        
        # Font
        font = QtGui.QFont("Monospace", 9)
        font.setStyleStrategy(font.styleStrategy() | QtGui.QFont.ForceIntegerMetrics)
        self.setFont(font)
        
        #Session
        self.session = session
        self.session.readyRead.connect(self.on_session_readyRead)
        self.session.screenReady.connect(self.on_session_screenReady)
        self.session.finished.connect(self.on_session_finished)
        
        # Scroll
        self.scrollBar = QtWidgets.QScrollBar(self)
        self.scrollBar.setCursor( QtCore.Qt.ArrowCursor )
        self.scrollBar.setMinimum(0)
        self.scrollBar.setMaximum(0)
        self.scrollBar.setValue(0)
        self.scrollBar.valueChanged.connect(self.on_scrollBar_valueChanged)
        
        # Scheme
        self.scheme = scheme or ColorScheme.default()
        
        self._last_update = None
        self._screen = []
        self._screen_history = []
        self._history_index = 0
        self._history_lines = 1000
        self._text = []
        self._cursor_rect = None
        self._cursor_col = 0
        self._cursor_row = 0
        self._press_pos = None
        self._selection = None
        self._clipboard = QtWidgets.QApplication.clipboard()

    # ---------------- Signals
    def on_session_finished(self, status):
        self.session = None
        self.sessionClosed.emit()

    def on_session_readyRead(self):
        if not self.is_alive():
            self.sessionClosed.emit()
        else:
            self.on_session_screenReady(self.session.dump())

    def on_session_screenReady(self, data):
        (self._cursor_col, self._cursor_row, scroll_up, scroll_down), screen = data
        if scroll_up:
            self.store_history(scroll_up, self._screen)
        self._screen = screen
        self._update_cursor_rect()
        self.update()
        
    def on_scrollBar_valueChanged(self, value):
        self._history_index = value
        self.update()

    # ------------------ Colors
    def setColorScheme(self, scheme):
        self.scheme = scheme
        self.update()

    def backgroundColor(self, index = None, attrs = constants.DEFAULTSGR):
        if index is None:
            return self.scheme.background()
        if attrs & constants.SGR49:
            return self.scheme.background()
        return self.scheme.color(index)
        
    def foregroundColor(self, index = None, attrs = constants.DEFAULTSGR):
        if index is None:
             return self.scheme.foreground()
        if attrs & constants.SGR39:
            return self.scheme.foreground(intense = bool(attrs & constants.SGR1))
        return self.scheme.color(index, intense = bool(attrs & constants.SGR1))

    def mapToStyle(self, foregroundIndex, backgroundIndex, attrs = constants.DEFAULTSGR):
        foregroundColor = self.foregroundColor(foregroundIndex, attrs)
        backgroundColor = self.backgroundColor(backgroundIndex, attrs)
        font = self.font()
        if attrs & constants.SGR7:
            foregroundColor, backgroundColor = backgroundColor, foregroundColor
        if attrs & constants.SGR4:
            font.setUnderline(True)
        if attrs & constants.SGR1:
            font.setBold(True)
        return (foregroundColor, backgroundColor, font)

    def send(self, s):
        self.session.write(s)

    def stop(self):
        self.session.stop()

    def pid(self):
        return self.session.pid()

    def info(self):
        if self.is_alive():
            return self.session.info()

    def setFont(self, font):
        QtWidgets.QWidget.setFont(self, font)
        self._update_metrics()
        
    def focusNextPrevChild(self, next):
        if not self.is_alive():
            return True
        return False

    def focusInEvent(self, event):
        self.update()

    def resizeEvent(self, event):
        self._columns, self._rows = self._pixel2pos(self.width() - self.scrollBar.width(), self.height())
        if self._columns > 0 and self._rows > 0:
            self.session.resize(self._columns, self._rows)
        self.scrollBar.setGeometry(QtCore.QRect(self.width() - 16, 0, 16, self.height()))

    def closeEvent(self, event):
        if not self.is_alive():
            return
        self.session.close()

    def store_history(self, lines, screen):
        self._screen_history.extend(screen[:lines])
        self._history_index = len(self._screen_history)
        
        if self._history_index > self._history_lines:
            index = self._history_index - self._history_lines
            self._screen_history = self._screen_history[index:]
            self._history_index = len(self._screen_history)

        self.scrollBar.setMaximum(self._history_index)
        self.scrollBar.setValue(self._history_index)

    def _update_metrics(self):
        fm = self.fontMetrics()
        self._char_height = fm.height()
        self._char_width = fm.width(" ")

    def _update_cursor_rect(self):
        cx, cy = self._pos2pixel(self._cursor_col, self._cursor_row)
        self._cursor_rect = QtCore.QRect(cx, cy, self._char_width, self._char_height)

        
    def _reset(self):
        self._update_metrics()
        self._update_cursor_rect()
        self.resizeEvent(None)
        self.update()

        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self._paint_screen(painter)
        if self._cursor_rect is not None and self.scrollBar.maximum() == self._history_index:
            self._paint_cursor(painter)
        if self._selection:
            self._paint_selection(painter)
        
    def _pixel2pos(self, x, y):
        col = int(round(x / self._char_width))
        row = int(round(y / self._char_height))
        return col, row


    def _pos2pixel(self, col, row):
        x = col * self._char_width
        y = row * self._char_height
        return x, y


    def _paint_cursor(self, painter):
        painter.setPen(QtGui.QPen(self.foregroundColor()))
        if self.hasFocus():
            painter.fillRect(self._cursor_rect, QtGui.QBrush(self.foregroundColor()))
        else:
            painter.drawRect(self._cursor_rect)

    def _paint_screen(self, painter):
        # Speed hacks: local name lookups are faster
        vars().update(QColor=QtGui.QColor, QBrush=QtGui.QBrush, QPen=QtGui.QPen, QRect=QtCore.QRect)
        
        char_width = self._char_width
        char_height = self._char_height
        painter_drawText = painter.drawText
        painter_fillRect = painter.fillRect
        painter_setPen = painter.setPen
        painter_setFont = painter.setFont
        align = QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
        # set defaults
        brush = QtGui.QBrush(self.scheme.background())
        painter_fillRect(self.rect(), brush)
        pen = QtGui.QPen(self.scheme.foreground())
        painter_setPen(pen)
        y = 0
        text = []
        # Calculate viewscreen
        viewscreen = (self._screen_history + self._screen)[self._history_index:self._history_index + len(self._screen)]
        for row, line in enumerate(viewscreen):
            col = 0
            text_line = ""
            for item in line:
                if isinstance(item, tuple):
                    foreground_color_idx, background_color_idx, flags = item
                    foregroundColor, backgroundColor, font = self.mapToStyle(
                        foreground_color_idx, 
                        background_color_idx, 
                        flags)
                    pen = QtGui.QPen(foregroundColor)
                    brush = QtGui.QBrush(backgroundColor)
                    painter_setFont(font)
                    painter_setPen(pen)
                else:
                    x = col * char_width
                    length = len(item)
                    rect = QtCore.QRect(x, y, x + char_width * length, y + char_height)
                    painter_fillRect(rect, brush)
                    painter_drawText(rect, align, item)
                    col += length
                    text_line += item
            # Clear last column            
            rect = QtCore.QRect(col * char_width, y, self.width(), y + char_height)
            brush = QtGui.QBrush(self.backgroundColor())
            painter_fillRect(rect, brush)
            
            y += char_height
            text.append(text_line)

        # Store text
        self._text = text
        
        # Clear last lines
        rect = QtCore.QRect(0, y, self.width(), self.height())
        brush = QtGui.QBrush(self.backgroundColor())
        painter_fillRect(rect, brush)

    def _paint_selection(self, painter):
        pcol = QtGui.QColor(200, 200, 200, 50)
        pen = QtGui.QPen(pcol)
        bcol = QtGui.QColor(230, 230, 230, 50)
        brush = QtGui.QBrush(bcol)
        painter.setPen(pen)
        painter.setBrush(brush)        
        for (start_col, start_row, end_col, end_row) in self._selection:
            x, y = self._pos2pixel(start_col, start_row)
            width, height = self._pos2pixel(end_col - start_col, end_row - start_row)
            rect = QtCore.QRect(x, y, width, height)
            #painter.drawRect(rect)
            painter.fillRect(rect, brush)

    FONT_MAX_SIZE = 32
    FONT_MIN_SIZE = 6
    def zoom_in(self):
        font = self.font()
        size = font.pointSize()
        if size >= self.FONT_MAX_SIZE:
            return
        size += 1
        font.setPointSize(size)
        self.setFont(font)
        self._reset()
        
    def zoom_out(self):
        font = self.font()
        size = font.pointSize()
        if size <= self.FONT_MIN_SIZE:
            return
        size -= 1
        font.setPointSize(size)
        self.setFont(font)
        self._reset()

    return_pressed = QtCore.Signal()

    def keyPressEvent(self, event):
        text = event.text()
        key = event.key()
        modifiers = event.modifiers()
        ctrl = modifiers == QtCore.Qt.ControlModifier
        if ctrl and key == QtCore.Qt.Key_Plus:
            self.zoom_in()
        elif ctrl and key == QtCore.Qt.Key_Minus:
                self.zoom_out()
        else:
            if self.scrollBar.maximum() != self._history_index:
                self.scrollBar.setValue(self.scrollBar.maximum())
            if text and key != QtCore.Qt.Key_Backspace:
                self.send(text)
            else:
                s = self.keymap.get(key)
                if s:
                    self.send(s)
                elif DEBUG:
                    print("Unkonwn key combination")
                    print("Modifiers:", modifiers)
                    print("Key:", key)
                    for name in dir(Qt):
                        if not name.startswith("Key_"):
                            continue
                        value = getattr(Qt, name)
                        if value == key:
                            print("Symbol: QtCore.Qt.%s" % name)
                    print("Text: %r" % text)
        event.accept()
        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.return_pressed.emit()

    def wheelEvent(self, event):
        if API == "pyqt5":
            delta = event.angleDelta().y()
        else:
            delta = event.delta()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if delta > 0:
                self.zoom_in()
            elif delta < 0:
                self.zoom_out()
            event.ignore()
        else:
            super(TerminalWidget, self).wheelEvent(event)
    
    def mousePressEvent(self, event):
        button = event.button()
        if button == QtCore.Qt.RightButton:
            ctx_event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse, event.pos())
            self.contextMenuEvent(ctx_event)
            self._press_pos = None
        elif button == QtCore.Qt.LeftButton:
            self._press_pos = event.pos()
            self._selection = None
            self.update()
        elif button == QtCore.Qt.MiddleButton:
            self._press_pos = None
            self._selection = None
            text = str(self._clipboard.text(QtGui.QClipboard.Selection))
            self.send(text.encode("utf-8"))
            #self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        self.update()

    def _selection_rects(self, start_pos, end_pos):
        sx, sy = start_pos.x(), start_pos.y()
        start_col, start_row = self._pixel2pos(sx, sy)
        ex, ey = end_pos.x(), end_pos.y()
        end_col, end_row = self._pixel2pos(ex, ey)
        if start_row == end_row:
            if ey > sy or end_row == 0:
                end_row += 1
            else:
                end_row -= 1
        if start_col == end_col:
            if ex > sx or end_col == 0:
                end_col += 1
            else:
                end_col -= 1
        if start_row > end_row:
            start_row, end_row = end_row, start_row
        if start_col > end_col:
            start_col, end_col = end_col, start_col
        if end_row - start_row == 1:
            return [ (start_col, start_row, end_col, end_row) ]
        else:
            return [
             (start_col, start_row, self._columns, start_row + 1),
             (0, start_row + 1, self._columns, end_row - 1),
             (0, end_row - 1, end_col, end_row)
             ]
             
    def text(self, rect=None):
        if rect is None:
            return "\n".join(self._text)
        else:
            text = []
            (start_col, start_row, end_col, end_row) = rect
            for row in range(start_row, end_row):
                text.append(self._text[row][start_col:end_col])
            return text
        
    def text_selection(self):
        text = []
        for (start_col, start_row, end_col, end_row) in self._selection:
            for row in range(start_row, end_row):
                text.append(self._text[row][start_col:end_col])
        return "\n".join(text)
    
    def column_count(self):
        return self._columns
    
    def row_count(self):
        return self._rows

    def mouseMoveEvent(self, event):
        if self._press_pos:
            move_pos = event.pos()
            self._selection = self._selection_rects(self._press_pos, move_pos)
    
            sel = self.text_selection()
            if DEBUG:
                print("%r copied to xselection" % sel)
            self._clipboard.setText(sel, QtGui.QClipboard.Selection)
            
            self.update()
        
    def mouseDoubleClickEvent(self, event):
        self._press_pos = None
        # double clicks create a selection for the word under the cursor
        pos = event.pos()
        x, y = pos.x(), pos.y()
        col, row = self._pixel2pos(x, y)
        line = self._text[row]
        # find start of word
        start_col = col 
        found_left = 0
        while start_col > 0:
            char = line[start_col]
            if not char.isalnum() and char not in ("_",):
                found_left = 1
                break
            start_col -= 1
        # find end of word
        end_col = col
        found_right = 0
        while end_col < self._columns:
            char = line[end_col]
            if not char.isalnum() and char not in ("_",):
                found_right = 1
                break
            end_col += 1
        self._selection = [ (start_col + found_left, row, end_col - found_right + 1, row + 1) ]
        
        sel = self.text_selection()
        if DEBUG:
            print("%r copied to xselection" % sel)
        self._clipboard.setText(sel, QtGui.QClipboard.Selection)

        self.update()
        
    def is_alive(self):
        return self.session and self.session.is_alive()
