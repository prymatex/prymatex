#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bisect import bisect
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QRect, Qt, SIGNAL
from PyQt4.QtGui import QTextEdit, QTextFormat, QMenu, \
    QTextCursor, QAction, QFont, QPalette, QPainter, QFontMetrics, QColor
    
from prymatex import resources
from prymatex.support import PMXSnippet, PMXMacro, PMXCommand, PMXSyntax, PMXPreferenceSettings
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core.base import PMXObject
from prymatex.gui.central import PMXBaseTab
from prymatex.gui.editor.sidebar import PMXSidebar
from prymatex.gui.editor.processors import PMXSyntaxHighlighter, PMXBlockUserData, PMXCommandProcessor, PMXSnippetProcessor, PMXMacroProcessor
from prymatex.gui.editor.codehelper import PMXCursorsHelper, PMXFoldingHelper, PMXCompleterHelper

class PMXCodeEditor(QtGui.QPlainTextEdit, PMXObject, PMXBaseTab):
    '''
    The GUI element which holds the editor.
    This class acts as a buffer for text, it does not know anything about
    the underlying filesystem.
    
    It holds the highlighter and the folding
    
    '''
    WORD = re.compile(r'\w+', re.UNICODE)
    PREFERENCE_CACHE = {}
    
    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'CodeEditor'
    
    @pmxConfigPorperty(default = u'3130E4FA-B10E-11D9-9F75-000D93589AF6', tm_name = u'OakDefaultLanguage')
    def defaultSyntax(self, uuid):
        self.syntax = self.application.supportManager.getBundleItem(uuid)
    
    softTabs = pmxConfigPorperty(default = True)
    tabSize = pmxConfigPorperty(default = 4)
    font = pmxConfigPorperty(default = QFont('Monospace', 10))
    
    @pmxConfigPorperty(default = u'766026CB-703D-4610-B070-8DE07D967C5F', tm_name = u'OakThemeManagerSelectedTheme')
    def theme(self, uuid):
        theme = self.application.supportManager.getTheme(uuid)
        self.syntaxProcessor.formatter = theme
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
        
        self.highlightCurrentLine()
    
    @property
    def tabKeyBehavior(self):
        return self.softTabs and u' ' * self.tabSize or u'\t'
    
    @property
    def snippetMode(self):
        """Retorna si el editor esta en modo snippet"""
        return self.snippetProcessor.hasSnippet
    
    @property
    def multiEditMode(self):
        """Retorna si el editor esta en modo multiedit"""
        return self.cursors.hasCursors
    
    @property
    def completerMode(self):
        """Retorna si el editor esta mostrando el completer"""
        return self.completer.popup().isVisible()
    
    def __init__(self, parent = None):
        QtGui.QPlainTextEdit.__init__(self, parent)
        PMXBaseTab.__init__(self)
        #Sidebar
        self.sidebar = PMXSidebar(self)
        
        #Processors
        self.syntaxProcessor = PMXSyntaxHighlighter(self)
        self.commandProcessor = PMXCommandProcessor(self)
        self.macroProcessor = PMXMacroProcessor(self)
        self.snippetProcessor = PMXSnippetProcessor(self)
        
        #Helpers
        self.cursors = PMXCursorsHelper(self)
        self.folding = PMXFoldingHelper(self)
        self.completer = PMXCompleterHelper(self)
        self.bookmarks = []
        
        self.setupUi()
        self.setupActions()
        self.connectSignals()
        self.configure()

    #=======================================================================
    # Connect Signals and Declare Events
    #=======================================================================
    def setupUi(self):
        #self.updateLineNumberAreaWidth(0)
        self.setWindowTitle(self.__class__.__name__)
        
    def connectSignals(self):
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.updateStatusBar)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.modificationChanged.connect(self.updateTabStatus)

    def setupActions(self):
        # Actions performed when a key is pressed
        self.actionIndent = QAction(self.trUtf8("Increase indentation"), self )
        self.connect(self.actionIndent, SIGNAL("triggered()"), self.indent)
        self.actionUnindent = QAction(self.trUtf8("Decrease indentation"), self )
        self.connect(self.actionUnindent, SIGNAL("triggered()"), self.unindent)
        self.actionFind = QAction(self.trUtf8("Find"), self)
    
    def isModified(self):
        return self.document().isModified()
    
    def getTabTitle(self):
        #Podemos marcar de otra forma cuando algo cambia :P
        return PMXBaseTab.getTabTitle(self)
    
    def getTabIcon(self):
        if self.isModified():
            return resources.ICONS["save"]
        elif self.fileInfo is not None:
            return self.application.fileManager.getFileIcon(self.fileInfo)
        return PMXBaseTab.getTabIcon(self)
    
    def open(self, fileInfo):
        syntax = self.application.supportManager.findSyntaxByFileType(fileInfo.fileName())
        if syntax is not None:
            self.syntax = syntax
        content = self.application.fileManager.openFile(fileInfo)
        self.setPlainText(content)
        PMXBaseTab.open(self, fileInfo)
        
    def save(self, fileInfo):
        self.application.fileManager.saveFile(fileInfo, self.toPlainText())
        self.document().setModified(False)
        PMXBaseTab.save(self, fileInfo)

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
        if not bool(user_data) and block.userState() == self.syntaxProcessor.MULTI_LINE:
            while not bool(block.userData()):
                block = block.previous()
            return block.userData().getLastScope()
        return user_data.getScopeAtPosition(cursor.columnNumber())
    
    def getCurrentWord(self):
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        return cursor.selectedText()
    
    def getSelectionBlockStartEnd(self):
        cursor = self.textCursor()
        start, end = cursor.selectionStart(), cursor.selectionEnd()
        if start > end:
            return self.document().findBlock(end), self.document().findBlock(start)
        else:
            return self.document().findBlock(start), self.document().findBlock(end)
    
    @property
    def status(self):
        ''' Estado actual del editor
        '''
        status = {}
        cursor = self.textCursor()
        status['line']  = cursor.blockNumber() + 1
        status['column'] = cursor.columnNumber() + 1
        status['scope'] = self.getCurrentScope()
        return status
    
    def updateStatusBar(self):
        #self.mainWindow.statusbar.updateStatus(self.status)
        pass

    @property
    def syntax(self):
        return self.syntaxProcessor.syntax
        
    @syntax.setter
    def syntax(self, syntax):
        assert syntax is not None, "Syntax can't be none"
        if self.syntaxProcessor.syntax != syntax:
            self.syntaxProcessor.syntax = syntax
            self.folding.indentSensitive = syntax.indentSensitive
            #self.mainWindow.statusbar.updateSyntax(syntax)
    
    @property
    def index(self):
        tab_widget = self.parent()
        return tab_widget.indexOf(self)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        menu.addAction(self.actionIndent)
        menu.addAction(self.actionUnindent)
        self.actionUnindent.setEnabled(self.canUnindent())
        menu.exec_(event.globalPos());
        del menu
        
    def lineNumberAreaWidth(self):
        return 3 + self.fontMetrics().width('9') * len(str(self.blockCount())) + self.sidebar.bookmarkArea + self.sidebar.foldArea 
        
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
    
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.sidebar.scroll(0, dy);
        else:
            self.sidebar.update(0, rect.y(), self.sidebar.width(), rect.height());
        if (rect.contains(self.viewport().rect())):
            self.updateLineNumberAreaWidth(0)
    
    def resizeEvent(self, event):
        super(PMXCodeEditor, self).resizeEvent(event)
        cr = self.contentsRect()
        self.sidebar.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
        
    def highlightCurrentLine(self):
        extraSelections = []
        if self.multiEditMode:
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

    #=======================================================================
    # QPlainTextEdit Events
    #=======================================================================
    def paintEvent(self, event):
        #QtGui.QPlainTextEdit.paintEvent(self, event)
        super(PMXCodeEditor, self).paintEvent(event)
        page_bottom = self.viewport().height()
        font_metrics = QFontMetrics(self.document().defaultFont())

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
            if block.isVisible() and self.folding.getFoldingMark(block) == self.folding.FOLDING_START and user_data.folded:
                painter.drawPixmap(font_metrics.width(block.text()) + 10,
                    round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.sidebar.foldingEllipsisIcon.height(),
                    self.sidebar.foldingEllipsisIcon)
            
            block = block.next()
        if self.multiEditMode:
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
            super(PMXCodeEditor, self).wheelEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            print "mouseDoubleClickEvent"
            self.cursors.mouseDoubleClickPoint(event.pos())
        else:
            super(PMXCodeEditor, self).mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.cursors.mousePressPoint(event.pos())
        else:
            super(PMXCodeEditor, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.cursors.mouseMovePoint(event.pos())
        else:
            super(PMXCodeEditor, self).mouseReleaseEvent(event)
 
    def mouseReleaseEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            print "mouseReleaseEvent"
            self.cursors.mouseReleasePoint(event.pos())
        else:
            super(PMXCodeEditor, self).mouseReleaseEvent(event)

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
    def keyPressEvent(self, event):
        '''
        This method is called whenever a key is pressed. The key code is stored in key_event.key()
        '''

        if self.completerMode:
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab, Qt.Key_Escape, Qt.Key_Backtab):
                event.ignore()
                self.completer.popup().hide()
                return
            elif event.key == Qt.Key_Space:
                self.completer.popup().hide()
        
        #Si lo toma un bundle item retorno
        if self.keyPressBundleItem(event):
            if self.multiEditMode:
                self.cursors.removeAll()
            return
        elif self.snippetMode and self.snippetProcessor.keyPressEvent(event): #Modo Snippet
            return
        elif self.multiEditMode and self.cursors.keyPressEvent(event): #Modo MultiEdit
            return
        elif self.keyPressSmartTyping(event): #Modo Normal
            return
        
        key = event.key()
    
        if key == Qt.Key_Tab:
            self.tabPressEvent(event)
        elif key == Qt.Key_Backtab:
            self.backtabPressEvent(event)
        elif key == Qt.Key_Backspace:
            self.backspacePressEvent(event)
        elif key == Qt.Key_Return:
            self.returnPressEvent(event)
        else:
            super(PMXCodeEditor, self).keyPressEvent(event)

        #Luego de tratar el evento, solo si se inserto algo de texto
        if event.text() != "":
            self.keyPressIndent(event)
            if self.completerMode:
                completionPrefix = self.getCurrentWord()
                self.completer.setCompletionPrefix(completionPrefix)
                #self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))
                #self.completer.setCurrentRow(0)
                self.completer.complete(self.cursorRect())
    
    def keyPressBundleItem(self, event):
        keyseq = int(event.modifiers()) + event.key()
        scope = self.getCurrentScope()
        items = self.application.supportManager.getKeyEquivalentItem(keyseq, scope)
        if items:
            if len(items) == 1:
                self.insertBundleItem(items[0])
            elif len(items) == 2 and items[0].TYPE != items[1].TYPE:
                #Son distintos desempato, el primero es el que mejor se ajusta
                self.insertBundleItem(items[0])
            else:
                self.selectBundleItem(items)
            return True
    
    def keyPressSmartTyping(self, event):
        cursor = self.textCursor()
        character = unicode(event.text())
        scope = self.getCurrentScope()
        preferences = self.getPreference(scope)
        pairs = filter(lambda pair: pair[0] == character, preferences.smartTypingPairs)
        if pairs:
            if cursor.hasSelection():
                position = cursor.selectionStart()
                text = pairs[0][0] + cursor.selectedText() + pairs[0][1]
                cursor.insertText(text)
                cursor.setPosition(position)
                cursor.setPosition(position + len(text), QTextCursor.KeepAnchor)
            else:
                position = cursor.position()
                super(PMXCodeEditor, self).keyPressEvent(event)
                cursor.insertText(pairs[0][1])
                cursor.setPosition(position + 1)
            self.setTextCursor(cursor)
            return True

    #=======================================================================
    # Tab Keyboard Events
    #=======================================================================
    def tabPressEvent(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.indent(self.tabKeyBehavior)
        else:
            scope = self.getCurrentScope()
            trigger = self.application.supportManager.getTabTriggerSymbol(unicode(cursor.block().text()), cursor.columnNumber())
            if trigger != None:
                snippets = self.application.supportManager.getTabTriggerItem(trigger, scope)
                if len(snippets) > 1:
                    self.selectBundleItem(snippets, tabTrigger = True)
                    return
                elif snippets:
                    self.insertBundleItem(snippets[0], tabTrigger = True)
                    return
            cursor.insertText(self.tabKeyBehavior)
    
    #=======================================================================
    # Backtab Keyboard Events
    #=======================================================================
    def backtabPressEvent(self, event):
        self.unindent()

    #=======================================================================
    # Backspace Keyboard Events
    #=======================================================================
    def backspacePressEvent(self, event):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            doc = self.document()
            scope = self.getCurrentScope()
            preferences = self.getPreference(scope)
            if preferences.smartTypingPairs:
                character = doc.characterAt(cursor.position() - 1)
                pairs = filter(lambda pair: pair[0] == character or pair[1] == character, preferences.smartTypingPairs)
                if pairs and pairs[0][0] == character and doc.characterAt(cursor.position()) == pairs[0][1]:
                    cursor.deleteChar()
                elif pairs and pairs[0][1] == character and doc.characterAt(cursor.position() - 2) == pairs[0][0]:
                    cursor.deletePreviousChar()
        super(PMXCodeEditor, self).keyPressEvent(event)
    
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
                self.syntax = syntax
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
    # BundleItems
    #==========================================================================
    def insertBundleItem(self, item, tabTrigger = False, disableIndent = False):
        ''' 
            Inserta un bundle item
        '''
        if item.TYPE == PMXSnippet.TYPE:
            self.snippetProcessor.configure(tabTrigger, disableIndent)
            print "Corriendo Snippet", item.name
            item.execute(self.snippetProcessor)
        elif item.TYPE == PMXCommand.TYPE:
            print "Corriendo Command", item.name
            item.execute(self.commandProcessor)
        elif item.TYPE == PMXSyntax.TYPE:
            self.syntax = item
        elif item.TYPE == PMXMacro.TYPE:
            self.debug("Corriendo Macro %s" % item.name)
            item.execute(self.macroProcessor)

    def selectBundleItem(self, items, tabTrigger = False):
        #Tengo mas de uno que hago?
        syntax = any(map(lambda item: item.TYPE == 'syntax', items))
        menu = QMenu()
        for index, item in enumerate(items, 1):
            action = menu.addAction(item.buildMenuTextEntry("&" + str(index)))
            receiver = lambda item = item: self.insertBundleItem(item, tabTrigger = tabTrigger)
            self.connect(action, SIGNAL('triggered()'), receiver)
        if syntax:
            point = self.mainWindow.cursor().pos()
        else:
            point = self.viewport().mapToGlobal(self.cursorRect(self.textCursor()).bottomRight())
        menu.exec_(point)
    
    def buildEnvironment(self, env = {}):
        cursor = self.textCursor()
        line = unicode(cursor.block().text())
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
                'TM_SOFT_TABS': self.softTabs and u'YES' or u'NO',
                'TM_TAB_SIZE': self.tabSize,
                'TM_NESTEDLEVEL': self.folding.getNestedLevel(cursor.block().blockNumber())
        })
        if current_word != None:
            env['TM_CURRENT_WORD'] = current_word
        if self.syntax != None:
            env['TM_MODE'] = self.syntax.name
        if self.fileInfo is not None:
            env['TM_FILEPATH'] = self.fileInfo.absoluteFilePath()
            env['TM_FILENAME'] = self.fileInfo.fileName()
            env['TM_DIRECTORY'] = self.fileInfo.absoluteDir().dirName()
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
        #self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))
        #self.completer.setCurrentRow(0)
        cr = self.cursorRect()
        self.completer.complete(cr, suggestions)
    
    #==========================================================================
    # Folding
    #==========================================================================
    def codeFoldingFold(self, line_number):
        self._fold(line_number)
        self.update()
        self.sidebar.update()
    
    def codeFoldingUnfold(self, line_number):
        self._unfold(line_number)
        self.update()
        self.sidebar.update()
        
    def _fold(self, line_number):
        milestone = self.document().findBlockByNumber(line_number - 1)
        if self.folding.getFoldingMark(milestone) == self.folding.FOLDING_START:
            startBlock = milestone.next()
            endBlock = self.folding.findBlockFoldClose(milestone)
        else:
            endBlock = milestone
            milestone = self.folding.findBlockFoldOpen(endBlock)
            startBlock = milestone.next()
        print startBlock.blockNumber(), milestone.blockNumber(), endBlock.blockNumber()
        block = startBlock
        while True:
            user_data = block.userData()
            user_data.foldedLevel += 1
            block.setVisible(user_data.foldedLevel == 0)
            if block == endBlock:
                break
            block = block.next()
        
        milestone.userData().folded = True
        self.document().markContentsDirty(startBlock.position(), endBlock.position())

    def _unfold(self, line_number):
        milestone = self.document().findBlockByNumber(line_number - 1)
        startBlock = milestone.next()
        endBlock = self.folding.findBlockFoldClose(milestone)
        if endBlock == None:
            return
        
        block = startBlock
        while True:
            user_data = block.userData()
            user_data.foldedLevel -= 1
            block.setVisible(user_data.foldedLevel == 0)
            if block == endBlock:
                break
            block = block.next()

        milestone.userData().folded = False
        self.document().markContentsDirty(startBlock.position(), endBlock.position())

    #==========================================================================
    # Bookmarks
    #==========================================================================    
    def toggleBookmark(self, line_number):
        if line_number in self.bookmarks:
            self.bookmarks.remove(line_number)
        else:
            index = bisect(self.bookmarks, line_number)
            self.bookmarks.insert(index, line_number)
        self.sidebar.update()
    
    def removeBookmarks(self):
        self.bookmarks = []
        self.sidebar.update()
    
    def bookmarkNext(self, line_number):
        index = bisect(self.bookmarks, line_number)
        if index < len(self.bookmarks):
            self.goToLine(self.bookmarks[index])
        else:
            self.goToLine(self.bookmarks[0])
    
    def bookmarkPrevious(self, line_number):
        if line_number in self.bookmarks:
            index = self.bookmarks.index(line_number)
        else:
            index = bisect(self.bookmarks, line_number)
        if index < len(self.bookmarks):
            self.goToLine(self.bookmarks[index - 1])
    
    def goToLine(self, lineno):
        cursor = self.textCursor()
        cursor.setPosition(self.document().findBlockByNumber(lineno - 1).position())
        self.setTextCursor(cursor)
    
    def goToColumn(self, column):
        cursor = self.textCursor()
        cursor.setPosition(cursor.block().position() + column)
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
        #counter = self.tabSize if self.softTabs else 1
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
                counter = self.tabSize if len(data.indent) > self.tabSize else len(data.indent)
                if counter > 0:
                    new_cursor.setPosition(start.position())
                    for _j in range(self.tabSize):
                        new_cursor.deleteChar()
                if start == end:
                    break
                start = start.next()
            del new_cursor
            cursor.endEditBlock()
        else:
            block = cursor.block()
            data = cursor.block().userData()
            counter = self.tabSize if len(data.indent) > self.tabSize else len(data.indent)
            if counter > 0:
                cursor.beginEditBlock()
                position = block.position() if block.position() <= cursor.position() <= block.position() + self.tabSize else cursor.position() - counter
                cursor.setPosition(block.position()) 
                for _ in range(counter):
                    cursor.deleteChar()
                cursor.setPosition(position)
                self.setTextCursor(cursor)
                cursor.endEditBlock()
                
    # FIXME: Return something sensible :P
    def canUnindent(self):
        return True
    
    def dragEnterEvent(self, dragEnterEvent):
        if dragEnterEvent.mimeData().hasFormat('text/plain'):
            dragEnterEvent.accept()
        else:
            dragEnterEvent.ignore()
    
    
    def dropEvent(self, dropEvent):
        '''
        When a file is dropped
        '''
        dropedText = dropEvent.mimeData().text()
        print dropedText
        filesToOpen = []
        
        while True:
            if dropedText and not dropedText.count('\n'):
                text = dropedText
            else:
                text, dropedText = dropedText.split('\n', 1)
            
            
             
        # Check if there were files droped

# TODO: Move to a more convinient location
from os.path import isfile, isdir
isFile = lambda s: s.startswith('file://') and isfile(s[7:])
isDir = lambda s: s.startswith('file://') and isdir(s[7:])
