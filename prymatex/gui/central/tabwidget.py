#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Copyright (c) 2008, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

#------------------------------------------------------------------------------

# Standard library imports.
import sys

# Major library imports.
import sip
from PyQt4 import QtCore, QtGui

class _TabWidget(QtGui.QTabWidget):
    """ The _TabWidget class is a QTabWidget with a dragable tab bar. """

    def __init__(self, root, *args):
        """ Initialise the instance. """

        QtGui.QTabWidget.__init__(self, *args)
        
        # XXX this requires Qt > 4.5
        if sys.platform == 'darwin':
            self.setDocumentMode(True)

        self._root = root

        # We explicitly pass the parent to the tab bar ctor to work round a bug
        # in PyQt v4.2 and earlier.
        self.setTabBar(_DragableTabBar(self._root, self))

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self._close_tab)        

    def _still_needed(self):
        """ Delete the tab widget (and any relevant parent splitters) if it is
        no longer needed.
        """

        if self.count() == 0:
            prune = self
            parent = prune.parent()

            # Go up the QSplitter hierarchy until we find one with at least one
            # sibling.
            while parent is not self._root and parent.count() == 1:
                prune = parent
                parent = prune.parent()

            prune.hide()
            prune.deleteLater()

    def tabRemoved(self, idx):
        """ Reimplemented to update the record of the current tab if it is
        removed.
        """

        self._still_needed()

        if self._root._current_tab_w is self and self._root._current_tab_idx == idx:
            self._root._current_tab_w = None

    def _close_tab(self, index):
        """ Close the current tab. """

        self._root._close_tab_request(self.widget(index))


class _DragableTabBar(QtGui.QTabBar):
    """ The _DragableTabBar class is a QTabBar that can be dragged around. """

    def __init__(self, root, parent):
        """ Initialise the instance. """

        QtGui.QTabBar.__init__(self, parent)

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

    def mousePressEvent(self, e):
        """ Reimplemented to handle mouse press events. """

        # There is something odd in the focus handling where focus temporarily
        # moves elsewhere (actually to a View) when switching to a different
        # tab page.  We suppress the notification so that the workbench doesn't
        # temporarily make the View active.
        self._root._repeat_focus_changes = False
        QtGui.QTabBar.mousePressEvent(self, e)
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

        QtGui.QTabBar.mouseMoveEvent(self, e)

        if self._drag_state is None:
            return

        if self._drag_state.dragging:
            self._drag_state.drag(e.pos())
        else:
            self._drag_state.start_dragging(e.pos())

            # If the mouse has moved far enough that dragging has started then
            # tell the user.
            if self._drag_state.dragging:
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)

    def mouseReleaseEvent(self, e):
        """ Reimplemented to handle mouse release events. """

        QtGui.QTabBar.mouseReleaseEvent(self, e)

        if e.button() != QtCore.Qt.LeftButton:
            return

        if self._drag_state is not None and self._drag_state.dragging:
            QtGui.QApplication.restoreOverrideCursor()
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

        if (pos - self._start_pos).manhattanLength() <= QtGui.QApplication.startDragDistance():
            return

        self.dragging = True

        # Create a clone of the tab being moved (except for its icon).
        otb = self._tab_bar
        tab = self._tab

        ctb = self._clone = QtGui.QTabBar()
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
