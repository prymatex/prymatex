'''
Holds everything in place, manages layout changes.
It belongs to a MainWindow
'''

class PMXMainWidget(QWidget):


    def __init__(self, parent = None):
        super(PMXMainWidget, self).__init__()


    def getLayout(self):
        pass


    def splitHorizontal(self):
        pass

    def splitVertical(self):
        pass

    def appendWidget(self, widget):
        '''
        Adds a widget to the current layout scheme
        '''

    def currentWidgets(self):
        '''
        @returns 
        '''
        raise NotImplementedExc

