#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from __future__ import unicode_literals

import re
import os
import sys
import difflib

from prymatex.qt import API
from prymatex.qt.extensions import HtmlItemDelegate
from prymatex.utils import text
from prymatex import resources

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import textcursor_to_tuple
from prymatex.core import config
from functools import reduce

class CompletionWidget(QtWidgets.QListWidget):
    def __init__(self, textedit, parent):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.SubWindow | QtCore.Qt.FramelessWindowHint)
        self.textedit = textedit
        self.completion_list = None
        self.match_flags = QtCore.Qt.MatchWrap | QtCore.Qt.MatchWildcard | QtCore.Qt.MatchCaseSensitive
        self.match_indexes = []
        self.current_index = -1
        self.enter_select = None
        self.hide()
        self.itemActivated.connect(self.__item_activated)
        self.currentRowChanged.connect(self.__item_highlighted)
        self.setAlternatingRowColors(True)
        self.setItemDelegate(HtmlItemDelegate(self))
        
    def _map_completions(self, completions):
        for completion in completions:
            item = QtWidgets.QListWidgetItem(self)
            if isinstance(completion, (tuple, list)):
                item.setText("%s" % completion[0])
                item.setData(QtCore.Qt.MatchRole, "%s" % completion[1])
            elif isinstance(completion, dict):
                text = completion.get("display", completion.get('title')) 
                item.setText("%s" % text)
                match = completion.get("match", text) 
                item.setData(QtCore.Qt.MatchRole, "%s" % match)
                image = completion.get("image")
                if image:
                    # TODO Obtener el icono del lugar correcto
                    image = resources.get_icon(image)
                    item.setIcon(icon)
                tooltip = completion.get("tool_tip")
                if tooltip:
                    item.setToolTip(tooltip)
            else:
                item.setText("%s" % completion)
                item.setData(QtCore.Qt.MatchRole, "%s" % completion)
            yield item

    def complete(self, completion_list, completion_prefix=None, automatic=True):
        if len(completion_list) == 1 and not automatic:
            self.__item_activated(completion_list[0])
        elif completion_list:
            self.completion_list = completion_list
            self.clear()
            for item in self._map_completions(completion_list):
                self.addItem(item)
            self.resize(self.sizeHint())
            self.setCurrentRow(0)
            
            QtWidgets.QApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)
            self.show()
            self.setFocus()
            self.raise_()
            
            # Retrieving current screen height
            desktop = QtWidgets.QApplication.desktop()
            srect = desktop.availableGeometry(desktop.screenNumber(self))
            screen_right = srect.right()
            screen_bottom = srect.bottom()
            
            point = self.textedit.cursorRect().bottomRight()
            offset = self.textedit.contentOffset()
            point.setX(point.x() + offset.x())
            point = self.textedit.mapToGlobal(point)
    
            # Computing completion widget and its parent right positions
            comp_right = point.x() + self.width()
            ancestor = self.parent()
            if ancestor is None:
                anc_right = screen_right
            else:
                anc_right = min([ancestor.x() + ancestor.width(), screen_right])
            
            # Moving completion widget to the left
            # if there is not enough space to the right
            if comp_right > anc_right:
                point.setX(point.x() - self.width())
            
            # Computing completion widget and its parent bottom positions
            comp_bottom = point.y() + self.height()
            ancestor = self.parent()
            if ancestor is None:
                anc_bottom = screen_bottom
            else:
                anc_bottom = min([ancestor.y()+ancestor.height(), screen_bottom])
            
            # Moving completion widget above if there is not enough space below
            x_position = point.x()
            if comp_bottom > anc_bottom:
                point = self.textedit.cursorRect().topRight()
                point = self.textedit.mapToGlobal(point)
                point.setX(x_position)
                point.setY(point.y() - self.height())
                
            if ancestor is not None:
                # Useful only if we set parent to 'ancestor' in __init__
                point = ancestor.mapFromGlobal(point)
            self.move(point)
            
            if completion_prefix:
                # When initialized, if completion text is not empty, we need 
                # to update the displayed list:
                self.setCompletionPrefix(completion_prefix)
        
    def hide(self):
        super().hide()
        self.textedit.setFocus()
        
    def keyPressEvent(self, event):
        text, key = event.text(), event.key()
        alt = event.modifiers() & QtCore.Qt.AltModifier
        shift = event.modifiers() & QtCore.Qt.ShiftModifier
        ctrl = event.modifiers() & QtCore.Qt.ControlModifier
        modifier = shift or ctrl or alt
        if (key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter) and self.enter_select) \
           or key == QtCore.Qt.Key_Tab:
            self.__item_activated()
        elif key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter,
                     QtCore.Qt.Key_Left, QtCore.Qt.Key_Right) or text in ('.', ':'):
            self.hide()
            self.textedit.keyPressEvent(event)
        elif key in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown,
                     QtCore.Qt.Key_Home, QtCore.Qt.Key_End,
                     QtCore.Qt.Key_CapsLock) and not modifier:
            super().keyPressEvent(event)
        elif len(text) or key == QtCore.Qt.Key_Backspace:
            self.textedit.keyPressEvent(event)
            alreadyTyped, start, end = self.textedit.wordUnderCursor(direction="left", search=True)
            self.setCompletionPrefix(alreadyTyped)
        elif ctrl and key == QtCore.Qt.Key_Space:
            self.current_index += 1
            if self.current_index >= len(self.match_indexes):
                self.current_index = 0
            self.setCurrentRow(self.match_indexes[self.current_index].row())
        elif modifier:
            self.textedit.keyPressEvent(event)
        else:
            self.hide()
            super().keyPressEvent(event)
    
    def setCompletionPrefix(self, completion_prefix):
        if completion_prefix:
            model = self.model()
            if self.match_flags & QtCore.Qt.MatchWildcard:
                completion_prefix = "*" + "*".join(list(completion_prefix)) + "*"
            self.match_indexes = model.match(model.index(0, 0, QtCore.QModelIndex()),
                QtCore.Qt.MatchRole, completion_prefix, -1, self.match_flags)
            if self.match_indexes:
                self.current_index = 0
                self.setCurrentRow(self.match_indexes[self.current_index].row())
            else:
                self.hide()
        else:
            self.hide()
    
    def focusOutEvent(self, event):
        event.ignore()
        # Don't hide it on Mac when main window loses focus because
        # keyboard input is lost
        # Fixes Issue 1318
        if sys.platform == "darwin":
            if event.reason() != Qt.ActiveWindowFocusReason:
                self.hide()
        else:
            self.hide()
        
    def __item_activated(self, item=None):
        if item is None:
            index = self.currentRow()
            item = self.completion_list[index]
        self.textedit.insertCompletion(item)
        self.hide()

    def __item_highlighted(self, index=None):
        item = self.completion_list[index]
        print(item)

    def sizeHint(self):
        size = QtCore.QSize()
        size.setHeight(super().sizeHint().height())
        size.setWidth(self.sizeHintForColumn(0))
        return size
    
class TextEditWidget(QtWidgets.QPlainTextEdit):
    # ------------------ Constants
    EOL_CHARS = [ item[0] for item in text.EOLS ]
    FONT_MAX_SIZE = 32
    FONT_MIN_SIZE = 6
    CHARACTER = "#"
    
    # ------------------ Signals
    activated = QtCore.Signal()
    deactivated = QtCore.Signal()
    
    extraSelectionChanged = QtCore.Signal()
    
    queryCompletions = QtCore.Signal()
    
    # ------------------ Find Flags
    FindBackward           = 1<<0
    FindCaseSensitive      = 1<<1
    FindWholeWord          = 1<<2
    FindRegularExpression  = 1<<3
    
    def __init__(self, **kwargs):
        super(TextEditWidget, self).__init__(**kwargs)
        
        self.__scopedExtraSelections = {}
        self.__textCharFormat = {}

        # Completer
        self.__completer = CompletionWidget(self, self.parent())

        # Defaults
        self.eol_chars = os.linesep
        self.soft_tabs = False
        self.tab_size = 2
        self.completion_auto = False

    # OVERRIDE: QtWidgets.QPlainTextEdit.setPalette()
    def setPalette(self, palette):
        super().setPalette(palette)
        self.__completer.setPalette(palette)

    # OVERRIDE: QtWidgets.QPlainTextEdit.setFont()
    def setFont(self, font):
        super().setFont(font)
        self.__completer.setFont(font)
    
    # OVERRIDE: QtWidgets.QPlainTextEdit.focusInEvent()
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.activated.emit()

    # OVERRIDE: QtWidgets.QPlainTextEdit.focusOutEvent()
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.deactivated.emit()

    #------ Completion
    def setCompletionMatchFlags(self, flags):
        """Match flags completion"""
        self.__completer.match_flags = flags
        
    def setCompletionEnter(self, state):
        """Enable Enter key to select completion"""
        self.__completer.enter_select = state
        
    def setCompletionAuto(self, auto):
        """Set code completion state"""
        self.completion_auto = auto

    def showCompletion(self, completions, completion_prefix="",
            automatic=True):
        """Display the possible completions"""
        if len(completions) == 0 or completions == [completion_prefix]:
            return
        # Sorting completion list (entries starting with underscore are 
        # put at the end of the list):
        # underscore = set([comp for comp in completions
        #                  if comp.startswith('_')])
        #completions = sorted(set(completions)-underscore, key=str_lower)+\
        #              sorted(underscore, key=str_lower)
        self.__completer.complete(completions, 
            completion_prefix=completion_prefix,
            automatic=automatic)
                
    def insertCompletion(self, completion):
        currentWord, start, end = self.currentWord()
        cursor = self.newCursorAtPosition(start, end)
        if isinstance(completion, (tuple, list)):
            completion = completion[1]
        elif isinstance(completion, dict):
            completion = completion.get('match', completion.get('display', completion.get('title')))
        cursor.insertText(completion)

    #------ EOL characters
    def setEolChars(self, eol_chars):
        """Set widget end-of-line (EOL) characters from chars_or_text"""
        
        if eol_chars in self.EOL_CHARS and self.eol_chars != eol_chars:
            self.eol_chars = eol_chars
            self.setModified(True)
        self.textChanged.emit()

    def eolChars(self):
        return self.eol_chars

    #------ Soft Tabs
    def setSoftTabs(self, soft):
        self.soft_tabs = soft
    
    def softTabs(self):
        return self.soft_tabs
        
    #------ Tab Size
    def setTabSize(self, size):
        self.tab_size = size
        self.setTabStopWidth(self.tab_size * self.characterWidth())
    
    def tabSize(self):
        return self.tab_size

    def tabKeyBehavior(self):
        return ' ' * self.tabSize() if self.softTabs() else '\t'

    #--------- Indentation
    def indentation(self, cursor = None, direction = "left"):
        cursor =  cursor or self.textCursor()
        sourceText = cursor.block().text()
        if direction == "left":
            sourceText = sourceText[:cursor.columnNumber()]
        elif direction == "right":
            sourceText = sourceText[cursor.columnNumber():]
        return text.white_space(sourceText)

    def indent(self, cursor = None):
        """Indents text, block selections."""
        cursor = QtGui.QTextCursor(cursor or self.textCursor())
        start, end = self.selectionBlockStartEnd(cursor)
        cursor.beginEditBlock()
        block = start
        while True:
            cursor = self.newCursorAtPosition(block.position())
            cursor.insertText(self.tabKeyBehavior())
            if block == end:
                break
            block = block.next()
        cursor.endEditBlock()

    def unindent(self, cursor = None):
        cursor = QtGui.QTextCursor(cursor or self.textCursor())
        start, end = self.selectionBlockStartEnd(cursor)
        cursor.beginEditBlock()
        tab_behavior = self.tabKeyBehavior()
        indent_len = len(self.tabKeyBehavior())
        block = start
        while True:
            cursor = self.newCursorAtPosition(block.position(), block.position() + indent_len)
            if cursor.selectedText() == tab_behavior:
                cursor.removeSelectedText()
            if block == end:
                break
            block = block.next()
        cursor.endEditBlock()

    # OVERRIDE: QPlainTextEdit.keyPressEvent()
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            cursor = self.textCursor()
            if not cursor.hasSelection():
                cursor.insertText(self.tabKeyBehavior())
            else:
                self.indent(cursor)
        elif event.key() == QtCore.Qt.Key_Backtab:
            self.unindent()
        else:
            super(TextEditWidget, self).keyPressEvent(event)
        
    # OVERRIDE: QPlainTextEdit.wheelEvent()
    def wheelEvent(self, event):
        if API == "pyqt5":
            delta = event.angleDelta().y()
        else:
            delta = event.delta()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if delta > 0:
                self.zoomIn()
            elif delta < 0:
                self.zoomOut()
            event.ignore()
        else:
            super(TextEditWidget, self).wheelEvent(event)

    #------ Retrieve text
    def currentWord(self):
        return self.wordUnderCursor(self.textCursor(), search=True)
        
    def currentText(self):
        return self.textUnderCursor(self.textCursor(), search=True)

    def wordUnderCursor(self, cursor = None, pattern = config.RE_WORD,
        direction = "both", search = False):
        #Como cambio el cursor hago una copia
        cursor = cursor or self.textCursor()
        selectCursor = QtGui.QTextCursor(cursor)
        character = self.document().characterAt(selectCursor.position() - 1)
        if search and pattern.match(character) is not None:
            selectCursor.movePosition(QtGui.QTextCursor.Left)
        selectCursor.select(QtGui.QTextCursor.WordUnderCursor)
        if selectCursor.hasSelection() and pattern.match(selectCursor.selectedText()):
            wordUnderCursor, start, end = selectCursor.selectedText(), selectCursor.selectionStart(), selectCursor.selectionEnd()
            if direction == "both":
                return wordUnderCursor, start, end
            elif direction == "left":
                index = cursor.position() - start
                return wordUnderCursor[:index], start, start + index
            elif direction == "right":
                index = end - cursor.position()
                return wordUnderCursor[len(wordUnderCursor) - index:], end - index, end
        return None, cursor.position(), cursor.position()
            
    def textUnderCursor(self, cursor = None, pattern = config.RE_WORD,
        direction = "both", search = False):
        cursor = cursor or self.textCursor()
        wordUnderCursor, start, end = self.wordUnderCursor(cursor = cursor,
            pattern = pattern, direction = direction, search = search)

        if wordUnderCursor:
            return wordUnderCursor, start, end
        elif search:
            columnNumber = cursor.columnNumber()
            line = cursor.block().text()
            blockPosition = cursor.block().position()
            first_part, last_part = line[:columnNumber][::-1], line[columnNumber:]
            rmatch = lmatch = None
            start = end = cursor.position()

            if direction in ("left", "both"):
                #Search left word
                lend = start
                lmatch = pattern.search(first_part)
                if lmatch is not None:
                    start = blockPosition + len(first_part[lmatch.end():])
                    lend = blockPosition + len(first_part[lmatch.start():])
                    if direction == "left":
                        return first_part[:lmatch.end()][::-1], start, lend

            if direction in ("right", "both"):
                #Search right word
                rstart = end
                rmatch = pattern.search(last_part)
                if rmatch is not None:
                    rstart = blockPosition + len(first_part)
                    end = blockPosition + len(first_part) + len(last_part[:rmatch.end()])
                    if direction == "right":
                        return last_part[:rmatch.start()], rstart, end

            # Si estamos aca es porque es both
            if lmatch is not None:
                return line[start - blockPosition : end - blockPosition], start, end
        return None, cursor.position(), cursor.position()

    #------ Retrieve cursors and blocks
    def newCursorAtPosition(self, position, anchor=None):
        cursor = QtGui.QTextCursor(self.document())
        if isinstance(position, QtCore.QPoint):
            position = self.cursorForPosition(position).position()
        if anchor and isinstance(anchor, QtCore.QPoint):
            anchor = self.cursorForPosition(anchor).position()
        cursor.setPosition(position)
        if anchor is not None:
            if anchor < 0:
                anchor = 0
            elif anchor >= self.document().characterCount():
                anchor = self.document().characterCount() - 1
            cursor.setPosition(anchor, QtGui.QTextCursor.KeepAnchor)
        return cursor

    def selectionBlockStartEnd(self, cursor=None):
        cursor = cursor or self.textCursor()
        return ( self.document().findBlock(cursor.selectionStart()),
            self.document().findBlock(cursor.selectionEnd()))

    #------ Retrieve and set cursor position
    def setCursorPosition(self, position):
        if isinstance(position, (tuple, list)):
            position = self.document().findBlockByNumber(position[0]).position() + position[1]
        self.setTextCursor(self.newCursorAtPosition(position))
        
    def cursorPosition(self):
        return self.textCursor().position()

    #------ Find Cursors
    def findPairCursor(self, b1, b2, cursor, backward = False):
        """
        Busca b2 asumiendo que b1 es su antitesis de ese modo controla el balanceo.
        b1 antitesis de b2
        b2 texto a buscar
        cursor representando la posicion a partir de la cual se busca
        backward buscar para atras
        Si b1 es igual a b2 no se controla el balanceo y se retorna la primera ocurrencia que se encuentre dentro del bloque actual
        """
        flags = QtGui.QTextDocument.FindFlags()
        if backward:
            flags |= QtGui.QTextDocument.FindBackward
        if cursor.hasSelection():
            if b1 == b2:
                startPosition = cursor.selectionStart() if backward else cursor.selectionEnd()
            else:
                startPosition = cursor.selectionEnd() if backward else cursor.selectionStart()
        else:
            startPosition = cursor.position()
        c1 = self.document().find(b1, startPosition, flags)
        c2 = self.document().find(b2, startPosition, flags)
        if b1 != b2:
            #Balanceo para cuando son distintos
            if backward:
                while c1 > c2:
                    c1 = self.document().find(b1, c1.selectionStart(), flags)
                    if c1 > c2:
                        c2 = self.document().find(b2, c2.selectionStart(), flags)
            else:
                while not c1.isNull() and c1.position() != -1 and c1 < c2:
                    c1 = self.document().find(b1, c1.selectionEnd(), flags)
                    if c1.isNull():
                        break
                    if c1 < c2:
                        c2 = self.document().find(b2, c2.selectionEnd(), flags)
            return c2
        else:
            #Cuando son iguales por ahora balanceo solo para el mismo bloque
            if not c2.isNull() and c2.block() == cursor.block():
                #Balanceamos usando el texto del block
                block = cursor.block()
                text = block.text()
                positionStart = cursor.selectionEnd() if backward else cursor.selectionStart()
                positionStart -= block.position()
                positionEnd = c2.selectionEnd() if c2 > cursor else c2.selectionStart()
                positionEnd -= block.position()
                if text[:positionStart].count(b2) % 2 == 0 and text[positionEnd:].count(b2) % 2 == 0:
                    return c2
        return QtGui.QTextCursor()

    def findMatchCursor(self, match, flags, cursor=None):
        """Busca la ocurrencia de match a partir de un cursor o el cursor actual"""
        cursor = QtGui.QTextCursor(cursor) if cursor is not None else self.textCursor()
        if flags & self.FindRegularExpression:
            match = QtCore.QRegExp(match, flags & self.FindCaseSensitive \
                and QtCore.Qt.CaseSensitive or QtCore.Qt.CaseInsensitive)
        if cursor.hasSelection():
            cursor.setPosition((flags & self.FindBackward) and cursor.selectionStart() or cursor.selectionEnd())
        return self.document().find(match, cursor, flags)

    def findAllCursors(self, match, flags):
        cursors = []
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        cursor = self.findMatchCursor(match, flags, cursor = cursor)
        while not cursor.isNull():
            cursors.append(cursor)
            cursor = self.findMatchCursor(match, flags, cursor = cursor)
        return cursors
    
    #------ TextCharFormats for key
    def registerTextCharFormat(self, key, frmt):
        self.__textCharFormat[key] = frmt

    def textCharFormat(self, key):
        if key in self.__textCharFormat:
            return self.__textCharFormat[key]
        return super(TextEditWidget, self).currentCharFormat()

    #------ Extra selections
    def __build_extra_selections(self, key, cursors):
        extraSelections = []
        for cursor in cursors:
            selection = QtWidgets.QTextEdit.ExtraSelection()
            selection.format = self.textCharFormat(key)
            selection.cursor = cursor
            extraSelections.append(selection)
        return extraSelections

    def extendExtraSelectionCursors(self, key, cursors):
        self.__scopedExtraSelections.setdefault(key, []).extend(self.__build_extra_selections(scope, cursors))

    def setExtraSelectionCursors(self, key, cursors):
        self.__scopedExtraSelections[key] = self.__build_extra_selections(key, cursors)

    def updateExtraSelectionCursors(self, cursorsDict):
        for key, cursors in cursorsDict.items():
            self.setExtraSelectionCursors(key, cursors)

    def updateExtraSelections(self):
        extraSelections = []
        for extras in self.__scopedExtraSelections.values():
            extraSelections.extend(extras)
        self.setExtraSelections(extraSelections)
        self.extraSelectionChanged.emit()

    def clearExtraSelections(self):
        self.__scopedExtraSelections.clear()
        self.updateExtraSelections()

    #------ Move text
    def __move_line(self, cursor, moveType):
        cursor.beginEditBlock()
        column = cursor.columnNumber()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        text1 = cursor.selectedText()
        cursor2 = QtGui.QTextCursor(cursor)
        otherBlock = cursor.block().next() if moveType == QtGui.QTextCursor.Down else cursor.block().previous()
        cursor2 = self.newCursorAtPosition(otherBlock.position())
        cursor2.select(QtGui.QTextCursor.LineUnderCursor)
        text2 = cursor2.selectedText()
        cursor.insertText(text2)
        cursor2.insertText(text1)
        cursor.setPosition(otherBlock.position() + column)
        cursor.endEditBlock()
        self.setTextCursor(cursor)

    def __move_text(self, cursor, moveType):
        cursor.beginEditBlock()
        openRight = cursor.position() == cursor.selectionEnd()
        text = cursor.selectedText()
        cursor.removeSelectedText()
        cursor.movePosition(moveType)
        start = cursor.position()
        cursor.insertText(text)
        end = cursor.position()
        cursor = self.newCursorAtPosition(start, end) if openRight else self.newCursorAtPosition(end, start)
        cursor.endEditBlock()
        self.setTextCursor(cursor)

    def moveUp(self, cursor=None):
        cursor = cursor or self.textCursor()
        if cursor.hasSelection():
            self.__move_text(cursor, QtGui.QTextCursor.Up)
        elif cursor.block() != self.document().firstBlock():
            self.__move_line(cursor, QtGui.QTextCursor.Up)

    def moveDown(self, cursor=None):
        cursor = cursor or self.textCursor()
        if cursor.hasSelection():
            self.__move_text(cursor, QtGui.QTextCursor.Down)
        elif cursor.block() != self.document().lastBlock():
            self.__move_line(cursor, QtGui.QTextCursor.Down)

    def moveLeft(self, cursor=None):
        cursor = cursor or self.textCursor()
        if cursor.hasSelection() and cursor.selectionStart() != 0:
            self.__move_text(cursor, QtGui.QTextCursor.Left)

    def moveRight(self, cursor=None):
        cursor = cursor or self.textCursor()
        if cursor.hasSelection() and cursor.selectionEnd() != self.document().characterCount():
            self.__move_text(cursor, QtGui.QTextCursor.Right)

    #------ Select Text
    def selectText(self, cursor=None):
        cursor = cursor or self.textCursor()
        text, start, end = self.textUnderCursor(cursor, search = True)
        if text:
            self.setTextCursor(self.newCursorAtPosition(start, end))

    def selectWord(self, cursor=None):
        cursor = cursor or self.textCursor()
        word, start, end = self.wordUnderCursor(cursor, search = True)
        if word:
            self.setTextCursor(self.newCursorAtPosition(start, end))

    def selectLine(self, cursor=None):
        cursor = cursor or self.textCursor()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        self.setTextCursor(cursor)

    def selectParagraph(self, cursor=None):
        cursor = cursor or self.textCursor()
        cursor.select(QtGui.QTextCursor.BlockUnderCursor)
        self.setTextCursor(cursor)

    def selectDocument(self, cursor=None):
        cursor = cursor or self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        self.setTextCursor(cursor)

    #------ Convert Text
    def __convert_text(self, cursor=None, convertFunction=lambda x: x):
        cursor = cursor or self.textCursor()
        tupleCursor = textcursor_to_tuple(cursor)
        cursor.beginEditBlock()
        if not cursor.hasSelection():
            word, start, end = self.wordUnderCursor(cursor = cursor, search = True)
            self.newCursorAtPosition(start, end).insertText(convertFunction(word))
        else:
            cursor.insertText(convertFunction(cursor.selectedText()))
        cursor.endEditBlock()
        self.setTextCursor(self.newCursorAtPosition(*tupleCursor))

    def convertToUppercase(self, cursor=None):
        self.__convert_text(cursor, text.upper_case)

    def convertToLowercase(self, cursor=None):
        self.__convert_text(cursor, text.lower_case)

    def convertToTitlecase(self, cursor=None):
        self.__convert_text(cursor, text.title_case)

    def convertToOppositeCase(self, cursor=None):
        self.__convert_text(cursor, text.opposite_case)

    def convertSpacesToTabs(self, cursor=None):
        self.__convert_text(cursor, text.spaces_to_tabs)

    def convertTabsToSpaces(self, cursor=None):
        self.__convert_text(cursor, text.tabs_to_spaces)

    def convertTranspose(self, cursor=None):
        self.__convert_text(cursor, text.transpose)

    #------ Set and Get Text
    def setPlainText(self, plainText):
        """Set the text of the editor"""
        QtWidgets.QPlainTextEdit.setPlainText(self, plainText)
        self.eol_chars = text.get_eol_chars(plainText)

    def toPlainText(self):
        """Same as 'toPlainText', replace \u2029 by \n
        """
        return QtWidgets.QPlainTextEdit.toPlainText(self).replace("\u2029", '\n')

    def selectedText(self, cursor=None):
        """
        Return text selected text cursor
        Replace the unicode line separator character \u2029 by \n
        """
        cursor = cursor or self.textCursor()
        return cursor.selectedText().replace("\u2029", '\n')

    def toPlainTextWithEol(self):
        """Same as 'toPlainText', replace '\n' by correct end-of-line characters"""
        plainText = QtWidgets.QPlainTextEdit.toPlainText(self)
        return plainText.replace("\n", self.eolChars())

    def selectedTextWithEol(self, cursor=None):
        """
        Return text selected text cursor
        Replace the unicode line separator character \u2029 by
        the line separator characters returned by eolChars
        """
        cursor = cursor or self.textCursor()
        return cursor.selectedText().replace("\u2029", self.eolChars())

    #------ Update Text
    def updatePlainText(self, text, cursor=None):
        if cursor:
            sourceText = cursor.selectedText()
            sourceOffset = cursor.selectionStart()
        else:
            sourceText = self.toPlainText()
            sourceOffset = 0

        def perform_action(code, cursor, text=""):
            def _nop():
                pass
            def _action():
                cursor.insertText(text)
            return _action if code in ["insert", "replace", "delete"] else _nop

        sequenceMatcher = difflib.SequenceMatcher(None, sourceText, text)
        opcodes = sequenceMatcher.get_opcodes()

        # Frozen cursors
        actions = [perform_action(
                code[0],
                self.newCursorAtPosition(code[1] + sourceOffset, code[2] + sourceOffset), text[code[3]:code[4]]
            ) for code in opcodes]
        # Doit
        for action in actions:
            action()

    #------ Text Zoom
    def zoomIn(self):
        font = self.font()
        size = font.pointSize()
        if size >= self.FONT_MAX_SIZE:
            return
        size += 1
        font.setPointSize(size)
        self.setFont(font)

    def zoomOut(self):
        font = self.font()
        size = font.pointSize()
        if size <= self.FONT_MIN_SIZE:
            return
        size -= 1
        font.setPointSize(size)
        self.setFont(font)

    #------ Character width
    def characterWidth(self):
        return self.fontMetrics().width(self.CHARACTER)

    def characterHeight(self):
        return self.fontMetrics().height()
