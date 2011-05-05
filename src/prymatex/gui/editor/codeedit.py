# -*- encoding: utf-8 -*-

import re, logging
from bisect import bisect
from PyQt4.QtCore import QRect, Qt, SIGNAL
from PyQt4.QtGui import QPlainTextEdit, QTextEdit, QTextFormat, QMenu, \
    QTextCursor, QAction, QFont, QPalette
from prymatex.bundles import PMXBundle, PMXSnippet, PMXMacro, PMXCommand, PMXSyntax, PMXTheme
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.gui.editor.sidebar import PMXSidebar
from prymatex.gui.editor.processor import PMXSyntaxProcessor, PMXBlockUserData, PMXCommandProcessor, PMXMacroProcessor

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
    WORD = re.compile(r'\w+', re.UNICODE)
        
    #=======================================================================
    # Settings, config
    #=======================================================================
    @pmxConfigPorperty(default = u'3130E4FA-B10E-11D9-9F75-000D93589AF6')
    def defaultSyntax(self, uuid):
        syntax = PMXSyntax.getSyntaxByUUID(uuid)
        if syntax != None:
            self.setSyntax(syntax)
    
    softTabs = pmxConfigPorperty(default = True)
    tabSize = pmxConfigPorperty(default = 4)
    font = pmxConfigPorperty(default = QFont('Monospace', 10))
    
    @pmxConfigPorperty(default = u'766026CB-703D-4610-B070-8DE07D967C5F')
    def theme(self, uuid):
        theme = PMXTheme.getThemeByUUID(uuid)
        self.syntaxProcessor.formatter = theme
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
    
    @property
    def snippetMode(self):
        return hasattr(self, 'snippet') and self.snippet != None
    
    @property
    def multiEditMode(self):
        """retorna si el editor esta en modo multiedit"""
        return bool(self.cursors)
    
    def __init__(self, parent = None):
        super(PMXCodeEdit, self).__init__(parent)
        self.sidebar = PMXSidebar(self)
        #Processors
        self.syntaxProcessor = PMXSyntaxProcessor(self)
        self.commandProcessor = PMXCommandProcessor(self)
        self.macroProcessor = PMXMacroProcessor(self)
        
        self.bookmarks = []
        self.folded = []
        self.cursors = []
        
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
        if not bool(user_data) and block.userState() == self.syntaxProcessor.MULTI_LINE:
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
        return None, 0
    
    def getSelectionBlockStartEnd(self):
        cursor = self.textCursor()
        start, end = cursor.selectionStart(), cursor.selectionEnd()
        if start > end:
            return self.document().findBlock(end), self.document().findBlock(start)
        else:
            return self.document().findBlock(start), self.document().findBlock(end)
    
    def sendCursorPosChange(self):
        c = self.textCursor()
        line  = c.blockNumber()
        col = c.columnNumber()
        self.editorCursorPositionChangedEvent(line+1, col+1)
        
    def setSyntax(self, syntax):
        #print self.syntaxProcessor.syntax, syntax
        if self.syntaxProcessor.syntax != syntax:
            self.syntaxProcessor.syntax = syntax
            self.editorSetSyntaxEvent(syntax)
    
    @property
    def syntax(self):
        return self.syntaxProcessor.syntax
        
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
    # QPlainTextEdit Events
    #=======================================================================
    def paintEvent(self, event):
        #self.syntaxProcessor.rehighlight()
        super(PMXCodeEdit, self).paintEvent(event)
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

    def mouseDoubleClickEvent(self, event):
        print "mouseDoubleClickEvent"
        super(PMXCodeEdit, self).mouseDoubleClickEvent(event)
        
    def mouseReleaseEvent(self, event):
        print "mouseReleaseEvent"
        super(PMXCodeEdit, self).mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        print "mousePressEvent"
        if event.modifiers() == Qt.ControlModifier:
            position = event.pos()
            cursor = self.cursorForPosition(position)
            self.cursors.append(QTextCursor(cursor))
            print self.cursors
        else:
            super(PMXCodeEdit, self).mousePressEvent(event)

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
        #Si lo toma un bundle item o un snippet retorno
        if self.snippetMode: #Modo Snippet
            if self.keyPressBundleItem(event):
                return
            elif self.keyPressSnippet(event):
                return
        elif self.multiEditMode:
            if self.keyPressBundleItem(event): #Modo MultiEdit
                self.cursors = []
                return
        else:
            if self.keyPressBundleItem(event): #Modo Normal
                return
            elif self.keyPressSmartTyping(event):
                return
        
        def handleEvent(event):
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
                super(PMXCodeEdit, self).keyPressEvent(event)
            
            #Luego de tratar el evento, solo si se inserto algo de texto
            if event.text() != "":
                self.keyPressIndent(event)
        
        if self.multiEditMode:
            if event.key() != Qt.Key_Escape:
                cursors = self.cursors + [ self.textCursor() ]
                for cursor in cursors:
                    self.setTextCursor(cursor)
                    handleEvent(event)
            else:
                self.cursors = []
        else:
            handleEvent(event)
    
    def keyPressBundleItem(self, event):
        code = int(event.modifiers()) + event.key()
        scope = self.getCurrentScope()
        items = PMXBundle.getKeyEquivalentItem(code, scope)
        if items:
            if len(items) > 1:
                self.selectBundleItem(items)
            else:
                self.insertBundleItem(items[0])
            return True

    def keyPressSnippet(self, event):
        key = event.key()
        cursor = self.textCursor()
        
        if key == Qt.Key_Tab or key == Qt.Key_Backtab:
            if cursor.hasSelection():
                (index, holder) = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
            else:
                (index, holder) = self.snippet.setDefaultHolder(cursor.position())
            if holder == None:
                self.snippet = None
                return False
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
            return True
        elif key == Qt.Key_Backspace or key == Qt.Key_Delete:
            starts = self.snippet.starts
            ends = self.snippet.ends
            if cursor.hasSelection():
                (index, holder) = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None:
                    self.snippet = None
                    return False
                holder.remove(cursor.selectionStart() - index, cursor.selectionEnd() - index)
                position = cursor.selectionStart()
            else:
                if key == Qt.Key_Delete:
                    (index, holder) = self.snippet.setDefaultHolder(cursor.position() + 1)
                else:
                    (index, holder) = self.snippet.setDefaultHolder(cursor.position())
                if holder == None:
                    self.snippet = None
                    return False
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
            return True
        elif 0x20 <= key <= 0x7E: #Para latin poner otra cosa
            starts = self.snippet.starts
            ends = self.snippet.ends
            if cursor.hasSelection():
                (index, holder) = self.snippet.setDefaultHolder(cursor.selectionStart(), cursor.selectionEnd())
                if holder == None or holder.last:
                    self.snippet = None
                    return False
                holder.remove(cursor.selectionStart() - index, cursor.selectionEnd() - index)
                position = cursor.selectionStart()
            else:
                (index, holder) = self.snippet.setDefaultHolder(cursor.position())
                if holder == None or holder.last:
                    self.snippet = None
                    return False
                position = cursor.position()
            holder.insert(unicode(event.text()), position - index)
            position += holder.position() - index + 1
            cursor.setPosition(starts)
            cursor.setPosition(ends, QTextCursor.KeepAnchor)
            cursor.insertText(str(self.snippet))
            self.snippet.ends = cursor.position()
            cursor.setPosition(position)
            self.setTextCursor(cursor)
            return True
            
    def keyPressSmartTyping(self, event):
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
            return True

    #=======================================================================
    # Tab Keyboard Events
    #=======================================================================
    def tabPressEvent(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection():
            self.indent(self.tabKeyBehavior)
        elif self.multiEditMode:
            cursor.insertText(self.tabKeyBehavior)
        else:
            scope = self.getCurrentScope()
            trigger = PMXBundle.getTabTriggerSymbol(unicode(cursor.block().text()), cursor.columnNumber())
            if trigger != None:
                snippets = PMXBundle.getTabTriggerItem(trigger, scope)
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
            preferences = PMXBundle.getPreferenceSettings(scope)
            if preferences.smartTypingPairs:
                character = doc.characterAt(cursor.position() - 1).toAscii()
                pairs = filter(lambda pair: pair[0] == character or pair[1] == character, preferences.smartTypingPairs)
                if pairs and pairs[0][0] == character and doc.characterAt(cursor.position()).toAscii() == pairs[0][1]:
                    cursor.deleteChar()
                elif pairs and pairs[0][1] == character and doc.characterAt(cursor.position() - 2).toAscii() == pairs[0][0]:
                    cursor.deletePreviousChar()
        super(PMXCodeEdit, self).keyPressEvent(event)
    
    #=======================================================================
    # Return Keyboard Events
    #=======================================================================
    def returnPressEvent(self, event):
        line = unicode(self.textCursor().block().text())
        if self.document().blockCount() == 1:
            syntax = PMXSyntax.findSyntaxByFirstLine(line)
            if syntax != None:
                self.setSyntax(syntax)
        super(PMXCodeEdit, self).keyPressEvent(event)
        cursor = self.textCursor()
        block = cursor.block()
        prev = cursor.block().previous()
        if prev.userData().indentMark == PMXBlockUserData.INDENT_INCREASE:
            print "increase"
            cursor.insertText(prev.userData().indent + self.tabKeyBehavior)
        elif prev.userData().indentMark == PMXBlockUserData.INDENT_NEXTLINE:
            print "increasenext"
        elif prev.userData().indentMark == PMXBlockUserData.UNINDENT:
            print "unindent"
        elif prev.userData().indentMark == PMXBlockUserData.INDENT_DECREASE:
            print "decrease"
            cursor.insertText(prev.userData().indent[:len(self.tabKeyBehavior)])
        else:
            print "preserve"
            cursor.insertText(prev.userData().indent)
    
    #=======================================================================
    # After Keyboard Events
    #=======================================================================
    
    def keyPressIndent(self, event):
        cursor = self.textCursor()
        block = cursor.block()
        prev = block.previous()
        if block.userData().indentMark == PMXBlockUserData.INDENT_DECREASE and prev.isValid() and prev.userData().indentMark == PMXBlockUserData.INDENT_NONE and block.userData().indent == prev.userData().indent:
            self.unindent()
    
    #==========================================================================
    # BundleItems
    #==========================================================================

    def insertBundleItem(self, item, tabTrigger = False, disableIndent = False):
        ''' Inserta un bundle item, por ahora un snippet, debe resolver el item antes de insertarlo
        '''
        cursor = self.textCursor()
        line = unicode(cursor.block().text())
        indentation = self.indentationWhitespace(line) if not disableIndent else ""
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
            item.execute(self.commandProcessor)
        elif isinstance(item, PMXSyntax):
            self.setSyntax(item)
        elif isinstance(item, PMXMacro):
            item.execute(self.macroProcessor)

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
    
    # item deprecated
    def buildEnvironment(self, item = None):
        cursor = self.textCursor()
        line = unicode(cursor.block().text())
        scope = self.getCurrentScope()
        preferences = PMXBundle.getPreferenceSettings(scope)
        current_word, _ = self.getCurrentWordAndIndex()
        if item != None:
            env = item.buildEnvironment()
        else:
            env = {}
        env.update({
                'TM_CURRENT_LINE': line,
                'TM_LINE_INDEX': cursor.columnNumber(), 
                'TM_LINE_NUMBER': cursor.block().blockNumber() + 1, 
                'TM_SCOPE': scope,
                'TM_SOFT_TABS': self.softTabs and u'YES' or u'NO',
                'TM_TAB_SIZE': self.tabSize,
        });
        if current_word != None:
            env['TM_CURRENT_WORD'] = current_word
        if self.syntax != None:
            env['TM_MODE'] = self.syntax.name
        if self.parent().file.path != None:
            env['TM_FILEPATH'] = self.parent().file.path
            env['TM_FILENAME'] = self.parent().file.filename
            env['TM_DIRECTORY'] = self.parent().file.directory
        if cursor.hasSelection():
            env['TM_SELECTED_TEXT'] = cursor.selectedText().replace(u'\u2029', '\n')
        env.update(preferences.shellVariables)
        return env

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
        if self.syntax.indentSensitive:
            end = start
            level = end.userData().indent
            while end.next().isValid() and level <= end.next().userData().indent:
                end = end.next()
                if end.userData().folding == PMXBlockUserData.FOLDING_STOP and end.userData().indent == level:
                    break
        else:
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
