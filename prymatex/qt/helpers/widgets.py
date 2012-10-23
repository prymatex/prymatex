#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

def center_widget(widget, scale = None):
    """
    Center de widget in the screen
    Scale is a tuple with width and height ex: (0.7, 0.65)
    """
    screen = QtGui.QDesktopWidget().screenGeometry()
    if scale is not None:
        widget.resize(screen.width() * scale[0], screen.height() * scale[1])
    widget.move((screen.width() - widget.size().width()) / 2, (screen.height() - widget.size().height()) / 2)
    