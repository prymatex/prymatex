# -*- encoding: utf-8 -*-

#
from PyQt4.QtCore import QRect, QObject
from PyQt4.QtGui import QPlainTextEdit, QTextEdit, QColor, QTextFormat, QMessageBox
from PyQt4.QtGui import QFileDialog, QTextCursor, QTextOption, QAction
from PyQt4.QtCore import Qt, SIGNAL

from logging import getLogger
import sys
import traceback

#PMX Libs
if __name__ == "__main__":
    from os.path import *
    pmx_base = abspath(join(dirname(__file__), '..', '..'))
    sys.path.append(pmx_base)

from prymatex.editor.sidearea import PMXSideArea
from prymatex.editor.syntax import PMXSyntaxProcessor, PMXSyntaxFormatter

#TODO: i18n
_ = lambda s: s

# Create the logger instance
logger = getLogger(__name__)


KEY_NAMES = dict([(getattr(Qt, keyname), keyname) for keyname in dir(Qt) if keyname.startswith('Key_')])


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
    
    return "%s <%s> Code: %d chr(%d) = %s" % (KEY_NAMES[key],  ", ".join(mods), key, key,
                                              key < 255 and chr(key) or 'N/A')




class FileBuffer(QObject):
    '''
    
    '''
    _counter = 0
    def __init__(self, file_name = None):
        pass
    
    def get_header(self):        
        return _("Untitled %d" % self.get_untitled_counter())
    
    @classmethod
    def get_untitled_counter(cls):
        ''' Contador '''
        v = FileBuffer._counter
        FileBuffer._counter += 1
        return v


_counter = 0



class PMXCodeEdit(QPlainTextEdit):
    '''
    The GUI element which holds the editor.
    It has a document
    It holds the highlighter
    '''

    MATCHES = ("()", "{}", "[]", "''", '""', )

    def __init__(self, parent = None):
        super(PMXCodeEdit, self).__init__(parent)
        self.side_area = PMXSideArea(self)
        self.setupUi()
        self.__title = _("Untitled docuemnt")
        self.__path = ''
        self.__last_save_time = None
        self.__soft_tabs = True
        self.__tab_length = 4
        self.character_actions = {}
        self.syntax_processor = PMXSyntaxProcessor(self.document(), formatter = PMXSyntaxFormatter.load_from_textmate_theme('LAZY'))
        
        option = QTextOption()
        option.setFlags(QTextOption.ShowTabsAndSpaces)
        self.document().setDefaultTextOption(option)

        self.character_actions.update({
            '(': '(${selection})',
            '[': '[${selection}]',
            "{": "{${selection}}",
            '"': '"${selection}"',
            "'": "'${selection}'",
            
        })
        self.setupActions()
        
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
    def title(self):
        return self.__title
        
    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def soft_tabs(self):
        return self.__soft_tabs
    @soft_tabs.setter
    def soft_tabs(self, value):
        self.__soft_tabs = value

    @property
    def tab_length(self):
        return self.__tab_length
    @tab_length.setter
    def tab_length(self, value):
        self.__tab_length = value

    @property
    def indent_text(self):
        if not self.soft_tabs:
            return '\t'
        else:
            return ' ' * self.tab_length

    @property
    def path(self):
        return self.__path
    @path.setter
    def path(self, value):
        self.__path = value
            
    
    
    def setTitle(self, title):
        '''
        Sets the tab title
        
        '''
        print "Seteo del título"
        tabwidget = self.parent()
        print "tabwidget", tabwidget
        tabwidget.setTabText(0, title)
        
         
        #tabwidget.setTabText()  
        #self.parent().setWindowTitle(title)
    
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
        self.actionIndent = QAction(_("Increase indentation"), self )
        self.connect(self.actionIndent, SIGNAL("triggered()"), self.indent)
        self.actionUnindent = QAction(_("Decrease indentation"), self )
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
    
    def do_save(self):
        '''
        This method is call to actually save the file, the path has to be
        set.
        '''
        assert self.path, _("No path defined!")
        buffer_contents = str(self.document().toPlainText())
        f = open(str(self.path), 'w')
        #TODO: Check exceptions, for example, disk full.
        f.write(buffer_contents)
        f.close()
     
    
    def save(self):
        '''
        Save the document.
        do_save() actually saves the document, but it should no be called
        directly because it expects self.path to be defined.
        '''
        if self.path:
            return self.do_save()
        else:
            self.path = QFileDialog.getSaveFileName(self, _("Save file as..."))
            if self.path:
                return self.do_save()
        return False
            
    
    
    
    def requestClose(self):
        '''
        When a editor has to be closed this method is called
        @returns true when it's safe to remove the editor wdiget, the user has been prompted
        for save
        '''
        if self.document().isModified():
            r = QMessageBox.question(self, _("Save changes?"), 
                                     _("Save changes for this file"),
                                     QMessageBox.Save | QMessageBox.Cancel | QMessageBox.No,
                                     QMessageBox.Cancel)
            
            if r == QMessageBox.Save:
                return self.save()
            elif r == QMessageBox.Cancel:
                return False
            elif r == QMessageBox.No:
                return True # Can close, discard changes
        return True
    
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
        cursor = self.cursorForPosition(point)
        block = cursor.block()
        if not block.isValid():
            return
        text = block.text()
        self.fontMetrics()
        font_width = self.fontMetrics().width(' ')
        line_width = font_width * text.length()
        char_number = point.x() / font_width
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
        key = key_event.key()
        print debug_key(key_event)
        
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

                    if text_arround in self.MATCHES:
                        cursor_left.removeSelectedText()
                        cursor_right.removeSelectedText()
                    else:
                        QPlainTextEdit.keyPressEvent(self, key_event)
                except Exception, e:
                    #traceback.print_exc()
                    QPlainTextEdit.keyPressEvent(self, key_event)
                
                
            else:
                QPlainTextEdit.keyPressEvent(self, key_event)
                
        elif key == Qt.Key_Enter and doc.blockCount() == 1:
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

        # Handle special keys such as ", (, [ and {
        elif key < 255 and chr(key) in self.character_actions:
            key_chr = chr(key)
            self.perform_character_action( self.character_actions[ key_chr ] )
        else:
            QPlainTextEdit.keyPressEvent(self, key_event)

    def perform_character_action(self, substition):
        try:
            text_start, text_end = substition.split('${selection}')
        except:
            print "Bad subsitution for %s" % subsitution
            return
        cursor = self.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(text_start)
            cursor.insertText(text)
            cursor.insertText(text_end)
        else:
            cursor.insertText(text_start)
            cursor.insertText(text_end)
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
            self.setTextCursor(cursor)

        cursor.endEditBlock()

    # TODO: Word wrapping fix
    def indent(self):
        '''
        Indents text
        '''
        block_count = self.selectionBlockEnd() - self.selectionBlockStart() + 1
        print ">>> Indent (%d blocks)" % block_count
        cursor = self.textCursor()
        cursor.beginEditBlock()
        new_cursor = QTextCursor(cursor)
        new_cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor, block_count -1)
        new_cursor.movePosition(QTextCursor.StartOfBlock)
        for _i in range(block_count):
            
            new_cursor.insertText(self.indent_text)
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


if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QFont
    app = QApplication(sys.argv)
    app.logger = {}
    win = PMXCodeEdit()
    win.setGeometry(40,20,600,400)
    win.setFont(QFont("Monospace", 12))
    # Testing
    win.setPlainText("PMXCodeEdit features\n"
    "--------------------\n"
    " * Block indent and unindent\n"
    " * String autoquote and smart unquotation\n"
    "\t* Bracket autoclose\n")
    win.selectAll()
    win.show()
    sys.exit(app.exec_())
    