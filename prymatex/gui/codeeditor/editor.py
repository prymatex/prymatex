#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
from bisect import bisect

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseEditor
from prymatex.widgets.texteditor import TextEditWidget

from prymatex import resources
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core import exceptions
from prymatex.qt.helpers.menus import extend_menu, update_menu
from prymatex.models.support import BundleItemTreeNode
from prymatex.gui.codeeditor.addons import CodeEditorAddon
from prymatex.gui.codeeditor.sidebar import CodeEditorSideBar, SideBarWidgetAddon
from prymatex.gui.codeeditor.processors import PMXCommandProcessor, PMXSnippetProcessor, PMXMacroProcessor
from prymatex.gui.codeeditor.modes import PMXMultiCursorEditorMode, PMXCompleterEditorMode, PMXSnippetEditorMode
from prymatex.gui.codeeditor.highlighter import PMXSyntaxHighlighter
from prymatex.gui.codeeditor.folding import PMXEditorFolding
from prymatex.gui.codeeditor.models import PMXSymbolListModel, PMXBookmarkListModel, PMXAlreadyTypedWords

from prymatex.support import PMXSnippet, PMXMacro, PMXCommand, PMXDragCommand, PMXSyntax, PMXPreferenceSettings

from prymatex.utils import coroutines
from prymatex.utils import text
from prymatex.utils.i18n import ugettext as _
from prymatex.utils.decorators.helpers import printtime

class CodeEditor(TextEditWidget, PMXBaseEditor):
    #=======================================================================
    # Scope groups
    #=======================================================================
    SORTED_GROUPS = [   "keyword", "entity", "meta", "variable", "markup", 
                        "support", "storage", "constant", "string", "comment", "invalid" ]

    # Aca vamos a guardar los scopes de los editores, quiza esto pueda ser un objeto factory,
    # por ahora la fabricacion la hace el editor en el factory method flyweightScopeFactory
    SCOPES = {}
        
    #=======================================================================
    # Signals
    #=======================================================================
    syntaxChanged = QtCore.pyqtSignal(object)
    syntaxReady = QtCore.pyqtSignal(object)
    themeChanged = QtCore.pyqtSignal()
    fontChanged = QtCore.pyqtSignal()
    modeChanged = QtCore.pyqtSignal()
    blocksRemoved = QtCore.pyqtSignal(QtGui.QTextBlock, int)
    blocksAdded = QtCore.pyqtSignal(QtGui.QTextBlock, int)
    extraSelectionChanged = QtCore.pyqtSignal()
    
    afterOpen = QtCore.pyqtSignal()
    afterSave = QtCore.pyqtSignal()
    afterClose = QtCore.pyqtSignal()
    afterReload = QtCore.pyqtSignal()
    beforeOpen = QtCore.pyqtSignal()
    beforeSave = QtCore.pyqtSignal()
    beforeClose = QtCore.pyqtSignal()
    beforeReload = QtCore.pyqtSignal()

    #================================================================
    # Regular expresions
    #================================================================
    #TODO: Ver que pasa con [A-Za-z_]+ en lugar de [A-Za-z_]*
    RE_WORD = re.compile(r"[A-Za-z_]*")
    
    #================================================================
    # Selection types
    #================================================================
    SelectWord = QtGui.QTextCursor.WordUnderCursor #0
    SelectLine = QtGui.QTextCursor.LineUnderCursor #1
    SelectParagraph = QtGui.QTextCursor.BlockUnderCursor #2 este no es un paragraph pero no importa
    SelectAll = QtGui.QTextCursor.Document #3
    SelectEnclosingBrackets = 4
    SelectCurrentScope = 5
    
    #================================================================
    # Move types
    #================================================================
    MoveLineUp = QtGui.QTextCursor.Up
    MoveLineDown = QtGui.QTextCursor.Down
    MoveColumnLeft = QtGui.QTextCursor.Left
    MoveColumnRight = QtGui.QTextCursor.Right
    
    #================================================================
    # Convert types
    #================================================================
    CONVERTERS = [  text.upper_case, 
                    text.lower_case, 
                    text.title_case,
                    text.opposite_case,
                    text.spaces_to_tabs,
                    text.tabs_to_spaces,
                    text.transpose
    ]
    ConvertToUppercase = 0
    ConvertToLowercase = 1
    ConvertToTitlecase = 2
    ConvertToOppositeCase = 3
    ConvertSpacesToTabs = 4
    ConvertTabsToSpaces = 5
    ConvertTranspose = 6

    #================================================================
    # Editor Flags
    #================================================================
    ShowTabsAndSpaces     = 1<<0
    ShowLineAndParagraphs = 1<<1
    ShowBookmarks         = 1<<2
    ShowLineNumbers       = 1<<3
    ShowFolding           = 1<<4
    WordWrap              = 1<<5
    MarginLine            = 1<<6
    IndentGuide           = 1<<7
    
    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'CodeEditor'
    
    defaultSyntax = pmxConfigPorperty(default = "3130E4FA-B10E-11D9-9F75-000D93589AF6", tm_name = 'OakDefaultLanguage')
    tabStopSoft = pmxConfigPorperty(default = True)
    
    @pmxConfigPorperty(default = 4)
    def tabStopSize(self, size):
        self.setTabStopWidth(size * 9)
    
    @pmxConfigPorperty(default = QtGui.QFont("Monospace", 9))
    def font(self, font):
        font.setStyleHint(QtGui.QFont.Monospace)
        font.setStyleStrategy(QtGui.QFont.ForceIntegerMetrics)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.document().setDefaultFont(font)
        #print QtGui.QFontMetrics(self.document().defaultFont()).width(" ")
        #print QtGui.QFontMetrics(self.document().defaultFont()).width("i")
        #print QtGui.QFontMetrics(self.document().defaultFont()).width("w")
        #print QtGui.QFontMetrics(self.document().defaultFont()).width("#")
        self.fontChanged.emit()
    
    @pmxConfigPorperty(default = '766026CB-703D-4610-B070-8DE07D967C5F', tm_name = 'OakThemeManagerSelectedTheme')
    def theme(self, uuid):
        theme = self.application.supportManager.getTheme(uuid)

        self.syntaxHighlighter.setTheme(theme)
        self.colours = theme.settings
        
        #Set color for QPlainTextEdit
        appStyle = """QPlainTextEdit {background-color: %s;
        color: %s;
        selection-background-color: %s; }""" % (self.colours['background'].name(), self.colours['foreground'].name(), self.colours['selection'].name())
        self.setStyleSheet(appStyle)
        self.themeChanged.emit()

    @pmxConfigPorperty(default = ShowLineNumbers)
    def defaultFlags(self, flags):
        self.setFlags(flags)

    #================================================================
    # INIT
    #================================================================
    def __init__(self, parent = None):
        TextEditWidget.__init__(self, parent)
        PMXBaseEditor.__init__(self)

        #Sidebars
        self.leftBar = CodeEditorSideBar(self)
        self.rightBar = CodeEditorSideBar(self)
        #self.updateViewportMargins()

        #Models
        self.bookmarkListModel = PMXBookmarkListModel(self)
        self.symbolListModel = PMXSymbolListModel(self)
        self.alreadyTypedWords = PMXAlreadyTypedWords(self)
        
        #Folding
        self.folding = PMXEditorFolding(self)
        
        #Processors
        self.commandProcessor = PMXCommandProcessor(self)
        self.macroProcessor = PMXMacroProcessor(self)
        self.snippetProcessor = PMXSnippetProcessor(self)

        #Highlighter
        self.syntaxHighlighter = PMXSyntaxHighlighter(self)
        #self.extraSelectionCursors = MultiListsDict()
        
        #Modes
        self.multiCursorMode = PMXMultiCursorEditorMode(self)
        self.completerMode = PMXCompleterEditorMode(self)
        self.snippetMode = PMXSnippetEditorMode(self)
        
        self.braces = []
        #Current braces for cursor position (leftBrace * rightBrace, oppositeLeftBrace, oppositeRightBrace) 
        # * the cursor is allways here>
        self._currentBraces = (None, None, None, None)
        
        #Block Count
        self.lastBlockCount = self.document().blockCount()

        #Connect context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showEditorContextMenu)

        self.completerTask = self.application.scheduler.idleTask()
        
        #Cursor history
        #self._cursorHistory, self._cursorHistoryIndex = [], 0
        
        #Esta señal es especial porque es emitida en el setFont por los settings
        self.fontChanged.connect(self.on_fontChanged)
        #Basic setup
        #self.setCenterOnScroll(True)
    
    # Connect Signals
    def connectSignals(self):
        self.rightBar.updateRequest.connect(self.updateViewportMargins)
        self.leftBar.updateRequest.connect(self.updateViewportMargins)
        
        self.syntaxHighlighter.highlightReady.connect(self.on_highlightReady)
        self.blockCountChanged.connect(self.on_blockCountChanged)
        self.updateRequest.connect(self.updateSideBars)
        self.cursorPositionChanged.connect(self.on_cursorPositionChanged)
        self.modificationChanged.connect(self.on_modificationChanged)
        self.syntaxChanged.connect(self.showSyntaxMessage)
        self.themeChanged.connect(self.highlightEditor)
        
        self.document().undoCommandAdded.connect(self.on_document_undoCommandAdded)

    def initialize(self, mainWindow):
        PMXBaseEditor.initialize(self, mainWindow)
        self.connectSignals()
        #Load Default Syntax
        syntax = self.application.supportManager.getBundleItem(self.defaultSyntax)
        self.setSyntax(syntax)
    
    def addAddon(self, addon):
        PMXBaseEditor.addAddon(self, addon)
        if isinstance(addon, SideBarWidgetAddon):
            self.addSideBarWidget(addon)

    def addSideBarWidget(self, widget):
        if widget.ALIGNMENT == QtCore.Qt.AlignRight:
            self.rightBar.addWidget(widget)
        else:
            self.leftBar.addWidget(widget)
        
    def showSyntaxMessage(self, syntax):
        self.showMessage("Syntax changed to <b>%s</b>" % syntax.name)
    
    def showMessage(self, *largs, **kwargs):
        self.mainWindow.showMessage(*largs, **kwargs)
        
    #================================================================
    # Update editor status, called from Highlighter
    #================================================================
    def updateIndent(self, block, userData, indent):
        self.logger.debug("Update Block Indent")
    
    def updateFolding(self, block, userData, foldingMark):
        self.logger.debug("Update Block Folding")
        if block.userData().foldingMark == None:
            self.folding.removeFoldingBlock(block)
        else:
            self.folding.addFoldingBlock(block)
        
    def updateSymbol(self, block, userData, symbol):
        self.logger.debug("Update Block Symbol")
        if block.userData().symbol is None:
            self.symbolListModel.removeSymbolBlock(block)
        else:
            self.symbolListModel.addSymbolBlock(block)
        
    def updateWords(self, block, userData, words):
        self.logger.debug("Update Words")
        #Quitar el block de las palabras anteriores
        self.alreadyTypedWords.removeWordsBlock(block, filter(lambda word: word not in words, userData.words))
        
        #Agregar las palabras nuevas
        self.alreadyTypedWords.addWordsBlock(block, filter(lambda word: word not in userData.words, words))
        userData.words = words
        
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
    
    def on_cursorPositionChanged(self):
        #El cursor se movio es hora de:
        self.setCurrentBraces()
        self.highlightEditor()

    def on_highlightReady(self):
        self.folding.indentSensitive = self.syntax().indentSensitive
        self.setBraces(self.syntax().scopeName)
        self.syntaxReady.emit(self.syntax())
        
    def on_fontChanged(self):
        font_metrics = QtGui.QFontMetrics(self.document().defaultFont())
        self.pos_margin = font_metrics.width("#") * 80
        self.setTabStopWidth(self.tabStopSize * font_metrics.width("#"))

    #=======================================================================
    # Base Editor Interface
    #=======================================================================
    @classmethod
    def acceptFile(cls, filePath, mimetype):
        return re.compile("text/.*").match(mimetype) is not None

    def open(self, filePath):
        """ Custom open for large files, use coroutines """
        self.application.fileManager.openFile(filePath)
        content = self.application.fileManager.readFile(filePath)
        self.setFilePath(filePath)
        self.beforeOpen.emit()
        self.setPlainText(content)
        self.afterOpen.emit()
        
    def save(self, filePath):
        self.beforeSave.emit()
        PMXBaseEditor.save(self, filePath)
        self.afterSave.emit()

    def close(self):
        self.beforeClose.emit()
        PMXBaseEditor.close(self)
        self.afterClose.emit()
    
    def reload(self):
        self.beforeReload.emit()
        content = self.application.fileManager.readFile(self.filePath)
        self.updatePlainText(content)
        PMXBaseEditor.reload(self)
        self.afterReload.emit()

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
        if self.getSyntax() is not None:
            return [ "%s (%s)" % (self.getSyntax().bundle.name, " ".join(map(lambda ft: "*." + ft, self.getSyntax().fileTypes))) ]
        return PMXBaseEditor.fileFilters(self)
    
    def setCursorPosition(self, position):
        cursor = self.textCursor()
        blockPosition = self.document().findBlockByNumber(position[0]).position()
        cursor.setPosition(blockPosition + position[1])
        self.setTextCursor(cursor)

    def cursorPosition(self):
        cursor = self.textCursor()
        return (cursor.block().blockNumber(), cursor.columnNumber())

    #=======================================================================
    # Scopes
    #=======================================================================
    @classmethod
    def flyweightScopeFactory(cls, scopeStack):
        scopeName = " ".join(scopeStack)
        scopeHash = hash(scopeName)
        if scopeHash not in cls.SCOPES:
            scopeData = cls.SCOPES.setdefault(scopeHash, {
                "name": scopeName,
                "settings": cls.application.supportManager.getPreferenceSettings(scopeName),
                "group": PMXSyntax.findGroup(scopeStack[::-1])
            })
            return scopeHash, scopeData["group"]
        else:
            return scopeHash, cls.SCOPES[scopeHash]["group"]
    
    #=======================================================================
    # Obteniendo datos del editor
    #=======================================================================
    def tabKeyBehavior(self):
        return self.tabStopSoft and unicode(' ') * self.tabStopSize or unicode('	')

    def preferenceSettings(self, scopeOrHash):
        scopeHash = scopeOrHash if isinstance(scopeOrHash, int) else hash(scopeOrHash)
        if scopeHash in self.SCOPES:
            return self.SCOPES[scopeHash]["settings"]
    
    def wordUnderCursor(self):
        """ Esto 'no' es lo mismo que currentWord """
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        return cursor.selectedText(), cursor.selectionStart(), cursor.selectionEnd()

    def scopeName(self, scopeHash):
        return self.SCOPES[scopeHash]["name"]

    def scope(self, cursor):
        userData = cursor.block().userData()
        return self.syntax().scopeName if userData is None else self.scopeName(userData.scopeAtPosition(cursor.columnNumber()))

    def currentPreferenceSettings(self):
        return self.preferenceSettings(self.currentScope())
        
    def currentScope(self):
        return self.scope(self.textCursor())

    def currentWord(self, direction = "both", search = True):
        return self.word(cursor = self.textCursor(), direction = direction, search = search)
        
    def word(self, cursor = None, pattern = RE_WORD, direction = "both", search = True):
        cursor = cursor or self.textCursor()
        line = cursor.block().text()
        position = cursor.position()
        columnNumber = cursor.columnNumber()
        #Get text before and after the cursor position.
        first_part, last_part = line[:columnNumber][::-1], line[columnNumber:]
        
        #Try left word
        lword = rword = ""
        m = pattern.match(first_part)
        if m and direction in ("left", "both"):
            lword = m.group(0)[::-1]
        #Try right word
        m = pattern.match(last_part)
        if m and direction in ("right", "both"):
            rword = m.group(0)
        
        if lword or rword:
            return lword + rword, position - len(lword), position + len(rword)
        
        if not search: 
            return "", position, position

        lword = rword = ""
        #Search left word
        for i in range(len(first_part)):
            lword += first_part[i]
            m = pattern.search(first_part[i + 1:])
            if m.group(0):
                lword += m.group(0)
                break
        lword = lword[::-1]
        #Search right word
        for i in range(len(last_part)):
            rword += last_part[i]
            m = pattern.search(last_part[i:])
            if m.group(0):
                rword += m.group(0)
                break
        lword = lword.lstrip()
        rword = rword.rstrip()
        return lword + rword, position - len(lword), position + len(rword)
    
    def getSelectionBlockStartEnd(self, cursor = None):
        cursor = cursor or self.textCursor()
        start, end = cursor.selectionStart(), cursor.selectionEnd()
        if start > end:
            return self.document().findBlock(end), self.document().findBlock(start)
        else:
            return self.document().findBlock(start), self.document().findBlock(end)

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

    # Syntax
    def getSyntax(self):
        return self.syntaxHighlighter.syntax
        
    def syntax(self):
        return self.syntaxHighlighter.syntax
        
    def setSyntax(self, syntax):
        if self.syntaxHighlighter.syntax != syntax:
            self.syntaxHighlighter.setSyntax(syntax)
            self.flyweightScopeFactory([ syntax.scopeName ])
            self.syntaxChanged.emit(syntax)

    # Move text
    def moveText(self, moveType):
        #Solo si tiene seleccion puede mover derecha y izquierda
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            if (moveType == QtGui.QTextCursor.Left and cursor.selectionStart() == 0) or (moveType == QtGui.QTextCursor.Right and cursor.selectionEnd() == self.document().characterCount()):
                return
            openRight = cursor.position() == cursor.selectionEnd()
            text = cursor.selectedText()
            cursor.removeSelectedText()
            cursor.movePosition(moveType)
            start = cursor.position()
            cursor.insertText(text)
            end = cursor.position()
            if openRight:
                cursor.setPosition(start)
                cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            else:
                cursor.setPosition(end)
                cursor.setPosition(start, QtGui.QTextCursor.KeepAnchor)
        elif moveType in [QtGui.QTextCursor.Up, QtGui.QTextCursor.Down]:
            if (moveType == QtGui.QTextCursor.Up and cursor.block() == cursor.document().firstBlock()) or (moveType == QtGui.QTextCursor.Down and cursor.block() == cursor.document().lastBlock()):
                return
            column = cursor.columnNumber()
            cursor.select(QtGui.QTextCursor.LineUnderCursor)
            text1 = cursor.selectedText()
            cursor2 = QtGui.QTextCursor(cursor)
            otherBlock = cursor.block().next() if moveType == QtGui.QTextCursor.Down else cursor.block().previous()
            cursor2.setPosition(otherBlock.position())
            cursor2.select(QtGui.QTextCursor.LineUnderCursor)
            text2 = cursor2.selectedText()
            cursor.insertText(text2)
            cursor2.insertText(text1)
            cursor.setPosition(otherBlock.position() + column)
        cursor.endEditBlock()
        self.setTextCursor(cursor)
    
    # Convert Text
    def convertText(self, convertType):
        cursor = self.textCursor()
        convertFunction = self.CONVERTERS[convertType]
        if convertType == self.ConvertSpacesToTabs:
            self.replaceSpacesForTabs()
        elif convertType == self.ConvertTabsToSpaces:
            self.replaceTabsForSpaces()
        else:
            if not cursor.hasSelection():
                word, start, end = self.currentWord()
                position = cursor.position()
                cursor.setPosition(start)
                cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
                cursor.insertText(convertFunction(word))
                cursor.setPosition(position)
            else:
                openRight = cursor.position() == cursor.selectionEnd()
                start, end = cursor.selectionStart(), cursor.selectionEnd()
                cursor.insertText(convertFunction(cursor.selectedText()))
                if openRight:
                    cursor.setPosition(start)
                    cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
                else:
                    cursor.setPosition(end)
                    cursor.setPosition(start, QtGui.QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)
        
    #=======================================================================
    # SideBars
    #=======================================================================
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
    
    #=======================================================================
    # Braces
    #=======================================================================
    def setBraces(self, scope):
        settings = self.preferenceSettings(scope)
        self.braces = settings.smartTypingPairs
        #self.braces = filter(lambda pair: pair[0] != pair[1], settings.smartTypingPairs)
        
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
        
    # -------------------- Highlight Editor
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
        self.setExtraSelectionCursors("line", [ cursor ])
        self.setExtraSelectionCursors("brace", filter(lambda cursor: cursor is not None, list(self._currentBraces)))
        for addon in self.addons:
            if isinstance(addon, CodeEditorAddon):
                self.updateExtraSelectionCursors(addon.extraSelectionCursors())
        self.updateExtraSelections()
        # Todo esta señal mandarla desde el updateExtraSelections
        self.extraSelectionChanged.emit()

    def select(self, selection):
        cursor = self.textCursor()
        if selection in [self.SelectLine, self.SelectParagraph, self.SelectAll]:
            #Handle by editor
            cursor.select(selection)
        elif selection == self.SelectWord:
            word, start, end = self.currentWord()
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        elif selection == self.SelectEnclosingBrackets:
            flags = QtGui.QTextDocument.FindFlags()
            flags |= QtGui.QTextDocument.FindBackward
            foundCursors = map(lambda (openBrace, closeBrace): (self.document().find(openBrace, cursor.selectionStart(), flags), closeBrace), self.braces)
            openCursor = reduce(lambda c1, c2: (not c1[0].isNull() and c1[0].selectionEnd() > c2[0].selectionEnd()) and c1 or c2, foundCursors)
            if not openCursor[0].isNull():
                closeCursor = self.findTypingPair(openCursor[0].selectedText(), openCursor[1], openCursor[0])
                if openCursor[0].selectionEnd() <= cursor.selectionStart() <= closeCursor.selectionStart():
                    cursor.setPosition(openCursor[0].selectionEnd())
                    cursor.setPosition(closeCursor.selectionStart(), QtGui.QTextCursor.KeepAnchor)
        elif selection == self.SelectCurrentScope:
            block = cursor.block()
            beginPosition = block.position()
            # TODO Todo lo que implique userData centrarlo en una API en la instancia de cada editor
            (start, end), scope = block.userData().scopeRange(cursor.columnNumber())
            if scope is not None:
                cursor.setPosition(beginPosition + start)
                cursor.setPosition(beginPosition + end, QtGui.QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

    #=======================================================================
    # QPlainTextEdit Events
    #=======================================================================
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
            positionY = round(blockGeometry.top())
            if block.isVisible():
                
                user_data = block.userData()
                if self.folding.isStart(self.folding.getFoldingMark(block)) and user_data.folded:
                    painter.drawPixmap(font_metrics.width(block.text()) + offset.x() + 5,
                        positionY + font_metrics.ascent() + font_metrics.descent() - resources.getImage("foldingellipsis").height(),
                        resources.getImage("foldingellipsis"))
                if self.showIndentGuide:
                    blockPattern = block
                    while blockPattern.isValid() and blockPattern.userData() and blockPattern.userData().blank:
                        blockPattern = blockPattern.next()
                    if blockPattern.isValid() and blockPattern.userData():
                        indentPattern = blockPattern.userData().indent
                        for s in range(0, (len(indentPattern) / len(self.tabKeyBehavior()))):
                            positionX = (font_metrics.width("#") * self.tabStopSize * s) + font_metrics.width("#") + offset.x()
                            painter.drawLine(positionX, positionY, positionX, positionY + font_metrics.height())
                
            block = block.next()

        if self.showMarginLine:
            painter.drawLine(self.pos_margin + offset.x(), 0, self.pos_margin + offset.x(), self.viewport().height())

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

    #=======================================================================
    # Mouse Events
    #=======================================================================
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

    #=======================================================================
    # Keyboard Events
    #=======================================================================
    def runKeyHelper(self, event):
        #No tengo modo activo, intento con los helpers
        #Obtener key, scope y cursor
        scope = self.currentScope()
        cursor = self.textCursor()
        for helper in self.findHelpers(event.key()):
            #Buscar Entre los helpers
            if helper.accept(event, cursor, scope):
                helper.execute(event, cursor, scope)
                return True
        return False

    def keyPressEvent(self, event):
        """
        This method is called whenever a key is pressed. The key code is stored in event.key()
        http://manual.macromates.com/en/working_with_text
        """
        
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

    #==========================================================================
    # Insert API
    #==========================================================================
    def updatePlainText(self, text):
        # delta update Muejejejejejejejejej
        import difflib
        
        def perform_action(code, cursor, text=""):
            def _nop():
                pass
            def _action():
                cursor.insertText(text)
            return _action if code in ["insert", "replace", "delete"] else _nop
        
        sequenceMatcher = difflib.SequenceMatcher(None, self.toPlainText(), text)
        opcodes = sequenceMatcher.get_opcodes()
        
        actions = map(lambda code: perform_action(code[0], self.newCursorAtPosition(code[1], code[2]), text[code[3]:code[4]]), opcodes)
        
        cursor = self.textCursor()
        
        cursor.beginEditBlock()
        map(lambda action: action(), actions)
        cursor.endEditBlock()
        
        self.ensureCursorVisible()

    def insertNewLine(self, cursor = None):
        cursor = cursor or self.textCursor()
        block = cursor.block()
        userData = cursor.block().userData()
        settings = self.preferenceSettings(self.scope(cursor))
        indentMarks = settings.indent(block.text()[:cursor.columnNumber()])
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
            indent = userData.indent[:len(self.tabKeyBehavior())]
        else:
            self.logger.debug("Preserve indent")
            indent = block.userData().indent[:cursor.columnNumber()]
        cursor.insertText("\n%s" % indent)
        self.ensureCursorVisible()

    #==========================================================================
    # Bundle Items
    #==========================================================================
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
        command = self.application.supportManager.buildAdHocCommand(commandScript, self.getSyntax().bundle, commandInput, commandOutput)
        self.insertBundleItem(command)
    
    def environmentVariables(self):
        environment = PMXBaseEditor.environmentVariables(self)
        cursor = self.textCursor()
        block = cursor.block()
        line = block.text()
        scope = self.currentScope()
        preferences = self.preferenceSettings(scope)
        current_word, start, end = self.currentWord()
        environment.update({
                'TM_CURRENT_LINE': line,
                'TM_LINE_INDEX': cursor.columnNumber(),
                'TM_LINE_NUMBER': block.blockNumber() + 1,
                'TM_COLUMN_NUMBER': cursor.columnNumber() + 1,
                'TM_SCOPE': scope,
                'TM_MODE': self.getSyntax().name,
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
            start, end = self.getSelectionBlockStartEnd()
            environment['TM_INPUT_START_COLUMN'] = cursor.selectionStart() - start.position() + 1
            environment['TM_INPUT_START_LINE'] = start.blockNumber() + 1
            environment['TM_INPUT_START_LINE_INDEX'] = cursor.selectionStart() - start.position()

        environment.update(preferences.shellVariables)
        return environment
        
    #==========================================================================
    # Completer
    #==========================================================================
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
        settings = self.currentPreferenceSettings()
        if not self.completerMode.hasSource("default"):
            def on_suggestionsReady(suggestions):
                if bool(suggestions):
                    self.completerMode.setSuggestions(suggestions, "default")
            self.defaultCompletion(settings, on_suggestionsReady)
        else:
            self.completerMode.switch()

    def runCompleter(self):
        settings = self.currentPreferenceSettings()
        def on_suggestionsReady(suggestions):
             if bool(suggestions):
                self.showCompleter(suggestions)
        self.defaultCompletion(settings, on_suggestionsReady)

    def defaultCompletion(self, settings, callback):
        if not self.completerTask.isRunning():
            self.completerTask = self.application.scheduler.newTask(self.completionSuggestions(settings = settings))
            def on_completerTaskReady(callback):
                def completerTaskReady(result):
                    callback(result.value)
                return completerTaskReady
            #En una clausura
            self.completerTask.done.connect(on_completerTaskReady(callback))

    def completionSuggestions(self, cursor = None, scope = None, settings = None):
        cursor = cursor or self.textCursor()
        scope = scope or self.scope(cursor)
        settings = settings or self.preferenceSettings(scope)
        
        #An array of additional candidates when cycling through completion candidates from the current document.
        completions = settings.completions[:]

        #A shell command (string) which should return a list of candidates to complete the current word (obtained via the TM_CURRENT_WORD variable).
        if settings.completionCommand:
            def commandCallback(context):
                print unicode(context)
            command = self.application.supportManager.buildAdHocCommand(settings.completionCommand, self.getSyntax().bundle, commandInput="document")
            self.commandProcessor.configure({ "asynchronous": False })
            command.executeCallback(self.commandProcessor, commandCallback)
            
        #A tab tigger completion
        tabTriggers = self.application.supportManager.getAllTabTiggerItemsByScope(scope)
        
        typedWords = self.alreadyTypedWords.typedWords(cursor.block())
        
        #Lo ponemos en la mezcladora
        suggestions = tabTriggers + map(lambda word: { "display": word, "image": "scope-root-keyword" }, completions)
        for group in CodeEditor.SORTED_GROUPS:
            newWords = filter(lambda word: word not in completions, typedWords.pop(group, []))
            suggestions += map(lambda word: { "display": word, "image": "scope-root-%s" % group }, newWords)
            completions += newWords
            yield
        
        for words in typedWords.values():
            newWords = filter(lambda word: word not in completions, words)
            suggestions += map(lambda word: { "display": word, "image": "scope-root-invalid" }, newWords)
            completions += newWords
            yield

        yield coroutines.Return(suggestions)

    #==========================================================================
    # Folding
    #==========================================================================
    def codeFoldingFold(self, block):
        self._fold(block)
        # self.update()
        # self.sidebar.update()

    def codeFoldingUnfold(self, block):
        self._unfold(block)
        # self.update()
        # self.sidebar.update()
        
    def _fold(self, block):
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

    def _unfold(self, block):
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

    #==========================================================================
    # Find and Replace
    #==========================================================================    
    def findTypingPair(self, b1, b2, cursor, backward = False):
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
            #Balanceo solo si son distintos
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
            if not c2.isNull():
                return c2
        else:
            if not c2.isNull() and c2.block() == cursor.block():
                #Ahora balanceamos usando el texto del block
                block = cursor.block()
                text = block.text()
                positionStart = cursor.selectionEnd() if backward else cursor.selectionStart()
                positionStart -= block.position()
                positionEnd = c2.selectionEnd() if c2 > cursor else c2.selectionStart()
                positionEnd -= block.position()
                if text[:positionStart].count(b2) % 2 == 0 and text[positionEnd:].count(b2) % 2 == 0:
                    return c2

    def findMatchCursor(self, match, flags, findNext = False, cursor = None, cyclicFind = False):
        cursor = cursor or self.textCursor()
        if not findNext and cursor.hasSelection():
            cursor.setPosition(cursor.selectionStart())
        cursor = self.document().find(match, cursor, flags)
        if cursor.isNull() and cyclicFind:
            cursor = self.textCursor()
            if flags & QtGui.QTextDocument.FindBackward:
                cursor.movePosition(QtGui.QTextCursor.End)
            else:
                cursor.movePosition(QtGui.QTextCursor.Start)
            cursor = self.document().find(match, cursor, flags)
        if not cursor.isNull():
            return cursor

    def findMatch(self, match, flags, findNext = False):
        cursor = self.findMatchCursor(match, flags, findNext)
        if cursor is not None:
            self.setTextCursor(cursor)
            return True
        return False
    
    def findAll(self, match, flags):
        cursors = []
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        cursor = self.findMatchCursor(match, flags, cursor = cursor, cyclicFind = False)
        while cursor is not None:
            cursors.append(cursor)
            cursor = QtGui.QTextCursor(cursor)
            cursor.setPosition(cursor.selectionEnd())
            cursor = self.findMatchCursor(match, flags, cursor = cursor, cyclicFind = False)
        return cursors
            
    def replaceMatch(self, match, text, flags, all = False):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        replaced = 0
        while True:
            if len(match) == 0 and len(text) == 0:
                break
            elif match == ' ' * len(match) and text == ' ' * len(text):
                break
            else:
                findCursor = self.findMatchCursor(match, flags, cyclicFind = True)
            if not findCursor: break
            if isinstance(match, QtCore.QRegExp):
                findCursor.insertText(re.sub(match.pattern(), text, cursor.selectedText()))
            else:
                findCursor.insertText(text)
            replaced += 1
            if not all: break
        cursor.endEditBlock()
        return replaced
    
    def replaceTabsForSpaces(self):
        match = "\t"
        self.replaceMatch(match, " " * self.tabStopSize, QtGui.QTextDocument.FindFlags(), True)
        
    def replaceSpacesForTabs(self):
        match = self.tabKeyBehavior()
        self.replaceMatch(match, "\t", QtGui.QTextDocument.FindFlags(), True)
        
    #==========================================================================
    # Bookmarks and gotos
    #==========================================================================    
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

    #===========================================================================
    # Zoom
    #===========================================================================
    FONT_MAX_SIZE = 32
    FONT_MIN_SIZE = 6
    def zoomIn(self):
        font = self.font
        size = self.font.pointSize()
        if size < self.FONT_MAX_SIZE:
            size += 1
            font.setPointSize(size)
        self.font = font

    def zoomOut(self):
        font = self.font
        size = font.pointSize()
        if size > self.FONT_MIN_SIZE:
            size -= 1
            font.setPointSize(size)
        self.font = font

    #===========================================================================
    # Text Indentation
    #===========================================================================
    def findPreviousNoBlankBlock(self, block):
        """ Return previous no blank indent block """
        block = block.previous()
        while block.isValid() and block.text().strip() == "":
            block = block.previous()
        if block.isValid():
            return block
        
    def findPreviousEqualIndentBlock(self, block, indent = None):
        """ Return previous equal indent block """
        indent = indent if indent != None else block.userData().indent
        block = self.findPreviousNoBlankBlock(block)
        while block is not None and block.userData().indent > indent:
            block = self.findPreviousNoBlankBlock(block)
        if block is not None and block.userData().indent == indent:
            return block
    
    def findPreviousMoreIndentBlock(self, block, indent = None):
        """ Return previous more indent block """
        indent = indent if indent != None else block.userData().indent
        block = self.findPreviousNoBlankBlock(block)
        while block is not None and block.userData().indent <= indent:
            block = self.findPreviousNoBlankBlock(block)
        if block is not None:
            return block
    
    def findPreviousLessIndentBlock(self, block, indent = None):
        """ Return previous less indent block """
        indent = indent if indent != None else block.userData().indent
        block = self.findPreviousNoBlankBlock(block)
        while block is not None and block.userData().indent >= indent:
            block = self.findPreviousNoBlankBlock(block)
        if block is not None:
            return block

    def indentBlocks(self, cursor = None):
        """Indents text, block selections."""
        cursor = QtGui.QTextCursor(cursor or self.textCursor())
        start, end = self.getSelectionBlockStartEnd(cursor)
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
        start, end = self.getSelectionBlockStartEnd(cursor)
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
    
    #===========================================================================
    # Menus
    #===========================================================================
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
        bundleMenu = self.application.supportManager.menuForBundle(self.getSyntax().bundle)
        extend_menu(menu, [ "-", bundleMenu ])

        #Se lo pasamos a los addons
        cursor = self.cursorForPosition(point)
        items = ["-"]
        for addon in self.addons:
            if isinstance(addon, CodeEditorAddon):
                items += addon.contributeToContextMenu(cursor)
        
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
        bundleMenu = self.application.supportManager.menuForBundle(self.getSyntax().bundle)
        if bundleMenu is not None:
            menues.append(bundleMenu)
            menues.append("-")
        if self.filePath:
            menues.append({
                "text": "Copy file path",
                "icon": resources.getIcon("edit-copy"),
                "callback": lambda editor = self: QtGui.QApplication.clipboard().setText(editor.filePath)  })
        return menues
    
    # Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls, addonClasses):
        edit = {
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
            'text': '&Text',
            'items': [ 
                {'text': 'Select',
                 'items': [
                    {'text': '&Word',
                     'callback': lambda editor: editor.select(0),
                     'shortcut': 'Ctrl+Meta+W',
                     },
                    {'text': '&Line',
                     'callback': lambda editor: editor.select(1),
                     'shortcut': 'Ctrl+Meta+L',
                     },
                    {'text': '&Paragraph',
                     'callback': lambda editor: editor.select(2),
                     'shortcut': '',
                     },
                    {'text': 'Enclosing &Brackets',
                     'callback': lambda editor: editor.select(editor.SelectEnclosingBrackets),
                     'shortcut': 'Ctrl+Meta+B',
                     },
                    {'text': 'Current &Scope',
                     'callback': lambda editor: editor.select(editor.SelectCurrentScope),
                     'shortcut': 'Ctrl+Meta+S',
                     },
                    {'text': '&All',
                     'callback': lambda editor: editor.select(3),
                     'shortcut': 'Ctrl+A',
                     }    
                ]},
                {'text': 'Convert',
                 'items': [
                    {'text': 'To Uppercase',
                     'shortcut': 'Ctrl+U',
                     'callback': lambda editor: editor.convertText(editor.ConvertToUppercase),
                     },
                    {'text': 'To Lowercase',
                     'shortcut': 'Ctrl+Shift+U',
                     'callback': lambda editor: editor.convertText(editor.ConvertToLowercase),
                     },
                    {'text': 'To Titlecase',
                     'shortcut': 'Ctrl+Alt+U',
                     'callback': lambda editor: editor.convertText(editor.ConvertToTitlecase),
                     },
                    {'text': 'To Opposite Case',
                     'shortcut': 'Ctrl+G',
                     'callback': lambda editor: editor.convertText(editor.ConvertToOppositeCase),
                     }, '-',
                    {'text': 'Tab to Spaces',
                     'callback': lambda editor: editor.convertText(editor.ConvertTabsToSpaces),
                     },
                    {'text': 'Spaces to Tabs',
                     'callback': lambda editor: editor.convertText(editor.ConvertSpacesToTabs),
                     }, '-',
                    {'text': 'Transpose',
                     'shortcut': 'Ctrl+T',
                     'callback': lambda editor: editor.convertText(editor.ConvertTranspose),
                     }
                ]},
                {'text': 'Move',
                 'items': [
                    {'text': 'Line Up',
                     'shortcut': 'Meta+Ctrl+Up',
                     'callback': lambda editor: editor.moveText(editor.MoveLineUp),
                     },
                    {'text': 'Line Down',
                     'shortcut': 'Meta+Ctrl+Down',
                     'callback': lambda editor: editor.moveText(editor.MoveLineDown),
                     },
                    {'text': 'Column Left',
                     'shortcut': 'Meta+Ctrl+Left',
                     'callback': lambda editor: editor.moveText(editor.MoveColumnLeft),
                     },
                    {'text': 'Column Right',
                     'shortcut': 'Meta+Ctrl+Right',
                     'callback': lambda editor: editor.moveText(editor.MoveColumnRight),
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
        menuContributions = { "Edit": edit, "View": view , "Text": text, "Navigation": navigation}
        for addon in addonClasses:
            update_menu(menuContributions, addon.contributeToMainMenu())
        return menuContributions
    
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.themes import ThemeSettingsWidget
        from prymatex.gui.settings.editor import EditorSettingsWidget
        from prymatex.gui.settings.addons import AddonsSettingsWidgetFactory
        return [ EditorSettingsWidget, ThemeSettingsWidget, AddonsSettingsWidgetFactory("editor") ]

    #===========================================================================
    # Menu Actions
    #===========================================================================
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
    
    def on_actionShowBookmarks_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.ShowBookmarks
        else:
            flags = self.getFlags() & ~self.ShowBookmarks
        self.setFlags(flags)
    
    def on_actionShowLineNumbers_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.ShowLineNumbers
        else:
            flags = self.getFlags() & ~self.ShowLineNumbers
        self.setFlags(flags)
        
    def on_actionShowFoldings_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.ShowFolding
        else:
            flags = self.getFlags() & ~self.ShowFolding
        self.setFlags(flags)
    
    def on_actionSelectBundleItem_triggered(self):
        scope = self.currentScope()
        items = self.application.supportManager.getActionItems(scope)
        def itemsToDict(items):
            for item in items:
                yield [dict(title = item.name, image = "bundle-item-%s" % item.TYPE), dict(title = item.bundle.name), dict(title = item.trigger)]
        index = self.mainWindow.bundleSelectorDialog.select(itemsToDict(items))
        if index is not None:
            self.insertBundleItem(items[index])
            
    def on_actionGoToSymbol_triggered(self):
        #TODO: Usar el modelo
        blocks = self.symbolListModel.blocks
        def symbolToDict(blocks):
            for block in blocks:
                userData = block.userData() 
                yield [dict(title = userData.symbol, image = resources.getIcon('bulletblue'))]
        index = self.mainWindow.symbolSelectorDialog.select(symbolToDict(blocks))
        if index is not None:
            self.goToBlock(blocks[index])
        
    def on_actionGoToBookmark_triggered(self):
        blocks = self.bookmarkListModel.blocks
        def bookmarkToDict(blocks):
            for block in blocks:
                yield [dict(title = block.text(), image = resources.getIcon('bookmarkflag'))]
        index = self.mainWindow.bookmarkSelectorDialog.select(bookmarkToDict(blocks))
        if index is not None:
            self.goToBlock(blocks[index])
    
    #============================================================
    # Text Menu Actions
    #============================================================
    def on_actionExecute_triggered(self):
        self.currentEditor().executeCommand()

    def on_actionFilterThroughCommand_triggered(self):
        self.statusBar().showCommand()
    
    #===========================================================================
    # Navigation API
    #===========================================================================
    def newCursorAtPosition(self, position, anchor = None):
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(position)
        if anchor is not None:
            cursor.setPosition(anchor, QtGui.QTextCursor.KeepAnchor)
        return cursor
        
    def restoreLocationMemento(self, memento):
        self.setTextCursor(memento)
        
    def on_document_undoCommandAdded(self):
        cursor = self.textCursor()
        if not (cursor.atEnd() or cursor.atStart()):
            self.saveLocationMemento(self.newCursorAtPosition(cursor.position() - 1))
    
    #===========================================================================
    # Drag and Drop
    #===========================================================================
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
            scope = self.currentScope()
            for file in files:                
                items = self.application.supportManager.getFileExtensionItem(file, scope)
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
        
