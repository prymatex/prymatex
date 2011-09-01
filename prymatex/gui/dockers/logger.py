#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.ui.logwidget import Ui_LogWidget

class PMXLoggerDock(QtGui.QDockWidget, Ui_LogWidget, PMXObject):
    '''
    Logging widget
    
    '''
    def __init__(self, handler, parent = None):
        super(PMXLoggerDock, self).__init__(parent)
        self.setupUi(self)
        self.setup()
        handler.output = self
        handler.capacity = 1

    
    def setup(self):
        #self.push#
        self.debug_levels_menu = QtGui.QMenu()
        self.debug_levels_action_group = QtGui.QActionGroup(self)
        for level, value in filter(lambda (key, value): type(key) == str, logging._levelNames.iteritems()):
            action = QtGui.QAction(level.title(), self)
            # Store debug info in a dict
            action.setData({'name': level, 'level': value})
            action.setCheckable(True)
            self.debug_levels_action_group.addAction(action)
            self.debug_levels_menu.addAction(action)
            
        self.debug_levels_menu.triggered.connect(self.debug_level_change)
        self.pushDebugLevel.setMenu(self.debug_levels_menu)
    
    def debug_level_change(self, action):
        new_level = action.data()
        self.debug("Level changed to %s", new_level)

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

