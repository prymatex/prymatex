#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class QAutoHideDockWidgets(QtGui.QToolBar):
    """
    QMainWindow "mixin" which provides auto-hiding support for dock widgets
    (not toolbars).
    """
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
        w = QtGui.QWidget(None)
        w.resize(10, 100)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.MinimumExpanding))
        self.addWidget(w)

        self.setAllowedAreas(self.DOCK_AREA_TO_TB[self._area])
        self.parent().addToolBar(self.DOCK_AREA_TO_TB[self._area], self)
        self.parent().centralWidget().installEventFilter(self)
        
        self.setVisible(False)
        self.hideDockWidgets()

    def _dockWidgets(self):
        mw = self.parent()
        for w in mw.findChildren(QtGui.QDockWidget):
            if mw.dockWidgetArea(w) == self._area and not w.isFloating():
                yield w

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