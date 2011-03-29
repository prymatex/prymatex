# -*- encoding: utf-8 -*-

import re, sys, logging
from bisect import bisect
from PyQt4.QtCore import QRect, Qt, SIGNAL
from PyQt4.QtGui import QPlainTextEdit, QTextEdit, QTextFormat, QMenu, \
    QTextCursor, QAction, QFont, QPalette, QToolTip
from PyQt4.QtWebKit import QWebView
from prymatex.bundles import PMXBundle, PMXPreference, PMXSnippet
from prymatex.bundles.command import PMXCommand
from prymatex.bundles.syntax import PMXSyntax
from prymatex.bundles.theme import PMXTheme
from prymatex.core.base import PMXObject
from prymatex.core.config import Setting
from prymatex.gui.editor.sidebar import PMXSidebar
from prymatex.gui.editor.syntax import PMXSyntaxProcessor, PMXBlockUserData

logger = logging.getLogger(__name__)

# Key press debugging 
KEY_NAMES = dict([(getattr(Qt, keyname), keyname) for keyname in dir(Qt) 
                  if keyname.startswith('Key_')])

def debug_key(key_event):
    ''' Prevents hair loss when debuging what the hell is going on '''
    key = key_event.key()
    mods = []
    modifiers = key_event.modifiers()
    if modifiers & Qt.AltModifier:
        mods.append("AltModifier")
    if modifiers & Qt.ControlModifier:
        mods.append("ControlModifier")
    if modifiers & Qt.MetaModifier:
        mods.append("MetaModifier")
    if modifiers & Qt.ShiftModifier:
        mods.append("ShiftModifier")
    
    return "%s <%s> Code: %d chr(%d) = %s" % (KEY_NAMES[key],  ", ".join(mods), 
                                              key, key, key < 255 and chr(key) 
                                              or 'N/A')

_counter = 0



class PMXCodeEdit(QPlainTextEdit, PMXObject):
    '''
    The GUI element which holds the editor.
    This class acts as a buffer for text, it does not know anything about
    the underlying filesystem.
    
    It holds the highlighter and the folding
    
    '''
    
    WHITESPACE = re.compile(r'^(?P<whitespace>\s+)', re.UNICODE)
    SPLITWORDS = re.compile(r'\s', re.UNICODE)
    WORD = re.compile(r'\w+', re.UNICODE)

    #=======================================================================
    # Settings, config and init
    #=======================================================================
    soft_tabs = Setting(default = True)
    tab_size = Setting(default = 4)
    _font = Setting(default = {"name": "Monospace", "size": 10}, 
                   fset = lambda self, value: self.setFont(QFont(value["name"], value["size"]))
                   )
    
    @property
    def tabKeyBehavior(self):
        return self.soft_tabs and u' ' * self.tab_size or u'\t'
    
    def setTheme(self, name):
        theme = PMXTheme.getThemeByName(self.theme_name)
        self.processor.formatter = theme
        style = theme.getStyle()
        foreground = style.getQColor('foreground')
        background = style.getQColor('background')
        selection = style.getQColor('selection')
        invisibles = style.getQColor('invisibles')
        palette = self.palette()
        palette.setColor(QPalette.Active, QPalette.Text, foreground)
        palette.setColor(QPalette.Active, QPalette.Base, background)
        palette.setColor(QPalette.Inactive, QPalette.Base, background)
        palette.setColor(QPalette.Active, QPalette.Highlight, selection)
        palette.setColor(QPalette.Active, QPalette.AlternateBase, invisibles)
        self.setPalette(palette)
        self.line_highlight = style.getQColor('lineHighlight')
        self.highlightCurrentLine()
        
    #theme_name = Setting(default = 'Twilight', fset = setTheme)
    theme_name = Setting(default = 'iPlastic', fset = setTheme)
    
    class Meta(object):
        settings = 'editor'
    
    def __init__(self, parent = None):
        super(PMXCodeEdit, self).__init__(parent)
        self.sidebar = PMXSidebar(self)
        self.processor = PMXSyntaxProcessor(self)
        self.bookmarks = []
        self.folded = []
        self.snippet = None
        # TODO: Load from config
        #option = QTextOption()
        #option.setFlags(QTextOption.ShowTabsAndSpaces)
        #self.document().setDefaultTextOption(option)

        # Actions performed when a key is pressed
        self.setupUi()
        self.setupActions()
        self.connectSignals()
        self.declareEvents()
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
        self.cursorPositionChanged.connect(self.sendCursorPosChange)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        
    def declareEvents(self):
        self.declareEvent('editorCursorPositionChangedEvent()')
        self.declareEvent('editorSetSyntaxEvent()')

    def setupActions(self):
        self.actionIndent = QAction(self.trUtf8("Increase indentation"), self )
        self.connect(self.actionIndent, SIGNAL("triggered()"), self.indent)
        self.actionUnindent = QAction(self.trUtf8("Decrease indentation"), self )
        self.connect(self.actionUnindent, SIGNAL("triggered()"), self.unindent)
        self.actionFind = QAction(self.trUtf8("Find"), self)

    def getCurrentScope(self):
        cursor = self.textCursor()
        block = cursor.block()
        user_data = block.userData()
        if user_data == None:
            return ""
        if not bool(user_data) and block.userState() == self.processor.MULTI_LINE:
            while not bool(block.userData()):
                block = block.previous()
            return block.userData().getLastScope()
        return user_data.getScopeAtPosition(cursor.columnNumber())
        
    def sendCursorPosChange(self):
        c = self.textCursor()
        line  = c.blockNumber()
        col = c.columnNumber()
        self.editorCursorPositionChangedEvent(line, col)
        
    def setSyntax(self, syntax):
        self.processor.syntax = syntax
        self.editorSetSyntaxEvent(syntax)
    
    @property
    def syntax(self):
        return self.processor.syntax
        
    @property
    def index(self):
        tab_widget = self.parent()
        return tab_widget.indexOf(self)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        
        menu.addAction(self.actionIndent)
        menu.addAction(self.actionUnindent)
        self.actionUnindent.setEnabled(self.can_unindent())

        menu.exec_(event.globalPos());
        del menu
        
    def lineNumberAreaWidth(self):
        # si tiene folding tengo que sumar mas 10
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
        super(PMXCodeEdit, self).resizeEvent(event)
        cr = self.contentsRect()
        self.sidebar.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
        
    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(self.line_highlight);
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
    
    def selectionBlockStart(self):
        '''
        Returns the block where the slection starts
        '''
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return -1
        return self.document().findBlock( cursor.selectionStart() ).blockNumber()
        
    def selectionBlockEnd(self):
        '''
        Returns the block number where the selection ends
        '''
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return -1
        return self.document().findBlock( cursor.selectionEnd() ).blockNumber()
    
    #=======================================================================
    # Mouse Events
    #=======================================================================
    
    def mousePressEvent(self, mouse_event):
        self.inserSpacesUpToPoint(mouse_event.pos())
        super(PMXCodeEdit, self).mousePressEvent(mouse_event)

    def mouseMoveEvent(self, event):
        position = event.pos()
        QToolTip.showText(self.mapToGlobal(position), "Cacho", self)
        super(PMXCodeEdit, self).mouseMoveEvent(event)

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
    
    def keyPressEvent(self, key_event):
        '''
        This method is called whenever a key is pressed. The key code is stored in key_event.key()
        '''
        
        #Check for snippet
        if self.snippet != None:
            key_event = self.keyPressSnippetEvent(key_event)
            if key_event == None:
                return
        
        key = key_event.key()
        cursor = self.textCursor()
        doc = self.document()
        line = unicode(cursor.block().text())
        
        if key == Qt.Key_Tab:
            #Find for getTabTriggerItem in bundles
            scope = self.getCurrentScope()
            words = self.SPLITWORDS.split(line[:cursor.columnNumber()])
            word = words and words[-1] or ""
            if scope and word:
                snippets = PMXBundle.getTabTriggerItem(word, scope)
                if len(snippets) > 1:
                    return self.selectBundleItem(snippets, tabTrigger = True)
                elif snippets:
                    return self.insertBundleItem(snippets[0], tabTrigger = True)
            cursor.beginEditBlock()
            cursor.insertText(self.tabKeyBehavior)
            cursor.endEditBlock()
        elif key == Qt.Key_Backtab:
            self.unindent()
        elif key == Qt.Key_Backspace:
            if not cursor.hasSelection():
                cursor_left = QTextCursor(cursor)
                cursor_right = QTextCursor(cursor)
                cursor_left.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
                cursor_right.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,1)
                try:
                    scope = self.getCurrentScope()
                    preferences = PMXPreference.buildSettings(PMXBundle.getPreferences(scope))
                    text_arround = "%s%s" % (cursor_left.selectedText(), cursor_right.selectedText())
                    if text_arround in map(lambda pair: "%s%s" % (pair[0], pair[1]), preferences["smartTypingPairs"]):
                        cursor_left.removeSelectedText()
                        cursor_right.removeSelectedText()
                    else:
                        QPlainTextEdit.keyPressEvent(self, key_event)
                except Exception:
                    QPlainTextEdit.keyPressEvent(self, key_event)
            else:
                QPlainTextEdit.keyPressEvent(self, key_event)
        elif key == Qt.Key_Return:
            if doc.blockCount() == 1:
                #Esto es un enter y es el primer blocke que tiene el documento
                syntax = PMXSyntax.findSyntaxByFirstLine(line)
                if syntax != None:
                    self.setSyntax(syntax)
            
            scope = self.getCurrentScope()
            preferences = PMXPreference.buildSettings(PMXBundle.getPreferences(scope))
            indentation = self.indentationWhitespace(line)
            #TODO: Move indentation to preferences
            if preferences["decreaseIndentPattern"] != None and preferences["decreaseIndentPattern"].match(line):
                logger.debug("decreaseIndentPattern")
                self.decreaseIndent(indentation)
                indentation = self.indentationWhitespace(line)
                QPlainTextEdit.keyPressEvent(self, key_event)
                self.indent(indentation)
            elif preferences["increaseIndentPattern"] != None in preferences and preferences["increaseIndentPattern"].match(line):
                logger.debug("increaseIndentPattern")
                QPlainTextEdit.keyPressEvent(self, key_event)
                self.increaseIndent(indentation)
            elif preferences["indentNextLinePattern"] != None in preferences and preferences["indentNextLinePattern"].match(line):
                logger.debug("indentNextLinePattern")
                QPlainTextEdit.keyPressEvent(self, key_event)
                self.increaseIndent(indentation)
            elif preferences["unIndentedLinePattern"] != None in preferences and preferences["unIndentedLinePattern"].match(line):
                logger.debug("unIndentedLinePattern")
                QPlainTextEdit.keyPressEvent(self, key_event)
            else:
                QPlainTextEdit.keyPressEvent(self, key_event)
                self.indent(indentation)
        elif key_event.text() != "":
            scope = self.getCurrentScope()
            preferences = PMXPreference.buildSettings(PMXBundle.getPreferences(scope))
            smart_typing_test = map(lambda pair: pair[0], preferences["smartTypingPairs"])
            character = unicode(key_event.text())
            # Handle smart typing pairs
            if character in smart_typing_test:
                self.performCharacterAction( preferences["smartTypingPairs"][smart_typing_test.index(character)])
            else:
                QPlainTextEdit.keyPressEvent(self, key_event)
        else:
            QPlainTextEdit.keyPressEvent(self, key_event)

    def keyPressSnippetEvent(self, key_event):
        key = key_event.key()
        cursor = self.textCursor()
        
        if key == Qt.Key_Tab or key == Qt.Key_Backtab:
            (index, holder) = self.snippet.setDefaultHolder(cursor.position())
            if holder == None:
                self.snippet = None
                return key_event
            if key == Qt.Key_Tab:
                holder = self.snippet.next()
            else:
                holder = self.snippet.previous()
            if holder == None:
                cursor.setPosition(self.snippet.ends)
            else:
                index = holder.position()
                cursor.setPosition(index)
                cursor.setPosition(index + len(holder), QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)
        elif key == Qt.Key_Backspace or key == Qt.Key_Delete:
            starts = self.snippet.starts
            ends = self.snippet.ends
            if cursor.hasSelection():
                (index, holder) = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None:
                    self.snippet = None
                    return key_event
                holder.remove(cursor.selectionStart() - index, cursor.selectionEnd() - index)
                position = cursor.selectionStart()
            else:
                if key == Qt.Key_Delete:
                    (index, holder) = self.snippet.setDefaultHolder(cursor.position() + 1)
                else:
                    (index, holder) = self.snippet.setDefaultHolder(cursor.position())
                if holder == None:
                    self.snippet = None
                    return key_event
                if key == Qt.Key_Delete:
                    holder.remove(cursor.position() - index, cursor.position() - index + 1)
                    position = cursor.position()
                else:
                    holder.remove(cursor.position() - index - 1, cursor.position() - index)
                    position = cursor.position() - 1
            #Ajuste
            position += (holder.position() - index)
            cursor.setPosition(starts)
            cursor.setPosition(ends, QTextCursor.KeepAnchor)
            cursor.insertText(str(self.snippet))
            self.snippet.ends = cursor.position()
            cursor.setPosition(position)
            self.setTextCursor(cursor)
        elif 0x20 <= key <= 0x7E: #Para latin poner otra cosa
            starts = self.snippet.starts
            ends = self.snippet.ends
            if cursor.hasSelection():
                (index, holder) = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None or holder.last:
                    self.snippet = None
                    return key_event
                holder.remove(cursor.selectionStart() - index, cursor.selectionEnd() - index)
                position = cursor.selectionStart()
            else:
                (index, holder) = self.snippet.setDefaultHolder(cursor.position())
                if holder == None or holder.last:
                    self.snippet = None
                    return key_event
                position = cursor.position()
            holder.insert(unicode(key_event.text()), position - index)
            position += holder.position() - index + 1
            cursor.setPosition(starts)
            cursor.setPosition(ends, QTextCursor.KeepAnchor)
            cursor.insertText(str(self.snippet))
            self.snippet.ends = cursor.position()
            cursor.setPosition(position)
            self.setTextCursor(cursor)
        else:
            return key_event

    def performCharacterAction(self, pair):
        '''
        Substitutions when some characters are typed.
        These substitutions are held in a dictionary
        '''
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.beginEditBlock()
            cursor.insertText(pair[0])
            cursor.insertText(text)
            cursor.endEditBlock()

            cursor.beginEditBlock()
            cursor.insertText(pair[1])
            cursor.endEditBlock()
        else:
            cursor.beginEditBlock()
            cursor.insertText(pair[0])
            cursor.endEditBlock()
            
            cursor.beginEditBlock()
            cursor.insertText(pair[1])
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
            cursor.endEditBlock()
            self.setTextCursor(cursor)
        cursor.endEditBlock()

    #==========================================================================
    # BundleItems
    #==========================================================================

    def insertBundleItem(self, item, tabTrigger = False, indent = True):
        ''' Inserta un bundle item, por ahora un snippet, debe resolver el item antes de insertarlo
        '''
        cursor = self.textCursor()
        line = unicode(cursor.block().text())
        indentation = indent and self.indentationWhitespace(line) or ""
        if tabTrigger and item.tabTrigger != None:
            for _ in range(len(item.tabTrigger)):
                cursor.deletePreviousChar()
        if isinstance(item, PMXSnippet):
            #Snippet Item needs compile and clone
            if not item.ready:
                item.compile()
            item = item.clone()
            item.resolve(indentation = indentation, tabreplacement = self.tabKeyBehavior, environment = self.buildEnvironment(item))
            #Set starts
            if cursor.hasSelection():
                item.starts = cursor.selectionStart()
            else:
                item.starts = cursor.position()
            #Insert Snippet
            #TODO: que no sea por str sino un un render o algo de eso
            cursor.insertText(str(item))
            #Set end
            item.ends = cursor.position()
            holder = item.next()
            if holder != None:
                index = holder.position()
                cursor.setPosition(index)
                cursor.setPosition(index + len(holder), QTextCursor.KeepAnchor)
                self.snippet = item
            else:
                cursor.setPosition(item.ends)
            self.setTextCursor(cursor)
        elif isinstance(item, PMXCommand):
            char = line and line[cursor.columnNumber() - 1] or ""
            item.resolve(unicode(self.toPlainText()), char, environment = self.buildEnvironment(item))
            functions = {
                         'replaceSelectedText': self.replaceSelectedText,
                         'replaceDocument': self.replaceDocument,
                         'insertText': self.insertText,
                         'afterSelectedText': self.afterSelectedText,
                         'insertAsSnippet': self.insertSnippet,
                         'showAsHTML': self.root.showHtml,
                         'showAsTooltip': self.root.showTooltip,
                         'createNewDocument': self.root.createNewDocument
                         }
            item.execute(functions)
        elif isinstance(item, PMXSyntax):
            self.setSyntax(item)

    def selectBundleItem(self, items, tabTrigger = False):
        syntax = any(map(lambda item: isinstance(item, PMXSyntax), items))
        menu = QMenu()
        for index, item in enumerate(items):
            action = menu.addAction(item.name + "\t &" + str(index + 1))
            receiver = lambda item = item: self.insertBundleItem(item, tabTrigger = tabTrigger)
            self.connect(action, SIGNAL('triggered()'), receiver)
        if syntax:
            point = self.root.cursor().pos()
        else:
            point = self.viewport().mapToGlobal(self.cursorRect(self.textCursor()).bottomRight())
        menu.exec_(point)
    
    def buildEnvironment(self, item):
        cursor = self.textCursor()
        line = unicode(cursor.block().text())
        scope = self.getCurrentScope()
        preferences = PMXPreference.buildSettings(PMXBundle.getPreferences(scope))
        try:
            match = filter(lambda m: m.start() <= cursor.columnNumber() <= m.end(), self.WORD.finditer(line)).pop()
            current_word = line[match.start():match.end()]
            current_word_index = match.start()
        except IndexError:
            current_word = ""
        env = item.buildEnvironment()
        env.update({
                'TM_CURRENT_LINE': line,
                'TM_LINE_INDEX': unicode(cursor.columnNumber()), 
                'TM_LINE_NUMBER': unicode(cursor.block().blockNumber()), 
                'TM_SCOPE': unicode(scope),
                'TM_SOFT_TABS': self.soft_tabs and u'YES' or u'NO',
                'TM_TAB_SIZE': unicode(self.tab_size),
        });
        if current_word != "":
            env['TM_CURRENT_WORD'] = unicode(current_word)
            env['TM_CURRENT_WORD_INDEX'] = unicode(current_word_index)
        if self.syntax != None:
            env['TM_MODE'] = unicode(self.syntax.name)
        if self.parent().file.path != None:
            env['TM_FILEPATH'] = unicode(self.parent().file.path)
            env['TM_FILENAME'] = unicode(self.parent().file.filename)
            env['TM_DIRECTORY'] = unicode(self.parent().file.directory)
        if cursor.hasSelection():
            env['TM_SELECTED_TEXT'] = unicode(cursor.selectedText().replace(u'\u2029', '\n'))
        env.update(self._meta.settings['static_variables'])
        env.update(preferences['shellVariables'])
        return env

    #==========================================================================
    # Commands
    #==========================================================================
    
    def replaceSelectedText(self, input, string):
        cursor = self.textCursor()
        position = cursor.selectionStart()
        cursor.removeSelectedText()
        cursor.setPosition(position)
        cursor.insertText(string)
        self.setTextCursor(cursor)
        
    def replaceDocument(self, input, string):
        print "replace document", string
        
    def insertText(self, input, string):
        cursor = self.textCursor()
        cursor.insertText(string)
    
    def afterSelectedText(self, input, string):
        cursor = self.textCursor()
        position = cursor.selectionEnd()
        cursor.setPosition(position)
        cursor.insertText(string)
    
    def insertSnippet(self, input, snippet):
        '''Create a new snippet and insert'''
        cursor = self.textCursor()
        if input == 'selection' and cursor.hasSelection():
            position = cursor.selectionStart()
            cursor.removeSelectedText()
            cursor.setPosition(position)
            self.setTextCursor(cursor)
        elif input == 'word':
            line = unicode(cursor.block().text())
            match = filter(lambda m: m.start() <= cursor.columnNumber() <= m.end(), self.WORD.finditer(line)).pop()
            current_word = line[match.start():match.end()]
            index = cursor.columnNumber() - match.start()
            for _ in range(index):
                cursor.deletePreviousChar()
            for _ in range(len(current_word) - index):
                cursor.deleteChar()
        self.insertBundleItem(snippet, indent = False)

    #==========================================================================
    # Folding
    #==========================================================================
    
    def codeFoldingEvent(self, line_number):
        if line_number in self.folded:
            self._unfold(line_number)
        else:
            self._fold(line_number)
        self.update()
        self.sidebar.update()
    
    def _fold(self, line_number):
        startBlock = self.document().findBlockByNumber(line_number - 1)
        endBlock = self._find_block_fold_closing(startBlock)

        block = startBlock
        while block.isValid() and block != endBlock:
            block = block.next()
            user_data = block.userData()
            user_data.folding += 1
            block.setVisible(user_data.folding == PMXBlockUserData.FOLDING_NONE)
            block = block.next()
        
        self.folded.append(line_number)
        self.document().markContentsDirty(startBlock.position(), endBlock.position())

    def _unfold(self, line_number):
        '''startBlock = self.document().findBlockByNumber(line_number - 1)
        endPos = self._find_block_fold_closing(startBlock)
        endBlock = self.document().findBlockByNumber(endPos)

        block = startBlock.next()
        while block.isValid() and block != endBlock:
            block.setVisible(True)
            block.setLineCount(block.layout().lineCount())
            endPos = block.position() + block.length()
            if block.blockNumber() in self.folded:
                close = self._find_fold_closing(block)
                block = self.document().findBlockByNumber(close)
            else:
                block = block.next()
        '''
        self.folded.remove(line_number)
        #self.document().markContentsDirty(startBlock.position(), endPos)

    def _find_block_fold_closing(self, start):
        end = start
        if start.userData().folding == PMXBlockUserData.FOLDING_START:
            #Find Next
            start_counter = 0
            while end.userData().folding != PMXBlockUserData.FOLDING_STOP or (end.userData().folding == PMXBlockUserData.FOLDING_STOP and start_counter != 0):
                end = end.next()
                if end.userDate().folding == PMXBlockUserData.FOLDING_START:
                    start_counter += 1
                elif end.userDate().folding == PMXBlockUserData.FOLDING_STOP:
                    start_counter -= 1
        else:
            #Find Previous
            end_counter = 0
            while end.userData().folding != PMXBlockUserData.FOLDING_START or (end.userData().folding == PMXBlockUserData.FOLDING_START and end_counter != 0):
                end = end.previous()
                if end.userDate().folding == PMXBlockUserData.FOLDING_STOP:
                    end_counter += 1
                elif end.userDate().folding == PMXBlockUserData.FOLDING_START:
                    end_counter -= 1
        return end
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
    
    #===========================================================================
    # Text Indentation
    #===========================================================================
    
    @classmethod
    def indentationWhitespace(cls, text):
        '''
        Gets text whitespace
        @param text: Text, QTextCursor o QTextBlock instance
        @return: The text whitespace
        '''
        match = cls.WHITESPACE.match(text)
        try:
            ws = match.group('whitespace')
            return ws
        except AttributeError:
            return ''
    
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
        block_count = self.selectionBlockEnd() - self.selectionBlockStart() + 1
        cursor = self.textCursor()
        cursor.beginEditBlock()
        new_cursor = QTextCursor(cursor)
        new_cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor, block_count - 1)
        new_cursor.movePosition(QTextCursor.StartOfBlock)
        for _i in range(block_count):
            new_cursor.insertText(indentation)
            new_cursor.movePosition(QTextCursor.NextBlock)
        self.setTextCursor(cursor)
        cursor.endEditBlock()

    def can_unindent(self):
        '''
        Check if un-indetation is possible
        @returns True if indentation is possible, false otherwise
        '''
        block_count = self.selectionBlockEnd() - self.selectionBlockStart() + 1
        new_cursor = QTextCursor( self.textCursor() )
        new_cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor, block_count -1)
        new_cursor.movePosition(QTextCursor.StartOfBlock)
        for i in range(block_count):
            if not new_cursor.block().text().startsWith(self.tabKeyBehavior):
                new_cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor, i)
                return False
        del new_cursor
        return True
    
    def unindent(self):
        '''
        Unindents text, fails if can_unindent() returns False
        '''
        if not self.can_unindent():
            return
        block_count = self.selectionBlockEnd() - self.selectionBlockStart() + 1
        cursor = self.textCursor()
        cursor.beginEditBlock()
        new_cursor = QTextCursor(cursor)
        new_cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor, block_count -1)
        new_cursor.movePosition(QTextCursor.StartOfBlock)

        for _i in range(block_count):
            if self.soft_tabs:
                for _j in range(self.tab_size):
                    new_cursor.deleteChar()
            else:
                new_cursor.deleteChar()
                    
            new_cursor.movePosition(QTextCursor.NextBlock)
            
            self.setTextCursor(cursor)
        cursor.endEditBlock()

    MAX_FONT_POINT_SIZE = 32
    MIN_FONT_POINT_SIZE = 6
    
    @property
    def font_size(self):
        font = self.font()
        pt_size = font.pointSize()
        return pt_size

    @font_size.setter
    def font_size(self, value):
        font = self.font()
        font.setPointSize(value)
        self.setFont(font)
        