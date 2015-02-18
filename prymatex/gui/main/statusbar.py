# encoding: utf-8

"""This module contains the main window status bar definition and widgets."""

from prymatex.core.components import PrymatexStatusBar
from prymatex.qt import QtGui, QtWidgets

class PrymatexMainStatusBar(QtWidgets.QStatusBar):
    def __init__(self, **kwargs):
        super(PrymatexMainStatusBar, self).__init__(**kwargs)
        self.window().editorChanged.connect(self.on_window_editorChanged)

    def addStatusBar(self, status_bar):
        if hasattr(status_bar, 'showMessage'):
            self.addPermanentWidget(status_bar, 1)
        else:
            self.addWidget(status_bar, 1)

    def statusBars(self):
        return self.findChildren(PrymatexStatusBar)

    # ------------- Editor changed signal
    def on_window_editorChanged(self, editor):
        for status_bar in self.statusBars():
            status_bar.setVisible(status_bar.acceptEditor(editor))

    def showMessage(self, message):
        super(PrymatexMainStatusBar, self).showMessage(message)
        for status_bar in self.statusBars():
            status_bar.showMessage(message)