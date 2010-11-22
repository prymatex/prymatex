'''
Created on 21/11/2010

@author: defo

A widget for logging
'''

# TODO: Check if twiggy or simple logger has to be used

from ui_logwindow import Ui_LogWidget
from PyQt4.QtGui import QWidget

class LogWidget(QWidget, Ui_LogWidget):
    '''
    Logging widget
    
    '''
    def __init__(self, parent = None):
        super(LogWidget, self).__init__(parent)
        self.setupUi(self) 
