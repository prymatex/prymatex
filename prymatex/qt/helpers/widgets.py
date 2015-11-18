#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtWidgets

def screen_geometry(widget):
    desktop = QtWidgets.QApplication.desktop()
    return desktop.availableGeometry(desktop.screenNumber(widget))

def center_widget(widget, scale=None):
    """
    Center de widget in the screen
    Scale is a tuple with width and height ex: (0.7, 0.65)
    """
    geometry = screen_geometry(widget)
    if scale is not None:
        widget.resize(geometry.width() * scale[0], geometry.height() * scale[1])
    size = widget.size()
    widget.move(
        geometry.left() + ((geometry.width() - size.width()) / 2),
        geometry.top() + ((geometry.height() - size.height()) / 2)
    )
