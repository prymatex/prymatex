# -*- encoding: utf-8 -*-

from PyQt4.QtCore import QRect, QObject
from PyQt4.QtGui import QPlainTextEdit, QTextEdit, QColor, QTextFormat, QMessageBox
from PyQt4.QtGui import QFileDialog
from logging import getLogger
from prymatex.editor.sidearea import PMXSideArea

#TODO: i18n
_ = lambda s: s

# Create the logger instance
logger = getLogger(__name__)


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
    
    

class PMXCodeEdit(QPlainTextEdit):
    '''
    The GUI element which holds the editor.
    It has a document
    It holds the highlighter
    '''
    def __init__(self, parent):
#        print "*" * 20
#        print "Se instancia un PMXCodeEdit", parent
#        print "*" * 20
        super(PMXCodeEdit, self).__init__(parent)
        self.side_area = PMXSideArea(self)
        self.setupUi()
        self.__title = _("Untitled docuemnt")
        self.__path = ''
        self.__last_save_time = None
    
    
    @property
    def index(self):
        '''
        Returns this tab index
        '''
        tab_widget = self.parent()
        return tab_widget.indexOf(self)
    
    
    def title(): #@NoSelf
        def fget(self):
            return self.__title
        def fset(self, title):
            self.__title = title
        return locals()
    title = property(**title())
    
    
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
    
    
    def debugIndex(self):
        pass