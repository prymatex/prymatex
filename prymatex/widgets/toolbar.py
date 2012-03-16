#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex import resources

class DockWidgetToolBar(QtGui.QToolBar):
    """QMainWindow "mixin" which provides auto-hiding support for dock widgets (not toolbars)."""
    DOCK_AREA_TO_TB = {
        QtCore.Qt.LeftDockWidgetArea: QtCore.Qt.LeftToolBarArea,
        QtCore.Qt.RightDockWidgetArea: QtCore.Qt.RightToolBarArea,
        QtCore.Qt.TopDockWidgetArea: QtCore.Qt.TopToolBarArea,
        QtCore.Qt.BottomDockWidgetArea: QtCore.Qt.BottomToolBarArea,
    }

    def __init__(self, area, parent, name="AUTO_HIDE"):
        QtGui.QToolBar.__init__(self, parent)
        assert isinstance(parent, QtGui.QMainWindow)
        assert area in self.DOCK_AREA_TO_TB
        self._area = area
        self.setObjectName(name)
        self.setWindowTitle(name)
        
        self.setFloatable(False)
        self.setMovable(False)
        self.setVisible(False)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.MinimumExpanding))
        self.setIconSize(QtCore.QSize(16,16));
        
        #Restore action 
        restoreAction = QtGui.QAction(self)
        restoreAction.setIcon(resources.getIcon("important"))
        restoreAction.triggered.connect(self.on_restoreAction_triggered)
        self.addAction(restoreAction)

        self.setAllowedAreas(self.DOCK_AREA_TO_TB[self._area])
        self.parent().addToolBar(self.DOCK_AREA_TO_TB[self._area], self)
        self.parent().centralWidget().installEventFilter(self)
        
        self.hideDockWidgets()

    def on_restoreAction_triggered(self):
        print "restore"
        
    def _dockWidgets(self):
        mainWindow = self.parent()
        for dockWidget in mainWindow.findChildren(QtGui.QDockWidget):
            
            if mainWindow.dockWidgetArea(dockWidget) == self._area and dockWidget.isVisible() and not dockWidget.isFloating():
                if dockWidget.toggleViewAction() not in self.actions():
                    self.addAction(dockWidget.toggleViewAction())
                yield dockWidget
            elif (dockWidget.toggleViewAction() in self.actions() and dockWidget.isVisible()) or mainWindow.dockWidgetArea(dockWidget) != self._area:
                self.removeAction(dockWidget.toggleViewAction())

    def _multiSetVisible(self, widgets, state):
        if state:
            self.setVisible(False)

        for w in widgets:
            w.setUpdatesEnabled(False)
        for w in widgets:
            w.setVisible(state)
        for w in widgets:
            w.setUpdatesEnabled(True)

        if not state and widgets:
            self.setVisible(True)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            assert obj == self.parent().centralWidget()
            self.hideDockWidgets()
        return False

    def setDockWidgetsVisible(self, state):
        self._multiSetVisible(list(self._dockWidgets()), state)

    def showDockWidgets(self): self.setDockWidgetsVisible(True)
    def hideDockWidgets(self): self.setDockWidgetsVisible(False)