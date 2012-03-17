#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex import resources
#TODO: Mover a prymatex.widgets
from prymatex.gui import utils

class DockWidgetToolBar(QtGui.QToolBar):
    """QMainWindow "mixin" which provides auto-hiding support for dock widgets (not toolbars)."""

    DOCK_AREA_TO_TB = {
        QtCore.Qt.LeftDockWidgetArea: QtCore.Qt.LeftToolBarArea,
        QtCore.Qt.RightDockWidgetArea: QtCore.Qt.RightToolBarArea,
        QtCore.Qt.TopDockWidgetArea: QtCore.Qt.TopToolBarArea,
        QtCore.Qt.BottomDockWidgetArea: QtCore.Qt.BottomToolBarArea,
    }

    def __init__(self, name, area, parent):
        QtGui.QToolBar.__init__(self, parent)
        assert isinstance(parent, QtGui.QMainWindow)
        assert area in self.DOCK_AREA_TO_TB
        self._area = area
        self.setObjectName(utils.textToObjectName(name, prefix="ToolBar"))
        self.setWindowTitle(name)
        
        self.setFloatable(False)
        self.setMovable(False)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.MinimumExpanding))
        self.setIconSize(QtCore.QSize(16,16));
        
        #Restore action
        restoreAction = QtGui.QAction(self)
        restoreAction.setIcon(resources.getIcon("stack"))
        restoreAction.triggered.connect(self.hide)
        self.addAction(restoreAction)
        
        self.visibilityChanged.connect(self.on_visibilityChanged)

    def on_visibilityChanged(self, visible):
        if visible:
            self.parent().centralWidget().installEventFilter(self)
            self.hideDockWidgets()
        else:
            self.parent().centralWidget().removeEventFilter(self)
            self.removeDockers()

    def _dockWidgets(self):
        mainWindow = self.parent()
        for dockWidget in mainWindow.findChildren(QtGui.QDockWidget):
            if mainWindow.dockWidgetArea(dockWidget) == self._area and dockWidget.isVisible() and not dockWidget.isFloating():
                if dockWidget.toggleViewAction() not in self.actions():
                    self.addAction(dockWidget.toggleViewAction())
                yield dockWidget
            elif (dockWidget.toggleViewAction() in self.actions() and dockWidget.isVisible()) or mainWindow.dockWidgetArea(dockWidget) != self._area:
                self.removeAction(dockWidget.toggleViewAction())

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            assert obj == self.parent().centralWidget()
            self.hideDockWidgets()
        return False

    def setDockWidgetsVisible(self, state):
        if not self.isHidden():
            self._multiSetVisible(list(self._dockWidgets()), state)

    def removeDockers(self):
        actions = self.actions()[1:]
        for action in actions:
            self.removeAction(action)
            action.trigger()
            
    def showDockWidgets(self): 
        for dockWidget in self._dockWidgets():
            dockWidget.show()
            
    def hideDockWidgets(self):
        for dockWidget in self._dockWidgets():
            dockWidget.hide()