# -*- encoding: utf-8 -*-

import re, logging
from bisect import bisect
from PyQt4.QtCore import QRect, Qt, SIGNAL, QEvent
from PyQt4.QtGui import QPlainTextEdit, QTextEdit, QTextFormat, QMenu, \
    QTextCursor, QAction, QFont, QPalette
from prymatex.bundles import PMXBundle, PMXSnippet
from prymatex.bundles.command import PMXCommand
from prymatex.bundles.syntax import PMXSyntax
from prymatex.bundles.theme import PMXTheme
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.gui.editor.sidebar import PMXSidebar
from prymatex.gui.editor.syntax import PMXSyntaxProcessor, PMXBlockUserData

logger = logging.getLogger(__name__)

# Key press debugging 
KEY_NAMES = dict([(getattr(Qt, keyname), keyname) for keyname in dir(Qt) 
                  if keyname.startswith('Key_')])

ANYKEY = -1

def debug_key(key_event):
    ''' Prevents hair loss when debuging what the hell is going on '''
    key = key_event.key()
    mods = []
    print "count: ", key_event.count()
    print "isAutoRepeat: ", key_event.isAutoRepeat()
    print "key: ", key_event.key()
    print "nativeModifiers: ", key_event.nativeModifiers()
    print "nativeScanCode: ", key_event.nativeScanCode()
    print "nativeVirtualKey: ", key_event.nativeVirtualKey()
    print "text: ", unicode(key_event.text()).encode('utf-8')
    print "isAccepted: ", key_event.isAccepted()
    print "modifiers: ", int(key_event.modifiers())
    modifiers = key_event.modifiers()
    if modifiers & Qt.AltModifier:
        mods.append("AltModifier")
    if modifiers & Qt.ControlModifier:
        mods.append("ControlModifier")
    if modifiers & Qt.MetaModifier:
        mods.append("MetaModifier")
    if modifiers & Qt.ShiftModifier:
        mods.append("ShiftModifier")
    
    print "%s <%s> Code: %d chr(%d) = %s" % (KEY_NAMES[key],  ", ".join(mods), 
                                              key, key, key < 255 and chr(key) 
                                              or 'N/A')
    
class PMXCodeEdit(QPlainTextEdit, PMXObject):
    '''
    The GUI element which holds the editor.
    This class acts as a buffer for text, it does not know anything about
    the underlying filesystem.
    
    It holds the highlighter and the folding
    
    '''
    
    WHITESPACE = re.compile(r'^(?P<whitespace>\s+)', re.UNICODE)
    TABTRIGGERSPLIT = re.compile(r"\w+|\W+", re.UNICODE)
    WORD = re.compile(r'\w+', re.UNICODE)
    
    fontMinSize = 6
    fontMaxSize = 30
    #=======================================================================
    # Settings, config
    #=======================================================================
    @pmxConfigPorperty(default = 'text.plain')
    def defaultSyntax(self, scope):
        syntax = PMXSyntax.getSyntaxByScope(scope)
        if syntax != None:
            self.setSyntax(syntax)
    
    softTabs = pmxConfigPorperty(default = True)
    tabSize = pmxConfigPorperty(default = 4)
    font = pmxConfigPorperty(default = QFont('Monospace', 10))
    
    @pmxConfigPorperty(default = 'Twilight')
    def theme(self, name):
        theme = PMXTheme.getThemeByName(name)
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
    
    class Meta(object):
        settings = 'editor'
    
    @property
    def tabKeyBehavior(self):
        return self.softTabs and u' ' * self.tabSize or u'\t'
    
    def __init__(self, parent = None):
        super(PMXCodeEdit, self).__init__(parent)
        self.sidebar = PMXSidebar(self)
        self.processor = PMXSyntaxProcessor(self)
        self.bookmarks = []
        self.folded = []
        self.snippet = None
        
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
        
    def getCurrentWordAndIndex(self):
        cursor = self.textCursor()
        line = unicode(cursor.block().text())
        matchs = filter(lambda m: m.start() <= cursor.columnNumber() <= m.end(), self.WORD.finditer(line))
        if matchs:
            match = matchs.pop()
            word = line[match.start():match.end()]
            index = cursor.columnNumber() - match.start()
            return word, index
        return "", 0
    
    def getTabTriggerSymbol(self):
        cursor = self.textCursor()
        line = unicode(cursor.block().text())
        matchs = filter(lambda m: m.start() <= cursor.columnNumber() <= m.end(), self.TABTRIGGERSPLIT.finditer(line))
        if matchs:
            match = matchs.pop()
            word = line[match.start():match.end()]
            index = cursor.columnNumber() - match.start()
            return word, index
        return "", 0
    
    def sendCursorPosChange(self):
        c = self.textCursor()
        line  = c.blockNumber()
        col = c.columnNumber()
        self.editorCursorPositionChangedEvent(line+1, col+1)
        
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

    #=======================================================================
    # Event Filter
    #=======================================================================
    def eventFilter(self, object, event):
        if (event.type() == QEvent.KeyPress):
            debug_key(event)
        return super(PMXCodeEdit, self).eventFilter(object, event)

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
            super(PMXCodeEdit, self).wheelEvent(event)
    
    def mousePressEvent(self, mouse_event):
        #self.inserSpacesUpToPoint(mouse_event.pos())
        super(PMXCodeEdit, self).mousePressEvent(mouse_event)

    def mouseMoveEvent(self, event):
        #position = event.pos()
        #QToolTip.showText(self.mapToGlobal(position), "Cacho", self)
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
    
    def keyPressEvent(self, event):
        '''
        This method is called whenever a key is pressed. The key code is stored in key_event.key()
        '''
        #Check for snippet mode
        event.ignore()
        if self.snippet != None:
            self.keyPressSnippetEvent(event)
            if event.isAccepted():
                return
        else:
            self.keyPressBundleItem(event)
            if event.isAccepted():
                return
        
        KEYEVENT_HANDLERS = {
            Qt.Key_Tab: [self.eventKeyTabBundleItem, self.eventKeyTabIndent],
            Qt.Key_Backtab: [self.eventKeyBacktabUnindent],
            Qt.Key_Backspace:  [self.eventKeyBackspaceSmartTyping],
            Qt.Key_Return: [self.eventKeyReturnSyntax], #, self.eventKeyReturnIndent
            ANYKEY: [self.eventKeyAnyIndent, self.eventKeyAnySmartTyping]
        } 

        handlers = KEYEVENT_HANDLERS[event.key()] if event.key() in KEYEVENT_HANDLERS else KEYEVENT_HANDLERS[ANYKEY]
        
        for handler in handlers:
            handler(event)
            if event.isAccepted():
                return
                
        super(PMXCodeEdit, self).keyPressEvent(event)
        
        #Cosas luego del evento
    
    def keyPressBundleItem(self, event):
        code = int(event.modifiers()) + event.key()
        scope = self.getCurrentScope()
        items = PMXBundle.getKeyEquivalentItem(code, scope)
        if items:
            if len(items) > 1:
                self.selectBundleItem(items)
            else:
                self.insertBundleItem(items[0])
            event.accept()
            
    def keyPressSnippetEvent(self, event):
        key = event.key()
        cursor = self.textCursor()
        
        if key == Qt.Key_Tab or key == Qt.Key_Backtab:
            (index, holder) = self.snippet.setDefaultHolder(cursor.position())
            if holder == None:
                self.snippet = None
                return
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
            event.accept()
        elif key == Qt.Key_Backspace or key == Qt.Key_Delete:
            starts = self.snippet.starts
            ends = self.snippet.ends
            if cursor.hasSelection():
                (index, holder) = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None:
                    self.snippet = None
                    return
                holder.remove(cursor.selectionStart() - index, cursor.selectionEnd() - index)
                position = cursor.selectionStart()
            else:
                if key == Qt.Key_Delete:
                    (index, holder) = self.snippet.setDefaultHolder(cursor.position() + 1)
                else:
                    (index, holder) = self.snippet.setDefaultHolder(cursor.position())
                if holder == None:
                    self.snippet = None
                    return
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
            event.accept()
        elif 0x20 <= key <= 0x7E: #Para latin poner otra cosa
            starts = self.snippet.starts
            ends = self.snippet.ends
            if cursor.hasSelection():
                (index, holder) = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None or holder.last:
                    self.snippet = None
                    return
                holder.remove(cursor.selectionStart() - index, cursor.selectionEnd() - index)
                position = cursor.selectionStart()
            else:
                (index, holder) = self.snippet.setDefaultHolder(cursor.position())
                if holder == None or holder.last:
                    self.snippet = None
                    return
                position = cursor.position()
            holder.insert(unicode(event.text()), position - index)
            position += holder.position() - index + 1
            cursor.setPosition(starts)
            cursor.setPosition(ends, QTextCursor.KeepAnchor)
            cursor.insertText(str(self.snippet))
            self.snippet.ends = cursor.position()
            cursor.setPosition(position)
            self.setTextCursor(cursor)
            event.accept()
    
    #=======================================================================
    # Tab Keyboard Events
    #=======================================================================
    
    def eventKeyTabBundleItem(self, event):
        scope = self.getCurrentScope()
        word, index = self.getCurrentWordAndIndex()
        #TODO: Ver si va a tener scope o no
        # if index is end of word
        if len(word) == index and (scope or word):
            snippets = PMXBundle.getTabTriggerItem(word, scope)
            if len(snippets) > 1:
                self.selectBundleItem(snippets, tabTrigger = True)
                event.accept()
            elif snippets:
                self.insertBundleItem(snippets[0], tabTrigger = True)
                event.accept()
    
    def eventKeyTabIndent(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.indent(self.tabKeyBehavior)
        else:
            cursor.insertText(self.tabKeyBehavior)
        event.accept()
    
    #=======================================================================
    # Backtab Keyboard Events
    #=======================================================================
    
    def eventKeyBacktabUnindent(self, event):
        self.unindent()
        event.accept()
    
    #=======================================================================
    # Backspace Keyboard Events
    #=======================================================================
    def eventKeyBackspaceSmartTyping(self, key_event):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            doc = self.document()
            scope = self.getCurrentScope()
            preferences = PMXBundle.getPreferenceSettings(scope)
            if preferences.smartTypingPairs:
                character = doc.characterAt(cursor.position() - 1).toAscii()
                pairs = filter(lambda pair: pair[0] == character or pair[1] == character, preferences.smartTypingPairs)
                if pairs and pairs[0][0] == character and doc.characterAt(cursor.position()).toAscii() == pairs[0][1]:
                    cursor.deleteChar()
                elif pairs and pairs[0][1] == character and doc.characterAt(cursor.position() - 2).toAscii() == pairs[0][0]:
                    cursor.deletePreviousChar()
    
    #=======================================================================
    # Return Keyboard Events
    #=======================================================================
    
    def eventKeyReturnSyntax(self, event):
        line = unicode(self.textCursor().block().text())
        if self.document().blockCount() == 1:
            syntax = PMXSyntax.findSyntaxByFirstLine(line)
            if syntax != None:
                self.setSyntax(syntax)
    
    def eventKeyReturnIndent(self, event):
        line = unicode(self.textCursor().block().text())
        scope = self.getCurrentScope()
        settings = PMXBundle.getPreferenceSettings(scope)
        acction = settings.indent(line)
        indentation = self.indentationWhitespace(line)
        if acction == settings.INDENT_INCREASE:
            print "increase"
            super(PMXCodeEdit, self).keyPressEvent(event)
            self.increaseIndent(indentation)
        elif acction == settings.INDENT_NEXTLINE:
            print "increasenext"
            super(PMXCodeEdit, self).keyPressEvent(event)
            self.increaseIndent(indentation)
        else:
            super(PMXCodeEdit, self).keyPressEvent(event)
            self.indent(indentation)
        event.accept()
    
    #=======================================================================
    # Other Keyboard Events
    #=======================================================================
    
    def eventKeyAnyIndent(self, key_event):
        key = key_event.key()
        if not (0 <= key <= 256):
            return False
        character = chr(key)
        cursor = self.textCursor()
        current_line = unicode(cursor.block().text()) + character
        scope = self.getCurrentScope()
        settings = PMXBundle.getPreferenceSettings(scope)
        acction = settings.indent(current_line)
        if acction == settings.INDENT_DECREASE:
            previous_block = cursor.block().previous()
            if previous_block:
                current_indentation = self.indentationWhitespace(current_line)
                previous_indentation = self.indentationWhitespace(previous_block.text())
                if current_indentation == previous_indentation:
                    self.unindent()
                    return True
        elif acction == settings.UNINDENT:
            print "unident"
        return False
    
    def eventKeyAnySmartTyping(self, event):
        cursor = self.textCursor()
        character = unicode(event.text())
        scope = self.getCurrentScope()
        preferences = PMXBundle.getPreferenceSettings(scope)
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
                super(PMXCodeEdit, self).keyPressEvent(event)
                cursor.insertText(pairs[0][1])
                cursor.setPosition(position + 1)
            self.setTextCursor(cursor)
            event.accept()

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
                         'showAsHTML': self.mainwindow.showHtml,
                         'showAsTooltip': self.mainwindow.showTooltip,
                         'createNewDocument': self.mainwindow.createNewDocument
                         }
            item.execute(functions)
        elif isinstance(item, PMXSyntax):
            self.setSyntax(item)

    def selectBundleItem(self, items, tabTrigger = False):
        syntax = any(map(lambda item: isinstance(item, PMXSyntax), items))
        menu = QMenu()
        for index, item in enumerate(items):
            action = menu.addAction(item.buildMenuTextEntry("&" + str(index + 1)))
            receiver = lambda item = item: self.insertBundleItem(item, tabTrigger = tabTrigger)
            self.connect(action, SIGNAL('triggered()'), receiver)
        if syntax:
            point = self.mainwindow.cursor().pos()
        else:
            point = self.viewport().mapToGlobal(self.cursorRect(self.textCursor()).bottomRight())
        menu.exec_(point)
    
    def buildEnvironment(self, item):
        cursor = self.textCursor()
        line = unicode(cursor.block().text())
        scope = self.getCurrentScope()
        preferences = PMXBundle.getPreferenceSettings(scope)
        try:
            match = filter(lambda m: m.start() <= cursor.columnNumber() <= m.end(), self.WORD.finditer(line)).pop()
            current_word = line[match.start():match.end()]
        except IndexError:
            current_word = ""
        env = item.buildEnvironment()
        env.update({
                'TM_CURRENT_LINE': line,
                'TM_LINE_INDEX': cursor.columnNumber(), 
                'TM_LINE_NUMBER': cursor.block().blockNumber() + 1, 
                'TM_SCOPE': scope,
                'TM_SOFT_TABS': self.softTabs and u'YES' or u'NO',
                'TM_TAB_SIZE': self.tabSize,
        });
        if current_word != "":
            env['TM_CURRENT_WORD'] = current_word
        if self.syntax != None:
            env['TM_MODE'] = self.syntax.name
        if self.parent().file.path != None:
            env['TM_FILEPATH'] = self.parent().file.path
            env['TM_FILENAME'] = self.parent().file.filename
            env['TM_DIRECTORY'] = self.parent().file.directory
        if cursor.hasSelection():
            env['TM_SELECTED_TEXT'] = cursor.selectedText().replace(u'\u2029', '\n')
        #env.update(self._meta.settings['static_variables'])
        env.update(preferences.shellVariables)
        return env

    #==========================================================================
    # Commands
    #==========================================================================
    
    def replaceSelectedText(self, string, **kwargs):
        if 'input' in kwargs and kwargs['input'] == 'document':
            self.replaceDocument(string, **kwargs)
        else:
            cursor = self.textCursor()
            position = cursor.selectionStart()
            cursor.insertText(string)
            cursor.setPosition(position, position + len(string))
            self.setTextCursor(cursor)
        
    def replaceDocument(self, string, **kwargs):
        self.document().setPlainText(string)
        
    def insertText(self, string, **kwargs):
        cursor = self.textCursor()
        cursor.insertText(string)
    
    def afterSelectedText(self, string, **kwargs):
        cursor = self.textCursor()
        position = cursor.selectionEnd()
        cursor.setPosition(position)
        cursor.insertText(string)
    
    def insertSnippet(self, snippet, **kwargs):
        '''Create a new snippet and insert'''
        cursor = self.textCursor()
        if 'input' in kwargs:
            if kwargs['input'] == 'selection':
                position = cursor.selectionStart()
                cursor.removeSelectedText()
                cursor.setPosition(position)
                self.setTextCursor(cursor)
                self.insertBundleItem(snippet, indent = False)
            elif kwargs['input'] == 'word':
                line = unicode(cursor.block().text())
                match = filter(lambda m: m.start() <= cursor.columnNumber() <= m.end(), self.WORD.finditer(line)).pop()
                current_word = line[match.start():match.end()]
                index = cursor.columnNumber() - len(current_word)
                index = index >= 0 and index or 0
                index = line.find(current_word, index)
                cursor.setPosition(cursor.block().position() + index)
                self.setTextCursor(cursor)
                for _ in range(len(current_word)):
                    cursor.deleteChar()
                self.insertBundleItem(snippet)
        else:
            self.insertBundleItem(snippet, indent = False)

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
        user_data = milestone.userData()
        if user_data.folding == PMXBlockUserData.FOLDING_START:
            startBlock = self.document().findBlockByNumber(line_number)
            endBlock = self._find_block_fold_close(startBlock)
        else:
            endBlock = milestone
            milestone = self._find_block_fold_open(endBlock)
            startBlock = milestone.next()
        if endBlock == None or startBlock == None:
            return;
        
        block = startBlock
        while True:
            user_data = block.userData()
            user_data.foldingLevel += 1
            block.setVisible(user_data.foldingLevel == PMXBlockUserData.FOLDING_NONE)
            if block == endBlock:
                break
            block = block.next()

        milestone.userData().folded = True
        self.document().markContentsDirty(startBlock.position(), endBlock.position())

    def _unfold(self, line_number):
        milestone = self.document().findBlockByNumber(line_number - 1)
        startBlock = self.document().findBlockByNumber(line_number)
        endBlock = self._find_block_fold_close(startBlock)
        if endBlock == None:
            return;
        
        block = startBlock
        while True:
            user_data = block.userData()
            user_data.foldingLevel -= 1
            block.setVisible(user_data.foldingLevel == PMXBlockUserData.FOLDING_NONE)
            if block == endBlock:
                break
            block = block.next()
        
        milestone.userData().folded = False
        self.document().markContentsDirty(startBlock.position(), endBlock.position())

    def _find_block_fold_close(self, start):
        end = start
        counter = 0
        while end.userData().folding != PMXBlockUserData.FOLDING_STOP or counter !=  0:
            if end.userData().folding == PMXBlockUserData.FOLDING_START:
                counter += 1
            elif end.userData().folding == PMXBlockUserData.FOLDING_STOP:
                counter -= 1
            end = end.next()
            if not end.isValid():
                return None
        return end
    
    def _find_block_fold_open(self, end):
        start = end.previous()
        counter = 0
        while start.userData().folding != PMXBlockUserData.FOLDING_START or counter !=  0:
            if start.userData().folding == PMXBlockUserData.FOLDING_STOP:
                counter += 1
            elif start.userData().folding == PMXBlockUserData.FOLDING_START:
                counter -= 1
            start = start.previous()
            if not start.isValid():
                return None
        return start
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
    
    def zoomIn(self):
        font = self.font
        size = self.font.pointSize()
        if size < self.fontMaxSize:
            size += 2
            font.setPointSize(size)
        self.font = font

    def zoomOut(self):
        font = self.font
        size = font.pointSize()
        if size > self.fontMinSize:
            size -= 2
            font.setPointSize(size)
        self.font = font

    
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
                counter = self.tabSize if data.indentLevel > self.tabSize else data.indentLevel
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
            counter = self.tabSize if data.indentLevel > self.tabSize else data.indentLevel
            if counter > 0:
                cursor.beginEditBlock()
                position = block.position() if block.position() <= cursor.position() <= block.position() + self.tabSize else cursor.position() - counter
                cursor.setPosition(block.position()) 
                for _ in range(counter):
                    cursor.deleteChar()
                cursor.setPosition(position)
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
        
