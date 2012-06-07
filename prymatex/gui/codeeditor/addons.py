#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.plugin import PMXBaseAddon
from prymatex.support import PMXPreferenceSettings

#========================================
# BASE EDITOR ADDON
#========================================
class CodeEditorBaseAddon(PMXBaseAddon):
    def initialize(self, editor):
        PMXBaseAddon.initialize(self, editor)
        self.editor = editor
        
    def finalize(self):
        pass

#========================================
# BASE EDITOR SIDEBAR ADDON
#========================================
class SideBarWidgetAddon(QtGui.QWidget, CodeEditorBaseAddon):
    ALIGNMENT = None
    updateRequest = QtCore.pyqtSignal()
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
    
    def setVisible(self, value):
        QtGui.QWidget.setVisible(self, value)
        self.updateRequest.emit()

    def translatePosition(self, position):
        font_metrics = QtGui.QFontMetrics(self.editor.font)
        fh = font_metrics.lineSpacing()
        ys = position.y()
        
        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        page_bottom = self.editor.viewport().height()
        while block.isValid():
            blockPosition = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            if blockPosition.y() > page_bottom:
                break
            if blockPosition.y() < ys and (blockPosition.y() + fh) > ys:
                break
            block = block.next()
        return block

class CompleterAddon(QtCore.QObject, CodeEditorBaseAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        self.charCounter = 0

    def initialize(self, editor):
        CodeEditorBaseAddon.initialize(self, editor)
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def on_editor_keyPressEvent(self, event):
        if event.text() and event.key() not in [ QtCore.Qt.Key_Space, QtCore.Qt.Key_Backspace ]:
            self.charCounter += 1
        else:
            self.charCounter = 0
        if self.charCounter == 3:
            completions, alreadyTyped = self.editor.completionSuggestions()
            if bool(completions):
                self.editor.showCompleter(completions, alreadyTyped)
                
class SmartUnindentAddon(QtCore.QObject, CodeEditorBaseAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def initialize(self, editor):
        CodeEditorBaseAddon.initialize(self, editor)
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def on_editor_keyPressEvent(self, event):
        #Solo si metio texto, sino lo hace cuando me muevo entre caracteres
        if event.text():
            cursor = self.editor.textCursor()
            currentBlock = cursor.block()
            previousBlock = currentBlock.previous()
            settings = self.editor.preferenceSettings(self.editor.currentScope())
            indentMarks = settings.indent(currentBlock.text())
            if PMXPreferenceSettings.INDENT_DECREASE in indentMarks and previousBlock.isValid() and currentBlock.userData().indent >= previousBlock.userData().indent:
                self.editor.unindentBlocks(cursor)
            
class SpellCheckerAddon(QtCore.QObject, CodeEditorBaseAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    def initialize(self, editor):
        CodeEditorBaseAddon.initialize(self, editor)
        self.connect(editor, QtCore.SIGNAL("keyPressEvent(QEvent)"), self.on_editor_keyPressEvent)
    
    def on_editor_keyPressEvent(self, event):
        if not event.modifiers() and event.key() in [ QtCore.Qt.Key_Space ]:
            cursor = self.editor.textCursor()
            currentBlock = cursor.block()
            spellRange = filter(lambda ((start, end), p): p.spellChecking,  currentBlock.userData().preferences)
            print spellRange
        
#=======================================
# SideBar Widgets
#=======================================
class ExtraSelectionSideBarAddon(SideBarWidgetAddon):
    def paintEvent(self, event):
        editorFont = QtGui.QFont(self.editor.font)
        page_bottom = self.editor.viewport().height()
        font_metrics = QtGui.QFontMetrics(editorFont)
        painter = QtGui.QPainter(self)
        painter.setPen(self.editor.colours["foreground"])
        painter.fillRect(self.rect(), self.editor.colours["foreground"])
        
        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        line_count = block.blockNumber()
        
        while block.isValid():
            line_count += 1
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible():
                #Line Numbers
                leftPosition = self.width() - font_metrics.width(str(line_count)) - 2
                painter.drawText(leftPosition,
                    round(position.y()) + font_metrics.ascent() + font_metrics.descent() - 2,
                    str(line_count))

            block = block.next()
        painter.end()
        QtGui.QWidget.paintEvent(self, event)

