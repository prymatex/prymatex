# -*- encoding: utf-8 -*-

#
import sys
import traceback
import re
import logging

from PyQt4.QtCore import QRect, QObject
from PyQt4.QtGui import QPlainTextEdit, QTextEdit, QColor, QTextFormat, QMessageBox
from PyQt4.QtGui import QFileDialog, QTextCursor, QTextOption, QAction, QWidget
from PyQt4.QtGui import QMenu, QVBoxLayout, QFont
from PyQt4.QtGui import QKeySequence, QColor
from PyQt4.QtCore import Qt, SIGNAL, QMetaObject, pyqtSignature

from prymatex.core.base import PMXObject
from prymatex.core.config import Setting

logger = logging.getLogger(__name__)

#PMX Libs
if __name__ == "__main__":
    from os.path import join, dirname, abspath
    pmx_base = abspath(join(dirname(__file__), '..', '..', '..'))
    sys.path.append(pmx_base)
    sys.path.append('../..')
    #pmx_base = abspath(join(dirname(__file__), '..', '..', '..'))

from prymatex.gui.editor.sidearea import PMXSideArea
from prymatex.bundles.syntax import find_syntax_by_first_line
from prymatex.gui.editor.syntax import PMXSyntaxProcessor
from prymatex.bundles.theme import PMXTheme

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

    PAIRS_MATCH_REMOVE = ("()", "{}", "[]", "''", '""', )
    
    #-----------------------------------
    # Settings
    #-----------------------------------
    soft_tabs = Setting(default = True)
    tab_length = Setting(default = 4)
    theme_name = Setting(default = 'IDLE')

    def __init__(self, parent = None):
        super(PMXCodeEdit, self).__init__(parent)
        self.side_area = PMXSideArea(self)
        self.setupUi()
        self.character_actions = {}
        try:
            formater = PMXTheme.getThemeByName(self.theme_name)
            self.syntax_processor = PMXSyntaxProcessor(self.document(), formatter = formater)
        except:
            logger.debug("Could not set syntax")
        
        # TODO: Load from config
        option = QTextOption()
        option.setFlags(QTextOption.ShowTabsAndSpaces)
        self.document().setDefaultTextOption(option)

        # Actions performed when a key is pressed
        self.character_actions = {}
        self.character_actions.update({
            '(': '(${selection})',
            '[': '[${selection}]',
            "{": "{${selection}}",
            '"': '"${selection}"',
            "'": "'${selection}'",
            
        })
        self.setupActions()
        
        self.setSignals()
        self.declareEvents()
        self.configure()
        
    class Meta(object):
        settings = 'editor'

    #=======================================================================
    # Signals and Events
    #=======================================================================
    def setSignals(self):
        self.connect(self, SIGNAL('cursorPositionChanged()'), self.sendCursorPosChange)
        
    def declareEvents(self):
        self.declareEvent('editorCursorPositionChangedEvent()')
        
    def get_current_scope(self):
        cursor = self.textCursor()
        user_data = cursor.block().userData()
        return user_data and user_data.get_scope_at(cursor.columnNumber()) or ""
        
    def sendCursorPosChange(self):
        c = self.textCursor()
        line  = c.blockNumber()
        col = c.columnNumber()
        self.editorCursorPositionChangedEvent(line, col)
        
        
    def set_syntax(self, syntax):
        self.syntax_processor.set_syntax(syntax)
    
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

    def setupUi(self):
        
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
        
        #Connects
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        #self.connect(self, SIGNAL("cursorPositionChanged()"), self.notifyCursorChange)
        self.setWindowTitle(self.__class__.__name__)

    def setupActions(self):
        self.actionIndent = QAction(self.trUtf8("Increase indentation"), self )
        self.connect(self.actionIndent, SIGNAL("triggered()"), self.indent)
        self.actionUnindent = QAction(self.trUtf8("Decrease indentation"), self )
        self.connect(self.actionUnindent, SIGNAL("triggered()"), self.unindent)

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
            #e8f2fe
            color = QColor(232, 242, 25)
            lineColor = QColor(color).lighter(180)
            selection.format.setBackground(lineColor);
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
    
    def keyPressEvent(self, key_event):
        '''
        This method is called whenever a key is pressed. The key code is
        stored in key_event.key()
        '''
        key = key_event.key()
        logger.debug(debug_key(key_event))
        
        cursor = self.textCursor()
        doc = self.document()

        if key == Qt.Key_Tab:
            self.indent()
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

                    if text_arround in self.PAIRS_MATCH_REMOVE:
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
                try:
                    text = doc.firstBlock().text()
                    syntax = find_syntax_by_first_line(text)
                    if syntax != None:
                        self.set_syntax(syntax)
                        self.parent().currentEditorChange.emit(self)
                except:
                    #logger.information("Error guessing syntax, maybe debuging?")
                    print "Error guessing syntax, maybe debuging?"

            #TODO: Manage thrugh config
            if True:
                if cursor.atBlockStart():
                    # Do not indent
                    return QPlainTextEdit.keyPressEvent(self, key_event)
                else:
                    cursor.movePosition(QTextCursor.StartOfLine, 
                                        QTextCursor.KeepAnchor, 1)
                    text = self.textWhitespace( cursor )
                    QPlainTextEdit.keyPressEvent(self, key_event)
                    if text:
                        self.textCursor().insertText(text)
            else:
                QPlainTextEdit.keyPressEvent(self, key_event)

        # Handle special keys such as ", (, [ and {
        elif key < 255 and chr(key) in self.character_actions:
            key_chr = chr(key)
            self.perform_character_action( self.character_actions[ key_chr ] )
        else:
            QPlainTextEdit.keyPressEvent(self, key_event)



    
    def perform_character_action(self, substition):
        '''
        Substitutions when some characters are typed.
        These substitutions are held in a dictionary
        '''
        try:
            text_start, text_end = substition.split('${selection}')
        except:
            print "Bad subsitution for %s" % subsitution
            return
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.beginEditBlock()
            cursor.insertText(text_start)
            cursor.insertText(text)
            cursor.endEditBlock()

            cursor.beginEditBlock()
            cursor.insertText(text_end)
            cursor.endEditBlock()
        else:
            cursor.beginEditBlock()
            cursor.insertText(text_start)
            cursor.endEditBlock()
            
            cursor.beginEditBlock()
            cursor.insertText(text_end)
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
            cursor.endEditBlock()
            self.setTextCursor(cursor)

        cursor.endEditBlock()

    
    #===========================================================================
    # Text Indentation
    #===========================================================================
    
    WHITESPACE_RE = re.compile(r'^(?P<whitespace>\s+)', re.UNICODE)    
    @classmethod
    def textWhitespace(cls, text):
        '''
        Gets text whitespace
        @param text: Text, QTextCursor o QTextBlock instance
        @return: The text whitespace
        '''
        if isinstance(text, QTextCursor):
            text = text.block().text()
        elif isinstance(text, QTextBlock):
            text = text.text()
        match = cls.WHITESPACE_RE.match(unicode(text))
        try:
            ws = match.group('whitespace')
            return ws
        except AttributeError:
            return ''
        
    # TODO: Word wrapping fix
    # TODO: Correct whitespace mix
    def indent(self):
        '''
        Indents text, it take cares of block selections.
        '''
        
        
        
        block_count = self.selectionBlockEnd() - self.selectionBlockStart() + 1
        
        cursor = self.textCursor()
        cursor.beginEditBlock()
        new_cursor = QTextCursor(cursor)
        new_cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor, block_count -1)
        new_cursor.movePosition(QTextCursor.StartOfBlock)
        for _i in range(block_count):

            # If the text is not inserted
            if self.indent_text == '\t':
                indent_text = '\t'
            else:
                curr_indent = self.textWhitespace( new_cursor )
                
                if not len(curr_indent):
                    # No indentation yet, so insert all chars
                                    
                    indent_text = self.indent_text
                else:
                    if self.soft_tabs:
                        # How many characters left?
                        n = self.tab_length - (len(curr_indent) % self.tab_length)
                        indent_text = n * ' '
                    else:
                        indent_text = self.indent_text
                        
            new_cursor.insertText(indent_text)
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
        print "<<< Unindent (%d blocks)" % block_count
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
        