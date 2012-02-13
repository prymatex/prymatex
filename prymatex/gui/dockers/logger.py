#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import BufferingHandler

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.ui.others.logwidget import Ui_LogWidget

class PMXLoggerDock(QtGui.QDockWidget, Ui_LogWidget, PMXBaseDock):
    """Logging widget
    """
    SHORTCUT = "F12"
    ICON = resources.getIcon("logger")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    
    def __init__(self, parent = None):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setupUi(self)
        self.handler = QtLogHandler(self)
        self.handler.setLevel(logging.DEBUG)
        self.setup()
    
    def setup(self):
        logging.root.addHandler(self.handler)
        self.debug_levels_menu = QtGui.QMenu()
        self.debug_levels_action_group = QtGui.QActionGroup(self)
        for level, value in filter(lambda (key, value): type(key) == str, logging._levelNames.iteritems()):
            action = QtGui.QAction(level.title(), self)
            action.setData({'name': level, 'level': value})
            action.setCheckable(True)
            self.debug_levels_action_group.addAction(action)
            self.debug_levels_menu.addAction(action)
            
        self.debug_levels_menu.triggered.connect(self.debug_level_change)
        self.pushDebugLevel.setMenu(self.debug_levels_menu)
    
    def debug_level_change(self, action):
        new_level = action.data()
        self.logger.debug("Level changed to %s", new_level)

class QtLogHandler(BufferingHandler):
    '''
    A handler to store logging ouput to be shown at a QTextEdit defined in LogDockWidget
    '''
    def __init__(self, widget):
        BufferingHandler.__init__(self, 100)
        self.widget = widget
    
    def flush(self):
        self.widget.textLog.append('\n'.join(map(lambda log: log.getMessage(), self.buffer)))
