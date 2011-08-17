#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from PyQt4.QtGui import QWidget, QDockWidget, QActionGroup, QAction, QMenu
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt
from prymatex.ui.logwidget import Ui_LogWidget

DEBUG_LEVELS = ("INFO",
                "DEBUG",
                "WARNING",
                "ERROR",
                "FATAL", 
                "CRITICAL",)

DEBUG_LEVELS = dict([(name, getattr(logging, name)) for name in DEBUG_LEVELS ])

class LogDockWidget(QDockWidget, Ui_LogWidget):
    '''
    Logging widget
    
    '''
    def __init__(self, parent = None):
        super(LogDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.setup()
        global handler
        handler.output = self
        handler.capacity = 1
        
    
    def setup(self):
        #self.push#
        self.debug_levels_menu = QMenu()
        self.debug_levels_action_group = QActionGroup(self)
        for level, value in DEBUG_LEVELS.iteritems():
            action = QAction(level.title(), self)
            # Store debug info in a dict
            action.setData({'name': level, 'level': value})
            action.setCheckable(True)
            self.debug_levels_action_group.addAction(action)
            self.debug_levels_menu.addAction(action)
            
        self.connect(self.debug_levels_menu, SIGNAL('triggered(QAction*)'), 
                                                    self.debug_level_change)
        self.pushDebugLevel.setMenu(self.debug_levels_menu)
    
    def debug_level_change(self, action):
        new_level = action.data()
        logger.info("Level changed to %s", new_level)
        

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
	super(LogDockWidget, self).keyPressEvent(event)

from logging.handlers import BufferingHandler

class QtLogHandler(logging.handlers.BufferingHandler):
    '''
    A handler to store logging ouput to be shown at a QTextEdit defined in
    LogDockWidget
    '''
    __output = None
    
    def __init__(self):
        BufferingHandler.__init__(self, 100)
    
    @property
    def output(self):
        return self.__output
    
    @output.setter
    def output(self, output):
        self.__output = output
    
    def flush(self):
        if self.output:
            #self.output.
            txt = '\n'.join(map(lambda log: log.getMessage(), self.buffer))
            self.output.textLog.append(txt)
        

handler = QtLogHandler()
