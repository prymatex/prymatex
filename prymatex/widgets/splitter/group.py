#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was adapted from spyderlib original developed by Riverbank Computing Limited
"""

# Standard library imports.
import sys
from functools import partial

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers.menus import create_menu

class GroupWidget(QtWidgets.QTabWidget):
    """ The GroupWidget class is a QTabWidget with a dragable tab bar. """

    def __init__(self, root, *args):
        """ Initialise the instance. """

        QtWidgets.QTabWidget.__init__(self, *args)
        
        # XXX this requires Qt > 4.5
        if sys.platform == 'darwin':
            self.setDocumentMode(True)

        self._root = root

        # We explicitly pass the parent to the tab bar ctor to work round a bug
        # in PyQt v4.2 and earlier.
        self.setTabBar(DragableTabBar(self._root, self))

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self._close_tab)        

    def _still_needed(self):
        """ Delete the tab widget (and any relevant parent splitters) if it is no longer needed. """

        if self.count() == 0:
            prune = self
            parent = prune.parent()

            # Go up the QSplitter hierarchy until we find one with at least one
            # sibling.
            while parent is not self._root and parent.count() == 1:
                prune = parent
                parent = prune.parent()
            
            #No remove is is last
            if parent is self._root and parent.count() == 1:
                return
            prune.hide()
            prune.deleteLater()

    def mouseDoubleClickEvent(self, event):
        self._root._tab_create_request(self)
        
    def tabRemoved(self, idx):
        """ Reimplemented to update the record of the current tab if it is removed. """
        
        self._still_needed()
        
        if self._root._current_group is self and self._root._current_tab_idx == idx:
            self._root._current_group = None

    def _close_tab(self, index):
        """ Close the current tab. """

        self._root._close_tab_request(self.widget(index))
    
    def _close_widget(self, widget):
        self._root._close_tab_request(widget)

class DragableTabBar(QtWidgets.QTabBar):
    """ The DragableTabBar class is a QTabBar that can be dragged around. """

    def __init__(self, root, parent):
        """ Initialise the instance. """

        QtWidgets.QTabBar.__init__(self, parent)

        # XXX this requires Qt > 4.5
        if sys.platform == 'darwin':
            self.setDocumentMode(True)

        self._root = root
        self._drag_state = None

    def keyPressEvent(self, e):
        """ Reimplemented to handle traversal across different tab widgets. """
        if e.key() == QtCore.Qt.Key_Left:
            self._root._move_left(self.parent(), self.currentIndex())
        elif e.key() == QtCore.Qt.Key_Right:
            self._root._move_right(self.parent(), self.currentIndex())
        else:
            e.ignore()
    
    def widgetAtPos(self, pos):
        ''' Returns the widget at position (QPoint)'''
        n = self._tab_at(pos)
        return self.parent().widget(n)

    def mousePressEvent(self, e):
        """ Reimplemented to handle mouse press events. """
        if e.button() == QtCore.Qt.RightButton:
            widget = self.widgetAtPos(e.pos())
            tabWidget = self.parent()
            tabSplitter = tabWidget._root
            tabMenu = { 
                "text": "Tab Menu",
                "items": [
                    {   "text": "Close",
                        "triggered": partial(tabWidget._close_widget, widget) 
                    },
                    {   "text": "Close all",
                        "triggered": tabSplitter.closeAll
                    },
                    {   "text": "Close other",
                        "triggered": partial(tabSplitter.closeAllExceptWidget, widget)
                    }
                ]
            }

            if self.parent().count() > 1:
                tabMenu["items"].extend([
                    "-", {
                        "text": "Split vertically",
                        "triggered": partial(tabSplitter.splitVertically, widget)   
                    }, {
                        "text": "Split horizontally",
                        "triggered": partial(tabSplitter.splitHorizontally, widget)
                    }
                ])
            tabMenu["items"].append("-")
            # Create custom menu
            tabMenu["items"].extend(widget.contributeToTabMenu())
            
            menu = create_menu(self, tabMenu)
            
            # Display menu
            menu.exec_(e.globalPos())
        elif e.button() == QtCore.Qt.LeftButton:

            # There is something odd in the focus handling where focus temporarily
            # moves elsewhere (actually to a View) when switching to a different
            # tab page.  We suppress the notification so that the workbench doesn't
            # temporarily make the View active.
            self._root._repeat_focus_changes = False
            QtWidgets.QTabBar.mousePressEvent(self, e)
            self._root._repeat_focus_changes = True
    
            # Update the current tab.
            self._root._set_current_tab(self.parent(), self.currentIndex())
            self._root._set_focus()
    
            if e.button() != QtCore.Qt.LeftButton:
                return
    
            if self._drag_state is not None:
                return
    
            # Potentially start dragging if the tab under the mouse is the current
            # one (which will eliminate disabled tabs).
            tab = self._tab_at(e.pos())
    
            if tab < 0 or tab != self.currentIndex():
                return
    
            self._drag_state = _DragState(self._root, self, tab, e.pos())

    def mouseMoveEvent(self, e):
        """ Reimplemented to handle mouse move events. """

        QtWidgets.QTabBar.mouseMoveEvent(self, e)

        if self._drag_state is None:
            return

        if self._drag_state.dragging:
            self._drag_state.drag(e.pos())
        else:
            self._drag_state.start_dragging(e.pos())

            # If the mouse has moved far enough that dragging has started then
            # tell the user.
            if self._drag_state.dragging:
                QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)

    def mouseReleaseEvent(self, e):
        """ Reimplemented to handle mouse release events. """

        QtWidgets.QTabBar.mouseReleaseEvent(self, e)

        if e.button() != QtCore.Qt.LeftButton:
            return

        if self._drag_state is not None and self._drag_state.dragging:
            QtWidgets.QApplication.restoreOverrideCursor()
            self._drag_state.drop(e.pos())

        self._drag_state = None

    def _tab_at(self, pos):
        """ Return the index of the tab at the given point. """

        for i in range(self.count()):
            if self.tabRect(i).contains(pos):
                return i

        return -1


class _DragState(object):
    """ The _DragState class handles most of the work when dragging a tab. """

    def __init__(self, root, tab_bar, tab, start_pos):
        """ Initialise the instance. """

        self.dragging = False

        self._root = root
        self._tab_bar = tab_bar
        self._tab = tab
        self._start_pos = QtCore.QPoint(start_pos)
        self._clone = None

    def start_dragging(self, pos):
        """ Start dragging a tab. """

        if (pos - self._start_pos).manhattanLength() <= QtWidgets.QApplication.startDragDistance():
            return

        self.dragging = True

        # Create a clone of the tab being moved (except for its icon).
        otb = self._tab_bar
        tab = self._tab

        ctb = self._clone = QtWidgets.QTabBar()
        if sys.platform == 'darwin' and QtCore.QT_VERSION >= 0x40500:
            ctb.setDocumentMode(True)
          
        ctb.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        ctb.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                           QtCore.Qt.Tool |
                           QtCore.Qt.X11BypassWindowManagerHint)
        ctb.setWindowOpacity(0.5)
        ctb.setElideMode(otb.elideMode())
        ctb.setShape(otb.shape())

        ctb.addTab(otb.tabText(tab))
        ctb.setTabTextColor(0, otb.tabTextColor(tab))

        # The clone offset is the position of the clone relative to the mouse.
        trect = otb.tabRect(tab)
        self._clone_offset = trect.topLeft() - pos

        # The centre offset is the position of the center of the clone relative
        # to the mouse.  The center of the clone determines the hotspot, not
        # the position of the mouse.
        self._centre_offset = trect.center() - pos

        self.drag(pos)

        ctb.show()

    def drag(self, pos):
        """ Handle the movement of the cloned tab during dragging. """

        self._clone.move(self._tab_bar.mapToGlobal(pos) + self._clone_offset)
        self._root._select(self._tab_bar.mapTo(self._root,
                                               pos + self._centre_offset))

    def drop(self, pos):
        """ Handle the drop of the cloned tab. """

        self.drag(pos)
        self._clone = None

        global_pos = self._tab_bar.mapToGlobal(pos)
        self._root._drop(global_pos, self._tab_bar.parent(), self._tab)

        self.dragging = False
