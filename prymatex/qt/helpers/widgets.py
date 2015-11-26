#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtWidgets
from prymatex.qt import QtCore

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

def move_widget(widget, point_rect):
    geometry = screen_geometry(widget)
    screen_right = geometry.right()
    screen_bottom = geometry.bottom()
    
    point = point_rect.bottomRight() if isinstance(point_rect, QtCore.QRect) else point_rect

    # Computing completion widget and its parent right positions
    comp_right = point.x() + widget.width()
    ancestor = widget.parent()
    if ancestor is None:
        anc_right = screen_right
    else:
        anc_right = min([ancestor.x() + ancestor.width(), screen_right])
    
    # Moving widget to the left
    # if there is not enough space to the right
    if comp_right > anc_right:
        point.setX(point.x() - widget.width())
    
    # Computing completion widget and its parent bottom positions
    comp_bottom = point.y() + widget.height()
    ancestor = widget.parent()
    if ancestor is None:
        anc_bottom = screen_bottom
    else:
        anc_bottom = min([ancestor.y()+ancestor.height(), screen_bottom])
    
    # Moving widget above if there is not enough space below
    x_position = point.x()
    if comp_bottom > anc_bottom and isinstance(point_rect, QtCore.QRect):
        point = point_rect.topRight()
        point.setX(x_position)
        point.setY(point.y() - widget.height())
        
    if ancestor is not None:
        # Useful only if we set parent to 'ancestor' in __init__
        point = ancestor.mapFromGlobal(point)
    widget.move(point)
    
        