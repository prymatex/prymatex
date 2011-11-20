# -*- coding: utf-8 -*-
import sys
import time
from PyQt4 import QtCore
from PyQt4 import QtGui 

# Import fiexes for stand alone testing
try:
    from .backend import Session
except ValueError:
    from backend import Session

import os

DEBUG = False

class TerminalWidget(QtGui.QWidget):
    ''' Terminal front end, connected to a Python only backend '''
    
    foreground_color_map = {
      0: "#000",
      1: "#b00",
      2: "#0b0",
      3: "#bb0",
      4: "#00b",
      5: "#b0b",
      6: "#0bb",
      7: "#bbb",
      8: "#666",
      9: "#f00",
      10: "#0f0",
      11: "#ff0",
      12: "#00f", # concelaed
      13: "#f0f", 
      14: "#000", # negative
      15: "#fff", # default
    }
    background_color_map = {
      0: "#000",
      1: "#b00",
      2: "#0b0",
      3: "#bb0",
      4: "#00b",
      5: "#b0b",
      6: "#0bb",
      7: "#bbb",
      12: "#aaa", # cursor
      14: "#000", # default
      15: "#fff", # negative
    }
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

    session_closed = QtCore.pyqtSignal()

    DEFAULT_FONT_NAME = "Monospace"
    DEFAULT_FONT_SIZE = 10

    def __init__(self, parent=None, command=None, 
                 font_name=DEFAULT_FONT_NAME,
                 font_size=DEFAULT_FONT_SIZE):
        super(TerminalWidget, self).__init__(parent)
        if isinstance(self.parent(), QtGui.QTabWidget):
            self.parent().setTabOrder(self, self)
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setAutoFillBackground(False)
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, True)
        self.setCursor(QtCore.Qt.IBeamCursor)
        font = QtGui.QFont(font_name)
        font.setPixelSize(font_size)
        self.setFont(font)
        self._session = None
        self._last_update = None
        self._screen = []
        self._text = []
        self._cursor_rect = None
        self._cursor_col = 0
        self._cursor_row = 0
        self._dirty = False
        self._blink = False
        self._press_pos = None
        self._selection = None
        self._clipboard = QtGui.QApplication.clipboard()
        QtGui.QApplication.instance().lastWindowClosed.connect(Session.close_all)
        self.execute()

    # Rosale's words, not even Phi should be hardcoded!
    USER_INDEX  =  0
    SHELL_INDEX = -1
    def execute(self, command = None):
        
        if command is None:
            with open('/etc/passwd') as passwd:
                # Read passwd lines and prepare a user, shell tuple
                passwd_splitter = lambda line: line.strip().split(':')
                userlines = map(passwd_splitter, passwd.readlines())
                user_shell_getter = lambda parts: (parts[self.USER_INDEX],
                                               parts[self.SHELL_INDEX])
                userlines = map(user_shell_getter, userlines)
                try:
                    user = os.getlogin()
                except OSError:
                    user = os.getenv('USER')
                command = dict(userlines)[user]
                print command
            
        command = '/bin/zsh'
        self._session = Session()
        self._session.start(command)
        self._timer_id = None
        # start timer either with high or low priority
        if self.hasFocus():
            self.focusInEvent(None)
        else:
            self.focusOutEvent(None)
            
            
    def send(self, s):
        self._session.write(s)

        
    def stop(self):
        self._session.stop()

        
    def pid(self):
        return self._session.pid()


    def setFont(self, font):
        super(TerminalWidget, self).setFont(font)
        self._update_metrics()

        
    def focusNextPrevChild(self, next):
        if not self._session.is_alive():
            return True
        return False


    def focusInEvent(self, event):
        if not self._session.is_alive():
            return
        if self._timer_id is not None:
            self.killTimer(self._timer_id)
        self._timer_id = self.startTimer(250)
        self.update_screen()


    def focusOutEvent(self, event):
        if not self._session.is_alive():
            return
        # reduced update interval 
        # -> slower screen updates
        # -> but less load on main app which results in better responsiveness
        if self._timer_id is not None:
            self.killTimer(self._timer_id)
        self._timer_id = self.startTimer(750)

    def resizeEvent(self, event):
        if not self._session.is_alive():
            return
        self._columns, self._rows = self._pixel2pos(self.width(), self.height())
        self._session.resize(self._columns, self._rows)


    def closeEvent(self, event):
        if not self._session.is_alive():
            return
        self._session.close()


    def timerEvent(self, event):
        if not self._session.is_alive():
            if self._timer_id is not None:
                self.killTimer(self._timer_id)
                self._timer_id = None
            if DEBUG:
                print "Session closed"
            self.session_closed.emit()
            return
        last_change = self._session.last_change()
        if not last_change:
            return
        if not self._last_update or last_change > self._last_update:
            self._last_update = last_change
            old_screen = self._screen
            (self._cursor_col, self._cursor_row), self._screen = self._session.dump()
            self._update_cursor_rect()
            if old_screen != self._screen:
                self._dirty = True
        if self.hasFocus():
            self._blink = not self._blink
        self.update()


    def _update_metrics(self):
        fm = self.fontMetrics()
        self._char_height = fm.height()
        self._char_width = fm.width("W")


    def _update_cursor_rect(self):
        cx, cy = self._pos2pixel(self._cursor_col, self._cursor_row)
        self._cursor_rect = QtCore.QRect(cx, cy, self._char_width, self._char_height)

        
    def _reset(self):
        self._update_metrics()
        self._update_cursor_rect()
        self.resizeEvent(None)
        self.update_screen()


    def update_screen(self):
        self._dirty = True
        self.update()

        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self._dirty:
            self._dirty = False
            self._paint_screen(painter)
        else:
            if self._cursor_rect and not self._selection:
                self._paint_cursor(painter)
        if self._selection:
            self._paint_selection(painter)
            self._dirty = True


    def _pixel2pos(self, x, y):
        col = int(round(x / self._char_width))
        row = int(round(y / self._char_height))
        return col, row


    def _pos2pixel(self, col, row):
        x = col * self._char_width
        y = row * self._char_height
        return x, y


    def _paint_cursor(self, painter):
        if self._blink:
            color = "#aaa"
        else:
            color = "#fff"
        painter.setPen(QtGui.QPen(QtGui.QColor(color)))
        painter.drawRect(self._cursor_rect)


    def _paint_screen(self, painter):
        # Speed hacks: local name lookups are faster
        vars().update(QColor=QtGui.QColor, QBrush=QtGui.QBrush, QPen=QtGui.QPen, QRect=QtCore.QRect)
        background_color_map = self.background_color_map
        foreground_color_map = self.foreground_color_map
        char_width = self._char_width
        char_height = self._char_height
        painter_drawText = painter.drawText
        painter_fillRect = painter.fillRect
        painter_setPen = painter.setPen
        align = QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
        # set defaults
        background_color = background_color_map[14]
        foreground_color = foreground_color_map[15]
        brush = QtGui.QBrush(QtGui.QColor(background_color))
        painter_fillRect(self.rect(), brush)
        pen = QtGui.QPen(QtGui.QColor(foreground_color))
        painter_setPen(pen)
        y = 0
        text = []
        text_append = text.append
        for row, line in enumerate(self._screen):
            col = 0
            text_line = ""
            for item in line:
                if isinstance(item, basestring):
                    x = col * char_width
                    length = len(item)
                    rect = QtCore.QRect(x, y, x + char_width * length, y + char_height)
                    painter_fillRect(rect, brush)
                    painter_drawText(rect, align, item)
                    col += length
                    text_line += item
                else:
                    foreground_color_idx, background_color_idx, underline_flag = item
                    foreground_color = foreground_color_map[foreground_color_idx]
                    background_color = background_color_map[background_color_idx]
                    pen = QtGui.QPen(QtGui.QColor(foreground_color))
                    brush = QtGui.QBrush(QtGui.QColor(background_color))
                    painter_setPen(pen)
                    #painter.setBrush(brush)
            y += char_height
            text_append(text_line)
        self._text = text

            
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


    def zoom_in(self):
        font = self.font()
        font.setPixelSize(font.pixelSize() + 2)
        self.setFont(font)
        self._reset()

        
    def zoom_out(self):
        font = self.font()
        font.setPixelSize(font.pixelSize() - 2)
        self.setFont(font)
        self._reset()
        

    return_pressed = QtCore.pyqtSignal()

    def keyPressEvent(self, event):
        text = unicode(event.text())
        key = event.key()
        modifiers = event.modifiers()
        ctrl = modifiers == QtCore.Qt.ControlModifier
        if ctrl and key == QtCore.Qt.Key_Plus:
            self.zoom_in()
        elif ctrl and key == QtCore.Qt.Key_Minus:
                self.zoom_out()
        else:
            if text and key != QtCore.Qt.Key_Backspace:
                self.send(text.encode("utf-8"))
            else:
                s = self.keymap.get(key)
                if s:
                    self.send(s.encode("utf-8"))
                elif DEBUG:
                    print "Unkonwn key combination"
                    print "Modifiers:", modifiers
                    print "Key:", key
                    for name in dir(QtCore.Qt):
                        if not name.startswith("Key_"):
                            continue
                        value = getattr(QtCore.Qt, name)
                        if value == key:
                            print "Symbol: Qt.%s" % name
                    print "Text: %r" % text
        event.accept()
        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.return_pressed.emit()


    def mousePressEvent(self, event):
        button = event.button()
        if button == QtCore.Qt.RightButton:
            ctx_event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse, event.pos())
            self.contextMenuEvent(ctx_event)
            self._press_pos = None
        elif button == QtCore.Qt.LeftButton:
            self._press_pos = event.pos()
            self._selection = None
            self.update_screen()
        elif button == QtCore.Qt.MiddleButton:
            self._press_pos = None
            self._selection = None
            text = unicode(self._clipboard.text(QtGui.QClipboard.Selection))
            self.send(text.encode("utf-8"))
            #self.update_screen()


    def mouseReleaseEvent(self, QMouseEvent):
        pass #self.update_screen()


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
                print "%r copied to xselection" % sel
            self._clipboard.setText(sel, QtGui.QClipboard.Selection)
            
            self.update_screen()


        
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
            print "%r copied to xselection" % sel
        self._clipboard.setText(sel, QtGui.QClipboard.Selection)

        self.update_screen()

        
    def is_alive(self):
        return (self._session and self._session.is_alive()) or False

    
if __name__ == "__main__":
    from PyQt4 import QtGui
    sys.path.append('..')
    app = QtGui.QApplication(sys.argv)
    widget = TerminalWidget()
    widget.show()
    sys.exit(app.exec_())