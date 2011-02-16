# -*- encoding: utf-8 -*-

#
import sys
import traceback
import re
import logging

from PyQt4.QtCore import QRect
from PyQt4.QtGui import QPlainTextEdit, QTextEdit, QTextFormat
from PyQt4.QtGui import QTextCursor, QAction, QFont, QPalette
from PyQt4.QtCore import Qt, SIGNAL

from prymatex.core.base import PMXObject
from prymatex.core.config import Setting
from prymatex.bundles import PMXBundle, PMXPreference

logger = logging.getLogger(__name__)

#PMX Libs
if __name__ == "__main__":
    from os.path import join, dirname, abspath
    pmx_base = abspath(join(dirname(__file__), '..', '..', '..'))
    sys.path.append(pmx_base)
    sys.path.append('../..')
    #pmx_base = abspath(join(dirname(__file__), '..', '..', '..'))

from prymatex.gui.editor.sidearea import PMXSideArea
from prymatex.gui.editor.syntax import PMXSyntaxProcessor
from prymatex.bundles.theme import PMXTheme
from prymatex.bundles.syntax import PMXSyntax

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

    #-----------------------------------
    # Settings
    #-----------------------------------
    soft_tabs = Setting(default = True)
    tab_length = Setting(default = 4)
    font = Setting(default = {"name": "Monospace", "size": 10}, 
                   fset = lambda self, value: self.setFont(QFont(value["name"], value["size"]))
                   )
    
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
        palette.setColor(QPalette.Active, QPalette.Highlight, selection)
        palette.setColor(QPalette.Active, QPalette.AlternateBase, invisibles)
        self.setPalette(palette)
        self.line_highlight = style.getQColor('lineHighlight')
        self.highlightCurrentLine()
        
    theme_name = Setting(default = 'Twilight', fset = setTheme)

    def __init__(self, parent = None):
        super(PMXCodeEdit, self).__init__(parent)
        self.side_area = PMXSideArea(self)
        self.processor = PMXSyntaxProcessor(self.document())
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
        
    class Meta(object):
        settings = 'editor'

    #=======================================================================
    # Signals and Events
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
        
    def getCurrentScope(self):
        cursor = self.textCursor()
        user_data = cursor.block().userData()
        return user_data and user_data.getScopeAtPosition(cursor.columnNumber()) or ""
        
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
        '''
        Returns this tab index
        '''
        tab_widget = self.parent()
        return tab_widget.indexOf(self)

    @property
    def indent_text(self):
        if not self.soft_tabs:
            return '\t'
        else:
            return ' ' * self.tab_length

    def contextMenuEvent(self, event):
        '''
        '''
        menu = self.createStandardContextMenu()
        
        menu.addAction(self.actionIndent)
        menu.addAction(self.actionUnindent)
        self.actionUnindent.setEnabled(self.can_unindent())

        menu.exec_(event.globalPos());
        del menu
        
    def lineNumberAreaWidth(self):
        # si tiene folding tengo que sumar mas 10
        return 3 + self.fontMetrics().width('9') * len(str(self.blockCount())) + 10
        
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
    
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.side_area.scroll(0, dy);
        else:
            self.side_area.update(0, rect.y(), self.side_area.width(), rect.height());
        if (rect.contains(self.viewport().rect())):
            self.updateLineNumberAreaWidth(0)
    
    def resizeEvent(self, event):
        super(PMXCodeEdit, self).resizeEvent(event)
        cr = self.contentsRect()
        self.side_area.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
        
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

    def mousePressEvent(self, mouse_event):
        self.inserSpacesUpToPoint(mouse_event.pos())
        super(PMXCodeEdit, self).mousePressEvent(mouse_event)

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
    
    def keyPressSnippetEvent(self, key_event):
        key = key_event.key()
        cursor = self.textCursor()
        row = cursor.blockNumber()
        column = cursor.columnNumber()

        if key == Qt.Key_Tab or key == Qt.Key_Backtab:
            if not cursor.hasSelection():
                holder = self.snippet.current()
            elif key == Qt.Key_Tab:
                holder = self.snippet.next()
            else:
                holder = self.snippet.previous()
            if holder == None:
                #The end
                index = self.snippet.ends
                #FIXME:
                holder = ""
            else:
                index = self.snippet.position(holder)
            block = self.document().findBlockByNumber(index[0])
            cursor.setPosition(block.position() + index[1])
            cursor.setPosition(block.position() + cursor.columnNumber() + len(holder), QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)
        else:
            starts = self.snippet.starts
            ends = self.snippet.ends
            holder = self.snippet.getHolder((row, column))
            QPlainTextEdit.keyPressEvent(self, key_event)
            if holder != None:
                index = self.snippet.position(holder)
                block = self.document().findBlockByNumber(index[0])
                holder.write(unicode(block.text())[index[1]: cursor.columnNumber()])
                block = self.document().findBlockByNumber(starts[0])
                cursor.setPosition(block.position() + starts[1])
                block = self.document().findBlockByNumber(ends[0])
                cursor.setPosition(block.position() + ends[1], QTextCursor.KeepAnchor)
                cursor.removeSelectedText();
                cursor.insertText(str(self.snippet))
                index = self.snippet.position(holder)
                block = self.document().findBlockByNumber(index[0])
                cursor.setPosition(block.position() + index[1] + len(holder))
                self.setTextCursor(cursor)
            else:
                self.snippet = None
            
    def insertSnippet(self, trigger, snippet):
        #TODO: si es mas de uno seleccionar uno, si no selecciona retornar falso
        snippet = snippet[0]
        tab = self.soft_tabs and ' ' * self.tab_length or '\t'
        cursor = self.textCursor()
        row = cursor.blockNumber()
        column = cursor.columnNumber()
        text = unicode(cursor.block().text())
        indentation = self.identationWhitespace(text)
        
        snippet.resolve(indentation, tab, (row , column - len(trigger)), {})
        self.snippet = snippet
        for _ in range(len(trigger)):
            cursor.deletePreviousChar()
        cursor.insertText(str(snippet))
        return True
    
    def keyPressEvent(self, key_event):
        '''
        This method is called whenever a key is pressed. The key code is
        stored in key_event.key()
        '''
        
        if self.snippet != None:
            return self.keyPressSnippetEvent(key_event)
        
        key = key_event.key()
        character = key < 255 and chr(key) or None
        cursor = self.textCursor()
        x = cursor.blockNumber()
        y = cursor.columnNumber()
        doc = self.document()
        text = unicode(cursor.block().text())
        
        #Esta es la clave para indexar los snippets en lugar de tanto quilombo
        print cursor.block().position() + cursor.columnNumber()
        
        scope = self.getCurrentScope()
        preferences = PMXPreference.buildSettings(PMXBundle.getPreferences(scope))
        smart_typing_test = map(lambda pair: pair[0], preferences["smartTypingPairs"])
        indentation = self.identationWhitespace(text)
        
        #logger.debug(debug_key(key_event))

        if key == Qt.Key_Tab:
            #Find for tabtrigger in bundles
            words = self.SPLITWORDS.split(text[:y])
            word = words and words[-1] or ""
            tab = self.soft_tabs and ' ' * self.tab_length or '\t'
            if scope and word:
                snippets = PMXBundle.getTabTriggerItem(word, scope)
                if snippets and self.insertSnippet(word, snippets):
                    return self.keyPressSnippetEvent(key_event)
            else:
                cursor.beginEditBlock()
                cursor.insertText(tab)
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
                    text_arround = "%s%s" % (cursor_left.selectedText(),
                                                cursor_right.selectedText())

                    if text_arround in map(lambda pair: "%s%s" % (pair[0], pair[1]), preferences["smartTypingPairs"]):
                        cursor_left.removeSelectedText()
                        cursor_right.removeSelectedText()
                    else:
                        QPlainTextEdit.keyPressEvent(self, key_event)
                except Exception, e:
                    #traceback.print_exc()
                    QPlainTextEdit.keyPressEvent(self, key_event)
            else:
                QPlainTextEdit.keyPressEvent(self, key_event)
                
        elif key == Qt.Key_Return:
            if doc.blockCount() == 1:
                #Esto es un enter y es el primer blocke que tiene el documento
                syntax = PMXSyntax.findSyntaxByFirstLine(text)
                if syntax != None:
                    self.setSyntax(syntax)
                    
            if "decreaseIndentPattern" in preferences and preferences["decreaseIndentPattern"].match(text):
                logger.debug("decreaseIndentPattern")
                self.decreaseIndent(indentation)
                indentation = self.identationWhitespace(text)
                QPlainTextEdit.keyPressEvent(self, key_event)
                self.indent(indentation)
            elif "increaseIndentPattern" in preferences and preferences["increaseIndentPattern"].match(text):
                logger.debug("increaseIndentPattern")
                QPlainTextEdit.keyPressEvent(self, key_event)
                self.increaseIndent(indentation)
            elif "indentNextLinePattern" in preferences and preferences["indentNextLinePattern"].match(text):
                logger.debug("indentNextLinePattern")
                QPlainTextEdit.keyPressEvent(self, key_event)
                self.increaseIndent(indentation)
            elif "unIndentedLinePattern" in preferences and preferences["unIndentedLinePattern"].match(text):
                logger.debug("unIndentedLinePattern")
                QPlainTextEdit.keyPressEvent(self, key_event)
            else:
                QPlainTextEdit.keyPressEvent(self, key_event)
                self.indent(indentation)

        # Handle smart typing pairs
        elif character in smart_typing_test:
            self.performCharacterAction( preferences["smartTypingPairs"][smart_typing_test.index(character)])
        else:
            QPlainTextEdit.keyPressEvent(self, key_event)
            
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

    #===========================================================================
    # Text Indentation
    #===========================================================================
    
    @classmethod
    def identationWhitespace(cls, text):
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
        self.indent(indentation + (self.soft_tabs and ' ' * self.tab_length or '\t'))
    
    def decreaseIndent(self, identation):
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
            if not new_cursor.block().text().startsWith(self.indent_text):
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
                for _j in range(self.tab_length):
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
        