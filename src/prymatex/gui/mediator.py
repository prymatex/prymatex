'''
Mediator which deals with the current tab and the current editor.

'''

from PyQt4.Qt import *
from logging import getLogger

logger = getLogger(__file__)

class BaseMediator(QObject):
    '''
    Base mediator
    '''
    def __init__(self, parent):
        super(BaseMediator, self).__init__(parent)

    @property
    def widget(self):
        return self.parent()


class TabWidgetMediator(BaseMediator):
    '''
    Mediates with the current TabWidget
    '''
    
    def openFile(self, path):
        #self.widget.centralWidget()
        print "Medaitor Open File", path

    @property
    def current_tabs_widget(self):
        return self.widget.tabWidgetEditors

    def getEditors(self):
        '''
        Returns editors
        '''
        #TODO: Implement this
        return []
        
    def addNewTab(self):
        self.current_tabs_widget.appendEmptyTab()
        
        #def appendEmptyTab(self):
        #'''
        #Creates a new empty tab and returns it
        #'''
        
        #editor = self.getEditor()
        ## Title should be filled after tab insertion
        #index = self.addTab(editor, editor.title)
        
        #self.setCurrentIndex(index)
        #if self.count() == 1:
            #editor.setFocus(Qt.TabFocusReason)
            #return editor
    



class CurrentEditorMediator(BaseMediator):
    '''
    Mediates with the current editor
    '''
    curosrPositionChange = pyqtSignal(int, int, name = "cursorPositionChange(int,int)")
    undoAvailable = pyqtSignal(name = "cursorPositionChange(int,int)")
    copyAvailable = pyqtSignal(bool)
    #void    currentCharFormatChanged ( const QTextCharFormat & f )
    #void    cursorPositionChanged ()
    redoAvailable = pyqtSignal(bool available )
    selectionChanged = pyqtSignal()
    #void    textChanged ()
    undoAvailable = pyqtSignal( bool)
    
    