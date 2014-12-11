# encoding: utf-8

"""This module contains the main window status bar definition and widgets."""

from prymatex.qt import QtGui, QtWidgets

class PrymatexMainStatusBar(QtWidgets.QStatusBar):
    def __init__(self, **kwargs):
        super(PrymatexMainStatusBar, self).__init__(**kwargs)
        self.window().currentEditorChanged.connect(self.on_currentEditorChanged)
        self.statusBars = []

    def addPermanentWidget(self, widget):
        self.statusBars.append(widget)
        super(PrymatexMainStatusBar, self).addPermanentWidget(widget, 1)

    def on_currentEditorChanged(self, editor):
        for bar in self.statusBars:
            bar.setVisible(bar.acceptEditor(editor))
        self.setVisible(editor is not None)
