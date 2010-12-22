from PyQt4.Qt import *
from logging import getLogger

logger = getLogger(__file__)

class BaseProxy(QObject):
    '''
    Base proxy for 
    '''
    def __init__(self, parent):
        super(BaseProxy, self).__init__(parent)

    @property
    def widget(self):
        return self.parent()


class TabWidgetProxy(BaseProxy):
    '''
    Proxies current TabWidget
    '''
    
    def openFile(self, path):
        #self.widget.centralWidget()
        print "Proxy Open File", path

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


class CurrentEditorProxy(BaseProxy):
    '''
    Proxies current editor
    '''
    pass