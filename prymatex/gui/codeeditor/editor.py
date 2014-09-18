#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import re
import operator

from prymatex.qt import QtCore, QtGui, Qt

from prymatex.core import PrymatexEditor
from prymatex.widgets.texteditor import TextEditWidget

from prymatex.core.settings import ConfigurableItem
from prymatex.qt.helpers import (extend_menu, keyevent_to_keysequence)
from prymatex.models.support import BundleItemTreeNode

from .userdata import CodeEditorBlockUserData
from .addons import CodeEditorAddon
from .sidebar import CodeEditorSideBar, SideBarWidgetMixin
from .processors import (CodeEditorCommandProcessor, CodeEditorSnippetProcessor,
    CodeEditorMacroProcessor, CodeEditorSyntaxProcessor, CodeEditorThemeProcessor)
from .modes import CodeEditorBaseMode

from .highlighter import CodeEditorSyntaxHighlighter
from .models import (SymbolListModel, BookmarkListModel,
    bundleItemSelectableModelFactory, bookmarkSelectableModelFactory,
    symbolSelectableModelFactory)

from prymatex.support import PreferenceMasterSettings

from prymatex.utils import text, encoding
from prymatex.utils.i18n import ugettext as _
from functools import reduce

class CodeEditor(PrymatexEditor, TextEditWidget):
    STANDARD_SIZES = (70, 78, 80, 100, 120)

    # -------------------- Signals
    syntaxChanged = QtCore.Signal()
    themeChanged = QtCore.Signal(object)
    filePathChanged = QtCore.Signal(str)
    blocksRemoved = QtCore.Signal(QtGui.QTextBlock, int)
    blocksAdded = QtCore.Signal(QtGui.QTextBlock, int)
    modeChanged = QtCore.Signal()
    beginMode = QtCore.Signal(object)
    endMode = QtCore.Signal(object)
    aboutToClose = QtCore.Signal()

    aboutToHighlightChange = QtCore.Signal()
    highlightChanged = QtCore.Signal()
    
    # ------------------ Flags
    ShowTabsAndSpaces     = 1<<0
    ShowLineAndParagraphs = 1<<1
    WordWrap              = 1<<2
    MarginLine            = 1<<3
    IndentGuide           = 1<<4
    HighlightCurrentLine  = 1<<5

    # ------------------- Settings
    SETTINGS = 'CodeEditor'

    removeTrailingSpaces = ConfigurableItem(default = False)
    autoBrackets = ConfigurableItem(default = True)
    smartHomeSmartEnd = ConfigurableItem(default = True)
    enableAutoCompletion = ConfigurableItem(default = True)
    wordLengthToComplete = ConfigurableItem(default = 3)

    marginLineSize = ConfigurableItem(default = 80)
    wordWrapSize = ConfigurableItem()
    indentUsingSpaces = ConfigurableItem(default = True)
    adjustIndentationOnPaste = ConfigurableItem(default = False)
    encoding = ConfigurableItem(default = 'utf_8')

    @ConfigurableItem(default = 4)
    def indentationWidth(self, size):
        self.repaint()

    @ConfigurableItem(default = 4)
    def tabWidth(self, size):
        self.setTabStopWidth(size * self.characterWidth())

    @ConfigurableItem(default = ("Monospace", 10))
    def defaultFont(self, value):
        font = QtGui.QFont(*value)
        font.setStyleStrategy(QtGui.QFont.ForceIntegerMetrics)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.setFont(font)

    @ConfigurableItem(default = "3130E4FA-B10E-11D9-9F75-000D93589AF6", tm_name = 'OakDefaultLanguage')
    def defaultSyntax(self, uuid):
        self._default_syntax = self.application().supportManager.getBundleItem(uuid)
        if self._default_syntax is None:
            # Load original default syntax
            self._default_syntax = self.application().supportManager.getBundleItem(self._settings.default("defaultSyntax"))
        self.insertBundleItem(self._default_syntax)
        
    @ConfigurableItem(default = '766026CB-703D-4610-B070-8DE07D967C5F', tm_name = 'OakThemeManagerSelectedTheme')
    def defaultTheme(self, uuid):
        self._default_theme = self.application().supportManager.getBundleItem(uuid)
        if self._default_theme is None:
            # Load original default theme
            self._default_theme = self.application().supportManager.getBundleItem(self._settings.default("defaultTheme"))
        self.insertBundleItem(self._default_theme)
        
    @ConfigurableItem(default = MarginLine | IndentGuide | HighlightCurrentLine)
    def defaultFlags(self, flags):
        self.setFlags(flags)

    # --------------------- init
    def __init__(self, **kwargs):
        super(CodeEditor, self).__init__(**kwargs)
        self.__current_mode = self
        self.__blockUserDataHandlers = []
        self.__preKeyPressHandlers = {
            QtCore.Qt.Key_Any: [ self.__insert_key_bundle_item, self.__insert_typing_pairs ],
            QtCore.Qt.Key_Return: [ self.__first_line_syntax, self.__insert_new_line ],
            QtCore.Qt.Key_Tab: [ self.__insert_tab_bundle_item, self.__indent_tab_behavior ],
            QtCore.Qt.Key_Home: [ self.__move_cursor_to_line_start ],
            QtCore.Qt.Key_Backtab: [ self.__unindent ],
            QtCore.Qt.Key_Backspace: [ self.__unindent_backward_tab_behavior, self.__remove_backward_braces ],
            QtCore.Qt.Key_Delete: [ self.__unindent_forward_tab_behavior, self.__remove_forward_braces ]
        }
        self.__postKeyPressHandlers = {}

        #Current pairs for cursor position (leftBrace <|> rightBrace, oppositeLeftBrace, oppositeRightBrace)
        # <|> the cursor is allways here
        self._currentPairs = (None, None, None, None)
        self.foldingellipsisImage = self.resources().get_image(":/sidebar/folding-ellipsis.png")
        
        # -------------------- Addons containers
        # Sidebars
        self.leftBar = CodeEditorSideBar(self)
        self.rightBar = CodeEditorSideBar(self)
        # Modes
        self.codeEditorModes = []
        
        #Models
        self.bookmarkListModel = BookmarkListModel(self)
        self.symbolListModel = SymbolListModel(self)
        self.bundleItemSelectableModel = bundleItemSelectableModelFactory(self)
        self.symbolSelectableModel = symbolSelectableModelFactory(self)

        #Processors
        self.processors = [
            CodeEditorSnippetProcessor(self),
            CodeEditorCommandProcessor(self),
            CodeEditorSyntaxProcessor(self),
            CodeEditorMacroProcessor(self),
            CodeEditorThemeProcessor(self)
        ]

        #Highlighter
        self.syntaxHighlighter = CodeEditorSyntaxHighlighter(self)
        self.syntaxHighlighter.aboutToHighlightChange.connect(self.aboutToHighlightChange.emit)
        self.syntaxHighlighter.highlightChanged.connect(self.highlightChanged.emit)

        #Block Count
        self.lastBlockCount = self.document().blockCount()
        
        # By default
        self.showMarginLine = True
        self.showIndentGuide = True
        self.showHighlightCurrentLine = True
        
        # Connect context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        # Connect Signals
        self.customContextMenuRequested.connect(self.showEditorContextMenu)

        # Sidebars signals
        self.rightBar.updateRequest.connect(self.updateViewportMargins)
        self.leftBar.updateRequest.connect(self.updateViewportMargins)

        # Document signals
        self.document().undoCommandAdded.connect(self.on_document_undoCommandAdded)

        # Editor signals
        self.blockCountChanged.connect(self.on_blockCountChanged)
        self.updateRequest.connect(self.updateSideBars)
        self.themeChanged.connect(self.highlightEditor)
        
        self.cursorPositionChanged.connect(self.setCurrentBraces)
        self.cursorPositionChanged.connect(self.highlightEditor)
        
        self.syntaxChanged.connect(lambda editor=self: 
            editor.showMessage("Syntax changed to <b>%s</b>" % editor.syntax().name)
        )

        # TODO Algo mejor para acomodar el ancho del tabulador
        self.fontChanged.connect(lambda ed = self: ed.setTabStopWidth(ed.tabWidth * ed.characterWidth()))
        self.beginMode.connect(self.on_beginMode)
        self.endMode.connect(self.on_endMode)

    def name(self):
        return "Edit"

    def window(self):
        parent = self.parent()
        while parent and not isinstance(parent, QtGui.QMainWindow):
            parent = parent.parent()
        return parent

    def initialize(self, **kwargs):
        super(CodeEditor, self).initialize(**kwargs)

        # Get dialogs
        self.selectorDialog = self.window().findChild(QtGui.QDialog, "SelectorDialog")
        self.browserDock = self.window().findChild(QtGui.QDockWidget, "BrowserDock")

    # -------------- Self Signal Connect
    def on_beginMode(self, mode):
        self.__current_mode = mode
        self.modeChanged.emit()

    def on_endMode(self, mode):
        self.__current_mode = self
        self.modeChanged.emit()

    # OVERRIDE: PrymatexEditor.addComponent()
    def addComponent(self, component):
        PrymatexEditor.addComponent(self, component)
        if isinstance(component, SideBarWidgetMixin):
            self.addSideBarWidget(component)
        elif isinstance(component, CodeEditorBaseMode):
            self.addCodeEditorMode(component)

    def addSideBarWidget(self, widget):
        if widget.ALIGNMENT == QtCore.Qt.AlignRight:
            self.rightBar.addWidget(widget)
        else:
            self.leftBar.addWidget(widget)

    def addCodeEditorMode(self, codeEditorMode):
        self.codeEditorModes.append(codeEditorMode)

    # -------------------- Notifications
    def showMessage(self, *largs, **kwargs):
        return self.window().showMessage(*largs, **kwargs)
        
    def showTooltip(self, *largs, **kwargs):
        if "point" not in kwargs:
            kwargs["point"] = self.mapToGlobal(
                self.cursorRect(self.textCursor()).bottomRight()
            )
        return self.window().showTooltip(*largs, **kwargs)
    
    def showStatus(self, *largs, **kwargs):
        return self.window().showStatus(*largs, **kwargs)

    # OVERRIDE: TextEditWidget.setPlainText()
    def setPlainText(self, text):
        from time import time
        self.syntaxHighlighter.stop()
        super(CodeEditor, self).setPlainText(text)
        self.highlightTime = time()
        def highlightReady(editor):
            def _ready(*args):
                self.logger().info("Time %f" % (time() - self.highlightTime))
            return _ready
        self.syntaxHighlighter.start(highlightReady(self))
        #self.syntaxHighlighter.start(lambda editor = self: editor.highlightChanged.emit())

    # --------------- Block User Data
    def registerBlockUserDataHandler(self, handler):
        self.__blockUserDataHandlers.append(handler)

    def blockUserData(self, block):
        # TODO: If block not is valid ?
        if block.userData() is None:
            userData = CodeEditorBlockUserData()
            # Indent and content
            userData.indentation = ""

            # Folding
            userData.foldingMark = PreferenceMasterSettings.FOLDING_NONE
            userData.foldedLevel = 0
            userData.folded = False

            # Now the handlers
            for handler in self.__blockUserDataHandlers:
                handler.contributeToBlockUserData(userData)
            block.setUserData(userData)
        return block.userData()

    def processBlockUserData(self, sourceText, block, userData):
        # Indent
        userData.indentation = text.white_space(sourceText)
        
        # Build cursor from block
        cursor = self.newCursorAtPosition(block.position() + len(userData.indentation))
        
        # Folding
        userData.foldingMark = self.preferenceSettings(cursor).folding(sourceText)
        
        # Handlers
        for handler in self.__blockUserDataHandlers:
            handler.processBlockUserData(sourceText, cursor, block, userData)

    def on_blockCountChanged(self, newBlockCount):
        self.logger().debug("block Count changed")
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
        super(CodeEditor, self).open(filePath)
        content, self.encoding = self.application().fileManager.readFile(filePath)
        self.setPlainText(content)
        
    def save(self, filePath):
        """ Save content of editor in a file """
        self.encoding = self.application().fileManager.writeFile(filePath, self.toPlainTextWithEol(), self.encoding)
        super(CodeEditor, self).save(filePath)

    def close(self):
        self.aboutToClose.emit()
        super(CodeEditor, self).close()

    def reload(self):
        PrymatexEditor.reload(self)
        content, self.encoding = self.application().fileManager.readFile(self.filePath())
        self.updatePlainText(content)

    def componentState(self):
        """Returns a Python dictionary containing the state of the editor."""
        state = super(CodeEditor, self).componentState()
        if self.isModified():
            state["text"] = self.toPlainTextWithEol()

        #Bookmarks
        state['bookmarks'] = self.bookmarkListModel.lineNumbers()
        
        #Syntax
        state['syntax'] = self.syntax().uuidAsText()

        #UserDatas
        state['data'] = []

        return state

    def setComponentState(self, componentState):
        """Restore the state from the given state (returned by a previous call to componentState())."""
        if "text" in componentState:
            self.setPlainText(componentState["text"])
        uuid = componentState.get("syntax")
        if uuid is not None:
            syntax = self.application().supportManager.getBundleItem(uuid)
            self.insertBundleItem(syntax)
        
    def isModified(self):
        return self.document().isModified()

    def isEmpty(self):
        return self.document().isEmpty()

    def setModified(self, modified):
        self.document().setModified(modified)

    def setFilePath(self, filePath):
        super(CodeEditor, self).setFilePath(filePath)
        self.filePathChanged.emit(filePath)
        extension = self.application().fileManager.extension(filePath)
        syntax = self.application().supportManager.findSyntaxByFileType(extension)
        if syntax is not None:
            self.insertBundleItem(syntax)

    def title(self):
        #Podemos marcar de otra forma cuando algo cambia :P
        return PrymatexEditor.title(self)

    def fileFilters(self):
        return [ "%s (%s)" % (self.syntax().bundle.name, " ".join(["*." + ft for ft in self.syntax().fileTypes])) ]
        #return PrymatexEditor.fileFilters(self)

    # ---------------------- Scopes
    def tokenAtPosition(self, position):
        if position < 0:
            position = 0
        elif position > self.document().characterCount():
            position = self.document().characterCount()
        block = self.document().findBlock(position)
        return self.blockUserData(block).tokenAtPosition(position - block.position())

    def scope(self, cursor = None):
        cursor = cursor or self.textCursor()
        leftToken, rightToken = (self.tokenAtPosition(cursor.selectionStart() - 1),
            self.tokenAtPosition(cursor.selectionEnd()))
        # Cursor scope
        leftScope, rightScope = [], []
        leftCursor = self.newCursorAtPosition(cursor.selectionStart())
        rightCursor = self.newCursorAtPosition(cursor.selectionEnd())
        if cursor.hasSelection():
            # If there is one or more selections: dyn.selection.
            # TODO If there is a single zero-width selection: dyn.caret.mixed.columnar.
            # TODO If there are multiple carets and/or selections: dyn.caret.mixed.
            leftScope.append("dyn.selection")
            rightScope.append("dyn.selection")
        # When there is only a single caret or a single continuous selection
        # the left scope may contain: dyn.caret.begin.line or dyn.caret.begin.document
        if leftCursor.atBlockStart():
            leftScope.append("dyn.caret.begin.line")
        if leftCursor.atStart():
            leftScope.append("dyn.caret.begin.document")
        # Likewise the right scope may contain: dyn.caret.end.line or dyn.caret.end.document.
        if rightCursor.atBlockEnd():
            rightScope.append("dyn.caret.end.line")
        if rightCursor.atEnd():
            rightScope.append("dyn.caret.end.document")

        return (leftToken.scope.auxiliary(leftScope, self.filePath()),
            rightToken.scope.auxiliary(rightScope, self.filePath()))

    def preferenceSettings(self, cursor = None):
        cursor = cursor or self.textCursor()
        leftToken, rightToken = (self.tokenAtPosition(cursor.selectionStart() - 1),
            self.tokenAtPosition(cursor.selectionEnd()))
        return self.application().supportManager.getPreferenceSettings(leftToken.scope, leftToken.scope)

    # ------------ Obteniendo datos del editor
    def currentMode(self):
        return self.__current_mode

    def tabKeyBehavior(self):
        return ' ' * self.indentationWidth if self.indentUsingSpaces else '\t'

    def blockIndentation(self, block):
        return self.blockUserData(block).indentation

    # ------------ Flags
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
        if options.wrapMode() & QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere:
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
            options.setWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        else:
            options.setWrapMode(QtGui.QTextOption.NoWrap)
        options.setFlags(oFlags)
        self.document().setDefaultTextOption(options)
        self.showMarginLine = bool(flags & self.MarginLine)
        self.showIndentGuide = bool(flags & self.IndentGuide)
        self.showHighlightCurrentLine = bool(flags & self.HighlightCurrentLine)

    # ------------------- Current Syntax and Theme
    def syntax(self):
        return self.findProcessor("syntax").bundleItem

    def theme(self):
        return self.findProcessor("theme").bundleItem
        
    # -------------------- SideBars
    def updateViewportMargins(self):
        self.setViewportMargins(self.leftBar.width(), 0, 0, 0)
        #self.setViewportMargins(self.leftBar.width(), 0, self.rightBar.width(), 0)

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
        if self.verticalScrollBar().isVisible():
            rightBarPosition -= self.verticalScrollBar().width()
        self.rightBar.setGeometry(QtCore.QRect(rightBarPosition, cr.top(), self.rightBar.width(), cr.height()))

    # -------------- Braces
    def setCurrentBraces(self, cursor = None):
        cursor = QtGui.QTextCursor(cursor) if cursor is not None else QtGui.QTextCursor(self.textCursor())
        cursor.clearSelection()
        settings = self.preferenceSettings(cursor)
        openBraces = [pair[0] for pair in settings.highlightPairs]
        closeBraces = [pair[1] for pair in settings.highlightPairs]

        leftChar = cursor.document().characterAt(cursor.position() - 1)
        rightChar = cursor.document().characterAt(cursor.position())
        
        self._currentPairs = (None, None, None, None)

        # TODO si no hay para uno no hay para ninguno, quitar el que esta si el findTypingPair retorna None
        if leftChar in openBraces:
            leftCursor = QtGui.QTextCursor(cursor)
            leftCursor.movePosition(QtGui.QTextCursor.PreviousCharacter, QtGui.QTextCursor.KeepAnchor)
            index = openBraces.index(leftChar)
            otherBrace = self.findTypingPair(leftChar, closeBraces[index], leftCursor)
            if otherBrace is not None:
                self._currentPairs = (leftCursor, None, otherBrace, None)
        if rightChar in openBraces:
            rightCursor = QtGui.QTextCursor(cursor)
            rightCursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
            index = openBraces.index(rightChar)
            otherBrace = self.findTypingPair(rightChar, closeBraces[index], rightCursor)
            if otherBrace is not None:
                self._currentPairs = (self._currentPairs[0], rightCursor, self._currentPairs[2], otherBrace)
        if leftChar in closeBraces and self._currentPairs[0] is None:  #Tener uno implica tener los dos por el if
            leftCursor = QtGui.QTextCursor(cursor)
            leftCursor.movePosition(QtGui.QTextCursor.PreviousCharacter, QtGui.QTextCursor.KeepAnchor)
            otherBrace = self.findTypingPair(leftChar, openBraces[closeBraces.index(leftChar)], leftCursor, True)
            if otherBrace is not None:
                self._currentPairs = (leftCursor, self._currentPairs[1], otherBrace, self._currentPairs[3])
        if rightChar in closeBraces and self._currentPairs[1] is None: #Tener uno implica tener los dos por el if
            rightCursor = QtGui.QTextCursor(cursor)
            rightCursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
            otherBrace = self.findTypingPair(rightChar, openBraces[closeBraces.index(rightChar)], rightCursor, True)
            if otherBrace is not None:
                self._currentPairs = (self._currentPairs[0], rightCursor, self._currentPairs[2], otherBrace)

    def currentBracesPairs(self, cursor = None, direction = "both"):
        """ Retorna el otro cursor correspondiente al cursor (brace)
        pasado o actual del editor, puede retornar None en caso de no
        estar cerrado el brace"""
        cursor = cursor or self.textCursor()
        brace1, brace2 = (None, None)
        if cursor.hasSelection():
            for index in [0, 1]:
                if self._currentPairs[index] is not None and cursor.selectedText() == self._currentPairs[index].selectedText():
                    brace1 = QtGui.QTextCursor(self._currentPairs[index + 2]) if self._currentPairs[index + 2] is not None else None
                    brace2 = cursor
                    break
        else:
            #print map(lambda c: c is not None and c.selectedText() or "None", self._currentPairs)
            if direction in ("left", "both"):
                brace1 = self._currentPairs[0]
                brace2 = self._currentPairs[2]
            if (brace1 is None or brace2 is None) and direction in ("right", "both"):
                brace1 = self._currentPairs[1]
                brace2 = self._currentPairs[3]
        if (brace1 is not None and brace2 is not None) and brace1.selectionStart() > brace2.selectionStart():
            return (brace2, brace1)
        return (brace1, brace2)

    def beforeBrace(self, cursor):
        return self._currentPairs[1] is not None and self._currentPairs[1].position() - 1 == cursor.position()

    def afterBrace(self, cursor):
        return self._currentPairs[0] is not None and self._currentPairs[0].position() + 1 == cursor.position()

    def besideBrace(self, cursor):
        return self.beforeBrace(cursor) or self.afterBrace(cursor)

    def surroundBraces(self, cursor):
        #TODO: Esto esta mal
        return self.beforeBrace(cursor) and self.afterBrace(cursor)

    #-------------------- Highlight Editor
    def highlightEditor(self):
        cursor = self.textCursor()
        cursor.clearSelection()
        if self.showHighlightCurrentLine:
            self.setExtraSelectionCursors("dyn.lineHighlight", [ cursor ])
        else:
            self.clearExtraSelectionCursors("dyn.lineHighlight")
        self.setExtraSelectionCursors("dyn.highlightPairs", [cursor for cursor in list(self._currentPairs) if cursor is not None])
        self.updateExtraSelections()

    # OVERRIDE: TextEditWidget.setPalette()
    def setPalette(self, palette):
        super(CodeEditor, self).setPalette(palette)
        self.viewport().setPalette(palette)
        self.leftBar.setPalette(palette)
        self.rightBar.setPalette(palette)
        
        # Register lineHighlight textCharFormat
        textCharFormat = QtGui.QTextCharFormat()
        textCharFormat.setBackground(palette.alternateBase().color())
        textCharFormat.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        self.registerTextCharFormat("dyn.lineHighlight", textCharFormat)
        
        # Register highlightPairs textCharFormat
        textCharFormat = QtGui.QTextCharFormat()
        textCharFormat.setFontUnderline(True)
        textCharFormat.setBackground(palette.alternateBase().color())
        textCharFormat.setUnderlineColor(palette.text().color())
        textCharFormat.setBackground(QtCore.Qt.transparent)
        self.registerTextCharFormat("dyn.highlightPairs", textCharFormat)

        for component in self.components():
            component.setPalette(palette)

    # OVERRIDE: TextEditWidget.setFont()
    def setFont(self, font):
        super(CodeEditor, self).setFont(font)
        for component in self.components():
            component.setFont(font)

    # OVERRIDE: TextEditWidget.focusInEvent()
    def focusInEvent(self, event):
        # TODO No es para este evento pero hay que poner en alugn lugar el update de las side bars
        super(CodeEditor, self).focusInEvent(event)
        self.updateSideBarsGeometry()

    # OVERRIDE: TextEditWidget.resizeEvent()
    def resizeEvent(self, event):
        super(CodeEditor, self).resizeEvent(event)
        self.updateSideBarsGeometry()

    # OVERRIDE: TextEditWidget.paintEvent()
    def paintEvent(self, event):
        super(CodeEditor, self).paintEvent(event)
        page_bottom = self.viewport().height()

        characterWidth = self.characterWidth()
        characterHeight = self.characterHeight()

        painter = QtGui.QPainter(self.viewport())
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)

        painter.setPen(self.palette().highlight().color())
        block = self.firstVisibleBlock()
        offset = self.contentOffset()
        while block.isValid() and self.blockUserData(block):
            # The top left position of the block in the document
            # position = self.blockBoundingGeometry(block).topLeft() + offset
            blockGeometry = self.blockBoundingGeometry(block)
            blockGeometry.translate(offset)
            # Check if the position of the block is out side of the visible area
            if blockGeometry.top() > page_bottom:
                break
            if block.isVisible():
                positionY = blockGeometry.top()
                if self.isFolded(block):
                    painter.drawPixmap(characterWidth * block.length() + offset.x() + 10,
                        positionY + characterHeight - self.foldingellipsisImage.height(),
                        self.foldingellipsisImage)
                if self.showIndentGuide:
                    blockPattern = block
                    while blockPattern.isValid() and self.blockUserData(blockPattern).blank():
                        blockPattern = blockPattern.next()
                    if blockPattern.isValid():
                        indentLen = len(self.blockUserData(blockPattern).indentation)
                        padding = characterWidth + offset.x()
                        for s in range(0, indentLen // self.indentationWidth):
                            positionX = (characterWidth * self.indentationWidth * s) + padding
                            painter.drawLine(positionX, positionY, positionX, positionY + characterHeight)

            block = block.next()

        if self.showMarginLine:
            pos_margin = characterWidth * self.marginLineSize
            painter.drawLine(pos_margin + offset.x(), 0, pos_margin + offset.x(), self.viewport().height())

        painter.end()

    # OVERRIDE: TextEditWidget.wheelEvent()
    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.delta() == 120:
                self.zoomIn()
            elif event.delta() == -120:
                self.zoomOut()
            event.ignore()
        else:
            TextEditWidget.wheelEvent(self, event)

    # OVERRIDE: TextEditWidget.mouseReleaseEvent(),
    def mouseReleaseEvent(self, event):
        freehanded = False
        if freehanded:
            #Modo freehanded
            cursor = self.cursorForPosition(event.pos())
            if not self.cursorRect(cursor).contains(event.pos()):
                cursor.beginEditBlock()
                while not self.cursorRect(cursor).top() <= event.pos().y() <= self.cursorRect(cursor).bottom():
                    cursor.insertText("\n")
                    print(cursor.position(), self.cursorRect(cursor))
                while self.cursorRect(cursor).x() <= event.pos().x():
                    cursor.insertText(" ")
                    print(cursor.position(), self.cursorRect(cursor))
                cursor.endEditBlock()
                self.setTextCursor(cursor)
            else:
                TextEditWidget.mouseReleaseEvent(self, event)
        else:
            TextEditWidget.mouseReleaseEvent(self, event)

    # --------------- Key press pre and post
    def registerKeyPressHandler(self, key, handler, important = False, after = False):
        keyPressHandlers = after and self.__postKeyPressHandlers or self.__preKeyPressHandlers
        handlers = keyPressHandlers.setdefault(key, [])
        if important:
            handlers.insert(0, handler)
        else:
            handlers.append(handler)

    # OVERRIDE: TextEditWidget.keyPressEvent()
    def keyPressEvent(self, event):
        def handle(event, keyPressHandlers):
            for handler in keyPressHandlers.get(QtCore.Qt.Key_Any, []):
                yield handler(event)
            for handler in keyPressHandlers.get(event.key(), []):
                yield handler(event)
        
        if not any(handle(event, self.__preKeyPressHandlers)):
            super(CodeEditor, self).keyPressEvent(event)

            handle(event, self.__postKeyPressHandlers)

    # ------------ Key press
    def __first_line_syntax(self, event):
        cursor = self.textCursor()
        if cursor.blockNumber() == 0:
            text = cursor.block().text()[:cursor.columnNumber()]
            syntax = self.application().supportManager.findSyntaxByFirstLine(text)
            if syntax is not None:
                self.insertBundleItem(syntax)
        return False
    
    def __insert_new_line(self, event):
        self.insertNewLine(self.textCursor())
        return True
    
    def __insert_key_bundle_item(self, event):
        keyseq = int(event.modifiers()) + event.key()
        # Try key equivalent
        if keyseq in self.application().supportManager.getAllKeyEquivalentCodes():
            leftScope, rightScope = self.scope()
            items = self.application().supportManager.getKeyEquivalentItem(
                keyseq, leftScope, rightScope)
            self.insertBundleItem(items)
            return bool(items)
        return False
    
    def __insert_tab_bundle_item(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection(): return False

        trigger = self.application().supportManager.getTabTriggerSymbol(cursor.block().text(), cursor.columnNumber())
        if not trigger: return False

        triggerCursor = self.newCursorAtPosition(cursor.position(), cursor.position() - len(trigger))
        leftScope, rightScope = self.scope(triggerCursor)
        items = self.application().supportManager.getTabTriggerItem(
            trigger, leftScope, rightScope)
        self.insertBundleItem(items, textCursor = triggerCursor)
        return bool(items)

    def __indent_tab_behavior(self, event):
        start, end = self.selectionBlockStartEnd()
        if start != end:
            self.indentBlocks()
        else:
            self.textCursor().insertText(self.tabKeyBehavior())
        return True
    
    def __move_cursor_to_line_start(self, event):
        cursor = self.textCursor()
        #Solo si el cursor no esta al final de la indentacion
        block = cursor.block()
        newPosition = block.position() + len(self.blockIndentation(block))
        if newPosition != cursor.position():
            cursor.setPosition(newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
            self.setTextCursor(cursor)
            return True
        return False

    def __unindent(self, event):
        self.unindentBlocks()
       
    def __unindent_backward_tab_behavior(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection(): return False
        lineText = cursor.block().text()
        if lineText[:cursor.columnNumber()].endswith(self.tabKeyBehavior()):
            counter = cursor.columnNumber() % self.tabWidth or self.tabWidth
            self.newCursorAtPosition(cursor.position(), cursor.position() - counter).removeSelectedText()
            return True
        return False
        
    def __remove_backward_braces(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection(): return False
        cursor1, cursor2 = self.currentBracesPairs(cursor, direction = "left")
        if cursor1 and cursor2  and (cursor1.selectionStart() == cursor2.selectionEnd() or cursor1.selectionEnd() == cursor2.selectionStart()):
            cursor.beginEditBlock()
            cursor1.removeSelectedText()
            cursor2.removeSelectedText()
            cursor.endEditBlock()
            return True
        return False

    def __unindent_forward_tab_behavior(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection(): return False
        lineText = cursor.block().text()
        if lineText[cursor.columnNumber():].startswith(self.tabKeyBehavior()):
            counter = cursor.columnNumber() % self.tabWidth or self.tabWidth
            self.newCursorAtPosition(cursor.position(), cursor.position() + counter).removeSelectedText()
            return True
        return False
        
    def __remove_forward_braces(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection(): return False
        cursor1, cursor2 = self.currentBracesPairs(cursor, direction = "right")
        if cursor1 and cursor2  and (cursor1.selectionStart() == cursor2.selectionEnd() or cursor1.selectionEnd() == cursor2.selectionStart()):
            cursor.beginEditBlock()
            cursor1.removeSelectedText()
            cursor2.removeSelectedText()
            cursor.endEditBlock()
            return True
        return False
        
    def __insert_typing_pairs(self, event):
        cursor = self.textCursor()
        settings = self.preferenceSettings(cursor)
        character = event.text()
        pairs = [pair for pair in settings.smartTypingPairs if character in pair]
        
        # No pairs
        if not pairs: return False

        pair = pairs[0]
        
        insert = replace = wrap = skip = False

        isOpen = character == pair[0]
        isClose = character == pair[1]
        meta_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        if isClose:
            cursor1, cursor2 = self.currentBracesPairs(cursor, direction = "right")
            if cursor1 and cursor2 and \
                character == cursor2.selectedText():
                cursor.movePosition(QtGui.QTextCursor.NextCharacter)
                self.setTextCursor(cursor)
                return True
            elif pair[0] != pair[1]:
                return False
        elif meta_down and isOpen:
            if cursor.hasSelection():
                selectedText = cursor.selectedText()
                if any([selectedText == pair[0] for pair in settings.smartTypingPairs]):
                    cursor1, cursor2 = self.currentBracesPairs(cursor)
                    cursor1.insertText(pair[0])
                    cursor2.insertText(pair[1])
                    return True
            else:
                cursor1, cursor2 = self.currentBracesPairs(cursor)
                if cursor1 and cursor2:
                    if cursor.position() == cursor1.selectionStart():
                        cursor1.setPosition(cursor1.selectionStart())
                        cursor2.setPosition(cursor2.selectionEnd())
                    else:
                        cursor1.setPosition(cursor1.selectionEnd())
                        cursor2.setPosition(cursor2.selectionStart())
                    cursor.beginEditBlock()
                    cursor1.insertText(pair[0])
                    cursor2.insertText(pair[1])
                    cursor.endEditBlock()
                    return True
                    
        word, wordStart, wordEnd = self.currentWord()
        if not (wordStart <= cursor.position() < wordEnd):
            position = cursor.position()
            cursor.insertText("%s%s" % (pair[0], pair[1]))
            cursor.setPosition(position + 1)
            self.setTextCursor(cursor)
            return True
        return False
        
    # ------------ Insert API
    def insertNewLine(self, cursor = None):
        cursor = cursor or self.textCursor()
        block = cursor.block()
        positionInBlock = cursor.positionInBlock()
        settings = self.preferenceSettings(cursor)

        indentationFlags = settings.indentationFlags(block.text()[:positionInBlock])

        tab_behavior = self.tabKeyBehavior()
        indentation = self.blockIndentation(block)

        if settings.INDENT_INCREASE in indentationFlags:
            self.logger().debug("Increase indentation")
            blockIndent = indentation + tab_behavior
        elif settings.INDENT_NEXTLINE in indentationFlags:
            #TODO: Creo que este no es el correcto
            self.logger().debug("Increase next line indentation")
            blockIndent = indentation + tab_behavior
        elif settings.UNINDENT in indentationFlags:
            self.logger().debug("Unindent")
            blockIndent = ""
        elif settings.INDENT_DECREASE in indentationFlags:
            self.logger().debug("Decrease indentation")
            blockIndent = indentation[:-len(tab_behavior)]
        else:
            self.logger().debug("Preserve indentation")
            blockIndent = indentation[:positionInBlock]
        cursor.insertText("\n%s" % blockIndent)
        self.ensureCursorVisible()

    # ------------ Bundle Items
    def findProcessor(self, nameType):
        for processor in self.processors:
            if nameType in processor.allowedTypes():
                return processor

    def bundleItemHandler(self):
        return self.insertBundleItem

    def insertBundleItem(self, items, **kwargs):
        """Inserta un bundle item"""
        if not isinstance(items, (list, tuple)):
            items = [ items ]

        def _insert_item(index):
            if index >= 0:
                processor = self.findProcessor(items[index].type())
                processor.configure(**kwargs)
                items[index].execute(processor)

        if len(items) > 1:
            syntax = any((item.type() == 'syntax' for item in items))

            self.showFlatPopupMenu(items, _insert_item, cursorPosition = not syntax)
        elif items:
            _insert_item(0)

    def insertSnippet(self, snippetContent, commandInput = "none", commandOutput = "insertText", **kwargs):
        snippet = self.application().supportManager.buildAdHocSnippet(
            snippetContent, self.syntax().bundle)
        self.insertBundleItem(snippet, **kwargs)
        
    def insertCommand(self, commandScript, commandInput = "none", commandOutput = "insertText", **kwargs):
        command = self.application().supportManager.buildAdHocCommand(
            commandScript, self.syntax().bundle,
            commandInput=commandInput, commandOutput=commandOutput)
        self.insertBundleItem(command, **kwargs)

    def environmentVariables(self):
        environment = PrymatexEditor.environmentVariables(self)
        environment.update(
            self.window().environmentVariables()
        )
        
        cursor = self.textCursor()
        block = cursor.block()
        line = block.text()

        leftScope, rightScope = self.scope(cursor)
        current_text, start, end = self.currentText()
        current_word, start, end = self.currentWord()

        theme = self.application().supportManager.getBundleItem(self.defaultTheme)

        # Build environment
        environment.update({
            'TM_FILENAME': self.title(),
            'TM_CURRENT_LINE': line,
            'TM_LINE_INDEX': cursor.positionInBlock(),
            'TM_LINE_NUMBER': block.blockNumber() + 1,
            'TM_CURRENT_THEME_PATH': theme.currentSourcePath(),
            'TM_COLUMN_NUMBER': cursor.positionInBlock() + 1,
            'TM_SCOPE': "%s" % rightScope,
            'TM_SCOPE_LEFT': "%s" % leftScope,
            'TM_MODE': self.syntax().name,
            'TM_SOFT_TABS': self.indentUsingSpaces and 'YES' or 'NO',
            'TM_TAB_SIZE': self.tabWidth
        })

        if current_word:
            self.logger().debug("Add current word to environment")
            environment['TM_CURRENT_WORD'] = current_word
        if current_text:
            self.logger().debug("Add current text to environment")
            environment['TM_CURRENT_TEXT'] = current_text
        if self.filePath():
            self.logger().debug("Add file path to environment")
            environment['TM_FILEPATH'] = self.filePath()
            environment['TM_DIRECTORY'] = self.application().fileManager.dirname(self.filePath())
        if self.project():
            self.logger().debug("Add project to environment")
            environment.update(self.project().environmentVariables())
        if cursor.hasSelection():
            self.logger().debug("Add selection to environment")
            environment['TM_SELECTED_TEXT'] = self.selectedTextWithEol(cursor)
            start, end = self.selectionBlockStartEnd()
            environment['TM_INPUT_START_COLUMN'] = cursor.selectionStart() - start.position() + 1
            environment['TM_INPUT_START_LINE'] = start.blockNumber() + 1
            environment['TM_INPUT_START_LINE_INDEX'] = cursor.selectionStart() - start.position()
        return environment

    # ---------- Completer
    def defaultCompletionCallback(self, suggestion):
        currentWord, start, end = self.currentWord()
        cursor = self.newCursorAtPosition(start, end) \
            if currentWord is not None else self.textCursor()
        snippet = suggestion.get('insert') or suggestion.get('display') or suggestion.get('title')
        self.insertSnippet(snippet, textCursor = cursor)

    # ---------- Folding
    def _find_block_fold_peer(self, block, direction = "down"):
        """ Direction are 'down' or up"""
        if direction == "down":
            assert self.isFoldingStartMarker(block), "Block isn't folding start"
        else:
            assert self.isFoldingStopMarker(block), "Block isn't folding stop"
        nest = 0
        while block.isValid():
            userData = self.blockUserData(block)
            if userData.foldingMark == PreferenceMasterSettings.FOLDING_START:
                nest += 1
            elif userData.foldingMark == PreferenceMasterSettings.FOLDING_STOP:
                nest -= 1
            if nest == 0:
                return block
            block = block.next() if direction == "down" else block.previous()

    def _find_indented_block_fold_close(self, block):
        assert self.isFoldingIndentedBlockStart(block), "Block isn't folding indented start"
        indentation = self.blockUserData(block).indentation
        indentedBlock = self.findIndentedBlock(block, indentation = indentation, comparison = operator.le)
        while indentedBlock.isValid() and self.isFoldingIndentedBlockIgnore(indentedBlock):
            indentedBlock = self.findIndentedBlock(indentedBlock, indentation = indentation, comparison = operator.le)
        if indentedBlock.isValid():
            return self.findNoBlankBlock(indentedBlock, "up")
        else:
            return self.document().lastBlock()

    def isFoldingStartMarker(self, block):
        return self.blockUserData(block).foldingMark == PreferenceMasterSettings.FOLDING_START

    def isFoldingStopMarker(self, block):
        return self.blockUserData(block).foldingMark == PreferenceMasterSettings.FOLDING_STOP

    def isFoldingIndentedBlockStart(self, block):
        return self.blockUserData(block).foldingMark == PreferenceMasterSettings.FOLDING_INDENTED_START

    def isFoldingIndentedBlockIgnore(self, block):
        return self.blockUserData(block).foldingMark == PreferenceMasterSettings.FOLDING_INDENTED_IGNORE

    def isFoldingMark(self, block):
        return self.isFoldingStartMarker(block) or self.isFoldingStopMarker(block) or self.isFoldingIndentedBlockStart(block)

    def isFolded(self, block):
        return self.isFoldingMark(block) and self.blockUserData(block).folded

    def codeFoldingFold(self, milestone):
        block = endBlock = None
        if self.isFoldingStartMarker(milestone):
            startBlock = block = milestone.next()
            endBlock = self._find_block_fold_peer(milestone, "down")
        elif self.isFoldingStopMarker(milestone):
            endBlock = milestone
            milestone = self._find_block_fold_peer(endBlock, "up")
            startBlock = block = milestone.next()
        elif self.isFoldingIndentedBlockStart(milestone):
            startBlock = block = milestone.next()
            endBlock = self._find_indented_block_fold_close(milestone)

        if block and endBlock and milestone:
            # Go!
            while block.isValid():
                userData = self.blockUserData(block)
                userData.foldedLevel += 1
                block.setVisible(userData.foldedLevel == 0)
                if block == endBlock:
                    break
                block = block.next()

            milestone.userData().folded = True
            self.document().markContentsDirty(startBlock.position(), endBlock.position())

    def codeFoldingUnfold(self, milestone):
        endBlock = None
        startBlock = block = milestone.next()
        if self.isFoldingStartMarker(milestone):
            endBlock = self._find_block_fold_peer(milestone, "down")
        elif self.isFoldingIndentedBlockStart(milestone):
            endBlock = self._find_indented_block_fold_close(milestone)

        if endBlock:
            # Go!
            while block.isValid():
                userData = self.blockUserData(block)
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
        self.replaceMatch(match, " " * self.tabWidth, QtGui.QTextDocument.FindFlags(), True)

    def convertSpacesToTabs(self):
        match = " " * self.tabWidth
        self.replaceMatch(match, "\t", QtGui.QTextDocument.FindFlags(), True)

    # -------------- Add select text functions
    def selectEnclosingBrackets(self, cursor = None):
        cursor = cursor or self.textCursor()
        settings = self.preferenceSettings(cursor)
        flags = QtGui.QTextDocument.FindFlags()
        flags |= QtGui.QTextDocument.FindBackward
        foundCursors = [(self.document().find(openBrace_closeBrace[0], cursor.selectionStart(), flags), openBrace_closeBrace[1]) for openBrace_closeBrace in settings.highlightPairs]
        openCursor = reduce(lambda c1, c2: (not c1[0].isNull() and c1[0].selectionEnd() > c2[0].selectionEnd()) and c1 or c2, foundCursors)
        if not openCursor[0].isNull():
            closeCursor = self.findTypingPair(openCursor[0].selectedText(), openCursor[1], openCursor[0])
            if openCursor[0].selectionEnd() <= cursor.selectionStart() <= closeCursor.selectionStart():
                # TODO New cursor at position
                cursor.setPosition(openCursor[0].selectionEnd())
                cursor.setPosition(closeCursor.selectionStart(), QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)

    def selectScope(self, cursor = None):
        cursor = cursor or self.textCursor()
        block = cursor.block()
        token = self.tokenAtPosition(cursor.position())
        cursor = self.newCursorAtPosition(block.position() + token.start,
            block.position() + token.end)
        self.setTextCursor(cursor)

    # ---------- Bookmarks and gotos
    def toggleBookmark(self, cursor = None):
        cursor = cursor or self.textCursor()
        self.bookmarkListModel.toggleBookmark(cursor)

    def bookmarkNext(self, cursor = None):
        cursor = cursor or self.textCursor()
        cursor = self.bookmarkListModel.nextBookmark(cursor)
        if cursor is not None:
            self.setTextCursor(cursor)

    def bookmarkPrevious(self, cursor = None):
        cursor = cursor or self.textCursor()
        cursor = self.bookmarkListModel.previousBookmark(cursor)
        print(cursor)
        if cursor is not None:
            self.setTextCursor(cursor)

    def clearBookmarks(self):
        self.bookmarkListModel.removeAllBookmarks()

    def selectAllBookmarks(self):
        pass

    # ----------------- Goto
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
            TextEditWidget.centerCursor(self)

    # ------------------- Text Indentation
    def findNoBlankBlock(self, block, direction = "down"):
        """ Return no blank block """
        block = block.next() if direction == "down" else block.previous()
        while block.isValid() and self.blockUserData(block).blank():
            block = block.next() if direction == "down" else block.previous()
        return block

    def findIndentedBlock(self, block, indentation = None, direction = "down", comparison = operator.eq):
        """ Return equal indentation block """
        indentation = indentation if indentation is not None else self.blockIndentation(block)
        block = self.findNoBlankBlock(block, direction)
        while block.isValid() and not comparison(self.blockIndentation(block), indentation):
            block = self.findNoBlankBlock(block, direction)
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
            indentation_len = len(self.blockIndentation(start))
            if self.indentUsingSpaces:
                counter = self.tabWidth if indentation_len > self.tabWidth else indentation_len
            else:
                counter = 1 if indentation_len else 0
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
                icon = self.resources().get_icon(item["image"]) if "image" in item else QtGui.QIcon()
            elif isinstance(item,  BundleItemTreeNode):
                title = "%s 	&%d" % (item.buildMenuTextEntry(False), index)
                icon = item.icon()
            else:
                title = "%s 	&%d" % (item, index)
                icon = QtGui.QIcon()
            menu.addAction(icon, title)

        def menu_aboutToHide():
            activeActionIndex = menu.actions().index(menu.activeAction()) if menu.activeAction() else -1
            callback(activeActionIndex)
        menu.aboutToHide.connect(menu_aboutToHide)

        if cursorPosition:
            cursor = self.newCursorAtPosition(self.textCursor().selectionStart())
            point = self.viewport().mapToGlobal(
                self.cursorRect(cursor).bottomLeft())
        else:
            point = self.window().cursor().pos()
        menu.popup(point)

    # Default Context Menus
    def showEditorContextMenu(self, point):
        menu = self.createStandardContextMenu()
        menu.setParent(self)

        #Bundle Menu
        bundleMenu = self.application().supportManager.menuForBundle(self.syntax().bundle)
        extend_menu(menu, [ "-", bundleMenu ])

        #Se lo pasamos a los addons
        cursor = self.cursorForPosition(point)
        items = ["-"]
        for addon in self.addons():
            items += addon.contributeToContextMenu(cursor = cursor)

        if len(items) > 1:
            actions = extend_menu(menu, items)

        menu.popup(self.mapToGlobal(point))

    # Contributes to Tab Menu
    def contributeToTabMenu(self):
        menues = []
        bundleMenu = self.application().supportManager.menuForBundle(self.syntax().bundle)
        if bundleMenu is not None:
            menues.append(bundleMenu)
            menues.append("-")
        if self.filePath() is not None:
            menues.extend([
                {   "text": "Path to clipboard",
                    "triggered": lambda ed = self: self.application().clipboard().setText(ed.filePath())  },
                {   "text": "Name to clipboard",
                    "triggered": lambda ed = self: self.application().clipboard().setText(ed.application.fileManager.basename(ed.filePath()))  },
                {   "text": "Directory to clipboard",
                    "triggered": lambda ed = self: self.application().clipboard().setText(ed.application.fileManager.dirname(ed.filePath()))  },
                ])
        return menues

    # Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls):
        menu = {}
        menu["edit"] = [
                '-',
                {'text': '&Mode',
                 'items': [{
                        'text': 'Freehanded',
                        'sequence': ("Editor", "FreehandedMode", 'Meta+Alt+E')
                    }, {
                        'text': 'Overwrite',
                        'sequence': ("Editor", "OverwriteMode", 'Meta+Alt+O')
                    }, {
                        'text': 'Multiedit',
                        'sequence': ("Editor", "MultieditMode", 'Meta+Alt+M')
                    }
                ]}
            ]
        menu["view"] = [
                '-',
                {'text': "Zoom in",
                  'sequence': ("Editor", "ZoomIn"),
                  'triggered': cls.zoomIn},
                 {'text': "Zoom out",
                  'sequence': ("Editor", "ZoomOut"),
                  'triggered': cls.zoomOut},
                '-',
                {'name': 'leftGutter',
                 'text': 'Left gutter',
                 'items': []},
                {'name': 'rightGutter',
                 'text': 'Right gutter',
                 'items': []
                }, '-',
                {'text': "Word wrap",
                 "items": [{
                        "text": "Automatic",
                        'toggled': cls.on_actionWordWrap_toggled,
                        'testChecked': lambda ed: bool(ed.getFlags() & ed.WordWrap)  and \
                            ed.wordWrapSize is Qt.QWIDGETSIZE_MAX
                    }, "-" ] + [ tuple([ {
                        "text": "%s" % size,
                        "toggled": lambda ed, checked, size=size: ed.on_actionWordWrap_toggled(checked, size=size),
                        'testChecked': lambda ed, size=size: bool(ed.getFlags() & ed.WordWrap) and \
                            ed.wordWrapSize == size
                    } for size in cls.STANDARD_SIZES]) ]
                },
                {'text': "Margin line",
                 "items": [{
                        "text": "None",
                        'toggled': lambda ed, checked: ed.on_actionMarginLine_toggled(not checked),
                        'testChecked': lambda ed: not bool(ed.getFlags() & ed.MarginLine)
                    }, "-" ] + [ tuple([ {
                        "text": "%s" % size,
                        "toggled": lambda ed, checked, size = size: ed.on_actionMarginLine_toggled(checked, size = size),
                        'testChecked': lambda ed, size = size: bool(ed.getFlags() & ed.MarginLine) and \
                            ed.marginLineSize == size
                    } for size in cls.STANDARD_SIZES]) ]
                }, '-',
                {'text': "Indent guide",
                 'toggled': cls.on_actionIndentGuide_toggled,
                 'testChecked': lambda ed: bool(ed.getFlags() & ed.IndentGuide)
                },
                {'text': "Highlight current line",
                 'toggled': cls.on_actionHighlightCurrentLine_toggled,
                 'testChecked': lambda ed: bool(ed.getFlags() & ed.HighlightCurrentLine)
                },
                {'text': "Show tabs and spaces",
                 'toggled': cls.on_actionShowTabsAndSpaces_toggled,
                 'testChecked': lambda ed: bool(ed.getFlags() & ed.ShowTabsAndSpaces) },
                {'text': "Show line and paragraph",
                 'toggled': cls.on_actionShowLineAndParagraphs_toggled,
                 'testChecked': lambda ed: bool(ed.getFlags() & ed.ShowLineAndParagraphs)
                }
            ]
        menu["text"] = {
            'before': 'bundles',
            'name': 'text',
            'text': '&Text',
            'items': [
                {'text': 'Select',
                 'items': [
                    {'text': '&Word',
                     'triggered': lambda ed: ed.selectWord(),
                     'sequence': ("Editor", "SelectWord", 'Ctrl+Meta+W'),
                     },
                    {'text': '&Text',
                     'triggered': lambda ed: ed.selectText(),
                     'sequence': ("Editor", "SelectText", 'Ctrl+Meta+T'),
                     },
                    {'text': '&Line',
                     'triggered': lambda ed: ed.selectLine(),
                     'sequence': ("Editor", "SelectLine", 'Ctrl+Meta+L'),
                     },
                    {'text': '&Paragraph',
                     'triggered': lambda ed: ed.selectParagraph()
                     },
                    {'text': 'Enclosing &brackets',
                     'triggered': lambda ed: ed.selectEnclosingBrackets(),
                     'sequence': ("Editor", "SelectEnclosingBrackets", 'Ctrl+Meta+B'),
                     },
                    {'text': '&Scope',
                     'triggered': lambda ed: ed.selectScope(),
                     'sequence': ("Editor", "SelectScope", 'Ctrl+Meta+S'),
                     },
                    {'text': '&All',
                     'triggered': lambda ed: ed.selectDocument(),
                     'sequence': ("Editor", "SelectAll", 'Ctrl+A'),
                     }
                ]},
                {'text': 'Convert',
                 'items': [
                    {'text': 'Uppercase',
                     'sequence': ("Editor", "ConvertUppercase", 'Ctrl+U'),
                     'triggered': lambda ed: ed.convertToUppercase(),
                     },
                    {'text': 'Lowercase',
                     'sequence': ("Editor", "ConvertLowercase", 'Ctrl+Shift+U'),
                     'triggered': lambda ed: ed.convertToLowercase(),
                     },
                    {'text': 'Titlecase',
                     'sequence': ("Editor", "ConvertTitlecase", 'Ctrl+Alt+U'),
                     'triggered': lambda ed: ed.convertToTitlecase(),
                     },
                    {'text': 'Opposite case',
                     'sequence': ("Editor", "ConvertOppositeCase", 'Ctrl+G'),
                     'triggered': lambda ed: ed.convertToOppositeCase(),
                     }, '-',
                    {'text': 'Tab to spaces',
                     'triggered': lambda ed: ed.convertTabsToSpaces(),
                     },
                    {'text': 'Spaces to tabs',
                     'triggered': lambda ed: ed.convertSpacesToTabs(),
                     }, '-',
                    {'text': 'Transpose',
                     'sequence': ("Editor", "ConvertTranspose", 'Ctrl+T'),
                     'triggered': lambda ed: ed.convertTranspose(),
                     }
                ]}, '-',
                {'text': 'Indentation',
                 'items': [
                    {'text': 'Indent using spaces',
                     'toggled': lambda ed, checked: ed.on_actionIndentation_toggled(checked),
                     'testChecked': lambda ed: ed.indentUsingSpaces
                     }, '-', ] + [ tuple([
                    {'text': 'Tab width: %d' % size,
                     'toggled': lambda ed, checked, size = size: ed.on_actionIndentation_toggled(ed.indentUsingSpaces, size = size),
                     'testChecked': lambda ed, size = size: (ed.indentUsingSpaces and ed.indentationWidth == size) or (not ed.indentUsingSpaces and ed.tabWidth == size)
                     } for size in range(1, 9) ]) ]
                },
                {'text': 'Line endings',
                 'items': [tuple(
                     [{'text': '%s' % name,
                     'toggled': lambda ed, checked, eol_chars = eol_chars: ed.setEolChars(eol_chars),
                     'testChecked': lambda ed, eol_chars = eol_chars: ed.lineSeparator() == eol_chars
                     } for eol_chars, _, name in text.EOLS])
                ]},
                {'text': 'Encoding',
                 'items': [tuple(
                     [{'text': "%s (%s)" % (language.split(",")[0].title(), codec),
                     'toggled': lambda ed, checked, codec = codec: ed.on_actionEncoding_toggled(codec),
                     'testChecked': lambda ed, codec = codec: ed.encoding == codec
                     } for codec, aliases, language in encoding.CODECS])
                ]}, '-',
                {'text': 'Select bundle item',
                 'sequence': ("Editor", "SelectBundleItem", 'Meta+Ctrl+T'),
                 'triggered': cls.on_actionSelectBundleItem_triggered,
                 },
                {'text': 'Execute line/selection',
                 'triggered': lambda ed: ed.executeCommand(),
                 }
            ]}
        menu["navigation"] = [
                "-",
                {'text': 'Bookmarks',
                 'items': [
                    {'text': 'Toggle bookmark',
                     'triggered': cls.toggleBookmark,
                     'sequence': ("Editor", "ToggleBookmark", 'Ctrl+F2'),
                     },
                    {'text': 'Next bookmark',
                     'triggered': cls.bookmarkNext,
                     'sequence': ("Editor", "NextBookmark", 'F2'),
                     },
                    {'text': 'Previous bookmark',
                     'triggered': cls.bookmarkPrevious,
                     'sequence': ("Editor", "PreviousBookmark", 'Shift+F2'),
                     },
                    {'text': 'Clear bookmarks',
                     'triggered': cls.clearBookmarks,
                     'sequence': ("Editor", "ClearBookmarks", 'Ctrl+Shift+F2'),
                     },
                    {'text': 'Select all bookmarks',
                     'triggered': cls.selectAllBookmarks,
                     'sequence': ("Editor", "SelectAllBookmarks", 'Alt+F2'),
                     }
                ]},
                "-",
                {'text': 'Go to &symbol',
                 'triggered': cls.on_actionGoToSymbol_triggered,
                 'sequence': ("Editor", "GoToSymbol", 'Meta+Ctrl+Shift+O'),
                 },
                {'text': 'Go to &bookmark',
                 'triggered': cls.on_actionGoToBookmark_triggered,
                 'sequence': ("Editor", "GoToBookmark", 'Meta+Ctrl+Shift+B'),
                 }
            ]
        return menu

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.theme import ThemeSettingsWidget
        from prymatex.gui.settings.editor import EditorSettingsWidget
        from prymatex.gui.settings.edit import EditSettingsWidget
        from prymatex.gui.settings.addons import AddonsSettingsWidgetFactory
        return [ EditorSettingsWidget, ThemeSettingsWidget, EditSettingsWidget, AddonsSettingsWidgetFactory("editor") ]

    def contributeToShortcuts(self):
        return [
            {'sequence': ("Editor", "MoveLineUp", 'Meta+Ctrl+Up'),
             'activated': self.moveUp,
             'context': QtCore.Qt.WidgetShortcut
             },
            {'sequence': ("Editor", "MoveLineDown", 'Meta+Ctrl+Down'),
             'activated': self.moveDown,
             'context': QtCore.Qt.WidgetShortcut
             },
            {'sequence': ("Editor", "MoveColumnLeft", 'Meta+Ctrl+Left'),
             'activated': self.moveLeft,
             'context': QtCore.Qt.WidgetShortcut
             },
            {'sequence': ("Editor", "MoveColumnRight", 'Meta+Ctrl+Right'),
             'activated': self.moveRight,
             'context': QtCore.Qt.WidgetShortcut
             }
        ]

    # ------------------ Menu Actions
    def on_actionIndentation_toggled(self, checked, size = None):
        if size is None:
          size = self.indentationWidth if self.indentUsingSpaces else self.tabWidth
        self.indentUsingSpaces = checked
        if self.indentUsingSpaces:
            self.indentationWidth = size
        else:
            self.tabWidth = size
        self.update()
        self.textChanged.emit()

    def on_actionEncoding_toggled(self, codec):
        if self.encoding != codec:
            self.encoding = codec
            self.textChanged.emit()

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

    def on_actionWordWrap_toggled(self, checked, size = Qt.QWIDGETSIZE_MAX):
        if checked:
            flags = self.getFlags() | self.WordWrap
            self.wordWrapSize = size
            if size != Qt.QWIDGETSIZE_MAX:
                size = (size * self.characterWidth()) + 2
            self.viewport().setMaximumWidth(size)
        else:
            self.wordWrapSize = None
            flags = self.getFlags() & ~self.WordWrap
        self.setFlags(flags)

    def on_actionHighlightCurrentLine_toggled(self, checked):
        if checked:
            flags = self.getFlags() | self.HighlightCurrentLine
        else:
            flags = self.getFlags() & ~self.HighlightCurrentLine
        self.setFlags(flags)

    def on_actionMarginLine_toggled(self, checked, size = None):
        if isinstance(size, int):
            self.marginLineSize = size
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
        bookmarkSelectableModel = bookmarkSelectableModelFactory(self)
        item = self.selectorDialog.select(bookmarkSelectableModel, title=_("Select Bookmark"))
        if item is not None:
            self.setTextCursor(item['bookmark'])

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
            files = [url.toLocalFile() for url in event.mimeData().urls()]
            for filePath in files:
                items = self.application().supportManager.getFileExtensionItem(filePath, self.scope())
                if items:
                    item = items[0]
                    env = {
                            #relative path of the file dropped (relative to the document directory, which is also set as the current directory).
                            'TM_DROPPED_FILE': filePath,
                            #the absolute path of the file dropped.
                            'TM_DROPPED_FILEPATH': filePath,
                            #the modifier keys which were held down when the file got dropped.
                            #This is a bitwise OR in the form: SHIFT|CONTROL|OPTION|COMMAND (in case all modifiers were down).
                            'TM_MODIFIER_FLAGS': filePath
                    }
                    self.insertBundleItem(item, environment = env)
                else:
                    self.application().openFile(filePath)
        elif event.mimeData().hasText():
            self.textCursor().insertText(event.mimeData().text())
