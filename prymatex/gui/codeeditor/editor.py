#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bisect import bisect
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QRect, Qt, SIGNAL
from PyQt4.QtGui import QTextEdit, QTextFormat, QMenu, \
    QTextCursor, QAction, QPalette, QPainter, QColor
    
from prymatex import resources
from prymatex.support import PMXSnippet, PMXMacro, PMXCommand, PMXSyntax, PMXPreferenceSettings
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core.base import PMXObject
from prymatex.core import exceptions
from prymatex.gui.central.editor import PMXBaseEditor
from prymatex.gui.codeeditor.sidebar import PMXSidebar
from prymatex.gui.codeeditor.processors import PMXCommandProcessor, PMXSnippetProcessor, PMXMacroProcessor
from prymatex.gui.codeeditor.helpers import KeyEquivalentHelper, TabTriggerHelper, SmartTypingHelper, PMXCursorsHelper, PMXCompleterHelper
from prymatex.gui.codeeditor.highlighter import PMXSyntaxHighlighter
from prymatex.gui.codeeditor.folding import PMXEditorFolding
from prymatex.gui.codeeditor.models import PMXSymbolListModel, PMXBookmarkListModel, PMXCompleterListModel

class PMXCodeEditor(QtGui.QPlainTextEdit, PMXObject, PMXBaseEditor):
    #=======================================================================
    # Signals
    #=======================================================================
    syntaxChanged = QtCore.pyqtSignal()
    bookmarkChanged = QtCore.pyqtSignal(QtGui.QTextBlock)
    symbolChanged = QtCore.pyqtSignal(QtGui.QTextBlock)
    foldingChanged = QtCore.pyqtSignal(QtGui.QTextBlock)
    textBlocksRemoved = QtCore.pyqtSignal()
    
    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'CodeEditor'
    
    defaultSyntax = pmxConfigPorperty(default = u'3130E4FA-B10E-11D9-9F75-000D93589AF6', tm_name = u'OakDefaultLanguage')
    tabStopSoft = pmxConfigPorperty(default = True)
    @pmxConfigPorperty(default = 4)
    def tabStopSize(self, size):
        """docstring for tabStopSize"""
        self.setTabStopWidth(size * 10)
    
    @pmxConfigPorperty(default = QtGui.QFont())
    def font(self, font):
        font.setStyleStrategy(QtGui.QFont.ForceIntegerMetrics | QtGui.QFont.PreferAntialias)
        font.setStyleHint(QtGui.QFont.Monospace)
        self.document().setDefaultFont(font)
    
    @pmxConfigPorperty(default = u'766026CB-703D-4610-B070-8DE07D967C5F', tm_name = u'OakThemeManagerSelectedTheme')
    def theme(self, uuid):
        theme = self.application.supportManager.getTheme(uuid)
        self.syntaxHighlighter.setTheme(theme)
        self.colours = theme.settings
        
        #Editor colours
        palette = self.palette()
        palette.setColor(QPalette.Active, QPalette.Text, self.colours['foreground'])
        palette.setColor(QPalette.Active, QPalette.Base, self.colours['background'])
        palette.setColor(QPalette.Inactive, QPalette.Base, self.colours['background'])
        palette.setColor(QPalette.Active, QPalette.Highlight, self.colours['selection'])
        palette.setColor(QPalette.Active, QPalette.AlternateBase, self.colours['invisibles'])
        self.setPalette(palette)
        
        #Sidebar colours
        self.sidebar.foreground = self.colours['foreground']
        self.sidebar.background = self.colours['gutter'] if 'gutter' in self.colours else self.colours['background']  
        
        self.syntaxHighlighter.rehighlight()
        self.highlightCurrentLine()
    
    #================================================================
    # Regular expresions
    #================================================================
    RE_WORD = re.compile('\w+')
    
    #================================================================
    # Selection types
    #================================================================
    SelectWord = QtGui.QTextCursor.WordUnderCursor #0
    SelectLine = QtGui.QTextCursor.LineUnderCursor #1
    SelectParagraph = QtGui.QTextCursor.BlockUnderCursor #2 este no es un paragraph pero no  importa
    SelectAll = QtGui.QTextCursor.Document #3
    SelectEnclosingBrackets = 4
    SelectCurrentScope = 5
    
    #================================================================
    # Editor Flags
    #================================================================
    ShowTabsAndSpaces = 0x01
    ShowLineAndParagraphs = 0x02
    ShowBookmarks = 0x04
    ShowLineNumbers = 0x08
    ShowFolding = 0x10
    
    #TODO: Move to the manager
    #Cache de preferencias
    PREFERENCE_CACHE = {}
    
    @property
    def tabKeyBehavior(self):
        return self.tabStopSoft and u' ' * self.tabStopSize or u'\t'
    
    def __init__(self, fileInfo = None, project = None, parent = None):
        QtGui.QPlainTextEdit.__init__(self, parent)
        PMXBaseEditor.__init__(self)
        #Sidebar
        self.sidebar = PMXSidebar(self)

        #Models
        self.bookmarks = PMXBookmarkListModel(self)
        self.symbols = PMXSymbolListModel(self)
        
        #Folding
        self.folding = PMXEditorFolding(self)
        
        #Helpers
        self.cursors = PMXCursorsHelper(self)
        self.completer = PMXCompleterHelper(self)
        
        #Processors
        self.commandProcessor = PMXCommandProcessor(self)
        self.macroProcessor = PMXMacroProcessor(self)
        self.snippetProcessor = PMXSnippetProcessor(self)

        #Install editor helpers OverwriteText for testing
        self.editorHelpers = [  KeyEquivalentHelper(self), 
                                TabTriggerHelper(self),
                                SmartTypingHelper(self),
                                self.completer,
                                self.cursors ]

        #Set syntax for fileInfo
        syntax = None
        if fileInfo is not None:
            syntax = self.application.supportManager.findSyntaxByFileType(fileInfo.completeSuffix())
        if syntax is None:
            syntax = self.application.supportManager.getBundleItem(self.defaultSyntax)
        self.setSyntax(syntax)

        self.connectSignals()
        self.configure()

    #=======================================================================
    # Connect Signals
    #=======================================================================
    def connectSignals(self):
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.modificationChanged.connect(self.updateTabStatus)

    def updateTabStatus(self):
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))

    #=======================================================================
    # Base Editor Interface
    #=======================================================================
    def isModified(self):
        return self.document().isModified()
    
    def isEmpty(self):
        return self.document().isEmpty()
        
    def setModified(self, modified):
        self.document().setModified(modified)
        
    def setFileInfo(self, fileInfo):
        syntax = self.application.supportManager.findSyntaxByFileType(fileInfo.completeSuffix())
        if syntax is not None:
            self.setSyntax(syntax)
        PMXBaseEditor.setFileInfo(self, fileInfo)
        
    def getTabTitle(self):
        #Podemos marcar de otra forma cuando algo cambia :P
        return PMXBaseEditor.getTabTitle(self)
    
    def getTabIcon(self):
        if self.isModified():
            return resources.ICONS["save"]
        elif self.fileInfo is not None:
            return self.application.fileManager.getFileIcon(self.fileInfo)
        return PMXBaseEditor.getTabIcon(self)
        
    @classmethod
    def newInstance(cls, fileInfo = None, parent = None):
        editor = cls(fileInfo, parent)
        return editor

    #=======================================================================
    # Obteniendo datos del editor
    #=======================================================================
    def getPreference(self, scope):
        if scope not in PMXCodeEditor.PREFERENCE_CACHE:
            PMXCodeEditor.PREFERENCE_CACHE[scope] = self.application.supportManager.getPreferenceSettings(scope)
        return PMXCodeEditor.PREFERENCE_CACHE[scope]

    def getCurrentScope(self):
        cursor = self.textCursor()
        block = cursor.block()
        user_data = block.userData()
        if user_data == None:
            return ""
        #FIXME: Esta condicion con el bucle no se puede o no se deberia dar nunca
        if not bool(user_data) and block.userState() == self.syntaxHighlighter.MULTI_LINE:
            while not bool(block.userData()):
                block = block.previous()
            return block.userData().getLastScope()
        return user_data.getScopeAtPosition(cursor.columnNumber())
    
    def getTextUnderCursor(self):
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        return cursor.selectedText()
        
    def getCurrentWord(self):
        #Current word is not the same that current Text
        word = self.getTextUnderCursor()
        if self.RE_WORD.match(word):
            return word
        return ""
    
    def getSelectionBlockStartEnd(self):
        cursor = self.textCursor()
        start, end = cursor.selectionStart(), cursor.selectionEnd()
        if start > end:
            return self.document().findBlock(end), self.document().findBlock(start)
        else:
            return self.document().findBlock(start), self.document().findBlock(end)

    def getFlags(self):
        flags = 0
        options = self.document().defaultTextOption()
        if options.flags() & QtGui.QTextOption.ShowTabsAndSpaces:
            flags |= self.ShowTabsAndSpaces
        if options.flags() & QtGui.QTextOption.ShowLineAndParagraphSeparators:
            flags |= self.ShowLineAndParagraphs
        if self.sidebar.showBookmarks:
            flags |= self.ShowBookmarks
        if self.sidebar.showLineNumbers:
            flags |= self.ShowLineNumbers
        if self.sidebar.showFolding:
            flags |= self.ShowFolding
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
        options.setFlags(oFlags)
        self.document().setDefaultTextOption(options)
        self.sidebar.showBookmarks = bool(flags & self.ShowBookmarks)
        self.sidebar.showLineNumbers = bool(flags & self.ShowLineNumbers)
        self.sidebar.showFolding = bool(flags & self.ShowFolding)
        self.updateLineNumberAreaWidth(0)
        self.viewport().repaint(self.viewport().visibleRegion())
        
    def getSyntax(self):
        return self.syntaxHighlighter.syntax
        
    def setSyntax(self, syntax):
        if hasattr(self, "syntaxHighlighter"):
            if self.syntaxHighlighter.syntax != syntax:
                self.syntaxHighlighter.syntax = syntax
                self.folding.indentSensitive = syntax.indentSensitive
                self.syntaxHighlighter.rehighlight()
                self.syntaxChanged.emit()
        else:
            self.syntaxHighlighter = PMXSyntaxHighlighter(self, syntax)
            self.folding.indentSensitive = syntax.indentSensitive
    
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        menu.popup(event.globalPos())
    
    #=======================================================================
    # Espacio para la sidebar
    #=======================================================================
    def lineNumberAreaWidth(self):
        area = self.sidebar.padding
        if self.sidebar.showLineNumbers:
            area += self.fontMetrics().width('0') * len(str(self.blockCount()))
        if self.sidebar.showBookmarks:
            area += self.sidebar.bookmarkArea
        if self.sidebar.showFolding:
            area += self.sidebar.foldArea
        return area
        
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
    
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.sidebar.scroll(0, dy);
        else:
            self.sidebar.update(0, rect.y(), self.sidebar.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
    
    def resizeEvent(self, event):
        QtGui.QPlainTextEdit.resizeEvent(self, event)
        cr = self.contentsRect()
        self.sidebar.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
        
    def highlightCurrentLine(self):
        extraSelections = []
        if self.cursors.isActive():
            for cursor in self.cursors:
                if cursor.hasSelection():
                    selection = QTextEdit.ExtraSelection()
                    selection.format.setBackground(self.colours['selection'])
                    selection.cursor = cursor
                    extraSelections.append(selection)
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(self.colours['lineHighlight'])
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def select(self, selection):
        if selection in range(4):
            self.textCursor().select(selection)
            
    #=======================================================================
    # QPlainTextEdit Events
    #=======================================================================
    def paintEvent(self, event):
        #QtGui.QPlainTextEdit.paintEvent(self, event)
        QtGui.QPlainTextEdit.paintEvent(self, event)
        page_bottom = self.viewport().height()
        font_metrics = QtGui.QFontMetrics(self.document().defaultFont())

        painter = QPainter(self.viewport())
        
        block = self.firstVisibleBlock()
        viewport_offset = self.contentOffset()
        line_count = block.blockNumber()
        while block.isValid():
            line_count += 1
            # The top left position of the block in the document
            position = self.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            user_data = block.userData()
            if block.isVisible() and self.folding.isStart(self.folding.getFoldingMark(block)) and user_data.folded:
                painter.drawPixmap(font_metrics.width(block.text()) + 10,
                    round(position.y()) + font_metrics.ascent() + font_metrics.descent() - resources.IMAGES["foldingellipsis"].height(),
                    resources.IMAGES["foldingellipsis"])
            
            block = block.next()
        if self.cursors.isActive():
            for cursor in self.cursors:
                rec = self.cursorRect(cursor)
                cursor = QtCore.QLine(rec.x(), rec.y(), rec.x(), rec.y() + font_metrics.ascent() + font_metrics.descent())
                painter.setPen(QtGui.QPen(self.colours['caret']))
                painter.drawLine(cursor)
        if self.cursors.isDragCursor:
            pen = QtGui.QPen(self.colours['caret'])
            pen.setWidth(2)
            painter.setPen(pen)
            color = QColor(self.colours['selection'])
            color.setAlpha(128)
            painter.setBrush(QtGui.QBrush(color))
            painter.setOpacity(0.2)
            painter.drawRect(self.cursors.getDragCursorRect())
        painter.end()

    #=======================================================================
    # Mouse Events
    #=======================================================================
    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.delta() == 120:
                self.zoomIn()
            elif event.delta() == -120:
                self.zoomOut()
            event.ignore()
        else:
            QtGui.QPlainTextEdit.wheelEvent(self, event)

    def mousePressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.application.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.cursors.mousePressPoint(event.pos())
        else:
            QtGui.QPlainTextEdit.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.cursors.mouseMovePoint(event.pos())
        else:
            QtGui.QPlainTextEdit.mouseReleaseEvent(self, event)
 
    def mouseReleaseEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.cursors.mouseReleasePoint(event.pos())
            self.application.restoreOverrideCursor()
        else:
            QtGui.QPlainTextEdit.mouseReleaseEvent(self, event)

    def inserSpacesUpToPoint(self, point, spacing_character = ' '):
        '''
        Inserts whitespace up to a point
        '''
        cursor = self.cursorForPosition(point)
        block = cursor.block()
        if not block.isValid():
            return
        text = block.text()
        self.fontMetrics()
        font_width = self.fontMetrics().width(' ')
        line_width = font_width * text.length()
        # Cast to int if Py > 3.x
        char_number = int(point.x() / font_width)
        char_number_delta = char_number - text.length()
        if char_number_delta > 0:
            # Insert some empty characters
            cursor.beginEditBlock()
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor, 1)
            #print "Inserting", char_number_delta
            cursor.insertText(spacing_character * char_number_delta)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor, 1)
            cursor.endEditBlock()
            self.setTextCursor(cursor)
            
        #print block.blockNumber(), ":", text, line_width, "px"
        #print char_number, text.length()
    
    #=======================================================================
    # Keyboard Events
    #=======================================================================
    def activeHelper(self):
        #retorna el primer helper activo
        for h in self.editorHelpers:
            if h.isActive():
                return h

    def keyPressEvent(self, event):
        '''
        This method is called whenever a key is pressed. The key code is stored in event.key()
        http://manual.macromates.com/en/working_with_text
        '''
        
        helper = self.activeHelper()
        if helper is None:
            scope = self.getCurrentScope()
            #Enviar activar a los helpers hasta que uno retorne True
            for helper in self.editorHelpers:
                helper.active(event, scope)
                if helper.isActive():
                    return helper.keyPressEvent(event)
        else:
            return helper.keyPressEvent(event)

        #No tengo ningun helper trabajando voy con el Modo Normal
        key = event.key()
        if key == Qt.Key_Tab:
            self.tabPressEvent(event)
        elif key == Qt.Key_Backtab:
            self.backtabPressEvent(event)
        elif key == Qt.Key_Return:
            self.returnPressEvent(event)
        elif key == Qt.Key_Insert:
            self.setOverwriteMode(not self.overwriteMode())
        else:
            QtGui.QPlainTextEdit.keyPressEvent(self, event)

        #Luego de tratar el evento, solo si se inserto algo de texto
        if event.text() != "":
            self.keyPressIndent(event)
            completionPrefix = self.getCurrentWord()
            if self.completer.isActive() and completionPrefix != self.completer.completionPrefix():
                self.completer.setCompletionPrefix(completionPrefix)
                self.completer.complete(self.cursorRect())
    
    #=======================================================================
    # Tab Keyboard Events
    #=======================================================================
    def tabPressEvent(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.indent(self.tabKeyBehavior)
        else:
            cursor.insertText(self.tabKeyBehavior)
    
    #=======================================================================
    # Backtab Keyboard Events
    #=======================================================================
    def backtabPressEvent(self, event):
        self.unindent()
    
    #=======================================================================
    # Return Keyboard Events
    #=======================================================================
    def returnPressEvent(self, event):
        cursor = self.textCursor()
        block = cursor.block()
        prev = cursor.block().previous()
        line = block.text()
        if self.document().blockCount() == 1:
            syntax = self.application.supportManager.findSyntaxByFirstLine(line)
            if syntax is not None:
                self.setSyntax(syntax)
        preference = self.getPreference(block.userData().getLastScope())
        indentMark = preference.indent(line)
        super(PMXCodeEditor, self).keyPressEvent(event)
        if indentMark == PMXPreferenceSettings.INDENT_INCREASE:
            self.debug("Increase indent")
            cursor.insertText(block.userData().indent + self.tabKeyBehavior)
        elif indentMark == PMXPreferenceSettings.INDENT_NEXTLINE:
            self.debug("Increase next line indent")
        elif indentMark == PMXPreferenceSettings.UNINDENT:
            self.debug("Unindent")
        elif indentMark == PMXPreferenceSettings.INDENT_DECREASE:
            self.debug("Decrease indent")
            cursor.insertText(prev.userData().indent[:len(self.tabKeyBehavior)])
        else:
            self.debug("Preserve indent")
            cursor.insertText(block.userData().indent)
    
    #=======================================================================
    # After Keyboard Events
    #=======================================================================
    
    def keyPressIndent(self, event):
        cursor = self.textCursor()
        block = cursor.block()
        prev = block.previous()
        preference = self.getPreference(block.userData().getLastScope())
        indentMark = preference.indent(block.text())
        if indentMark == PMXPreferenceSettings.INDENT_DECREASE and prev.isValid() and block.userData().indent == prev.userData().indent:
            self.unindent()
    
    #==========================================================================
    # Bundle Items
    #==========================================================================
    def insertBundleItem(self, item, **processorSettings):
        ''' 
            Inserta un bundle item
        '''
        if item.TYPE == PMXSnippet.TYPE:
            self.snippetProcessor.configure(processorSettings)
            self.debug("Corriendo Snippet %s" % item.name)
            item.execute(self.snippetProcessor)
        elif item.TYPE == PMXCommand.TYPE or item.TYPE == PMXDragCommand.TYPE:
            self.commandProcessor.configure(processorSettings)
            self.debug("Corriendo Command %s" % item.name)
            item.execute(self.commandProcessor)
        elif item.TYPE == PMXSyntax.TYPE:
            self.debug("Cambiando syntax %s" % item.name)
            self.setSyntax(item)
        elif item.TYPE == PMXMacro.TYPE:
            self.debug("Corriendo Macro %s" % item.name)
            item.execute(self.macroProcessor)

    def selectBundleItem(self, items, tabTriggered = False):
        #Tengo mas de uno que hago?, muestro un menu
        syntax = any(map(lambda item: item.TYPE == 'syntax', items))
        menu = QtGui.QMenu(self)
        for index, item in enumerate(items, 1):
            receiver = lambda item = item: self.insertBundleItem(item, tabTriggered = tabTriggered)
            action = item.buildTriggerItemAction(menu, receiver, mnemonic = "&" + str(index))
            menu.addAction(action)
        if syntax:
            point = self.mainWindow.cursor().pos()
        else:
            point = self.viewport().mapToGlobal(self.cursorRect(self.textCursor()).bottomRight())
        menu.popup(point)
    
    def executeCommand(self, command = None, input = "none", output = "insertText"):
        if command is None:
            command = self.textCursor().selectedText() if self.textCursor().hasSelection() else self.textCursor().block().text()
        hash = {    'command': command, 
                       'name': command,
                      'input': input,
                     'output': output }
        command = PMXCommand(self.application.supportManager.uuidgen(), "internal", hash = hash)
        command.bundle = self.application.supportManager.getDefaultBundle()
        self.insertBundleItem(command)
    
    def buildEnvironment(self, env = {}):
        """ http://manual.macromates.com/en/environment_variables.html """
        cursor = self.textCursor()
        line = cursor.block().text()
        scope = self.getCurrentScope()
        preferences = self.getPreference(scope)
        current_word = self.getCurrentWord()
        #Combine base env from params and editor env
        env.update({
                'TM_CURRENT_LINE': line,
                'TM_LINE_INDEX': cursor.columnNumber(), 
                'TM_LINE_NUMBER': cursor.block().blockNumber() + 1,
                'TM_COLUMN_NUMBER': cursor.columnNumber() + 1, 
                'TM_SCOPE': scope,
                'TM_MODE': self.getSyntax().name,
                'TM_SOFT_TABS': self.tabStopSoft and u'YES' or u'NO',
                'TM_TAB_SIZE': self.tabStopSize,
                'TM_NESTEDLEVEL': self.folding.getNestedLevel(cursor.block().blockNumber())
        })

        if current_word != None:
            env['TM_CURRENT_WORD'] = current_word
        if self.fileInfo is not None:
            env['TM_FILEPATH'] = self.fileInfo.absoluteFilePath()
            env['TM_FILENAME'] = self.fileInfo.fileName()
            env['TM_DIRECTORY'] = self.fileInfo.absoluteDir().dirName()
        if self.project is not None:
            env['TM_PROJECT_DIRECTORY'] = ""
            env['TM_SELECTED_FILES'] = ""
            env['TM_SELECTED_FILE'] = ""
        if cursor.hasSelection():
            env['TM_SELECTED_TEXT'] = cursor.selectedText()
            start, end = self.getSelectionBlockStartEnd()
            env['TM_INPUT_START_COLUMN'] = cursor.selectionStart() - start.position() + 1
            env['TM_INPUT_START_LINE'] = start.blockNumber() + 1
            env['TM_INPUT_START_LINE_INDEX'] = cursor.selectionStart() - start.position()
            
        env.update(preferences.shellVariables)
        return env

    #==========================================================================
    # Completer
    #==========================================================================
    def showCompleter(self, suggestions):
        completionPrefix = self.getCurrentWord()
        self.completer.setCompletionPrefix(completionPrefix)
        self.completer.setModel(PMXCompleterListModel(suggestions, self))
        cr = self.cursorRect()
        self.completer.complete(cr)
    
    #==========================================================================
    # Folding
    #==========================================================================
    def codeFoldingFold(self, block):
        self._fold(block)
        self.update()
        self.sidebar.update()
    
    def codeFoldingUnfold(self, block):
        self._unfold(block)
        self.update()
        self.sidebar.update()
        
    def _fold(self, block):
        milestone = block
        if self.folding.isStart(self.folding.getFoldingMark(milestone)):
            startBlock = milestone.next()
            endBlock = self.folding.findBlockFoldClose(milestone)
        else:
            endBlock = milestone
            milestone = self.folding.findBlockFoldOpen(endBlock)
            startBlock = milestone.next()
        block = startBlock
        while True:
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
        while True:
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
    def findMatch(self, match, flags, findNext = False):
        cursor = self.textCursor()
        if not findNext and cursor.hasSelection():
            cursor.setPosition(cursor.selectionStart())
        cursor = self.document().find(match, cursor, flags)
        if cursor.isNull():
            cursor = self.textCursor()
            if flags & QtGui.QTextDocument.FindBackward:
                cursor.movePosition(QtGui.QTextCursor.End)
            else:
                cursor.movePosition(QtGui.QTextCursor.Start)
            cursor = self.document().find(match, cursor, flags)
        if not cursor.isNull():
            self.setTextCursor(cursor)
            return True
        return False

    def replaceMatch(self, match, text, flags, all = False):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        replaced = False
        while True:
            replace = self.findMatch(match, flags)
            if not replace: break
            cursor = self.textCursor()
            cursor.insertText(text)
            if not all: break
        cursor.endEditBlock()
        return replaced

    #==========================================================================
    # Bookmarks and gotos
    #==========================================================================    
    def toggleBookmark(self, block = None):
        block = block or self.textCursor().block()
        self.bookmarks.toggleBookmark(block)
        self.sidebar.update()
    
    def removeAllBookmarks(self):
        self.bookmarks.removeAllBookmarks()
        self.sidebar.update()
    
    def bookmarkNext(self, block = None):
        block = block or self.textCursor().block()
        block = self.bookmarks.nextBookmark(block)
        if block is not None:
            self.goToBlock(block)

    def bookmarkPrevious(self, block = None):
        block = block or self.textCursor().block()
        block = self.bookmarks.previousBookmark(block)
        if block is not None:
            self.goToBlock(block)

    def goToBlock(self, block):
        cursor = self.textCursor()
        cursor.setPosition(block.position())
        self.setTextCursor(cursor)    

    def goToLine(self, lineNumber):
        cursor = self.textCursor()
        cursor.setPosition(self.document().findBlockByNumber(lineNumber - 1).position())
        self.setTextCursor(cursor)
    
    def goToColumn(self, columnNumber):
        cursor = self.textCursor()
        cursor.setPosition(cursor.block().position() + columnNumber)
        self.setTextCursor(cursor)
    
    #===========================================================================
    # Zoom
    #===========================================================================
    FONT_MAX_SIZE = 32
    FONT_MIN_SIZE = 6
    def zoomIn(self):
        font = self.font
        size = self.font.pointSize()
        if size < self.FONT_MAX_SIZE:
            size += 2
            font.setPointSize(size)
        self.font = font

    def zoomOut(self):
        font = self.font
        size = font.pointSize()
        if size > self.FONT_MIN_SIZE:
            size -= 2
            font.setPointSize(size)
        self.font = font

    #===========================================================================
    # Text Indentation
    #===========================================================================
    def increaseIndent(self, indentation):
        self.indent(indentation + (self.tabKeyBehavior))
    
    def decreaseIndent(self, indentation):
        self.unindent()
        
    # TODO: Word wrapping fix
    # TODO: Correct whitespace mix
    def indent(self, indentation):
        '''
        Indents text, it take cares of block selections.
        '''
        cursor = self.textCursor()
        start, end = self.getSelectionBlockStartEnd()
        cursor.beginEditBlock()
        new_cursor = QTextCursor(cursor)
        while True:
            new_cursor.setPosition(start.position())
            new_cursor.insertText(indentation)
            if start == end:
                break
            start = start.next()
        del new_cursor
        cursor.endEditBlock()        

    def unindent(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            start, end = cursor.selectionStart(), cursor.selectionEnd()
            if start > end:
                end, start = self.document().findBlock(start), self.document().findBlock(end)
            else:
                end, start = self.document().findBlock(end), self.document().findBlock(start)
            cursor.beginEditBlock()
            new_cursor = QTextCursor(cursor)
            while True:
                data = start.userData()
                counter = self.tabStopSize if len(data.indent) > self.tabStopSize else len(data.indent)
                if counter > 0:
                    new_cursor.setPosition(start.position())
                    for _j in range(self.tabStopSize):
                        new_cursor.deleteChar()
                if start == end:
                    break
                start = start.next()
            del new_cursor
            cursor.endEditBlock()
        else:
            block = cursor.block()
            data = cursor.block().userData()
            counter = self.tabStopSize if len(data.indent) > self.tabStopSize else len(data.indent)
            if counter > 0:
                cursor.beginEditBlock()
                position = block.position() if block.position() <= cursor.position() <= block.position() + self.tabStopSize else cursor.position() - counter
                cursor.setPosition(block.position()) 
                for _ in range(counter):
                    cursor.deleteChar()
                cursor.setPosition(position)
                self.setTextCursor(cursor)
                cursor.endEditBlock()
                
    # FIXME: Return something sensible :P
    def canUnindent(self):
        return True
    
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls() or mimeData.hasText():
            event.accept()
    
    def dragMoveEvent(self, event):
        cursor = self.cursorForPosition(event.pos())
        self.setTextCursor(cursor)
    
    def dropEvent(self, event):
        '''
        When a url or text is dropped
        '''
        mimeData = event.mimeData()
        if mimeData.hasText():
            self.textCursor().insertText(mimeData.text())
        elif mimeData.hasUrls():
            for url in mimeData.urls():
                self.textCursor().insertText(url.toString())
    
    
