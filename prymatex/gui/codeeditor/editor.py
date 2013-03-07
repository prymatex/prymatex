#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseEditor
from prymatex.widgets.texteditor import TextEditWidget

from prymatex import resources
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core import exceptions
from prymatex.qt.helpers.menus import extend_menu, update_menu
from prymatex.models.support import BundleItemTreeNode

from prymatex.gui.codeeditor.userdata import CodeEditorBlockUserData
from prymatex.gui.codeeditor.addons import CodeEditorAddon
from prymatex.gui.codeeditor.sidebar import CodeEditorSideBar, SideBarWidgetAddon
from prymatex.gui.codeeditor.processors import PMXCommandProcessor, PMXSnippetProcessor, PMXMacroProcessor
from prymatex.gui.codeeditor.modes import PMXMultiCursorEditorMode, PMXCompleterEditorMode, PMXSnippetEditorMode
from prymatex.gui.codeeditor.highlighter import PMXSyntaxHighlighter
from prymatex.gui.codeeditor.folding import CodeEditorFolding
from prymatex.gui.codeeditor.models import (SymbolListModel, BookmarkListModel, 
                                            AlreadyTypedWords, 
                                            bundleItemSelectableModelFactory,
                                            bookmarkSelectableModelFactory,
                                            symbolSelectableModelFactory)

from prymatex.support import PMXSnippet, PMXMacro, PMXCommand, PMXDragCommand, PMXSyntax, PMXPreferenceSettings

from prymatex.utils import coroutines
from prymatex.utils import text as texttools
from prymatex.utils.i18n import ugettext as _
from prymatex.utils.decorators.helpers import printtime

WIDTH_CHARACTER = "#"

class CodeEditor(TextEditWidget, PMXBaseEditor):
    # -------------------- Scope groups
    SORTED_GROUPS = [   "keyword", "entity", "meta", "variable", "markup", 
                        "support", "storage", "constant", "string", "comment", "invalid" ]

    # Aca vamos a guardar los scopes de los editores, quiza esto pueda ser un objeto factory,
    # por ahora la fabricacion la hace el editor en el factory method flyweightScopeFactory
    SCOPES = {}
        
    # -------------------- Signals
    syntaxChanged = QtCore.pyqtSignal(object)
    themeChanged = QtCore.pyqtSignal()
    modeChanged = QtCore.pyqtSignal()
    blocksRemoved = QtCore.pyqtSignal(QtGui.QTextBlock, int)
    blocksAdded = QtCore.pyqtSignal(QtGui.QTextBlock, int)
    
    aboutToHighlightChange = QtCore.pyqtSignal()
    highlightChanged = QtCore.pyqtSignal()
    
    # ------------------ Flags
    ShowTabsAndSpaces     = 1<<0
    ShowLineAndParagraphs = 1<<1
    WordWrap              = 1<<2
    MarginLine            = 1<<3
    IndentGuide           = 1<<4
    HighlightCurrentLine  = 1<<5
    
    # ------------------- Settings
    SETTINGS_GROUP = 'CodeEditor'
    
    
    tabStopSoft = pmxConfigPorperty(default = True)
    marginLineSpaces = pmxConfigPorperty(default = 80)
    
    
    @pmxConfigPorperty(default = 4)
    def tabStopSize(self, size):
        self.setTabStopWidth(size * 9)
    
    @pmxConfigPorperty(default = QtGui.QFont("Monospace", 9))
    def defaultFont(self, font):
        self.setFont(font)

    @pmxConfigPorperty(default = "3130E4FA-B10E-11D9-9F75-000D93589AF6", tm_name = 'OakDefaultLanguage')
    def defaultSyntax(self, uuid):
        syntax = self.application.supportManager.getBundleItem(uuid)
        self.setSyntax(syntax)
    
    
    @pmxConfigPorperty(default = '766026CB-703D-4610-B070-8DE07D967C5F', tm_name = 'OakThemeManagerSelectedTheme')
    def defaultTheme(self, uuid):
        theme = self.application.supportManager.getTheme(uuid)

        self.syntaxHighlighter.setTheme(theme)
        self.colours = theme.settings
        
        #Set color for QPlainTextEdit
        appStyle = """QPlainTextEdit {background-color: %s;
        color: %s;
        selection-background-color: %s; }""" % (self.colours['background'].name(), self.colours['foreground'].name(), self.colours['selection'].name())
        self.setStyleSheet(appStyle)
        self.themeChanged.emit()

    @pmxConfigPorperty(default = MarginLine | IndentGuide | HighlightCurrentLine)
    def defaultFlags(self, flags):
        self.setFlags(flags)


    # --------------------- init
    def __init__(self, parent = None):
        TextEditWidget.__init__(self, parent)
        PMXBaseEditor.__init__(self)

        self.__blockUserDataHandlers = []
        
        self.braces = []
        #Current braces for cursor position (leftBrace <|> rightBrace, oppositeLeftBrace, oppositeRightBrace) 
        # <|> the cursor is allways here
        self._currentBraces = (None, None, None, None)
        
        #Sidebars
        self.leftBar = CodeEditorSideBar(self)
        self.rightBar = CodeEditorSideBar(self)

        #Models
        self.bookmarkListModel = BookmarkListModel(self)
        self.symbolListModel = SymbolListModel(self)
        self.alreadyTypedWords = AlreadyTypedWords(self)
        self.bundleItemSelectableModel = bundleItemSelectableModelFactory(self)
        self.symbolSelectableModel = symbolSelectableModelFactory(self)
        self.bookmarkSelectableModel = bookmarkSelectableModelFactory(self)
        
        #Folding
        self.folding = CodeEditorFolding(self)
        
        #Processors
        self.commandProcessor = PMXCommandProcessor(self)
        self.macroProcessor = PMXMacroProcessor(self)
        self.snippetProcessor = PMXSnippetProcessor(self)

        #Highlighter
        self.syntaxHighlighter = PMXSyntaxHighlighter(self)
        
        # TODO Quiza algo como que los modos se registren solos?
        #Modes
        self.multiCursorMode = PMXMultiCursorEditorMode(self)
        self.completerMode = PMXCompleterEditorMode(self)
        self.snippetMode = PMXSnippetEditorMode(self)
        
        #Block Count
        self.lastBlockCount = self.document().blockCount()

        #Connect context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showEditorContextMenu)

        self.completerTask = self.application.scheduler.idleTask()
        
        #Register text formaters
        self.registerTextCharFormatBuilder("line", self.textCharFormat_line_builder)
        self.registerTextCharFormatBuilder("selection", self.textCharFormat_selection_builder)
        self.registerTextCharFormatBuilder("brace", self.textCharFormat_brace_builder)

        # Sidebars signals
        self.rightBar.updateRequest.connect(self.updateViewportMargins)
        self.leftBar.updateRequest.connect(self.updateViewportMargins)
        
        # Document signals
        self.document().undoCommandAdded.connect(self.on_document_undoCommandAdded)        

        # Editor signals
        self.blockCountChanged.connect(self.on_blockCountChanged)
        self.updateRequest.connect(self.updateSideBars)
        self.modificationChanged.connect(self.on_modificationChanged)
        self.syntaxChanged.connect(self.on_syntaxChanged)
        self.themeChanged.connect(self.highlightEditor)

    def initialize(self, mainWindow):
        PMXBaseEditor.initialize(self, mainWindow)
        self.selectorDialog = self.mainWindow.findChild(QtGui.QDialog, "SelectorDialog")
        self.browserDock = self.mainWindow.findChild(QtGui.QDockWidget, "BrowserDock")

        # Ultimo en conectar esta señal, para poder hacer el update
        self.cursorPositionChanged.connect(self.setCurrentBraces)
        self.cursorPositionChanged.connect(self.highlightEditor)

    # ----------- Override from PMXBaseComponent
    def addComponent(self, component):
        PMXBaseEditor.addComponent(self, component)
        if isinstance(component, SideBarWidgetAddon):
            self.addSideBarWidget(component)

    def addSideBarWidget(self, widget):
        if widget.ALIGNMENT == QtCore.Qt.AlignRight:
            self.rightBar.addWidget(widget)
        else:
            self.leftBar.addWidget(widget)

    def on_syntaxChanged(self, syntax):
        # Build basic scope
        scopeHash = self.flyweightScopeFactory([syntax.scopeName])
        
        # Set braces
        settings = self.scope(scopeHash = scopeHash, attribute='settings')
        self.braces = settings.smartTypingPairs
        
        self.showMessage("Syntax changed to <b>%s</b>" % syntax.name)
    
    def showMessage(self, *largs, **kwargs):
        self.application.showMessage(*largs, **kwargs)

    def setPlainText(self, text):
        self.syntaxHighlighter.stop()
        self.aboutToHighlightChange.emit()
        QtGui.QPlainTextEdit.setPlainText(self, text)
        self.syntaxHighlighter.runAsyncHighlight(lambda editor = self: editor.highlightChanged.emit())
            
    # --------------- Block User Data
    def registerBlockUserDataHandler(self, handler):
        self.__blockUserDataHandlers.append(handler)
    
    def blockUserDataFactory(self, block):
        userData = CodeEditorBlockUserData()
        map(lambda handler: handler.contributeToBlockUserData(userData), self.__blockUserDataHandlers)
        return userData

    def processBlockUserData(self, text, block, userData):
        # Indent
        indent = texttools.whiteSpace(text)
        if indent != userData.indent:
            userData.indent = indent
        # Handlers
        map(lambda handler: handler.processBlockUserData(text, block, userData), self.__blockUserDataHandlers)
        
    def on_modificationChanged(self, value):
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))
    
    def on_blockCountChanged(self, newBlockCount):
        self.logger.debug("block Count changed")
        block = self.textCursor().block()
        if self.lastBlockCount > self.document().blockCount():
            self.blocksRemoved.emit(block, self.lastBlockCount - newBlockCount)
        else:
            self.blocksAdded.emit(block, newBlockCount - self.lastBlockCount)
        self.lastBlockCount = self.document().blockCount()

    # ------------- Base Editor Api
    @classmethod
    def acceptFile(cls, filePath, mimetype):
        return re.compile("text/.*").match(mimetype) is not None

    def open(self, filePath):
        """ Custom open for large files """
        PMXBaseEditor.open(self, filePath)
        content = self.application.fileManager.readFile(filePath)
        self.setPlainText(content)
    
    def close(self):
        PMXBaseEditor.close(self)
        QtGui.QPlainTextEdit.close(self)
        
    def reload(self):
        PMXBaseEditor.reload(self)
        content = self.application.fileManager.readFile(self.filePath)
        self.updatePlainText(content)

    def saveState(self):
        """Returns a Python dictionary containing the state of the editor."""
        state = {}
        #Bookmarks
        state['bookmarks'] = self.bookmarkListModel.lineNumbers()
        
        #UserDatas
        state['data'] = []
        
        return state
    
    def restoreState(self, state):
        """Restore the state from the given state (returned by a previous call to state())."""
        pass

    def isModified(self):
        return self.document().isModified()
    
    def isEmpty(self):
        return self.document().isEmpty()
        
    def setModified(self, modified):
        self.document().setModified(modified)
        
    def setFilePath(self, filePath):
        extension = self.application.fileManager.extension(filePath)
        syntax = self.application.supportManager.findSyntaxByFileType(extension)
        if syntax is not None:
            self.setSyntax(syntax)
        PMXBaseEditor.setFilePath(self, filePath)
        
    def tabTitle(self):
        #Podemos marcar de otra forma cuando algo cambia :P
        return PMXBaseEditor.tabTitle(self)
    
    def fileFilters(self):
        return [ "%s (%s)" % (self.syntax().bundle.name, " ".join(map(lambda ft: "*." + ft, self.syntax().fileTypes))) ]
        #return PMXBaseEditor.fileFilters(self)
    
    def setCursorPosition(self, position):
        cursor = self.textCursor()
        blockPosition = self.document().findBlockByNumber(position[0]).position()
        cursor.setPosition(blockPosition + position[1])
        self.setTextCursor(cursor)

    def cursorPosition(self):
        cursor = self.textCursor()
        return (cursor.block().blockNumber(), cursor.positionInBlock())

    # ---------------------- Scopes
    @classmethod
    def flyweightScopeFactory(cls, scopeStack):
        # TODO Analizar mejor la utilidad de esto, quiza dejar los nombres en listas sea mejor
        scopeName = " ".join(scopeStack)
        scopeHash = hash(scopeName)
        if scopeHash not in cls.SCOPES:
            scopeData = cls.SCOPES.setdefault(scopeHash, {
                "name": scopeName,
                "settings": cls.application.supportManager.getPreferenceSettings(scopeName),
                "group": PMXSyntax.findGroup(scopeStack[::-1])
            })
        return scopeHash
    
    
    def scope(self, cursor = None, block = None, blockPosition = None, documentPosition = None,
                scopeHash = None, direction = "right", attribute = "name"):
        if scopeHash is not None:
            return self.SCOPES[scopeHash][attribute]
        if block is None:
            cursor = cursor or (documentPosition is not None and self.cursorAtPosition(documentPosition)) or self.textCursor()
            block = cursor.block()
        userData = block.userData()
        positionInBlock = blockPosition or (cursor is not None and cursor.positionInBlock()) or 0
        if direction == "right":
            # TODO: Cuando el syntax processor funcione bien sacar este or
            rightScope = userData is not None and userData.scopeAtPosition(positionInBlock) or hash(self.syntax().scopeName)
            return self.SCOPES[rightScope][attribute]
        elif direction == "left":
            # TODO: Cuando el syntax processor funcione bien sacar este or
            leftScope = userData is not None and userData.scopeAtPosition(positionInBlock - 1) or hash(self.syntax().scopeName)
            return self.SCOPES[leftScope][attribute]
        elif direction == "both":
            # TODO: Cuando el syntax processor funcione bien sacar este or
            leftScope = userData is not None and userData.scopeAtPosition(positionInBlock - 1) or hash(self.syntax().scopeName)
            rightScope = userData is not None and userData.scopeAtPosition(positionInBlock) or hash(self.syntax().scopeName)
            return self.SCOPES[leftScope][attribute], self.SCOPES[rightScope][attribute]
        
        
    def scopes(self, block = None, attribute = "name", scope_filter = lambda attr: True):
        block = block or self.textCursor().block()
        userData = block.userData()
        if userData is None: return []
        return filter(
                    lambda ((start, end), attr): scope_filter(attr), 
                    map(
                        lambda ((start, end), scope): ((start, end), self.SCOPES[scope][attribute]),
                        userData.scopeRanges()
                        )
                    )
    

    # ------------ Obteniendo datos del editor
    def tabKeyBehavior(self):
        return self.tabStopSoft and unicode(' ') * self.tabStopSize or unicode('	')


    # Flags
    def getFlags(self):
        flags = 0
        options = self.document().defaultTextOption()
        if options.flags() & QtGui.QTextOption.ShowTabsAndSpaces:
            flags |= self.ShowTabsAndSpaces
        if options.flags() & QtGui.QTextOption.ShowLineAndParagraphSeparators:
            flags |= self.ShowLineAndParagraphs
        if self.showMarginLine:
            flags |= self.MarginLine
        if self.showIndentGuide:
            flags |= self.IndentGuide
        if self.showHighlightCurrentLine:
            flags |= self.HighlightCurrentLine
        if options.wrapMode() & QtGui.QTextOption.WordWrap:
            flags |= self.WordWrap
        return flags
        
    def setFlags(self, flags):
        options = self.document().defaultTextOption()
        oFlags = options.flags()
        if flags & self.ShowTabsAndSpaces:
            oFlags |= QtGui.QTextOption.ShowTabsAndSpaces
        else:
            oFlags &= ~QtGui.QTextOption.ShowTabsAndSpaces
        if flags & self.ShowLineAndParagraphs:
            oFlags |= QtGui.QTextOption.ShowLineAndParagraphSeparators
        else:
            oFlags &= ~QtGui.QTextOption.ShowLineAndParagraphSeparators
        if flags & self.WordWrap:
            options.setWrapMode(QtGui.QTextOption.WordWrap)
        else:
            options.setWrapMode(QtGui.QTextOption.NoWrap)
        options.setFlags(oFlags)
        self.document().setDefaultTextOption(options)
        self.showMarginLine = bool(flags & self.MarginLine)
        self.showIndentGuide = bool(flags & self.IndentGuide)
        self.showHighlightCurrentLine = bool(flags & self.HighlightCurrentLine)

    # ------------------- Syntax
    def syntax(self):
        return self.syntaxHighlighter.syntax
        
    def setSyntax(self, syntax):
        if self.syntaxHighlighter.syntax != syntax:
            self.syntaxHighlighter.stop()
            self.aboutToHighlightChange.emit()
            
            # Set syntax
            self.syntaxHighlighter.setSyntax(syntax)
            self.syntaxChanged.emit(syntax)
            
            # Run
            self.syntaxHighlighter.runAsyncHighlight(lambda editor = self: editor.highlightChanged.emit())


    # -------------------- SideBars
    def updateViewportMargins(self):
        self.setViewportMargins(self.leftBar.width(), 0, self.rightBar.width(), 0)
    
    def updateSideBars(self, rect, dy):
        if dy:
            self.rightBar.scroll(0, dy)
            self.leftBar.scroll(0, dy)
        else:
            self.rightBar.update(0, rect.y(), self.rightBar.width(), rect.height())
            self.leftBar.update(0, rect.y(), self.leftBar.width(), rect.height())
    
    def updateSideBarsGeometry(self):
        cr = self.contentsRect()
        self.leftBar.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.leftBar.width(), cr.height()))
        rightBarPosition = cr.right() - self.rightBar.width()
        if self.application.platform == "win32" and self.verticalScrollBar().isVisible():
            rightBarPosition -= self.verticalScrollBar().width()
        self.rightBar.setGeometry(QtCore.QRect(rightBarPosition, cr.top(), self.rightBar.width(), cr.height()))
    

    # -------------- Braces
    def setCurrentBraces(self, cursor = None):
        cursor = QtGui.QTextCursor(cursor) if cursor is not None else QtGui.QTextCursor(self.textCursor())
        cursor.clearSelection()
        openBraces = map(lambda pair: pair[0], self.braces)
        closeBraces = map(lambda pair: pair[1], self.braces)
        
        leftChar = cursor.document().characterAt(cursor.position() - 1)
        rightChar = cursor.document().characterAt(cursor.position())
        
        self._currentBraces = (None, None, None, None)

        # TODO si no hay para uno no hay para ninguno, quitar el que esta si el findTypingPair retorna None
        if leftChar in openBraces:
            leftCursor = QtGui.QTextCursor(cursor)
            leftCursor.movePosition(QtGui.QTextCursor.PreviousCharacter, QtGui.QTextCursor.KeepAnchor)
            index = openBraces.index(leftChar)
            otherBrace = self.findTypingPair(leftChar, closeBraces[index], leftCursor)
            if otherBrace is not None:
                self._currentBraces = (leftCursor, None, otherBrace, None)
        if rightChar in openBraces:
            rightCursor = QtGui.QTextCursor(cursor)
            rightCursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
            index = openBraces.index(rightChar)
            otherBrace = self.findTypingPair(rightChar, closeBraces[index], rightCursor)
            if otherBrace is not None:
                self._currentBraces = (self._currentBraces[0], rightCursor, self._currentBraces[2], otherBrace)
        if leftChar in closeBraces and self._currentBraces[0] is None:  #Tener uno implica tener los dos por el if
            leftCursor = QtGui.QTextCursor(cursor)
            leftCursor.movePosition(QtGui.QTextCursor.PreviousCharacter, QtGui.QTextCursor.KeepAnchor)
            otherBrace = self.findTypingPair(leftChar, openBraces[closeBraces.index(leftChar)], leftCursor, True)
            if otherBrace is not None:
                self._currentBraces = (leftCursor, self._currentBraces[1], otherBrace, self._currentBraces[3])
        if rightChar in closeBraces and self._currentBraces[1] is None: #Tener uno implica tener los dos por el if
            rightCursor = QtGui.QTextCursor(cursor)
            rightCursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
            otherBrace = self.findTypingPair(rightChar, openBraces[closeBraces.index(rightChar)], rightCursor, True)
            if otherBrace is not None:
                self._currentBraces = (self._currentBraces[0], rightCursor, self._currentBraces[2], otherBrace)

    def currentBracesPairs(self, cursor = None, direction = "both"):
        """ Retorna el otro cursor correspondiente al cursor (brace) pasado o actual del editor, puede retornar None en caso de no estar cerrado el brace"""
        cursor = cursor or self.textCursor()
        brace1, brace2 = (None, None)
        if cursor.hasSelection():
            for index in [0, 1]:
                if self._currentBraces[index] is not None and cursor.selectedText() == self._currentBraces[index].selectedText():
                    brace1 = QtGui.QTextCursor(self._currentBraces[index + 2]) if self._currentBraces[index + 2] is not None else None
                    brace2 = cursor
                    break
        else:
            #print map(lambda c: c is not None and c.selectedText() or "None", self._currentBraces)
            if direction in ("left", "both"):
                brace1 = self._currentBraces[0]
                brace2 = self._currentBraces[2]
            if (brace1 is None or brace2 is None) and direction in ("right", "both"):
                brace1 = self._currentBraces[1]
                brace2 = self._currentBraces[3]
        if (brace1 is not None and brace2 is not None) and brace1.selectionStart() > brace2.selectionStart():
            return (brace2, brace1)
        return (brace1, brace2)

    def beforeBrace(self, cursor):
        return self._currentBraces[1] is not None and self._currentBraces[1].position() - 1 == cursor.position()
    
    def afterBrace(self, cursor):
        return self._currentBraces[0] is not None and self._currentBraces[0].position() + 1 == cursor.position()
        
    def besideBrace(self, cursor):
        return self.beforeBrace(cursor) or self.afterBrace(cursor)

    def surroundBraces(self, cursor):
        #TODO: Esto esta mal
        return self.beforeBrace(cursor) and self.afterBrace(cursor)
        
    #-------------------- Highlight Editor
    def textCharFormat_line_builder(self):
        format = QtGui.QTextCharFormat()
        format.setBackground(self.colours['lineHighlight'])
        format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        return format
        
    def textCharFormat_brace_builder(self):
        format = QtGui.QTextCharFormat()
        format.setForeground(self.colours['caret'])
        format.setFontUnderline(True)
        format.setUnderlineColor(self.colours['foreground']) 
        format.setBackground(QtCore.Qt.transparent)
        return format

    def textCharFormat_selection_builder(self):
        format = QtGui.QTextCharFormat()
        format.setBackground(self.colours['selection'])
        return format
        
    def highlightEditor(self):
        cursor = self.textCursor()
        cursor.clearSelection()
        if self.showHighlightCurrentLine:
            self.setExtraSelectionCursors("line", [ cursor ])
        else:
            self.clearExtraSelectionCursors("line")
        self.setExtraSelectionCursors("brace", filter(lambda cursor: cursor is not None, list(self._currentBraces)))
        self.updateExtraSelections()

        
    # ------------ QPlainTextEdit Events
    def focusInEvent(self, event):
        # TODO No es para este evento pero hay que poner en alugn lugar el update de las side bars
        QtGui.QPlainTextEdit.focusInEvent(self, event)
        self.updateSideBarsGeometry()
        
    def resizeEvent(self, event):
        QtGui.QPlainTextEdit.resizeEvent(self, event)
        self.updateSideBarsGeometry()

    def paintEvent(self, event):
        QtGui.QPlainTextEdit.paintEvent(self, event)
        page_bottom = self.viewport().height()
        # TODO: los widgets se pueden hacer del fontMetric, que tal poner algo que me retorne directamente el ancho de un caracter?
        font_metrics = QtGui.QFontMetrics(self.document().defaultFont())

        painter = QtGui.QPainter(self.viewport())
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
            
        painter.setPen(self.colours['selection'])
        block = self.firstVisibleBlock()
        offset = self.contentOffset()
        while block.isValid() and block.userData():
            # The top left position of the block in the document
            # position = self.blockBoundingGeometry(block).topLeft() + offset
            blockGeometry = self.blockBoundingGeometry(block)
            # Check if the position of the block is out side of the visible area
            if blockGeometry.top() > page_bottom:
                break
            if block.isVisible():
                positionY = round(blockGeometry.top()) + offset.y()
                user_data = block.userData()
                if self.folding.isStart(self.folding.getFoldingMark(block)) and user_data.folded:
                    painter.drawPixmap(font_metrics.width(block.text()) + offset.x() + 5,
                        positionY + font_metrics.ascent() + font_metrics.descent() - resources.getImage("foldingellipsis").height(),
                        resources.getImage("foldingellipsis"))
                if self.showIndentGuide:
                    blockPattern = block
                    while blockPattern.isValid() and blockPattern.userData() and blockPattern.userData().blank():
                        blockPattern = blockPattern.next()
                    if blockPattern.isValid() and blockPattern.userData():
                        indentPattern = blockPattern.userData().indent
                        for s in range(0, (len(indentPattern) / len(self.tabKeyBehavior()))):
                            positionX = (font_metrics.width(WIDTH_CHARACTER) * self.tabStopSize * s) + font_metrics.width(WIDTH_CHARACTER) + offset.x()
                            painter.drawLine(positionX, positionY, positionX, positionY + font_metrics.height())
                
            block = block.next()

        if self.showMarginLine:
            pos_margin = self.fontMetrics().width(WIDTH_CHARACTER) * self.marginLineSpaces
            painter.drawLine(pos_margin + offset.x(), 0, pos_margin + offset.x(), self.viewport().height())

        if self.multiCursorMode.isActive():
            ctrl_down = bool(self.application.keyboardModifiers() & QtCore.Qt.ControlModifier)
            for index, cursor in enumerate(self.multiCursorMode.cursors, 1):
                rec = self.cursorRect(cursor)
                fakeCursor = QtCore.QLine(rec.x(), rec.y(), rec.x(), rec.y() + font_metrics.ascent() + font_metrics.descent())
                colour = self.colours['caret']
                painter.setPen(QtGui.QPen(colour))
                if ctrl_down:
                    painter.drawText(rec.x() + 2, rec.y() + font_metrics.ascent(), str(index))
                if (self.multiCursorMode.hasSelection() and not self.multiCursorMode.isSelected(cursor)) or \
                (ctrl_down and not self.multiCursorMode.hasSelection()):
                     colour = self.colours['selection']
                painter.setPen(QtGui.QPen(colour))
                painter.drawLine(fakeCursor)

        if self.multiCursorMode.isDragCursor:
            pen = QtGui.QPen(self.colours['caret'])
            pen.setWidth(2)
            painter.setPen(pen)
            color = QtGui.QColor(self.colours['selection'])
            color.setAlpha(128)
            painter.setBrush(QtGui.QBrush(color))
            painter.setOpacity(0.2)
            painter.drawRect(self.multiCursorMode.getDragCursorRect())
        painter.end()


    # ----------------- Mouse Events
    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.delta() == 120:
                self.zoomIn()
            elif event.delta() == -120:
                self.zoomOut()
            event.ignore()
        else:
            QtGui.QPlainTextEdit.wheelEvent(self, event)

    def mousePressEvent(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier or self.multiCursorMode.isActive():
            self.multiCursorMode.mousePressPoint(event.pos())
        else:
            QtGui.QPlainTextEdit.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier or self.multiCursorMode.isActive():
            #En este modo no hago el cursor visible
            self.multiCursorMode.mouseMovePoint(event.pos())
            self.viewport().repaint(self.viewport().visibleRegion())
        else:
            self.ensureCursorVisible()
            QtGui.QPlainTextEdit.mouseReleaseEvent(self, event)
 
    def mouseReleaseEvent(self, event):
        freehanded = False
        if self.multiCursorMode.isActive():
            self.multiCursorMode.mouseReleasePoint(event.pos(), bool(event.modifiers() & QtCore.Qt.MetaModifier))
            self.viewport().repaint(self.viewport().visibleRegion())
        elif freehanded:
            #Modo freehanded
            cursor = self.cursorForPosition(event.pos())
            if not self.cursorRect(cursor).contains(event.pos()):
                cursor.beginEditBlock()
                while not self.cursorRect(cursor).top() <= event.pos().y() <= self.cursorRect(cursor).bottom():
                    cursor.insertText("\n")
                    print cursor.position(), self.cursorRect(cursor)
                while self.cursorRect(cursor).x() <= event.pos().x():
                    cursor.insertText(" ")
                    print cursor.position(), self.cursorRect(cursor)
                cursor.endEditBlock()
                self.setTextCursor(cursor)
            else:
                QtGui.QPlainTextEdit.mouseReleaseEvent(self, event)
        else:
            QtGui.QPlainTextEdit.mouseReleaseEvent(self, event)


    # -------------------- Keyboard Events
    def runKeyHelper(self, event):
        #No tengo modo activo, intento con los helpers
        cursor = self.textCursor()
        for helper in self.findHelpers(event.key()):
            #Buscar Entre los helpers
            if helper.accept(event, cursor):
                helper.execute(event, cursor)
                return True
        return False

    def keyPressEvent(self, event):
        """This method is called whenever a key is pressed.
        The key code is stored in event.key()"""
        
        #Primero ver si tengo un modo activo,
        for mode in [ self.snippetMode, self.multiCursorMode, self.completerMode ]:
            if mode.isActive():
                return mode.keyPressEvent(event)
        
        if not self.runKeyHelper(event):
            #No tengo helper paso el evento a la base
            QtGui.QPlainTextEdit.keyPressEvent(self, event)
            
            self.emit(QtCore.SIGNAL("keyPressEvent(QEvent)"), event)

    def keyReleaseEvent(self, event):
        #Primero ver si tengo un modo activo,
        for mode in [ self.snippetMode, self.multiCursorMode, self.completerMode ]:
            if mode.isActive():
                return mode.keyReleaseEvent(event)
        QtGui.QPlainTextEdit.keyReleaseEvent(self, event)


    # ------------ Insert API
    def insertNewLine(self, cursor = None):
        cursor = cursor or self.textCursor()
        block = cursor.block()
        positionInBlock = cursor.positionInBlock()
        userData = cursor.block().userData()
        settings = self.scope(attribute='settings')
        indentMarks = settings.indent(block.text()[:positionInBlock])
        if PMXPreferenceSettings.INDENT_INCREASE in indentMarks:
            self.logger.debug("Increase indent")
            indent = userData.indent + self.tabKeyBehavior()
        elif PMXPreferenceSettings.INDENT_NEXTLINE in indentMarks:
            #TODO: Creo que este no es el correcto
            self.logger.debug("Increase next line indent")
            indent = userData.indent + self.tabKeyBehavior()
        elif PMXPreferenceSettings.UNINDENT in indentMarks:
            self.logger.debug("Unindent")
            indent = ""
        elif PMXPreferenceSettings.INDENT_DECREASE in indentMarks:
            self.logger.debug("Decrease indent")
            indent = userData.indent[:-len(self.tabKeyBehavior())]
        else:
            self.logger.debug("Preserve indent")
            indent = block.userData().indent[:positionInBlock]
        cursor.insertText("\n%s" % indent)
        self.ensureCursorVisible()


    # ------------ Bundle Items
    def bundleItemHandler(self):
        return self.insertBundleItem


    def insertBundleItem(self, item, **processorSettings):
        """Inserta un bundle item"""
        
        if item.TYPE == PMXSnippet.TYPE:
            self.snippetProcessor.configure(processorSettings)
            self.textCursor().beginEditBlock()
            item.execute(self.snippetProcessor)
            self.textCursor().endEditBlock()
        elif item.TYPE == PMXCommand.TYPE or item.TYPE == PMXDragCommand.TYPE:
            self.commandProcessor.configure(processorSettings)
            self.textCursor().beginEditBlock()
            item.execute(self.commandProcessor)
            self.textCursor().endEditBlock()
        elif item.TYPE == PMXMacro.TYPE:
            self.macroProcessor.configure(processorSettings)
            self.textCursor().beginEditBlock()
            item.execute(self.macroProcessor)
            self.textCursor().endEditBlock()
        elif item.TYPE == PMXSyntax.TYPE:
            self.setSyntax(item)


    def selectBundleItem(self, items, tabTriggered = False):
        #Tengo mas de uno que hago?, muestro un menu
        syntax = any(map(lambda item: item.TYPE == 'syntax', items))
        
        def insertBundleItem(index):
            if index >= 0:
                self.insertBundleItem(items[index], tabTriggered = tabTriggered)
        
        self.showFlatPopupMenu(items, insertBundleItem, cursorPosition = not syntax)


    def executeCommand(self, commandScript = None, commandInput = "none", commandOutput = "insertText"):
        if commandScript is None:
            commandScript = self.textCursor().selectedText() if self.textCursor().hasSelection() else self.textCursor().block().text()
        command = self.application.supportManager.buildAdHocCommand(commandScript, self.syntax().bundle, commandInput, commandOutput)
        self.insertBundleItem(command)


    def environmentVariables(self):
        environment = PMXBaseEditor.environmentVariables(self)
        cursor = self.textCursor()
        block = cursor.block()
        line = block.text()
        leftScope, rightScope = self.scope(direction = "both")
        current_word, start, end = self.currentWord()
        environment.update({
                'TM_CURRENT_LINE': line,
                'TM_LINE_INDEX': cursor.positionInBlock(),
                'TM_LINE_NUMBER': block.blockNumber() + 1,
                'TM_COLUMN_NUMBER': cursor.positionInBlock() + 1,
                'TM_SCOPE': rightScope,
                'TM_SCOPE_LEFT': leftScope,
                'TM_MODE': self.syntax().name,
                'TM_SOFT_TABS': self.tabStopSoft and unicode('YES') or unicode('NO'),
                'TM_TAB_SIZE': self.tabStopSize,
                'TM_NESTEDLEVEL': self.folding.getNestedLevel(block)
        })

        if current_word:
            self.logger.debug("Add current word to environment")
            environment['TM_CURRENT_WORD'] = current_word
        if self.filePath is not None:
            self.logger.debug("Add file path to environment")
            environment['TM_FILEPATH'] = self.filePath
            environment['TM_FILENAME'] = self.application.fileManager.basename(self.filePath)
            environment['TM_DIRECTORY'] = self.application.fileManager.dirname(self.filePath)
        if self.project is not None:
            self.logger.debug("Add project to environment")
            environment.update(self.project.environmentVariables())
        if cursor.hasSelection():
            self.logger.debug("Add selection to environment")
            environment['TM_SELECTED_TEXT'] = cursor.selectedText().replace(u"\u2029", '\n').replace(u"\u2028", '\n')
            start, end = self.selectionBlockStartEnd()
            environment['TM_INPUT_START_COLUMN'] = cursor.selectionStart() - start.position() + 1
            environment['TM_INPUT_START_LINE'] = start.blockNumber() + 1
            environment['TM_INPUT_START_LINE_INDEX'] = cursor.selectionStart() - start.position()
        
        settings = self.scope(attribute = 'settings')
        environment.update(settings.shellVariables)
        return environment
        

    # ---------- Completer
    def showCompleter(self, suggestions, source = "default", alreadyTyped = None, caseInsensitive = True, callback = None):
        currentAlreadyTyped = self.currentWord(direction = "left", search = False)[0]
        if alreadyTyped is None or currentAlreadyTyped.startswith(alreadyTyped) or callback is not None:
            case = QtCore.Qt.CaseInsensitive if caseInsensitive else QtCore.Qt.CaseSensitive
            self.completerMode.setCaseSensitivity(case)
            self.completerMode.setActivatedCallback(callback)
            self.completerMode.setStartCursorPosition(self.textCursor().position() - len(currentAlreadyTyped))
            self.completerMode.setSuggestions(suggestions, source)
            self.completerMode.setCompletionPrefix(currentAlreadyTyped)
            self.completerMode.complete(self.cursorRect())

    
    def showCachedCompleter(self):
        if not self.completerMode.hasSource("default"):
            return
        currentAlreadyTyped = self.currentWord(direction = "left", search = False)[0]
        if currentAlreadyTyped:
            self.completerMode.setActivatedCallback(None)
            self.completerMode.setStartCursorPosition(self.textCursor().position() - len(currentAlreadyTyped))
            self.completerMode.setSource("default")
            self.completerMode.setCompletionPrefix(currentAlreadyTyped)
            self.completerMode.complete(self.cursorRect())


    def switchCompleter(self):
        settings = self.scope(attribute='settings')
        if not self.completerMode.hasSource("default"):
            def on_suggestionsReady(suggestions):
                if bool(suggestions):
                    self.completerMode.setSuggestions(suggestions, "default")
            self.defaultCompletion(settings, on_suggestionsReady)
        else:
            self.completerMode.switch()


    def runCompleter(self):
        settings = self.scope(attribute='settings')
        def on_suggestionsReady(suggestions):
             if bool(suggestions):
                self.showCompleter(suggestions)
        self.defaultCompletion(settings, on_suggestionsReady)


    def defaultCompletion(self, settings, callback):
        if not self.completerTask.isRunning():
            self.completerTask = self.application.scheduler.newTask(self.runCompletionSuggestions(settings = settings))
            def on_completerTaskReady(callback):
                def completerTaskReady(result):
                    callback(result.value)
                return completerTaskReady
            #En una clausura
            self.completerTask.done.connect(on_completerTaskReady(callback))


    def runCompletionSuggestions(self, cursor = None, scope = None, settings = None):
        cursor = cursor or self.textCursor()
        settings = settings or self.scope(cursor = cursor, attribute = 'settings')
        scope = scope or self.scope(cursor = cursor)
        currentAlreadyTyped = self.currentWord(direction = "left", search = False)[0]
        
        #An array of additional candidates when cycling through completion candidates from the current document.
        completions = settings.completions[:]
        
        #A shell command (string) which should return a list of candidates to complete the current word (obtained via the TM_CURRENT_WORD variable).
        if settings.completionCommand:
            def commandCallback(context):
                print unicode(context)
            command = self.application.supportManager.buildAdHocCommand(settings.completionCommand, self.syntax().bundle, commandInput="document")
            self.commandProcessor.configure({ "asynchronous": False })
            command.executeCallback(self.commandProcessor, commandCallback)
            
        #A tab tigger completion
        tabTriggers = self.application.supportManager.getAllTabTiggerItemsByScope(scope)
        
        typedWords = self.alreadyTypedWords.typedWords()
        
        #Lo ponemos en la mezcladora por grupos
        suggestions = tabTriggers + map(lambda word: { "display": word, "image": "scope-root-keyword" }, completions)
        for group in CodeEditor.SORTED_GROUPS:
            newWords = filter(lambda word: word not in completions and word != currentAlreadyTyped, typedWords.pop(group, []))
            suggestions += map(lambda word: { "display": word, "image": "scope-root-%s" % group }, newWords)
            completions += newWords
            yield
        
        #Finalizamos con las que quedaron guachas
        for words in typedWords.values():
            newWords = filter(lambda word: word not in completions and word != currentAlreadyTyped, words)
            suggestions += map(lambda word: { "display": word, "image": "scope-root-invalid" }, newWords)
            completions += newWords
            yield

        yield coroutines.Return(suggestions)


    # ---------- Folding
    def codeFoldingFold(self, block):
        milestone = block
        if self.folding.isStart(self.folding.getFoldingMark(milestone)):
            startBlock = milestone.next()
            endBlock = self.folding.findBlockFoldClose(milestone)
            if endBlock is None:
                return
        else:
            endBlock = milestone
            milestone = self.folding.findBlockFoldOpen(endBlock)
            if milestone is None:
                return
            startBlock = milestone.next()
        block = startBlock
        while block.isValid():
            userData = block.userData()
            userData.foldedLevel += 1
            block.setVisible(userData.foldedLevel == 0)
            if block == endBlock:
                break
            block = block.next()
        
        milestone.userData().folded = True
        self.document().markContentsDirty(startBlock.position(), endBlock.position())

    def codeFoldingUnfold(self, block):
        milestone = block
        startBlock = milestone.next()
        endBlock = self.folding.findBlockFoldClose(milestone)
        if endBlock == None:
            return
        
        block = startBlock
        while block.isValid():
            userData = block.userData()
            userData.foldedLevel -= 1
            block.setVisible(userData.foldedLevel == 0)
            if block == endBlock:
                break
            block = block.next()

        milestone.userData().folded = False
        self.document().markContentsDirty(startBlock.position(), endBlock.position())


    # ---------- Override convert tabs <---> spaces
    def convertTabsToSpaces(self):
        match = "\t"
        self.replaceMatch(match, " " * self.tabStopSize, QtGui.QTextDocument.FindFlags(), True)
        
    def convertSpacesToTabs(self):
        match = " " * self.tabStopSize
        self.replaceMatch(match, "\t", QtGui.QTextDocument.FindFlags(), True)

        
    # -------------- Add select text functions
    def selectEnclosingBrackets(self, cursor = None):
        cursor = cursor or self.textCursor()
        flags = QtGui.QTextDocument.FindFlags()
        flags |= QtGui.QTextDocument.FindBackward
        foundCursors = map(lambda (openBrace, closeBrace): (self.document().find(openBrace, cursor.selectionStart(), flags), closeBrace), self.braces)
        openCursor = reduce(lambda c1, c2: (not c1[0].isNull() and c1[0].selectionEnd() > c2[0].selectionEnd()) and c1 or c2, foundCursors)
        if not openCursor[0].isNull():
            closeCursor = self.findTypingPair(openCursor[0].selectedText(), openCursor[1], openCursor[0])
            if openCursor[0].selectionEnd() <= cursor.selectionStart() <= closeCursor.selectionStart():
                cursor.setPosition(openCursor[0].selectionEnd())
                cursor.setPosition(closeCursor.selectionStart(), QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
    
    def selectCurrentScope(self, cursor = None):
        cursor = cursor or self.textCursor()
        block = cursor.block()
        beginPosition = block.position()
        # TODO Todo lo que implique userData centrarlo en una API en la instancia de cada editor
        (start, end), scope = block.userData().scopeRange(cursor.positionInBlock())
        if scope is not None:
            cursor.setPosition(beginPosition + start)
            cursor.setPosition(beginPosition + end, QtGui.QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)
    
    # ---------- Bookmarks and gotos
    def toggleBookmark(self, block = None):
        block = block or self.textCursor().block()
        self.bookmarkListModel.toggleBookmark(block)
    
    def removeAllBookmarks(self):
        self.bookmarkListModel.removeAllBookmarks()
    
    def bookmarkNext(self, block = None):
        block = block or self.textCursor().block()
        block = self.bookmarkListModel.nextBookmark(block)
        if block is not None:
            self.goToBlock(block)

    def bookmarkPrevious(self, block = None):
        block = block or self.textCursor().block()
        block = self.bookmarkListModel.previousBookmark(block)
        if block is not None:
            self.goToBlock(block)

    def goToBlock(self, block):
        cursor = self.textCursor()
        cursor.setPosition(block.position())
        self.setTextCursor(cursor)    
        self.centerCursor()

    def goToLine(self, lineNumber):
        cursor = self.textCursor()
        cursor.setPosition(self.document().findBlockByNumber(lineNumber - 1).position())
        self.setTextCursor(cursor)
        self.centerCursor()
    
    def goToColumn(self, columnNumber):
        cursor = self.textCursor()
        cursor.setPosition(cursor.block().position() + columnNumber)
        self.setTextCursor(cursor)
    
    def centerCursor(self, cursor = None):
        if cursor is not None:
            #Scroll to the center of cursor block number
            pageStep = self.verticalScrollBar().pageStep()
            currentValue = self.verticalScrollBar().value()
            blockNumber = cursor.block().blockNumber()
            scrollIndex = 0 if pageStep > blockNumber else blockNumber - (pageStep / 2)
            self.verticalScrollBar().setValue(scrollIndex)
        else:
            QtGui.QPlainTextEdit.centerCursor(self)


    # ------------------- Text Indentation
    def findPreviousNoBlankBlock(self, block):
        """ Return previous no blank indent block """
        block = block.previous()
        while block.isValid() and block.userData() and block.userData().blank():
            block = block.previous()
        if block.isValid():
            return block
        
    def findPreviousEqualIndentBlock(self, block, indent = None):
        """ Return previous equal indent block """
        indent = indent if indent != None else block.userData().indent
        block = self.findPreviousNoBlankBlock(block)
        while block and block.userData() and block.userData().indent > indent:
            block = self.findPreviousNoBlankBlock(block)
        if block and block.userData() and block.userData().indent == indent:
            return block
            
    def findPreviousMoreIndentBlock(self, block, indent = None):
        """ Return previous more indent block """
        indent = indent if indent != None else block.userData().indent
        block = self.findPreviousNoBlankBlock(block)
        while block and block.userData() and block.userData().indent <= indent:
            block = self.findPreviousNoBlankBlock(block)
        if block and block.userData():
            return block
    
    def findPreviousLessIndentBlock(self, block, indent = None):
        """ Return previous less indent block """
        indent = indent if indent != None else block.userData().indent
        block = self.findPreviousNoBlankBlock(block)
        while block and block.userData() and block.userData().indent >= indent:
            block = self.findPreviousNoBlankBlock(block)
        if block and block.userData():
            return block

    def indentBlocks(self, cursor = None):
        """Indents text, block selections."""
        cursor = QtGui.QTextCursor(cursor or self.textCursor())
        start, end = self.selectionBlockStartEnd(cursor)
        cursor.beginEditBlock()
        while True:
            cursor.setPosition(start.position())
            cursor.insertText(self.tabKeyBehavior())
            if start == end:
                break
            start = start.next()
        cursor.endEditBlock()

    def unindentBlocks(self, cursor = None):
        cursor = QtGui.QTextCursor(cursor or self.textCursor())
        start, end = self.selectionBlockStartEnd(cursor)
        cursor.beginEditBlock()
        while True:
            data = start.userData()
            if self.tabStopSoft:
                counter = self.tabStopSize if len(data.indent) > self.tabStopSize else len(data.indent)
            else:
                counter = 1 if len(data.indent) else 0
            if counter > 0:
                cursor.setPosition(start.position())
                for _ in range(counter):
                    cursor.deleteChar()
            if start == end:
                break
            start = start.next()
        cursor.endEditBlock()
    

    # --------------- Menus
    # Flat Popup Menu
    def showFlatPopupMenu(self, menuItems, callback, cursorPosition = True):
        menu = QtGui.QMenu(self)
        for index, item in enumerate(menuItems, 1):
            if isinstance(item, dict):
                title = "%s 	&%d" % (item["title"], index)
                icon = resources.getIcon(item["image"]) if "image" in item else QtGui.QIcon()
            elif isinstance(item,  basestring):
                title = "%s 	&%d" % (item, index)
                icon = QtGui.QIcon()
            elif isinstance(item,  BundleItemTreeNode):
                title = "%s 	&%d" % (item.buildMenuTextEntry(False), index)
                icon = item.icon
            menu.addAction(icon, title)
        
        def menu_aboutToHide():
            activeActionIndex = menu.actions().index(menu.activeAction()) if menu.activeAction() else -1
            callback(activeActionIndex)
        menu.aboutToHide.connect(menu_aboutToHide)
        
        point = self.viewport().mapToGlobal(self.cursorRect(self.textCursor()).bottomRight()) if cursorPosition else self.mainWindow.cursor().pos()
        menu.popup(point)
    
    # Default Context Menus
    def showEditorContextMenu(self, point):
        menu = self.createStandardContextMenu()
        menu.setParent(self)

        #Bundle Menu
        bundleMenu = self.application.supportManager.menuForBundle(self.syntax().bundle)
        extend_menu(menu, [ "-", bundleMenu ])

        #Se lo pasamos a los addons
        cursor = self.cursorForPosition(point)
        items = ["-"]
        for component in self.components():
            if isinstance(component, CodeEditorAddon):
                items += component.contributeToContextMenu(cursor)
        
        if len(items) > 1:
            actions = extend_menu(menu, items)
            for action in actions:
                if hasattr(action, 'callback'):
                    if action.isCheckable():
                        self.connect(action, QtCore.SIGNAL('triggered(bool)'), action.callback)
                    else:
                        self.connect(action, QtCore.SIGNAL('triggered()'), action.callback)

        menu.popup(self.mapToGlobal(point))
    
    # Contributes to Tab Menu
    def contributeToTabMenu(self):
        menues = []
        bundleMenu = self.application.supportManager.menuForBundle(self.syntax().bundle)
        if bundleMenu is not None:
            menues.append(bundleMenu)
            menues.append("-")
        if self.filePath:
            menues.extend([
                {   "text": "Path to Clipboard",
                    "callback": lambda editor = self: self.application.clipboard().setText(editor.filePath)  },
                {   "text": "Name to Clipboard",
                    "callback": lambda editor = self: self.application.clipboard().setText(editor.application.fileManager.basename(editor.filePath))  },
                {   "text": "Directory to Clipboard",
                    "callback": lambda editor = self: self.application.clipboard().setText(editor.application.fileManager.dirname(editor.filePath))  },
                ])
        return menues
    
    # Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls):
        edit = {
            'name': 'edit',
            'text': 'Edit',
            'items': [
                '-',
                {'text': 'Mode',
                 'items': [
                    {'text': 'Freehanded Editing', 'shortcut': 'Meta+Alt+E'},
                    {'text': 'Overwrite Mode', 'shortcut': 'Meta+Alt+O'},
                    {'text': 'Multi Edit Mode', 'shortcut': 'Meta+Alt+M'}
                 ]}
            ]
        }
        view = {
            'name': 'view',
            'text': 'View',
            'items': [
                {'text': 'Font',
                 'items': [
                     {'text': "Zoom In",
                      'shortcut': "Ctrl++",
                      'callback': cls.zoomIn},
                     {'text': "Zoom Out",
                      'shortcut': "Ctrl+-",
                      'callback': cls.zoomOut}
                ]},
                {'text': 'Left Gutter',
                 'items': []},
                 {'text': 'Right Gutter',
                 'items': []},
                '-',
                {'text': "Show Tabs And Spaces",
                 'callback': cls.on_actionShowTabsAndSpaces_toggled,
                 'checkable': True,
                 'testChecked': lambda editor: bool(editor.getFlags() & editor.ShowTabsAndSpaces) },
                {'text': "Show Line And Paragraph",
                 'callback': cls.on_actionShowLineAndParagraphs_toggled,
                 'checkable': True, 
                 'testChecked': lambda editor: bool(editor.getFlags() & editor.ShowLineAndParagraphs) }, 
                {'text': "Word Wrap",
                 'callback': cls.on_actionWordWrap_toggled,
                 'checkable': True,
                 'testChecked': lambda editor: bool(editor.getFlags() & editor.WordWrap) },
                "-",
                {'text': "Highlight Current Line",
                 'callback': cls.on_actionHighlightCurrentLine_toggled,
                 'checkable': True,
                 'testChecked': lambda editor: bool(editor.getFlags() & editor.HighlightCurrentLine) },
                {'text': "Margin Line",
                 'callback': cls.on_actionMarginLine_toggled,
                 'checkable': True,
                 'testChecked': lambda editor: bool(editor.getFlags() & editor.MarginLine) },
                {'text': "Indent Guide",
                 'callback': cls.on_actionIndentGuide_toggled,
                 'checkable': True,
                 'testChecked': lambda editor: bool(editor.getFlags() & editor.IndentGuide) },
            ]}
        text = {
            'name': 'text',
            'text': '&Text',
            'items': [ 
                {'text': 'Select',
                 'items': [
                    {'text': '&Word',
                     'callback': lambda editor: editor.selectWordCurrent(),
                     'shortcut': 'Ctrl+Meta+W',
                     },
                    {'text': '&Word Under',
                     'callback': lambda editor: editor.selectWordUnder(),
                     'shortcut': 'Ctrl+Meta+W',
                     },
                    {'text': '&Line',
                     'callback': lambda editor: editor.selectLine(),
                     'shortcut': 'Ctrl+Meta+L',
                     },
                    {'text': '&Paragraph',
                     'callback': lambda editor: editor.selectParagraph(),
                     'shortcut': '',
                     },
                    {'text': 'Enclosing &Brackets',
                     'callback': lambda editor: editor.selectEnclosingBrackets(),
                     'shortcut': 'Ctrl+Meta+B',
                     },
                    {'text': 'Current &Scope',
                     'callback': lambda editor: editor.selectCurrentScope(),
                     'shortcut': 'Ctrl+Meta+S',
                     },
                    {'text': '&All',
                     'callback': lambda editor: editor.selectDocument(),
                     'shortcut': 'Ctrl+A',
                     }    
                ]},
                {'text': 'Convert',
                 'items': [
                    {'text': 'To Uppercase',
                     'shortcut': 'Ctrl+U',
                     'callback': lambda editor: editor.convertToUppercase(),
                     },
                    {'text': 'To Lowercase',
                     'shortcut': 'Ctrl+Shift+U',
                     'callback': lambda editor: editor.convertToLowercase(),
                     },
                    {'text': 'To Titlecase',
                     'shortcut': 'Ctrl+Alt+U',
                     'callback': lambda editor: editor.convertToTitlecase(),
                     },
                    {'text': 'To Opposite Case',
                     'shortcut': 'Ctrl+G',
                     'callback': lambda editor: editor.convertToOppositeCase(),
                     }, '-',
                    {'text': 'Tab to Spaces',
                     'callback': lambda editor: editor.convertTabsToSpaces(),
                     },
                    {'text': 'Spaces to Tabs',
                     'callback': lambda editor: editor.convertSpacesToTabs(),
                     }, '-',
                    {'text': 'Transpose',
                     'shortcut': 'Ctrl+T',
                     'callback': lambda editor: editor.convertTranspose(),
                     }
                ]},
                {'text': 'Move',
                 'items': [
                    {'text': 'Line Up',
                     'shortcut': 'Meta+Ctrl+Up',
                     'callback': lambda editor: editor.moveUp(),
                     },
                    {'text': 'Line Down',
                     'shortcut': 'Meta+Ctrl+Down',
                     'callback': lambda editor: editor.moveDown(),
                     },
                    {'text': 'Column Left',
                     'shortcut': 'Meta+Ctrl+Left',
                     'callback': lambda editor: editor.moveLeft(),
                     },
                    {'text': 'Column Right',
                     'shortcut': 'Meta+Ctrl+Right',
                     'callback': lambda editor: editor.moveRight(),
                     }  
                  ]},
                '-',
                {'text': 'Select Bundle Item',
                 'shortcut': 'Meta+Ctrl+T',
                 'callback': cls.on_actionSelectBundleItem_triggered,
                 },
                {'text': 'Execute Line/Selection',
                 'callback': lambda editor: editor.executeCommand(),
                 }
            ]}
        navigation = {
            'name': 'navigation',
            'text': 'Navigation',
            'items': [
                "-",
                {'text': 'Toggle Bookmark',
                 'callback': cls.toggleBookmark,
                 'shortcut': 'Meta+F12',
                 },
                {'text': 'Next Bookmark',
                 'callback': cls.bookmarkNext,
                 'shortcut': 'Meta+Alt+F12',
                 },
                {'text': 'Previous Bookmark',
                 'callback': cls.bookmarkPrevious,
                 'shortcut': 'Meta+Shift+F12',
                 },
                {'text': 'Remove All Bookmarks',
                 'callback': cls.removeAllBookmarks,
                 'shortcut': 'Meta+Ctrl+F12',
                 },
                "-",
                {'text': 'Go To &Symbol',
                 'callback': cls.on_actionGoToSymbol_triggered,
                 'shortcut': 'Meta+Ctrl+Shift+O',
                 },
                {'text': 'Go To &Bookmark',
                 'callback': cls.on_actionGoToBookmark_triggered,
                 'shortcut': 'Meta+Ctrl+Shift+B',
                 }
            ]}
        # TODO Hacerlo una lista
        menuContributions = { "edit": edit, "view": view , "text": text, "navigation": navigation}
        return menuContributions
    
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.theme import ThemeSettingsWidget
        from prymatex.gui.settings.editor import EditorSettingsWidget
        from prymatex.gui.settings.edit import EditSettingsWidget
        from prymatex.gui.settings.addons import AddonsSettingsWidgetFactory
        return [ EditorSettingsWidget, ThemeSettingsWidget, EditSettingsWidget, AddonsSettingsWidgetFactory("editor") ]


    # ------------------ Menu Actions
    def on_actionShowTabsAndSpaces_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.ShowTabsAndSpaces
        else:
            flags = self.getFlags() & ~self.ShowTabsAndSpaces
        self.setFlags(flags)


    def on_actionShowLineAndParagraphs_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.ShowLineAndParagraphs
        else:
            flags = self.getFlags() & ~self.ShowLineAndParagraphs
        self.setFlags(flags)


    def on_actionWordWrap_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.WordWrap
        else:
            flags = self.getFlags() & ~self.WordWrap
        self.setFlags(flags)


    def on_actionHighlightCurrentLine_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.HighlightCurrentLine
        else:
            flags = self.getFlags() & ~self.HighlightCurrentLine
        self.setFlags(flags)


    def on_actionMarginLine_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.MarginLine
        else:
            flags = self.getFlags() & ~self.MarginLine
        self.setFlags(flags)


    def on_actionIndentGuide_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.IndentGuide
        else:
            flags = self.getFlags() & ~self.IndentGuide
        self.setFlags(flags)


    def on_actionSelectBundleItem_triggered(self):
        item = self.selectorDialog.select(self.bundleItemSelectableModel, title=_("Select Bundle Item"))

        # Select one?
        if item is not None:
            self.insertBundleItem(item['data'])

    
    def on_actionGoToSymbol_triggered(self):
        item = self.selectorDialog.select(self.symbolSelectableModel, title = _("Select Symbol"))
        if item is not None:
            self.goToBlock(item['data'])


    def on_actionGoToBookmark_triggered(self):
        item = self.selectorDialog.select(self.bookmarkSelectableModel, title=_("Select Bookmark"))
        if item is not None:
            self.goToBlock(item['data'])


    # ---------------------- Navigation API
    def restoreLocationMemento(self, memento):
        self.setTextCursor(memento)
        
    def on_document_undoCommandAdded(self):
        cursor = self.textCursor()
        if not (cursor.atEnd() or cursor.atStart()):
            self.saveLocationMemento(self.newCursorAtPosition(cursor.position() - 1))
    

    # ----------------- Drag and Drop
    def dragEnterEvent(self, event):
        self.setFocus(QtCore.Qt.MouseFocusReason)
        mimeData = event.mimeData()
        if mimeData.hasUrls() or mimeData.hasText():
            event.accept()
    
    def dragMoveEvent(self, event):
        cursor = self.cursorForPosition(event.pos())
        self.setTextCursor(cursor)
    
    def dropEvent(self, event):
        """When a url or text is dropped"""
        #mimeData = event.mimeData()
        if event.mimeData().hasUrls():
            files = map(lambda url: url.toLocalFile(), event.mimeData().urls())
            for file in files:                
                items = self.application.supportManager.getFileExtensionItem(file, self.scope())
                if items:
                    item = items[0]
                    env = { 
                            #relative path of the file dropped (relative to the document directory, which is also set as the current directory).
                            'TM_DROPPED_FILE': file,
                            #the absolute path of the file dropped.
                            'TM_DROPPED_FILEPATH': file,
                            #the modifier keys which were held down when the file got dropped.
                            #This is a bitwise OR in the form: SHIFT|CONTROL|OPTION|COMMAND (in case all modifiers were down).
                            'TM_MODIFIER_FLAGS': file
                    }
                    self.insertBundleItem(item, environment = env)
                else:
                    self.application.openFile(file)
        elif event.mimeData().hasText():
            self.textCursor().insertText(event.mimeData().text())
        
