#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.qt.helpers import text_to_objectname
  
class DockWidgetToolBar(QtWidgets.QToolBar):
    """QMainWindow "mixin" which provides auto-hiding support for dock widgets (not toolbars)."""

    DOCK_AREA_TO_TB = {
        QtCore.Qt.LeftDockWidgetArea: QtCore.Qt.LeftToolBarArea,
        QtCore.Qt.RightDockWidgetArea: QtCore.Qt.RightToolBarArea,
        QtCore.Qt.TopDockWidgetArea: QtCore.Qt.TopToolBarArea,
        QtCore.Qt.BottomDockWidgetArea: QtCore.Qt.BottomToolBarArea,
    }
    
    def __init__(self, name, area, parent):
        QtWidgets.QToolBar.__init__(self, parent)
        assert isinstance(parent, QtWidgets.QMainWindow)
        assert area in self.DOCK_AREA_TO_TB
        self._area = area
        self.setObjectName(text_to_objectname(name, prefix="ToolBar"))
        self.setWindowTitle(name)
        
        #Button Style
        #self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.setFloatable(False)
        self.setMovable(False)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding))
        self.setIconSize(QtCore.QSize(16,16));
        
        #Restore action
        self.restoreAction = QtWidgets.QAction(self)
        self.restoreAction.setIcon(self.parent().resources().get_icon("TitleBarUnshadeButton"))
        self.restoreAction.triggered.connect(self.hide)
        self.addAction(self.restoreAction)
        
        #self.visibilityChanged.connect(self.on_visibilityChanged)

    def on_actionTriggered(self, action):
        self.hideDockWidgets(excludeAction = action)

    def on_visibilityChanged(self, visible):
        if visible:
            self.parent().centralWidget().installEventFilter(self)
            self.actionTriggered.connect(self.on_actionTriggered)
            self.hideDockWidgets()
        else:
            self.parent().centralWidget().removeEventFilter(self)
            self.actionTriggered.disconnect(self.on_actionTriggered)
            self.removeDockers()

    def dockWidgets(self):
        mainWindow = self.parent()
        for dockWidget in mainWindow.findChildren(QtWidgets.QDockWidget):
            if mainWindow.dockWidgetArea(dockWidget) == self._area and dockWidget.isVisible() and not dockWidget.isFloating():
                if dockWidget.toggleViewAction() not in self.actions():
                    self.addAction(dockWidget.toggleViewAction())
                yield dockWidget
            elif (dockWidget.toggleViewAction() in self.actions() and dockWidget.isVisible()) or mainWindow.dockWidgetArea(dockWidget) != self._area:
                self.removeAction(dockWidget.toggleViewAction())

    def allDockWidgets(self):
        mainWindow = self.parent()
        for dockWidget in mainWindow.findChildren(QtWidgets.QDockWidget):
            if mainWindow.dockWidgetArea(dockWidget) == self._area and not dockWidget.isFloating():
                yield dockWidget
                
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            assert obj == self.parent().centralWidget()
            self.hideDockWidgets()
        return False

    def hasDockers(self):
        return self.actions() > 1
        
    def removeDockers(self):
        dockers = list(self.allDockWidgets())
        if not dockers: return
        actions = self.actions()[1:]
        
        for action in actions:
            self.removeAction(action)
            list(map(lambda dock: dock.show(), [dock for dock in dockers if dock.toggleViewAction() == action]))
        
    def hideDockWidgets(self, excludeAction = None):
        for dockWidget in self.dockWidgets():
            if excludeAction is None or (excludeAction is not None and excludeAction != dockWidget.toggleViewAction()):
                dockWidget.hide()
