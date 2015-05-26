#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import re
import operator

from prymatex.qt import QtCore, QtGui, Qt, QtWidgets, API

from prymatex.core import PrymatexEditor
from prymatex.core import constants
from prymatex.core.settings import ConfigurableItem

from prymatex.widgets.texteditor import TextEditWidget
from prymatex.widgets.texteditor import CompletionWidget

from prymatex.qt.helpers import (extend_menu, keyevent_to_keysequence, keyevent_to_tuple)
from prymatex.models.support import BundleItemTreeNode

from .addons import CodeEditorAddon
from .sidebar import CodeEditorSideBar, SideBarWidgetMixin
from .processors import (CodeEditorCommandProcessor, CodeEditorSnippetProcessor,
    CodeEditorMacroProcessor, CodeEditorSyntaxProcessor, CodeEditorThemeProcessor)
from .modes import CodeEditorBaseMode

from .highlighter import CodeEditorSyntaxHighlighter
from .models import (SymbolListModel, BookmarkListModel, FoldingListModel,
    bundleItemSelectableModelFactory, bookmarkSelectableModelFactory,
    symbolSelectableModelFactory)

from prymatex.utils import text, encoding
from prymatex.utils.i18n import ugettext as _
from functools import reduce

class CodeEditor(PrymatexEditor, TextEditWidget):
    STANDARD_SIZES = (70, 78, 80, 100, 120)
    MAX_FOLD_LEVEL = 10
    
    # -------------------- Signals
    aboutToSave = QtCore.Signal()
    saved = QtCore.Signal()
    aboutToClose = QtCore.Signal()
    closed = QtCore.Signal()

    syntaxChanged = QtCore.Signal(object)
    themeChanged = QtCore.Signal(object)
    filePathChanged = QtCore.Signal(str)
    
    modeChanged = QtCore.Signal(object)

    queryCompletions = QtCore.Signal(bool)
    newLocationMemento = QtCore.Signal(object)
    keyPressed = QtCore.Signal(QtCore.QEvent)
    
    # ------------------ Flags
    ShowTabsAndSpaces     = 1<<0
    ShowLineAndParagraphs = 1<<1
    WordWrap              = 1<<2
    MarginLine            = 1<<3
    IndentGuide           = 1<<4
    HighlightCurrentLine  = 1<<5

    # ------------------- Settings
    remove_trailing_spaces = ConfigurableItem(default=False)
    auto_brackets = ConfigurableItem(default=True)
    smart_home_smart_end = ConfigurableItem(default=True)
    enable_auto_completion = ConfigurableItem(default=True)
    word_length_to_complete = ConfigurableItem(default=3)

    adjust_indentation_on_paste = ConfigurableItem(default=False)
    encoding = ConfigurableItem(default='utf_8')

    @ConfigurableItem(default=80)
    def margin_line_size(self, size):
        self.viewport().update()

    @ConfigurableItem(default=Qt.QWIDGETSIZE_MAX)
    def word_wrap_size(self, size):
        # TODO: Ver que hacer con este offset tan feo de 2
        size = (size * self.characterWidth()) + 2
        self.viewport().setMaximumWidth(size < Qt.QWIDGETSIZE_MAX \
            and size or Qt.QWIDGETSIZE_MAX)
    
    @ConfigurableItem(default=True)
    def indent_using_spaces(self, soft):
        self.setSoftTabs(soft)

    @ConfigurableItem(default=4)
    def indentation_width(self, size):
        self.setTabSize(size)
        self.viewport().update()

    @ConfigurableItem(default=("Monospace", 10))
    def default_font(self, value):
        font = QtGui.QFont(*value)
        font.setStyleStrategy(QtGui.QFont.ForceIntegerMetrics)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.setFont(font)

    @ConfigurableItem(default="3130E4FA-B10E-11D9-9F75-000D93589AF6", tm_name='OakDefaultLanguage')
    def default_syntax(self, uuid):
        self._default_syntax = self.application().supportManager.getBundleItem(uuid)
        if self._default_syntax is None:
            # Load original default syntax
            self._default_syntax = self.application().supportManager.getBundleItem(self._settings.default("defaultSyntax"))
        self.insertBundleItem(self._default_syntax)

    @ConfigurableItem(default='766026CB-703D-4610-B070-8DE07D967C5F', tm_name='OakThemeManagerSelectedTheme')
    def default_theme(self, uuid):
        self._default_theme = self.application().supportManager.getBundleItem(uuid)
        if self._default_theme is None:
            # Load original default theme
            self._default_theme = self.application().supportManager.getBundleItem(self._settings.default("defaultTheme"))
        self.insertBundleItem(self._default_theme)

    @ConfigurableItem(default=MarginLine | IndentGuide | HighlightCurrentLine)
    def default_flags(self, flags):
        self.setFlags(flags)

    # --------------------- init
    def __init__(self, **kwargs):
        super(CodeEditor, self).__init__(**kwargs)
        
        # By default
        self.showMarginLine = True
        self.showIndentGuide = True
        self.showHighlightCurrentLine = True

        # Cursors
        self.__text_cursors = []
        self.__highlight_cursors = []

        # Modes
        self.__modes = []
        
        # Command api
        self.__command_history = []
        self.__command_index = -1
        self.__last_content = ""

        # Processors
        self.processors = [
            CodeEditorSnippetProcessor(self),
            CodeEditorCommandProcessor(self),
            CodeEditorSyntaxProcessor(self),
            CodeEditorMacroProcessor(self),
            CodeEditorThemeProcessor(self)
        ]

        # Highlighter
        self.syntaxHighlighter = CodeEditorSyntaxHighlighter(self)

        # Sidebars
        self.leftBar = CodeEditorSideBar(self)
        self.rightBar = CodeEditorSideBar(self)

        #Models
        self.bookmarkListModel = BookmarkListModel(self)
        self.symbolListModel = SymbolListModel(self)
        self.foldingListModel = FoldingListModel(self)
        self.bundleItemSelectableModel = bundleItemSelectableModelFactory(self)
        self.symbolSelectableModel = symbolSelectableModelFactory(self)

        # Custom context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showEditorContextMenu)

        # Sidebars signals
        self.rightBar.updateRequest.connect(self.updateViewportMargins)
        self.leftBar.updateRequest.connect(self.updateViewportMargins)

        # Document signals
        self.document().undoCommandAdded.connect(self.on_document_undoCommandAdded)
        self.document().contentsChange.connect(self.on_document_contentsChange)

        # Editor signals
        self.updateRequest.connect(self.updateSideBars)
        self.themeChanged.connect(self._update_highlight)
        self.cursorPositionChanged.connect(self._update_highlight)
        self.cursorPositionChanged.connect(self._update_position)

        self.syntaxChanged.connect(lambda syntax, editor=self: 
            editor.showMessage("Syntax changed to <b>%s</b>" % syntax.name)
        )
        
    def highlighter(self):
        return self.syntaxHighlighter

    def window(self):
        parent = self.parent()
        while parent and not isinstance(parent, QtWidgets.QMainWindow):
            parent = parent.parent()
        return parent

    # OVERRIDE: PrymatexEditor.initialize()
    def initialize(self, **kwargs):
        super(CodeEditor, self).initialize(**kwargs)
        
        # Update properties
        self._update_properties()
        self.syntaxChanged.connect(self._update_properties)
        self.filePathChanged.connect(self._update_properties)
        self.application().supportManager.propertiesChanged.connect(self._update_properties)

        # Get dialogs
        self.selectorDialog = self.window().findChild(QtWidgets.QDialog, "SelectorDialog")
        self.browserDock = self.window().findChild(QtWidgets.QDockWidget, "BrowserDock")

    def finalize(self):
        self.application().supportManager.propertiesChanged.disconnect(self._update_properties)
        
    def _update_properties(self, *args, **kwargs):
        properties = self.propertiesSettings()
        if properties.lineEndings:
            self.setEolChars(properties.lineEndings)
        if properties.encoding:
            self.encoding = properties.encoding
        # Font
        if properties.fontName:
            font = QtGui.QFont(properties.fontName)
        else:
            font = self.font()
        if properties.fontSize:
            font.setPointSize(properties.fontSize)
        self.setFont(font)
        if properties.showInvisibles is not None:
            flags = self.getFlags()
            invisibles = self.ShowTabsAndSpaces | self.ShowLineAndParagraphs
            if properties.showInvisibles:
                flags = flags | invisibles 
            else:
                flags = flags & ~invisibles
            self.setFlags(flags)
        if properties.spellChecking is not None:
            pass
        if properties.softWrap is not None:
            pass
        if properties.wrapColumn:
            pass
        if properties.softTabs is not None:
            self.setSoftTabs(properties.softTabs)
        if properties.tabSize:
            self.setTabSize(properties.tabSize)
        if properties.theme:
            theme = self.application().supportManager.getBundleItem(properties.theme)
            if theme is not None:
                self.insertBundleItem(theme)

    # -------------- Extra Cursors
    def clearExtraCursors(self):
        changed = len(self.__text_cursors) > 0
        self.__text_cursors = []
        if changed:
            self.cursorPositionChanged.emit()

    def setTextCursors(self, cursors):
        assert len(cursors) > 0, "Cursors should contain at last one cursor"
        currents = self.textCursors()
        changed = len(currents) != len(cursors) or \
            any(map(lambda cs: cs[0] != cs[1], zip(currents, cursors)))
        if changed:
            self.__text_cursors = cursors[1:]
            self.setTextCursor(cursors[0])
            if self.textCursor() == currents[0]: 
                self.cursorPositionChanged.emit()

    def textCursors(self):
        return [self.textCursor()] + [QtGui.QTextCursor(c) for c in self.__text_cursors]  
    
    # -------------- Highlight Cursors
    def setHighlightCursors(self, cursors):
        self.__highlight_cursors = cursors
        self.viewport().update()

    def highlightCursors(self):
        return self.__highlight_cursors[:]
        
    # -------------- Editor Modes
    def beginMode(self, mode):
        self.__modes.append(mode)
        self.modeChanged.emit(mode)

    def endMode(self, mode):
        if mode == self.__modes[-1]:
            self.modeChanged.emit(self.__modes.pop())

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
    
    def addCodeEditorMode(self, mode):
        if not self.__modes:
            self.__modes.append(mode)

    # -------------------- Notifications
    def showMessage(self, *largs, **kwargs):
        return self.window().showMessage(*largs, **kwargs)
    
    # -------------------- Status
    def setStatus(self, key, value, timeout=None):
        return self.window().setStatus(key, value, timeout)

    def status(self, key):
        return self.window().status(key)

    def eraseStatus(self, key):
        return self.window().eraseStatus(key)

    # OVERRIDE: TextEditWidget.setPlainText()
    def setPlainText(self, text):
        self.syntaxHighlighter.stop()
        super(CodeEditor, self).setPlainText(text)
        self.syntaxHighlighter.start()

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
        self.aboutToSave.emit()
        self.encoding = self.application().fileManager.writeFile(filePath, self.toPlainTextWithEol(), self.encoding)
        super(CodeEditor, self).save(filePath)
        self.window().setStatus("saved", "Saved %s (%s)" % (filePath, self.encoding), 2000)
        self.saved.emit()

    def close(self):
        self.aboutToClose.emit()
        super(CodeEditor, self).close()
        self.closed.emit()

    def reload(self):
        super(CodeEditor, self).reload()
        content, self.encoding = self.application().fileManager.readFile(self.filePath())
        self.updatePlainText(content)

    # ------------ Component State save and restore
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
        extension = self.application().fileManager.extension(filePath)
        syntax = self.application().supportManager.findSyntaxByFileType(extension)
        if syntax is not None:
            self.insertBundleItem(syntax)
        self.filePathChanged.emit(filePath)

    def fileFilters(self):
        return [ "%s (%s)" % (self.syntax().bundle.name, " ".join(["*." + ft for ft in self.syntax().fileTypes])) ]
        #return PrymatexEditor.fileFilters(self)

    # ---------------------- Scopes
    def scope(self, cursor):
        left_syntax_scope, right_syntax_scope = self.blockUserData(cursor.block()).syntaxScope(cursor)
        left_cursor_scope, right_cursor_scope = self.application().supportManager.cursorScope(cursor)
        auxiliary_scope = self.application().supportManager.auxiliaryScope(self.filePath())
        return (left_syntax_scope + left_cursor_scope + auxiliary_scope, 
            right_syntax_scope + right_cursor_scope + auxiliary_scope)
        
    def preferenceSettings(self, cursor=None):
        return self.application().supportManager.getPreferenceSettings(
            *self.scope(cursor or self.textCursor())
        )

    def propertiesSettings(self, cursor=None):
        return self.application().supportManager.getPropertiesSettings(
            self.filePath(), *self.scope(cursor or self.textCursor())
        )
    
    # --------------- Block User Data
    def blockUserData(self, block):
        return block.userData() or self.findProcessor("syntax").emptyUserData()

    def isBlockReady(self, block):
        return block.isValid() and self.findProcessor("syntax").testRevision(block)

    # ------------ Obteniendo datos del editor
    def currentMode(self):
        return self.__modes[-1]
    
    def defaultMode(self):
        return self.__modes[0]

    def isModeActive(self, mode):
        return mode in self.__modes

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
            cursors = self.textCursors()
            if len(cursors) > 1:
                topLeft = self.cursorRect(self.newCursorAtPosition(cursors[0].selectionStart())).topLeft()
                bottomRight = self.cursorRect(self.newCursorAtPosition(cursors[-1].selectionEnd())).bottomRight()
                self.viewport().update(QtCore.QRect(topLeft, bottomRight))

    def updateSideBarsGeometry(self):
        cr = self.contentsRect()
        self.leftBar.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.leftBar.width(), cr.height()))
        rightBarPosition = cr.right() - self.rightBar.width()
        if self.verticalScrollBar().isVisible():
            rightBarPosition -= self.verticalScrollBar().width()
        self.rightBar.setGeometry(QtCore.QRect(rightBarPosition, cr.top(), self.rightBar.width(), cr.height()))

    # -------------- Completions
    def _query_completions(self, automatic=True):
        print("Go")
        """Trigger completion"""
        if not self.isCompletionWidgetVisible():
            self.queryCompletions.emit(automatic)
        
    # -------------- Smart Typing Pairs
    def _smart_typing_pairs(self, cursor):
        settings = self.preferenceSettings(cursor)
        return self._find_all_pairs(cursor, 
            [pair[0] for pair in settings.smartTypingPairs], 
            [pair[1] for pair in settings.smartTypingPairs]
        )

    # -------------- Highlight Pairs    
    def _highlight_pairs(self, cursor):
        settings = self.preferenceSettings(cursor)
        return self._find_all_pairs(cursor, 
            [pair[0] for pair in settings.highlightPairs], 
            [pair[1] for pair in settings.highlightPairs]
        )
        
    def _find_all_pairs(self, cursor, open_pairs, close_pairs):
        left_char = cursor.document().characterAt(cursor.position() - 1)
        right_char = cursor.document().characterAt(cursor.position())

        #Current pairs for cursor position (left <|> right, oppositeLeft, oppositeRight)
        # <|> the cursor is allways here
        pairs = (None, None, None, None)

        # TODO si no hay para uno no hay para ninguno, quitar el que esta si el findPairCursor retorna Null
        if left_char in open_pairs:
            leftCursor = QtGui.QTextCursor(cursor)
            leftCursor.movePosition(QtGui.QTextCursor.PreviousCharacter, QtGui.QTextCursor.KeepAnchor)
            index = open_pairs.index(left_char)
            otherBrace = self.findPairCursor(left_char, close_pairs[index], leftCursor)
            if not otherBrace.isNull():
                pairs = (leftCursor, None, otherBrace, None)
        if right_char in open_pairs:
            rightCursor = QtGui.QTextCursor(cursor)
            rightCursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
            index = open_pairs.index(right_char)
            otherBrace = self.findPairCursor(right_char, close_pairs[index], rightCursor)
            if not otherBrace.isNull():
                pairs = (pairs[0], rightCursor, pairs[2], otherBrace)
        if left_char in close_pairs and pairs[0] is None:  #Tener uno implica tener los dos por el if
            leftCursor = QtGui.QTextCursor(cursor)
            leftCursor.movePosition(QtGui.QTextCursor.PreviousCharacter, QtGui.QTextCursor.KeepAnchor)
            otherBrace = self.findPairCursor(left_char, open_pairs[close_pairs.index(left_char)], leftCursor, True)
            if not otherBrace.isNull():
                pairs = (leftCursor, pairs[1], otherBrace, pairs[3])
        if right_char in close_pairs and pairs[1] is None: #Tener uno implica tener los dos por el if
            rightCursor = QtGui.QTextCursor(cursor)
            rightCursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
            otherBrace = self.findPairCursor(right_char, open_pairs[close_pairs.index(right_char)], rightCursor, True)
            if not otherBrace.isNull():
                pairs = (pairs[0], rightCursor, pairs[2], otherBrace)
        return pairs

    # ------------ Find functions
    def findMatch(self, match, flags, cursor=None, cyclic=False):
        cursor = self.findMatchCursor(match, flags, cursor=cursor)
        if cursor.isNull() and cyclic:
            cursor = QtGui.QTextCursor(self.document())
            if flags & self.FindBackward:
                cursor.movePosition(QtGui.QTextCursor.End)
            cursor = self.findMatchCursor(match, flags, cursor=cursor)
        if not cursor.isNull():
            self.setTextCursor(cursor)
        return not cursor.isNull()

    def findAll(self, match, flags):
        cursors = self.findAllCursors(match, flags)
        if cursors:
            self.setTextCursors(cursors)
            return True
        return False

    # ------------- Replace functions
    def replaceMatch(self, match, text, flags, all_text=False, cursor=None):
        cursor = QtGui.QTextCursor(cursor) if cursor else self.textCursor()
        if cursor.hasSelection():
            cursor.setPosition((flags & self.FindBackward) and cursor.selectionEnd() or cursor.selectionStart())
        if all_text:
            cursor.movePosition(QtGui.QTextCursor.Start)
        cursor.beginEditBlock()
        replaced = 0
        findCursor = cursor
        while True:
            findCursor = self.findMatchCursor(match, flags, cursor=findCursor)
            if findCursor.isNull(): break
            if flags & self.FindRegularExpression:
                findCursor.insertText(
                    re.sub(match.pattern(), text, self.selectedText(findCursor)))
            else:
                findCursor.insertText(text)
            replaced += 1
            if not all_text:
                self.setTextCursor(findCursor)
                break
        cursor.endEditBlock()
        return replaced

    def _update_position(self):
        cursor = self.textCursor()
        st = []
        if cursor.hasSelection():
            start, end = self.selectionBlockStartEnd(cursor)
            if start != end:
                st.append('%d lines' % (end.blockNumber() - start.blockNumber() + 1))
            st.append('%d characters selected' % (cursor.selectionEnd() - cursor.selectionStart()))
        else:
            st.append('Line %d' % (cursor.blockNumber() + 1))
            st.append('Column %d' % (cursor.positionInBlock() + 1))
        self.window().setStatus('position', ', '.join(st))

    #-------------------- Highlight Editor on signal trigger
    def _update_highlight(self):
        selections = []
        lines = []
        pairs = []
        current = self.textCursor()
        for cursor in self.textCursors():
            if cursor.hasSelection() and current != cursor:
                selections.append(QtGui.QTextCursor(cursor))
            cursor.clearSelection()
            if self.showHighlightCurrentLine and not any(
                filter(lambda c: c.block() == cursor.block(), lines)):
                lines.append(cursor)
            pairs.extend([c for c in self._highlight_pairs(cursor) if c is not None])

        # Extra cursors selection
        self.setExtraSelectionCursors("dyn.selection", selections)
        # Current line
        self.setExtraSelectionCursors("dyn.highlight.line", lines)
        # Pairs
        self.setExtraSelectionCursors("dyn.highlight.pairs", pairs)
        self.updateExtraSelections()

    # OVERRIDE: TextEditWidget.setPalette()
    def setPalette(self, palette):
        super(CodeEditor, self).setPalette(palette)
        self.viewport().setPalette(palette)
        self.leftBar.setPalette(palette)
        self.rightBar.setPalette(palette)
        
        # Register selection textCharFormat
        # Register lineHighlight textCharFormat
        textCharFormat = QtGui.QTextCharFormat()
        textCharFormat.setBackground(palette.highlight().color())
        self.registerTextCharFormat("dyn.selection", textCharFormat)
        
        # Register lineHighlight textCharFormat
        textCharFormat = QtGui.QTextCharFormat()
        textCharFormat.setBackground(palette.alternateBase().color())
        textCharFormat.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        self.registerTextCharFormat("dyn.highlight.line", textCharFormat)
        
        # Register highlightPairs textCharFormat
        textCharFormat = QtGui.QTextCharFormat()
        textCharFormat.setFontUnderline(True)
        textCharFormat.setBackground(palette.alternateBase().color())
        textCharFormat.setUnderlineColor(palette.text().color())
        textCharFormat.setBackground(QtCore.Qt.transparent)
        self.registerTextCharFormat("dyn.highlight.pairs", textCharFormat)

        for component in self.components():
            component.setPalette(palette)

    # OVERRIDE: TextEditWidget.setFont()
    def setFont(self, font):
        super(CodeEditor, self).setFont(font)
        self.setTabStopWidth(self.tabSize() * self.characterWidth())
        for component in self.components():
            component.setFont(font)

    # OVERRIDE: TextEditWidget.resizeEvent()
    def resizeEvent(self, event):
        super(CodeEditor, self).resizeEvent(event)
        self.updateSideBarsGeometry()

    # OVERRIDE: TextEditWidget.paintEvent()
    def paintEvent(self, event):
        super(TextEditWidget, self).paintEvent(event)

        painter = QtGui.QPainter(self.viewport())
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        cursorPosition = self.getPaintContext().cursorPosition
        page_bottom = self.viewport().height()
        characterWidth = self.characterWidth()
        characterHeight = self.characterHeight()

        highlight = self.highlightCursors()
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

                # -------------- Folding Image
                if self.foldingListModel.isFolded(self.newCursorAtPosition(block.position())):
                    painter.setPen(self.palette().base().color())
                    painter.drawPixmap(characterWidth * block.length() + offset.x() + 10,
                        positionY + characterHeight - self.foldingListModel.foldingellipsisImage.height(),
                        self.foldingListModel.foldingellipsisImage)

                # -------------- Indent guide
                if self.showIndentGuide:
                    painter.setPen(self.palette().highlight().color())
                    blockPattern = block
                    while blockPattern.isValid() and self.blockUserData(blockPattern).blank:
                        blockPattern = blockPattern.next()
                    if blockPattern.isValid():
                        indentLen = len(self.blockUserData(blockPattern).indentation)
                        padding = characterWidth + offset.x()
                        for s in range(0, indentLen // self.indentation_width):
                            positionX = (characterWidth * self.indentation_width * s) + padding
                            painter.drawLine(positionX, positionY, positionX, positionY + characterHeight)
                
                # -------------- Highlight Cursors
                painter.setPen(self.palette().brightText().color())
                for c in [c for c in highlight if c.block() == block and c.hasSelection()]:
                    topLeft = self.cursorRect(self.newCursorAtPosition(c.selectionStart())).topLeft()
                    bottomRight = self.cursorRect(self.newCursorAtPosition(c.selectionEnd())).bottomRight()
                    painter.drawRoundedRect(
                        QtCore.QRect(topLeft, bottomRight), 
                        0.2 * characterWidth,
                        0.2 * characterWidth)

            block = block.next()

        if self.showMarginLine:
            painter.setPen(self.palette().highlight().color())
            pos_margin = characterWidth * self.margin_line_size
            painter.drawLine(pos_margin + offset.x(), 0, pos_margin + offset.x(), self.viewport().height())

        # -------------- Extra Cursors
        if cursorPosition != -1:
            painter.setPen(self.palette().brightText().color())
            for c in self.textCursors()[1:]:
                rec = self.cursorRect(c)
                painter.drawLine(rec.x(), rec.y(), rec.x(), rec.y() + characterHeight)

        painter.end()

    # -------------- Event handling
    def keyPress_handlers(self, event):
        for mode in self.__modes[::-1]:
            for handler in mode.keyPress_handlers(event):
                yield handler
     
    def _handle_event(self, handlers, event):
        for handler in handlers:
            yield handler(event)
    
    # OVERRIDE: TextEditWidget.keyPressEvent()
    def keyPressEvent(self, event):
        if not any(self._handle_event(self.keyPress_handlers(event), event)):
            super(CodeEditor, self).keyPressEvent(event)
            self.keyPressed.emit(event)

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

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self._update_position()

    # --------------- Key press pre and post
    def trySyntaxByText(self, cursor):
        text = cursor.block().text()[:cursor.positionInBlock()]
        syntax = self.application().supportManager.findSyntaxByFirstLine(text)
        if syntax is not None:
            self.insertBundleItem(syntax)
        
    # ------------ Insert API
    def insertNewLine(self, cursor = None):
        cursor = cursor or self.textCursor()
        # TODO: Is first line ? then try new syntax
        if cursor.blockNumber() == 0:
            self.trySyntaxByText(cursor)
        block = cursor.block()
        positionInBlock = cursor.positionInBlock()
        settings = self.preferenceSettings(cursor)

        indentationFlag = settings.indentationFlag(block.text()[:positionInBlock])

        tab_behavior = self.tabKeyBehavior()
        indentation = self.blockIndentation(block)

        if indentationFlag is constants.INDENT_INCREASE:
            self.logger().debug("Increase indentation")
            blockIndent = indentation + tab_behavior
        elif indentationFlag is constants.INDENT_NEXTLINE:
            #TODO: Creo que este no es el correcto
            self.logger().debug("Increase next line indentation")
            blockIndent = indentation + tab_behavior
        elif indentationFlag is constants.INDENT_UNINDENT:
            self.logger().debug("Unindent")
            blockIndent = ""
        elif indentationFlag is constants.INDENT_DECREASE:
            self.logger().debug("Decrease indentation")
            blockIndent = indentation[:-len(tab_behavior)]
        else:
            self.logger().debug("Preserve indentation")
            blockIndent = indentation[:positionInBlock]
        cursor.insertText("\n%s" % blockIndent)
        self.ensureCursorVisible()

    # ------------ Command API
    def commandHistory(self, index, modifying_only=False):
        index = self.__command_index + index
        if 0 <= index < len(self.__command_history):
            command = self.__command_history[index]
            if not modifying_only or command[0] in ('replace', 'delete', 'insert'):
                return command
        return (None, None, 0)

    def __run_command(self, name, args):
        repeat = 0
        if self.__command_history and \
            self.__command_history[-1][0] == name and \
            self.__command_history[-1][1] == args:
                repeat = self.__command_history[-1][2] + 1
        self.__command_history.append((name, args, repeat))
        self.__command_index = len(self.__command_history) - 1

    def on_document_contentsChange(self, position, charsRemoved, charsAdded):
        text = self.toPlainText()
        command = None
        if charsRemoved and charsAdded:
            command = ('replace', { 
                    'characters': self.__last_content[position:position + charsRemoved],
                    'by': text[position:position + charsAdded],
                    'position': position
                })
            if command[1]['characters'] == command[1]['by']:
                command = None
        elif charsRemoved:
            command = ('delete', { 
                    'characters': self.__last_content[position:position + charsRemoved],
                    'position': position
                })
        elif charsAdded:
            command = ('insert', { 
                    'characters': text[position:position + charsAdded],
                    'position': position
                })
        self.__last_content = text
        if command is not None:
            self.__run_command(*command)
        
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
                item = items[index]
                name = item.type()
                processor = self.findProcessor(name)
                processor.configure(**kwargs)
                self.__run_command("insert_%s" % name, item.dump(allKeys=True))
                item.execute(processor)

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

        current_text, start, end = self.currentText()
        current_word, start, end = self.currentWord()

        theme = self.theme()

        # Build environment
        environment.update({
            'TM_DISPLAYNAME': self.title(),
            'TM_CURRENT_LINE': line,
            'TM_LINE_INDEX': cursor.positionInBlock(),
            'TM_LINE_NUMBER': block.blockNumber() + 1,
            'TM_CURRENT_THEME_PATH': theme.currentSourcePath(),
            'TM_COLUMN_NUMBER': cursor.positionInBlock() + 1,
            'TM_MODE': self.syntax().name,
            'TM_SOFT_TABS': self.softTabs() and 'YES' or 'NO',
            'TM_TAB_SIZE': self.tabSize()
        })
        
        if self.isBlockReady(block):
            leftScope, rightScope = self.scope(cursor)
            environment['TM_SCOPE'] = "%s" % rightScope
            environment['TM_SCOPE_LEFT'] = "%s" % leftScope
        if current_word:
            self.logger().debug("Add current word to environment")
            environment['TM_CURRENT_WORD'] = current_word
        if current_text:
            self.logger().debug("Add current text to environment")
            environment['TM_CURRENT_TEXT'] = current_text
        if self.filePath():
            self.logger().debug("Add file path to environment")
            environment['TM_FILEPATH'] = self.filePath()
            environment['TM_FILENAME'] = self.application().fileManager.basename(self.filePath())
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

    # ---------- Folding
    def _find_indented_block_fold_close(self, cursor):
        assert self.foldingListModel.isFoldingIndentedBlockStart(cursor), "Block isn't folding indented start"
        block = cursor.block()
        indentation = self.blockUserData(block).indentation
        indentedBlock = self.findIndentedBlock(block, indentation=indentation, comparison=operator.le)
        while indentedBlock.isValid() and self.foldingListModel.isFoldingIndentedBlockIgnore(self.newCursorAtPosition(indentedBlock.position())):
            indentedBlock = self.findIndentedBlock(indentedBlock, indentation=indentation, comparison=operator.le)
        if indentedBlock.isValid():
            return self.findNoBlankBlock(indentedBlock, "up")
        else:
            return self.document().lastBlock()

    def _find_block_fold_peer(self, milestone, direction = "down"):
        """ Direction are 'down' or up"""
        block = milestone.block()
        if direction == "down":
            assert self.foldingListModel.isStart(milestone), "Block isn't folding start"
        else:
            assert self.foldingListModel.isStop(milestone), "Block isn't folding stop"
        if direction == "down" and self.foldingListModel.isFoldingIndentedBlockStart(milestone):
            block = self._find_indented_block_fold_close(milestone)
        else:
            nest = 0
            while block.isValid():
                cursor = self.newCursorAtPosition(block.position())
                if self.foldingListModel.isFoldingStartMarker(cursor):
                    nest += 1
                elif self.foldingListModel.isFoldingStopMarker(cursor):
                    nest -= 1
                if nest == 0:
                    break
                block = block.next() if direction == "down" else block.previous()
        if direction == "down":
            return milestone.block(), block
        return block, milestone.block()

    def _find_all_milestones_by_level(self):
        levels = {}
        def _collect(start, end, l):
            block = start
            while block != end:
                cursor = self.newCursorAtPosition(block.position())
                if self.foldingListModel.isStart(cursor):
                    new_start, new_end = self._find_block_fold_peer(cursor)
                    levels.setdefault(l, []).append(cursor)
                    block = _collect(new_start.next(), new_end, l + 1)
                else:
                    block = block.next()
            return block
        _collect(self.document().begin(), self.document().end(), 1)
        return levels
            
    def toggleFolding(self, milestone):
        if self.foldingListModel.isFoldingMarker(milestone):
            if self.foldingListModel.isFolded(milestone):
                self.foldingListModel.unfold(milestone)
            else:
                startBlock, endBlock = self._find_block_fold_peer(milestone, 
                    self.foldingListModel.isStop(milestone) and "up" or "down")
                
                if startBlock.isValid() and endBlock.isValid():
                    # Go!
                    self.foldingListModel.fold(
                        self.newCursorAtPosition(startBlock.position()),
                        self.newCursorAtPosition(endBlock.position())
                    )

    # ---------- Override convert tabs <---> spaces
    def convertTabsToSpaces(self):
        match = "\t"
        self.replaceMatch(match, " " * self.tabWidth, QtGui.QTextDocument.FindFlags(), True)

    def convertSpacesToTabs(self):
        match = " " * self.tabWidth
        self.replaceMatch(match, "\t", QtGui.QTextDocument.FindFlags(), True)

    # -------------- Add select text functions
    def selectEnclosingBrackets(self, cursor=None):
        cursor = cursor or self.textCursor()
        settings = self.preferenceSettings(cursor)
        flags = QtGui.QTextDocument.FindFlags()
        flags |= QtGui.QTextDocument.FindBackward
        foundCursors = [(self.document().find(openBrace_closeBrace[0], cursor.selectionStart(), flags), openBrace_closeBrace[1]) for openBrace_closeBrace in settings.highlightPairs]
        openCursor = reduce(lambda c1, c2: (not c1[0].isNull() and c1[0].selectionEnd() > c2[0].selectionEnd()) and c1 or c2, foundCursors)
        if not openCursor[0].isNull():
            closeCursor = self.findPair(openCursor[0].selectedText(), openCursor[1], openCursor[0])
            if openCursor[0].selectionEnd() <= cursor.selectionStart() <= closeCursor.selectionStart():
                # TODO New cursor at position
                cursor.setPosition(openCursor[0].selectionEnd())
                cursor.setPosition(closeCursor.selectionStart(), QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)

    def selectScope(self, cursor=None):
        cursor = cursor or self.textCursor()
        start, end = self.blockUserData(cursor.block()).scopePosition(cursor)
        self.setTextCursor(self.newCursorAtPosition(start, end))

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
        while block.isValid() and self.blockUserData(block).blank:
            block = block.next() if direction == "down" else block.previous()
        return block

    def findIndentedBlock(self, block, indentation = None, direction = "down", comparison = operator.eq):
        """ Return equal indentation block """
        if indentation is None:
            indentation_block = block if not self.blockUserData(block).blank else self.findNoBlankBlock(block, direction)
            indentation = self.blockIndentation(indentation_block)
        block = self.findNoBlankBlock(block, direction)
        while block.isValid() and not comparison(self.blockIndentation(block), indentation):
            block = self.findNoBlankBlock(block, direction)
        return block

    # --------------- Menus
    # Flat Popup Menu
    def showFlatPopupMenu(self, menuItems, callback, cursorPosition = True):
        menu = QtWidgets.QMenu(self)
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
            items += addon.contributeToContextMenu(cursor=cursor)

        if len(items) > 1:
            actions = extend_menu(menu, items)

        menu.popup(self.viewport().mapToGlobal(point))

    # Contributes to Tab Menu
    def contributeToTabMenu(self):
        menues = []
        bundleMenu = self.application().supportManager.menuForBundle(self.syntax().bundle)
        if bundleMenu is not None:
            menues.append(bundleMenu)
            menues.append("-")
        if self.filePath() is not None:
            menues.extend([
                {   "text": "Path to Clipboard",
                    "triggered": lambda checked, ed=self: self.application().clipboard().setText(ed.filePath())  },
                {   "text": "Name to Clipboard",
                    "triggered": lambda checked, ed=self: \
                        self.application().clipboard().setText(
                            ed.application().fileManager.basename(ed.filePath())
                        )  
                },
                {   "text": "Directory to Clipboard",
                    "triggered": lambda checked, ed=self: \
                        self.application().clipboard().setText(
                            ed.application().fileManager.dirname(ed.filePath())
                        )  
                }
                ])
        return menues

    # Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls):
        menu = {}
        menu["edit"] = [
            '-',
            {'text': '&Mode',
             'name': 'mode',
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

        menu["edit"] = [
            {'before': 'delete',
             'text': '&Paste and Indent',
             'triggered': lambda ed, checked=False: ed.zoomIn()
            }, {'before': 'delete',
             'text': '&Paste from History',
             'testEnabled': lambda ed: False,
             'triggered': lambda ed, checked=False: ed.zoomIn()
            }
        ]

        menu["view"] = [
            '-',
            {'text': "Zoom In",
              'sequence': ("Editor", "ZoomIn"),
              'triggered': lambda ed, checked=False: ed.zoomIn()},
             {'text': "Zoom Out",
              'sequence': ("Editor", "ZoomOut"),
              'triggered': lambda ed, checked=False: ed.zoomOut()},
            '-',
            {'name': 'leftGutter',
             'text': 'Left Gutter',
             'items': []},
            {'name': 'rightGutter',
             'text': 'Right Gutter',
             'items': []
            }, '-',
            {'text': "Code Folding",
             'items': [{
                    'text': "Fold",
                    'triggered': cls.on_actionFold_triggered,
                    'sequence': ("Editor", "Fold", 'Ctrl+Shift+['),
                }, {
                    'text': "Unfold",
                    'triggered': cls.on_actionUnfold_triggered,
                    'sequence': ("Editor", "Unfold", 'Ctrl+Shift+]'),
                }, {
                    'text': "Unfold All",
                    'triggered': cls.on_actionUnfoldAll_triggered
                }, "-" ] + [ tuple([ {
                    'text': "Fold Level %s" % level,
                    'triggered': lambda ed, checked, level=level: ed.on_actionFold_triggered(checked, level=level)
                } for level in range(1, cls.MAX_FOLD_LEVEL) ]) ] + [ 
                    '-', {
                    'text': "Fold Tab Attributes",
                    'triggered': cls.on_actionFold_triggered
                }]
            },
            {'text': "Word Wrap",
             'items': [{
                    'text': "Enabled",
                    'checkable': True,
                    'triggered': lambda ed, checked: ed.on_actionWordWrap_triggered(checked, size=Qt.QWIDGETSIZE_MAX),
                    'testChecked': lambda ed: bool(ed.getFlags() & ed.WordWrap)
                }, "-" ] + [ tuple(
                [{
                    'text': "Automatic",
                    'checkable': True,
                    'triggered': lambda ed, checked: ed.on_actionWordWrap_triggered(checked, size=Qt.QWIDGETSIZE_MAX),
                    'testChecked': lambda ed: bool(ed.getFlags() & ed.WordWrap) and ed.wordWrapSize == Qt.QWIDGETSIZE_MAX
                }] + [{
                    'text': "%s" % size,
                    'checkable': True,
                    'triggered': lambda ed, checked, size=size: ed.on_actionWordWrap_triggered(checked, size=size),
                    'testChecked': lambda ed, size=size: bool(ed.getFlags() & ed.WordWrap) and \
                        ed.wordWrapSize == size
                } for size in cls.STANDARD_SIZES]) ]
            },
            {'text': "Margin Line",
             'items': [{
                    'text': "Enabled",
                    'checkable': True,
                    'triggered': cls.on_actionMarginLine_triggered,
                    'testChecked': lambda ed: bool(ed.getFlags() & ed.MarginLine)
                }, "-" ] + [ tuple([ {
                    'text': "%s" % size,
                    'checkable': True,
                    'triggered': lambda ed, checked, size = size: ed.on_actionMarginLine_triggered(checked, size = size),
                    'testChecked': lambda ed, size = size: bool(ed.getFlags() & ed.MarginLine) and \
                        ed.margin_line_size == size
                } for size in cls.STANDARD_SIZES]) ]
            }, '-',
            {'text': "Indent Guide",
             'checkable': True,
             'triggered': cls.on_actionIndentGuide_triggered,
             'testChecked': lambda ed: bool(ed.getFlags() & ed.IndentGuide)
            },
            {'text': "Highlight Current Line",
             'checkable': True,
             'triggered': cls.on_actionHighlightCurrentLine_triggered,
             'testChecked': lambda ed: bool(ed.getFlags() & ed.HighlightCurrentLine)
            },
            {'text': "Show Tabs and Spaces",
             'checkable': True,
             'triggered': cls.on_actionShowTabsAndSpaces_triggered,
             'testChecked': lambda ed: bool(ed.getFlags() & ed.ShowTabsAndSpaces) },
            {'text': "Show Line and Paragraph",
             'checkable': True,
             'triggered': cls.on_actionShowLineAndParagraphs_triggered,
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
                     'triggered': lambda ed, checked=False: ed.selectWord(),
                     'sequence': ("Editor", "SelectWord", 'Ctrl+Meta+W'),
                     },
                    {'text': '&Text',
                     'triggered': lambda ed, checked=False: ed.selectText(),
                     'sequence': ("Editor", "SelectText", 'Ctrl+Meta+T'),
                     },
                    {'text': '&Line',
                     'triggered': lambda ed, checked=False: ed.selectLine(),
                     'sequence': ("Editor", "SelectLine", 'Ctrl+Meta+L'),
                     },
                    {'text': '&Paragraph',
                     'triggered': lambda ed, checked=False: ed.selectParagraph()
                     },
                    {'text': 'Enclosing &brackets',
                     'triggered': lambda ed, checked=False: ed.selectEnclosingBrackets(),
                     'sequence': ("Editor", "SelectEnclosingBrackets", 'Ctrl+Meta+B'),
                     },
                    {'text': '&Scope',
                     'triggered': lambda ed, checked=False: ed.selectScope(),
                     'sequence': ("Editor", "SelectScope", 'Ctrl+Meta+S'),
                     },
                    {'text': '&All',
                     'triggered': lambda ed, checked=False: ed.selectDocument(),
                     'sequence': ("Editor", "SelectAll", 'Ctrl+A'),
                     }
                ]},
                {'text': 'Convert',
                 'items': [
                    {'text': 'Uppercase',
                     'sequence': ("Editor", "ConvertUppercase", 'Ctrl+U'),
                     'triggered': lambda ed, checked=False: ed.convertToUppercase(),
                     },
                    {'text': 'Lowercase',
                     'sequence': ("Editor", "ConvertLowercase", 'Ctrl+Shift+U'),
                     'triggered': lambda ed, checked=False: ed.convertToLowercase(),
                     },
                    {'text': 'Titlecase',
                     'sequence': ("Editor", "ConvertTitlecase", 'Ctrl+Alt+U'),
                     'triggered': lambda ed, checked=False: ed.convertToTitlecase(),
                     },
                    {'text': 'Opposite Case',
                     'sequence': ("Editor", "ConvertOppositeCase", 'Ctrl+G'),
                     'triggered': lambda ed, checked=False: ed.convertToOppositeCase(),
                     }, '-',
                    {'text': 'Tab to Spaces',
                     'triggered': lambda ed, checked=False: ed.convertTabsToSpaces(),
                     },
                    {'text': 'Spaces to Tabs',
                     'triggered': lambda ed, checked=False: ed.convertSpacesToTabs(),
                     }, '-',
                    {'text': 'Transpose',
                     'sequence': ("Editor", "ConvertTranspose", 'Ctrl+T'),
                     'triggered': lambda ed, checked=False: ed.convertTranspose(),
                     }
                ]}, '-',
                {'text': 'Indentation',
                 'items': [
                    {'text': 'Indent Using Spaces',
                     'checkable': True,
                     'triggered': lambda ed, checked: ed.on_actionIndentation_triggered(checked),
                     'testChecked': lambda ed: ed.indent_using_spaces
                     }, '-', ] + [ tuple([
                    {'text': 'Width: %d' % size,
                     'checkable': True,
                     'triggered': lambda ed, checked, size = size: ed.on_actionIndentation_triggered(ed.indent_using_spaces, size = size),
                     'testChecked': lambda ed, size = size: (ed.indent_using_spaces and ed.indentation_width == size) or (not ed.indent_using_spaces and ed.tabWidth == size)
                     } for size in range(1, 9) ]) ]
                },
                {'text': 'Line Endings',
                 'items': [tuple(
                     [{'text': '%s' % name,
                     'checkable': True,
                     'triggered': lambda ed, checked, eol_chars = eol_chars: ed.setEolChars(eol_chars),
                     'testChecked': lambda ed, eol_chars = eol_chars: ed.eolChars() == eol_chars
                     } for eol_chars, _, name in text.EOLS])
                ]},
                {'text': 'Encoding',
                 'items': [tuple(
                     [{'text': "%s (%s)" % (language.split(",")[0].title(), codec),
                     'checkable': True,
                     'triggered': lambda ed, checked, codec = codec: ed.on_actionEncoding_triggered(codec),
                     'testChecked': lambda ed, codec = codec: ed.encoding == codec
                     } for codec, aliases, language in encoding.CODECS])
                ]}, '-',
                {'text': 'Select Bundle Item',
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
                {'text': 'Toggle Bookmark',
                 'triggered': cls.toggleBookmark,
                 'sequence': ("Editor", "ToggleBookmark", 'Ctrl+F2'),
                 },
                {'text': 'Next Bookmark',
                 'triggered': cls.bookmarkNext,
                 'sequence': ("Editor", "NextBookmark", 'F2'),
                 },
                {'text': 'Previous Bookmark',
                 'triggered': cls.bookmarkPrevious,
                 'sequence': ("Editor", "PreviousBookmark", 'Shift+F2'),
                 },
                {'text': 'Clear Bookmarks',
                 'triggered': cls.clearBookmarks,
                 'sequence': ("Editor", "ClearBookmarks", 'Ctrl+Shift+F2'),
                 },
                {'text': 'Select All Bookmarks',
                 'triggered': cls.selectAllBookmarks,
                 'sequence': ("Editor", "SelectAllBookmarks", 'Alt+F2'),
                 }
            ]},
            "-",
            {'text': 'Go to &Symbol',
             'triggered': cls.on_actionGoToSymbol_triggered,
             'sequence': ("Editor", "GoToSymbol", 'Meta+Ctrl+Shift+O'),
             },
            {'text': 'Go to &Bookmark',
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
             },
            {'sequence': ("Editor", "CodeCompletion", 'Ctrl+Space'),
             'activated': self._query_completions,
             'context': QtCore.Qt.WidgetShortcut
             }
        ]

    # ------------------ Menu Actions
    def on_actionIndentation_triggered(self, checked, size = None):
        if size is None:
          size = self.indentation_width if self.indent_using_spaces else self.tabWidth
        self.indent_using_spaces = checked
        if self.indent_using_spaces:
            self.indentation_width = size
        else:
            self.tabWidth = size
        self.update()
        self.textChanged.emit()

    def on_actionEncoding_triggered(self, codec):
        if self.encoding != codec:
            self.encoding = codec
            self.textChanged.emit()

    def on_actionShowTabsAndSpaces_triggered(self, checked):
        if checked:
            flags = self.getFlags() | self.ShowTabsAndSpaces
        else:
            flags = self.getFlags() & ~self.ShowTabsAndSpaces
        self.setFlags(flags)

    def on_actionShowLineAndParagraphs_triggered(self, checked):
        if checked:
            flags = self.getFlags() | self.ShowLineAndParagraphs
        else:
            flags = self.getFlags() & ~self.ShowLineAndParagraphs
        self.setFlags(flags)

    def on_actionWordWrap_triggered(self, checked, size = None):
        if isinstance(size, int):
            self.wordWrapSize = size
        if checked:
            flags = self.getFlags() | self.WordWrap
        else:
            flags = self.getFlags() & ~self.WordWrap
        self.setFlags(flags)

    def on_actionHighlightCurrentLine_triggered(self, checked):
        if checked:
            flags = self.getFlags() | self.HighlightCurrentLine
        else:
            flags = self.getFlags() & ~self.HighlightCurrentLine
        self.setFlags(flags)

    def on_actionMarginLine_triggered(self, checked, size = None):
        if isinstance(size, int):
            self.margin_line_size = size
        if checked:
            flags = self.getFlags() | self.MarginLine
        else:
            flags = self.getFlags() & ~self.MarginLine
        self.setFlags(flags)

    def on_actionIndentGuide_triggered(self, checked):
        if checked:
            flags = self.getFlags() | self.IndentGuide
        else:
            flags = self.getFlags() & ~self.IndentGuide
        self.setFlags(flags)

    def on_actionSelectBundleItem_triggered(self, checked=False):
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

    def on_actionFold_triggered(self, checked=False, level=None):
        # if level then find folding for level number and fold
        if isinstance(level, int):
            milestones = self._find_all_milestones_by_level()
            if level in milestones:
                self.foldingListModel.unfoldall()
                for milestone in milestones.get(level, []):
                    self.toggleFolding(milestone)
        else:
            cursor = self.textCursor()
            start, end = self.selectionBlockStartEnd(cursor)
            milestone = start
            milestone_cursor = self.newCursorAtPosition(milestone.position())
            if start == end:
                while milestone.isValid() and (not self.foldingListModel.isStart(milestone_cursor) or \
                    self.foldingListModel.isFolded(milestone_cursor)):
                    milestone = self.findIndentedBlock(milestone, 
                        direction="up", comparison=operator.lt
                    )
                    milestone_cursor = self.newCursorAtPosition(milestone.position())
                if milestone.isValid():
                    self.toggleFolding(milestone_cursor)
                    if cursor.block() != milestone_cursor.block():
                        self.setTextCursor(milestone_cursor)
            else:
                # The cursor has selection, fold the selection
                self.foldingListModel.fold(
                    milestone_cursor,
                    self.newCursorAtPosition(end.position())
                )
                self.setCursorPosition(cursor.selectionStart())

    def on_actionUnfold_triggered(self, checked=False):
        start, end = self.selectionBlockStartEnd()
        block = start
        while block.isValid():
            self.foldingListModel.unfold(
                self.newCursorAtPosition(block.position())
            )
            if block == end:
                break
            block = block.next()

    def on_actionUnfoldAll_triggered(self, checked=False):
        self.foldingListModel.unfoldall()

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
