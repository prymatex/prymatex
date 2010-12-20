# -*- encoding: utf-8 -*-

#
from PyQt4.QtCore import QRect, QObject
from PyQt4.QtGui import QPlainTextEdit, QTextEdit, QColor, QTextFormat, QMessageBox
from PyQt4.QtGui import QFileDialog, QTextCursor
from PyQt4.QtCore import Qt

from logging import getLogger
import sys

#PMX Libs
if __name__ == "__main__":
    from os.path import *
    pmx_base = abspath(join(dirname(__file__), '..', '..'))
    sys.path.append(pmx_base)

from prymatex.editor.sidearea import PMXSideArea


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


PREVIOUS_CHAR = [
    (QTextCursor.PreviousCharacter, QTextCursor.MoveAnchor, 1),
]    


SUBSTITUTIONS = {'(': '(${selection})',
                 '[': '[${selection}]',
                 '{': '{\n\t${selection\n}',
                 '"': '"${selection}"',
                 "'": "'${selection}'",
                 }
class PMXCodeEdit(QPlainTextEdit):
    '''
    The GUI element which holds the editor.
    It has a document
    It holds the highlighter
    '''

    # Key substition map, for example when you type (, it should insert
    # a (${cursor})
    SUBST_MAP = {
        Qt.Key_ParenLeft: ("()", PREVIOUS_CHAR, ),
        Qt.Key_BraceLeft: ("{}", PREVIOUS_CHAR, ),
        Qt.Key_BracketLeft: ("[]", PREVIOUS_CHAR, ),
        Qt.Key_QuoteDbl: ('""', PREVIOUS_CHAR, ),
        Qt.Key_Apostrophe: ("''", PREVIOUS_CHAR, ),
        Qt.Key_Less: ("<>", PREVIOUS_CHAR, ),
    }
    
    def __init__(self, parent = None):
        super(PMXCodeEdit, self).__init__(parent)
        self.side_area = PMXSideArea(self)
        self.setupUi()
        self.__title = _("Untitled docuemnt")
        self.__path = ''
        self.__last_save_time = None
        self.__soft_tabs = True
        self.__tab_length = 4
    
    
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
    
        
    def path(): #@NoSelf
        def fget(self):
            return self.__path
        def fset(self, path):
            self.__path = path
            
        return locals()
    path = property(**path())
    
    
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        a = menu.addAction(_("My Menu Item"))
        self.connect(self, )
        
        menu.exec_(event.globalPos());
        del menu
    
    
    
    def selectionBlockStart(self):
        '''
        Returns the block where the slection starts
        '''
        if not self.hasSelection():
            return -1
        return self.document().findBlock( cursor.selectionStart() )
        
    def selectionBlockEnd(self):
        '''
        Returns the block number where the selection ends
        '''
        if not self.hasSelection():
            return -1
        return self.document().findBlock( cursor.selectionEnd() )

    
        
    
        
    def keyPressEvent(self, key_event):
        key = key_event.key()
        print debug_key(key_event)
        
        cursor = self.textCursor()

        doc = self.document()
        start_block_pos, end_block_pos = cursor.selectionStart(), cursor.selectionEnd()
        start_block, end_block = map(doc.findBlock, (start_block_pos, end_block_pos))
        blocknum_start, blocknum_end = start_block.blockNumber(), end_block.blockNumber()

        blocknum_diff = blocknum_end - blocknum_start


        # All keys in http://doc.trolltech.com/qtjambi-4.4/html/com/trolltech/qt/core/Qt.Key.html
        if key == Qt.Key_Tab:
            
            if key_event.modifiers() & Qt.ShiftModifier:
                self.unindent()
            else:
                self.indent()


        # elif key == 16777220 and doc.blockCount() == 1:
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
                
        elif key in self.SUBST_MAP and not cursor.hasSelection():
            text, movement = self.SUBST_MAP[key]
            cursor.beginEditBlock()
            cursor.insertText(text)
            for action_params in movement:
                mode, anchor, amount = action_params
                cursor.movePosition(mode, anchor, amount)
            cursor.endEditBlock()
            self.setTextCursor(cursor)
            
        else:
            QPlainTextEdit.keyPressEvent(self, key_event)
        
    def indent(self):
        '''
        Indents text
        '''
        print "Indent"
        blocknum_diff = self.selectionBlockEnd() - self.selectionBlockEnd()
        
        cursor.beginEditBlock()
        new_cursor = QTextCursor(cursor)
        new_cursor.movePosition(QTextCursor.StartOfBlock)
        for _i in range(blocknum_diff +1):
            new_cursor.insertText(self.indent_text)
            new_cursor.movePosition(QTextCursor.NextBlock)
            
        self.setTextCursor(new_cursor)
        cursor.endEditBlock()
        
    def unindent(self):
        '''
        Unindents text
        '''
        print "Unindent"

    


if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QFont
    app = QApplication(sys.argv)
    app.logger = {}
    win = PMXCodeEdit()
    win.setGeometry(40,20,600,400)
    win.setFont(QFont("Verdana", 15))
    
    win.show()
    sys.exit(app.exec_())
    