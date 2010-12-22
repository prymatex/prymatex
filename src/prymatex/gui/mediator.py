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


NO_SPLIT   = 0
SPLIT_VERT = 1
SPLIT_HORI = 2

class TabWidgetMediator(BaseMediator):
    '''
    Mediates with the current TabWidget.
    If the screen is splitted this object proviedes a simple interface
    with the current active widget.


    Actions -----------> Mediator ------------------
                                                    |
                                                    v
                                             *---------------------*
                                             | Current Tab Wideget |
                                             *---------------------*
                                             | Could be in a       |
                                             | QSplitter           |
                                             *---------------------*
                                              
    '''

    def __init__(self, parent):
        super(TabWidgetMediator, self).__init__(parent)
        #self.connect(self.current_tabs_widget, SIGNAL('tab

    def get_factory_for_file(path):
        pass
    
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
        
        widget = self.current_tabs_widget.appendEmptyTab()
        

    current_split = NO_SPLIT
    
    def splitHorizontally(self):
        logger.debug("Split V")
        
        
    def splitVertically(self):
        logger.debug("Split V")
    
    def focusNextTab(self):
        '''
        Focus next tab
        '''
        curr = self.current_tabs_widget.currentIndex()
        count = self.current_tabs_widget.count()

        if curr < count -1:
            prox = curr +1
        else:
            prox = 0
        self.current_tabs_widget.setCurrentIndex(prox)
        self.current_tabs_widget.currentWidget().setFocus( Qt.TabFocusReason )

    def focusPrevTab(self):
        curr = self.current_tabs_widget.currentIndex()
        count = self.current_tabs_widget.count()

        if curr > 0:
            prox = curr -1
        else:
            prox = count -1
        self.current_tabs_widget.setCurrentIndex(prox)
        self.current_tabs_widget.currentWidget().setFocus(Qt.TabFocusReason)

    

    def moveTabLeft(self):
        ''' Moves the current tab to the left '''
        if self.current_tabs_widget.count() == 1:
            return
        count = self.current_tabs_widget.count()
        index = self.current_tabs_widget.currentIndex()
        text = self.current_tabs_widget.tabText(index)
        widget = self.current_tabs_widget.currentWidget()
        self.current_tabs_widget.removeTab(index)
        index -= 1
        if index < 0:
            index = count
        self.current_tabs_widget.insertTab(index, widget, text)
        self.current_tabs_widget.setCurrentWidget(widget)

    def moveTabRight(self):
        '''
        Moves the current tab to the right
        '''
        if self.current_tabs_widget.count() == 1:
            return
        count = self.current_tabs_widget.count()
        index = self.current_tabs_widget.currentIndex()
        text = self.current_tabs_widget.tabText(index)
        widget = self.current_tabs_widget.currentWidget()
        self.current_tabs_widget.removeTab(index)
        index += 1
        if index >= count:
            index = 0
        self.current_tabs_widget.insertTab(index, widget, text)
        self.current_tabs_widget.setCurrentWidget(widget)


class CurrentEditorMediator(BaseMediator):
    '''
    Mediates with the current editor
    '''
    pass