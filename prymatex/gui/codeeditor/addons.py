#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.core.plugin import PMXBaseAddon
from prymatex.support import PMXPreferenceSettings
from prymatex.gui import utils

class CodeEditorBaseAddon(PMXBaseAddon):
    def initialize(self, editor):
        PMXBaseAddon.initialize(self, editor)
        self.editor = editor
        
    def finalize(self):
        pass

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
# Widgets
#=======================================
class SideBarWidgetAddon(QtGui.QWidget, CodeEditorBaseAddon):
    ALIGNMENT = None
    visibilityChanged = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
    
    def setVisible(self, value):
        QtGui.QWidget.setVisible(self, value)
        self.visibilityChanged.emit(value)

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

class LineNumberSideBarAddon(SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignLeft
    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.foreground = self.editor.colours["foreground"]
        self.editor.blockCountChanged.connect(self.updateWidth)
        self.editor.blockCountChanged.connect(self.updateColours)
        
    def updateColours(self):
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.foreground = self.editor.colours["foreground"]
        self.repaint(self.rect())

    def updateWidth(self, newBlockCount):
        width = self.fontMetrics().width(str(newBlockCount)) + 4
        if self.width() != width:
            self.setFixedWidth(width)

    @classmethod
    def contributeToMenu(cls):
        def on_actionShowLineNumbers_toggled(editor, checked):
            instance = editor.addonByClassName(cls.__name__)
            instance.setVisible(checked)

        def on_actionShowLineNumbers_testChecked(editor):
            instance = editor.addonByClassName(cls.__name__)
            return instance.isVisible()
        
        menuEntry = {'title': "Line Numbers",
            'callback': on_actionShowLineNumbers_toggled,
            'shortcut': 'F10',
            'checkable': True,
            'testChecked': on_actionShowLineNumbers_testChecked }
        return menuEntry

    def paintEvent(self, event):
        editorFont = QtGui.QFont(self.editor.font)
        page_bottom = self.editor.viewport().height()
        font_metrics = QtGui.QFontMetrics(editorFont)
        current_block = self.editor.document().findBlock(self.editor.textCursor().position())
        
        painter = QtGui.QPainter(self)
        painter.setPen(self.foreground)
        painter.fillRect(self.rect(), self.background)

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

            editorFont.setBold(block == current_block)
            painter.setFont(editorFont)

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
        
class BookmarkSideBarAddon(SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    def __init__(self, parent):
        SideBarWidgetAddon.__init__(self, parent)
        self.bookmarkflagImage = resources.getImage("bookmarkflag")
        self.setFixedWidth(self.bookmarkflagImage.width())
        
    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.editor.blockCountChanged.connect(self.updateColours)
        
    def updateColours(self):
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.repaint(self.rect())

    @classmethod
    def contributeToMenu(cls):
        def on_actionShowBookmarks_toggled(editor, checked):
            instance = editor.addonByClassName(cls.__name__)
            instance.setVisible(checked)

        def on_actionShowBookmarks_testChecked(editor):
            instance = editor.addonByClassName(cls.__name__)
            return instance.isVisible()
        
        menuEntry = {'title': "Bookmarks",
            'callback': on_actionShowBookmarks_toggled,
            'shortcut': 'Alt+F10',
            'checkable': True,
            'testChecked': on_actionShowBookmarks_testChecked }
        return menuEntry

    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font)
        page_bottom = self.editor.viewport().height()
       
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        
        while block.isValid():
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible() and block in self.editor.bookmarkListModel:
                painter.drawPixmap(2,
                    round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.bookmarkflagImage.height(),
                    self.bookmarkflagImage)

            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        self.editor.toggleBookmark(block)
        self.repaint(self.rect())
            
class FoldingSideBarAddon(SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    def __init__(self, parent):
        SideBarWidgetAddon.__init__(self, parent)
        self.foldingcollapsedImage = resources.getImage("foldingcollapsed")
        self.foldingtopImage = resources.getImage("foldingtop")
        self.foldingbottomImage = resources.getImage("foldingbottom")
        self.setFixedWidth(self.foldingbottomImage.width())
        
    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.editor.themeChanged.connect(self.updateColours)
        
    def updateColours(self):
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.repaint(self.rect())
    
    @classmethod
    def contributeToMenu(cls):
        def on_actionShowFoldings_toggled(editor, checked):
            instance = editor.addonByClassName(cls.__name__)
            instance.setVisible(checked)

        def on_actionShowFoldings_testChecked(editor):
            instance = editor.addonByClassName(cls.__name__)
            return instance.isVisible()
        
        menuEntry = {'title': 'Foldings',
            'callback': on_actionShowFoldings_toggled,
            'shortcut': 'Shift+F10',
            'checkable': True,
            'testChecked': on_actionShowFoldings_testChecked }
        return menuEntry

    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font)
        page_bottom = self.editor.viewport().height()
       
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        
        while block.isValid():
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible():
                userData = block.userData()
    
                mark = self.editor.folding.getFoldingMark(block)
                if self.editor.folding.isStart(mark):
                    if userData.folded:
                        painter.drawPixmap(1,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingcollapsedImage.height(),
                            self.foldingcollapsedImage)
                    else:
                        painter.drawPixmap(1,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingtopImage.height(),
                            self.foldingtopImage)
                elif self.editor.folding.isStop(mark):
                    painter.drawPixmap(1,
                        round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingbottomImage.height(),
                        self.foldingbottomImage)

            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        if self.editor.folding.isFoldingMark(block):
            if self.editor.folding.isFolded(block):
                self.editor.codeFoldingUnfold(block)
            else:
                self.editor.codeFoldingFold(block)
