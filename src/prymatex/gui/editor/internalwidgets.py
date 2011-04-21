'''
Some custom widgets used in the editor widget class
'''

from PyQt4.QtGui import QComboBox, QSpinBox, QWidget, QTextCursor, QTextDocument
from PyQt4.QtCore import Qt, pyqtSignal, QRegExp, QString
from prymatex.core.base import PMXObject


class PMXRefocusWidget(QWidget, PMXObject):
    '''
    Refoucs Editor when the widget is hidden
    '''
    showed = pyqtSignal()
       
    def hideEvent(self, event):
        super(PMXRefocusWidget, self).hideEvent(event)
        self.mainwindow.currentEditorWidget.setFocus(Qt.MouseFocusReason)
        
    def showEvent(self, event):
        super(PMXRefocusWidget, self).showEvent(event)
        self.showed.emit()
        
        
class PMXFindBox(QComboBox):
    editionFinished = pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    STYLE_NO_MATCH = ''' background-color: red; color: #fff; '''
    STYLE_MATCH = ' background-color: #dea;'
    STYLE_NORMAL = ''
    
    # Signals
    findMatchCountChanged =  pyqtSignal(int)
    
    def __init__(self, parent = None):
        super(PMXFindBox, self).__init__(parent)
        self.editTextChanged.connect(self.perofrmTextDocumentSearch)
        print "Findbox parent", self.parent()
    
    def keyPressEvent(self, event):
        super(PMXFindBox, self).keyPressEvent(event)
        key = event.key() 
        if key in self.KEY_TRIGGERS:
            self.editionFinished.emit()
        elif key in (Qt.Key_Backspace, Qt.Key_Delete):
            self.perofrmTextDocumentSearch()
        elif key in (Qt.Key_Return, ):
            self.findNext()
        
    
    def setTextEdit(self, value):
        self.__textEdit = value
    
    textEdit = property(fget = lambda s: s.__textEdit, fset = setTextEdit,
                        doc = 'QTextEdit where find actions are preformed')
    
    def showEvent(self, event):
        super(PMXFindBox, self).showEvent(event)
        self.setStyleSheet(self.STYLE_NORMAL)
    
    @property
    def regexp(self):
        regexp = QRegExp(self.currentText())
        # Test code
        if self.caseSensitive:
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive
            
        regexp.setCaseSensitivity(caseSensitivity)
        return regexp
    
    @property
    def flags(self):
        flags = QTextDocument.FindFlags(0)
        
        if self.wholeWord:
            flags |= QTextDocument.FindWholeWords
        return flags
    
    def perofrmTextDocumentSearch(self, text = None):
        '''
        Perofrms text searches
        '''
        if text is None:
            text = self.currentText()
        if text.length() == 0:
            self.setStyleSheet(self.STYLE_NORMAL)
            return
        
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.textEdit.setTextCursor(cursor)
        
        found_cursors = []
        
        while True:
            
            cursor = self.textEdit.document().find(self.regexp, cursor, self.flags)

            if cursor.isNull():
                break
            found_cursors.append(cursor)
            
        if not found_cursors:
            self.setStyleSheet(self.STYLE_NO_MATCH)
        else:
            self.setStyleSheet(self.STYLE_MATCH)
            self.textEdit.setTextCursor(found_cursors[0])
            
        self.findMatchCountChanged.emit( len(found_cursors) )
        #print "Matches for '%s' are %d" % (text, len(found_cursors))
        
    def findNext(self):
        print "findNext"
        cursor = self.textEdit.document().find(self.regexp, self.textEdit.textCursor(), self.flags)
        if cursor.isNull():
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.textEdit.setTextCursor(cursor)
            cursor = self.textEdit.document().find(self.regexp, cursor, self.flags)
        if not cursor.isNull():
            self.textEdit.setTextCursor(cursor)
    
    def findPrevious(self):
        print "findPrevious" 
        cursor = self.textEdit.document().find(self.regexp, self.textEdit.textCursor(), self.flags | QTextDocument.FindBackward)
        if cursor.isNull():
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
            cursor = self.textEdit.document().find(self.regexp, cursor, self.flags | QTextDocument.FindBackward)
        if not cursor.isNull():
            self.textEdit.setTextCursor(cursor)
    
    
    __caseSensitive = False
    def setCaseSensitive(self, toggled):
        self.__caseSensitive = toggled
        if self.currentText().length():
            self.perofrmTextDocumentSearch()
    
    caseSensitive = property(fget = lambda s: s.__caseSensitive, fset = setCaseSensitive)
    
    __regex = False
    def setRegex(self, toggled):
        self.__regex = toggled
        if self.currentText().length():
            self.perofrmTextDocumentSearch()
    
    regex = property(fget = lambda s: s.__regex, fset = setRegex)
    
    __wholeWord = False
    def setWholeWord(self, toggled):
        self.__wholeWord = toggled
        if self.currentText().length():
            self.perofrmTextDocumentSearch()
    wholeWord = property(fget = lambda s: s.__wholeWord, fset = setWholeWord)
    

class PMXReplaceBox(QComboBox):
    editionFinished = pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    def keyPressEvent(self, event):
        super(PMXReplaceBox, self).keyPressEvent(event)
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()


class PMXCommonSearchBox(QComboBox):
    '''
    Common behaviour between the search and replace widgtets
    '''
    editionFinished = pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    
    def keyPressEvent(self, event):
        super(PMXCommonSearchBox, self).keyPressEvent(event)
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()
        


class PMXSpinGoToLine(QSpinBox):
    editionFinished = pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    
    def __init__(self, parent = None):
        super(PMXSpinGoToLine, self).__init__(parent)
        self.setMinimum(1) # There's no line 0
        
    def keyPressEvent(self, event):
        super(PMXSpinGoToLine, self).keyPressEvent(event)
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()