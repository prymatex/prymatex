#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Copyright (c) 2008, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

#------------------------------------------------------------------------------

# Major library imports.
import sip

from PyQt4 import QtCore, QtGui

from prymatex.widgets.tabwidget import _TabWidget, _DragableTabBar

def createDisambiguatedTitles(addedTitles, newTitle):
    titleFormat = newTitle[0] + " (%s)"
    usedSubtitles = [ newTitle[1] ]
    for addedTitle in addedTitles:
        for index in xrange(1, len(addedTitle)):
            if addedTitle[index] not in usedSubtitles:
                usedSubtitles.append(addedTitle[index])
                break
    return (map(lambda subTitle: titleFormat % subTitle, usedSubtitles[1:]), titleFormat % usedSubtitles[0])

class SplitTabWidget(QtGui.QSplitter):
    """ The SplitTabWidget class is a hierarchy of QSplitters the leaves of
    which are QTabWidgets.  Any tab may be moved around with the hierarchy
    automatically extended and reduced as required.
    """
    
    # Signals
    #newWindowRequest = QtCore.pyqtSignal(QtCore.QPoint, QtGui.QWidget)
    tabCloseRequest = QtCore.pyqtSignal(QtGui.QWidget)
    tabCreateRequest = QtCore.pyqtSignal()
    currentWidgetChanged = QtCore.pyqtSignal(QtGui.QWidget)
    
    # The different hotspots of a QTabWidget.  An non-negative value is a tab
    # index and the hotspot is to the left of it.
    _HS_NONE = -1
    _HS_AFTER_LAST_TAB = -2
    _HS_NORTH = -3
    _HS_SOUTH = -4
    _HS_EAST = -5
    _HS_WEST = -6
    _HS_OUTSIDE = -7

    def __init__(self, *args):
        """ Initialise the instance. """

        QtGui.QSplitter.__init__(self, *args)

        self.clear()

        self.connect(QtGui.qApp,
                     QtCore.SIGNAL('focusChanged(QWidget *,QWidget *)'),
                     self._focus_changed)

    def __len__(self):
        count = 0
        for tw in self.findChildren(_TabWidget):
            count += tw.count()
        return count
    
    def clear(self):
        """ Restore the widget to its pristine state. """

        w = None
        for i in range(self.count()):
            w = self.widget(i)
            w.hide()
            w.deleteLater()
        del w

        self._repeat_focus_changes = True
        self._rband = None
        self._selected_tab_widget = None
        self._selected_hotspot = self._HS_NONE

        self._current_tab_w = None
        self._current_tab_idx = -1

    def saveState(self):
        """ Returns a Python object containing the saved state of the widget.
        Widgets are saved only by their object name.
        """

        return self._save_qsplitter(self)

    def _save_qsplitter(self, qsplitter):
        # A splitter state is a tuple of the QSplitter state (as a string) and
        # the list of child states.
        sp_ch_states = []

        # Save the children.
        for i in range(qsplitter.count()):
            ch = qsplitter.widget(i)

            if isinstance(ch, _TabWidget):
                # A tab widget state is a tuple of the current tab index and
                # the list of individual tab states.
                tab_states = []

                for t in range(ch.count()):
                    # A tab state is a tuple of the widget's object name and
                    # the title.
                    name = unicode(ch.widget(t).objectName())
                    title = unicode(ch.tabText(t))

                    tab_states.append((name, title))

                ch_state = (ch.currentIndex(), tab_states)
            else:
                # Recurse down the tree of splitters.
                ch_state = self._save_qsplitter(ch)

            sp_ch_states.append(ch_state)

        return (str(QtGui.QSplitter.saveState(qsplitter)), sp_ch_states)

    def restoreState(self, state, factory):
        """ Restore the contents from the given state (returned by a previous
        call to saveState()).  factory is a callable that is passed the object
        name of the widget that is in the state and needs to be restored.  The
        callable returns the restored widget.
        """

        # Ensure we are not restoring to a non-empty widget.
        assert self.count() == 0

        self._restore_qsplitter(state, factory, self)

    def _restore_qsplitter(self, state, factory, qsplitter):
        sp_qstate, sp_ch_states = state

        # Go through each child state which will consist of a tuple of two
        # objects.  We use the type of the first to determine if the child is a
        # tab widget or another splitter.
        for ch_state in sp_ch_states:
            if isinstance(ch_state[0], int):
                current_idx, tabs = ch_state

                new_tab = _TabWidget(self)

                # Go through each tab and use the factory to restore the page.
                for name, title in tabs:
                    page = factory(name)

                    if page is not None:
                        new_tab.addTab(page, title)

                # Only add the new tab widget if it is used.
                if new_tab.count() > 0:
                    qsplitter.addWidget(new_tab)

                    # Set the correct tab as the current one.
                    new_tab.setCurrentIndex(current_idx)
                else:
                    del new_tab
            else:
                new_qsp = QtGui.QSplitter()

                # Recurse down the tree of splitters.
                self._restore_qsplitter(ch_state, factory, new_qsp)

                # Only add the new splitter if it is used.
                if new_qsp.count() > 0:
                    qsplitter.addWidget(new_qsp)
                else:
                    del new_qsp

        # Restore the QSplitter state (being careful to get the right
        # implementation).
        QtGui.QSplitter.restoreState(qsplitter, sp_qstate)

    def addTab(self, w):
        """ Add a new tab to the main tab widget. """

        if self.count() > 0:
            # Find the first tab widget going down the left of the hierarchy. This
            # will be the one in the top left corner.
            
            ch = self.widget(0)
            while not isinstance(ch, _TabWidget):
                assert isinstance(ch, QtGui.QSplitter)
                ch = ch.widget(0)
        else:
            # There is no tab widget so create one.
            ch = _TabWidget(self)
            self.addWidget(ch)

        idx = ch.addTab(w, self.disambiguatedWidgetTitle(w))
        self.setWidgetToolTip(w, w.tabToolTip())
        self.setWidgetIcon(w, w.tabIcon())
        self.connect(w, QtCore.SIGNAL("tabStatusChanged()"), self._update_tab_status)
        
        if ch is not self._current_tab_w:
            self._set_current_tab(ch, idx)
            #ch.tabBar().setFocus()
    
    def removeTab(self, w):
        """ Remove tab to the tab widget."""
        tw, tidx = self._tab_widget(w)

        if tw is not None:
            self.disconnect(w, QtCore.SIGNAL("tabStatusChanged()"), self._update_tab_status)
            self._remove_tab(tw, tidx)
            if tw.count() == 0 and self.count() > 1:
                for tw in self.findChildren(_TabWidget):
                    if tw.count() != 0:
                        break
                self._set_current_tab(tw, 0)
            elif tidx != 0:
                self._set_current_tab(tw, tidx - 1)
            else:
                self._set_current_tab(tw, tidx)
            #tw.tabBar().setFocus()

    def setCurrentWidget(self, w):
        """ Make the given widget current. """

        tw, tidx = self._tab_widget(w)

        if tw is not None:
            self._set_current_tab(tw, tidx)

    def currentWidget(self):
        """ Return current widget. """
        
        if self._current_tab_w != None and self._current_tab_idx != -1:
            return self._current_tab_w.widget(self._current_tab_idx)

    def _update_tab_status(self):
        sender = self.sender()
        self.setWidgetTitle(sender, sender.tabTitle())
        self.setWidgetIcon(sender, sender.tabIcon())
        self.setWidgetToolTip(sender, sender.tabToolTip())
                
    def _close_tab_request(self, w):
        """ A close button was clicked in one of out _TabWidgets """
        
        self.tabCloseRequest.emit(w)

    def _current_tab_changed(self, w):
        """ A close button was clicked in one of out _TabWidgets """
        
        self.currentWidgetChanged.emit(w)
        
    def setWidgetIcon(self, w, icon):
        """ Set the active icon on a widget. """

        tw, tidx = self._tab_widget(w)

        if tw is not None:
            tw.setTabIcon(tidx, icon)

    def disambiguatedWidgetTitle(self, widget):  
        #Buscar todas las tabs con el mismo nombre
        newWidgetTitle = widget.tabTitle()
        addedWidgets = self.widgetsByTitle(newWidgetTitle)
        if addedWidgets:
            addedTitles, newWidgetTitle = createDisambiguatedTitles(map(lambda widget: widget.tabTitles(), addedWidgets), widget.tabTitles())
            for widget, title in zip(addedWidgets, addedTitles):
                self.setWidgetTitle(widget, title)
        return newWidgetTitle

    def widgetsByTitle(self, title):
        widgets = []
        for tw in self.findChildren(_TabWidget):
            for index in xrange(tw.count()):
                widget = tw.widget(index)
                if widget.tabTitle() == title:
                    widgets.append(widget)
        return widgets

    def setWidgetTitle(self, w, title):
        """ Set the title for the given widget. """

        tw, idx = self._tab_widget(w)

        if tw is not None:
            tw.setTabText(idx, title)
    
    def setWidgetToolTip(self, w, toolTip):
        """ Set the title for the given widget. """

        tw, idx = self._tab_widget(w)

        if tw is not None:
            tw.setTabToolTip(idx, toolTip)
    
    def setTabTextColor(self, w, color):
        """ 
        Set the tab text color on a particular widget w
        """
        tw, tidx = self._tab_widget(w)

        if tw is not None:
            tw.tabBar().setTabTextColor(tidx, color)

    def getAllWidgets(self):
        widgets = []
        for tw in self.findChildren(_TabWidget):
            for index in xrange(tw.count()):
                widgets.append(tw.widget(index))
        return widgets
    
    def closeAllExceptWidget(self, widget):
        count = 0
        for w in self.getAllWidgets():
            if w is widget:
                continue
            self._close_tab_request(w)
            count += 1
        return count
    
    def closeAll(self):
        return self.closeAllExceptWidget(None)
    
    def _tab_widget(self, w):
        """ Return the tab widget and index containing the given widget. """

        for tw in self.findChildren(_TabWidget):
            idx = tw.indexOf(w)

            if idx >= 0:
                return (tw, idx)

        return (None, None)

    def _set_current_tab(self, tw, tidx):
        """ Set the new current tab. """

        # Handle the trivial case.
        if self._current_tab_w is tw and self._current_tab_idx == tidx:
            return

        if tw is not None:
            tw.setCurrentIndex(tidx)
        
        # Save the new current widget.
        self._current_tab_w = tw
        widget = self._current_tab_w.widget(tidx)
        self._current_tab_idx = tidx if widget is not None else -1
        self.currentWidgetChanged.emit(widget)

    def _set_focus(self):
        """ Set the focus to an appropriate widget in the current tab. """

        # Only try and change the focus if the current focus isn't already a
        # child of the widget.
        w = self._current_tab_w.widget(self._current_tab_idx)
        fw = self.window().focusWidget()

        if fw is not None and not w.isAncestorOf(fw):
            # Find a widget to focus using the same method as
            # QStackedLayout::setCurrentIndex().  First try the last widget
            # with the focus.
            nfw = w.focusWidget()

            if nfw is None:
                # Next, try the first child widget in the focus chain.
                nfw = fw.nextInFocusChain()

                while nfw is not fw:
                    if nfw.focusPolicy() & QtCore.Qt.TabFocus and \
                       nfw.focusProxy() is None and \
                       nfw.isVisibleTo(w) and \
                       nfw.isEnabled() and \
                       w.isAncestorOf(nfw):
                        break

                    nfw = nfw.nextInFocusChain()
                else:
                    # Fallback to the tab page widget.
                    nfw = w

            nfw.setFocus()

    def _focus_changed(self, old, new):
        """ Handle a change in focus that affects the current tab. """

        # It is possible for the C++ layer of this object to be deleted between
        # the time when the focus change signal is emitted and time when the
        # slots are dispatched by the Qt event loop. This may be a bug in PyQt4.
        if sip.isdeleted(self):
            return
        
        if self._repeat_focus_changes:
            self.emit(QtCore.SIGNAL('focusChanged(QWidget *,QWidget *)'), old, new)

        if isinstance(new, _DragableTabBar):
            ntw = new.parent()
            ntidx = ntw.currentIndex()
        else:
            ntw, ntidx = self._tab_widget_of(new)
        
        if ntw is not None:
            self._set_current_tab(ntw, ntidx)

        # See if the widget that has lost the focus is ours.
        otw, _ = self._tab_widget_of(old)

        if otw is not None or ntw is not None:
            if ntw is None:
                nw = None
            else:
                nw = ntw.widget(ntidx)
            self.emit(QtCore.SIGNAL('hasFocus'), nw)

    def _tab_widget_of(self, target):
        """ Return the tab widget and index of the widget that contains the
        given widget.
        """

        for tw in self.findChildren(_TabWidget):
            for tidx in range(tw.count()):
                w = tw.widget(tidx)

                if w is not None and w.isAncestorOf(target):
                    return (tw, tidx)

        return (None, None)

    def _move_left(self, tw, tidx):
        """ Move the current tab to the one logically to the left. """

        tidx -= 1

        if tidx < 0:
            # Find the tab widget logically to the left.
            twlist = self.findChildren(_TabWidget)
            i = twlist.index(tw)
            i -= 1

            if i < 0:
                i = len(twlist) - 1

            tw = twlist[i]

            # Move the to right most tab.
            tidx = tw.count() - 1

        self._set_current_tab(tw, tidx)
        #tw.setFocus()

    def _move_right(self, tw, tidx):
        """ Move the current tab to the one logically to the right. """

        tidx += 1

        if tidx >= tw.count():
            # Find the tab widget logically to the right.
            twlist = self.findChildren(_TabWidget)
            i = twlist.index(tw)
            i += 1

            if i >= len(twlist):
                i = 0

            tw = twlist[i]

            # Move the to left most tab.
            tidx = 0

        self._set_current_tab(tw, tidx)
        #tw.setFocus()

    def _select(self, pos):
        tw, hs, hs_geom = self._hotspot(pos)

        # See if the hotspot has changed.
        if self._selected_tab_widget is not tw or self._selected_hotspot != hs:
            if self._selected_tab_widget is not None:
                self._rband.hide()

            if tw is not None and hs != self._HS_NONE:
                if self._rband:
                    self._rband.deleteLater()
                position = QtCore.QPoint(*hs_geom[0:2])
                window = tw.window()
                self._rband = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,
                                                window)
                self._rband.move(window.mapFromGlobal(position))
                self._rband.resize(*hs_geom[2:4])
                self._rband.show()

            self._selected_tab_widget = tw
            self._selected_hotspot = hs

    def _drop(self, pos, stab_w, stab):
        self._rband.hide()

        # Get the destination locations.
        dtab_w = self._selected_tab_widget
        dhs = self._selected_hotspot
        if dhs == self._HS_NONE:
            return
        elif dhs != self._HS_OUTSIDE:
            dsplit_w = dtab_w.parent()
            while not isinstance(dsplit_w, SplitTabWidget):
                dsplit_w = dsplit_w.parent()

        self._selected_tab_widget = None
        self._selected_hotspot = self._HS_NONE

        # See if the tab is being moved to a new window.
        if dhs == self._HS_OUTSIDE:
            # Disable tab tear-out for now. It works, but this is something that
            # should be turned on manually. We need an interface for this.
            #ticon, ttext, ttextcolor, twidg = self._remove_tab(stab_w, stab)
            self.newWindowRequest.emit(pos, twidg)
            return

        # See if the tab is being moved to an existing tab widget.
        if dhs >= 0 or dhs == self._HS_AFTER_LAST_TAB:
            # Make sure it really is being moved.
            if stab_w is dtab_w:
                if stab == dhs:
                    return

                if dhs == self._HS_AFTER_LAST_TAB and stab == stab_w.count()-1:
                    return

            QtGui.qApp.blockSignals(True)

            ticon, ttext, ttextcolor, twidg = self._remove_tab(stab_w, stab)

            if dhs == self._HS_AFTER_LAST_TAB:
                idx = dtab_w.addTab(twidg, ticon, ttext)
                dtab_w.tabBar().setTabTextColor(idx, ttextcolor)
            elif dtab_w is stab_w:
                # Adjust the index if necessary in case the removal of the tab
                # from its old position has skewed things.
                dst = dhs

                if dhs > stab:
                    dst -= 1

                idx = dtab_w.insertTab(dst, twidg, ticon, ttext)
                dtab_w.tabBar().setTabTextColor(idx, ttextcolor)
            else:
                idx = dtab_w.insertTab(dhs, twidg, ticon, ttext)
                dtab_w.tabBar().setTabTextColor(idx, ttextcolor)

            dsplit_w._set_current_tab(dtab_w, idx)

        else:
            # Ignore drops to the same tab widget when it only has one tab.
            if stab_w is dtab_w and stab_w.count() == 1:
                return

            QtGui.qApp.blockSignals(True)

            # Remove the tab from its current tab widget and create a new one
            # for it.
            ticon, ttext, ttextcolor, twidg = self._remove_tab(stab_w, stab)
            new_tw = _TabWidget(dsplit_w)
            new_tw.addTab(twidg, ticon, ttext)
            new_tw.tabBar().setTabTextColor(0, ttextcolor)

            # Get the splitter containing the destination tab widget.
            dspl = dtab_w.parent()
            dspl_idx = dspl.indexOf(dtab_w)

            if dhs in (self._HS_NORTH, self._HS_SOUTH):
                dspl, dspl_idx = dsplit_w._horizontal_split(dspl, dspl_idx, dhs)
            else:
                dspl, dspl_idx = dsplit_w._vertical_split(dspl, dspl_idx, dhs)

            # Add the new tab widget in the right place.
            dspl.insertWidget(dspl_idx, new_tw)

            dsplit_w._set_current_tab(new_tw, 0)
        
        dsplit_w._set_focus()

        # Signal that the tab's SplitTabWidget has changed, if necessary.
        if dsplit_w != self:
            self.currentWidgetChanged.emit(twidg)
        
        QtGui.qApp.blockSignals(False)

    def _horizontal_split(self, spl, idx, hs):
        """ Returns a tuple of the splitter and index where the new tab widget
        should be put.
        """

        if spl.orientation() == QtCore.Qt.Vertical:
            if hs == self._HS_SOUTH:
                idx += 1
        elif spl is self and spl.count() == 1:
            # The splitter is the root and only has one child so we can just
            # change its orientation.
            spl.setOrientation(QtCore.Qt.Vertical)

            if hs == self._HS_SOUTH:
                idx = -1
        else:
            new_spl = QtGui.QSplitter(QtCore.Qt.Vertical)
            new_spl.addWidget(spl.widget(idx))
            spl.insertWidget(idx, new_spl)

            if hs == self._HS_SOUTH:
                idx = -1
            else:
                idx = 0

            spl = new_spl

        return (spl, idx)

    def _vertical_split(self, spl, idx, hs):
        """ Returns a tuple of the splitter and index where the new tab widget
        should be put.
        """

        if spl.orientation() == QtCore.Qt.Horizontal:
            if hs == self._HS_EAST:
                idx += 1
        elif spl is self and spl.count() == 1:
            # The splitter is the root and only has one child so we can just
            # change its orientation.
            spl.setOrientation(QtCore.Qt.Horizontal)

            if hs == self._HS_EAST:
                idx = -1
        else:
            new_spl = QtGui.QSplitter(QtCore.Qt.Horizontal)
            new_spl.addWidget(spl.widget(idx))
            spl.insertWidget(idx, new_spl)

            if hs == self._HS_EAST:
                idx = -1
            else:
                idx = 0

            spl = new_spl

        return (spl, idx)

    def _remove_tab(self, tab_w, tab):
        """ Remove a tab from a tab widget and return a tuple of the icon,
        label text and the widget so that it can be recreated.
        """

        icon = tab_w.tabIcon(tab)
        text = tab_w.tabText(tab)
        text_color = tab_w.tabBar().tabTextColor(tab)
        w = tab_w.widget(tab)
        tab_w.removeTab(tab)

        return (icon, text, text_color, w)

    def _hotspot(self, pos):
        """ Return a tuple of the tab widget, hotspot and hostspot geometry (as
        a tuple) at the given position.
        """
        global_pos = self.mapToGlobal(pos)
        miss = (None, self._HS_NONE, None)

        # Get the bounding rect of the cloned QTbarBar.
        top_widget = QtGui.qApp.topLevelAt(global_pos)
        if isinstance(top_widget, QtGui.QTabBar):
            cloned_rect = top_widget.frameGeometry()
        else:
            cloned_rect = None
        
        # Determine which visible SplitTabWidget, if any, is under the cursor
        # (compensating for the cloned QTabBar that may be rendered over it).
        split_widget = None
        for top_widget in QtGui.qApp.topLevelWidgets():
            for split_widget in top_widget.findChildren(SplitTabWidget):
                visible_region = split_widget.visibleRegion()
                widget_pos = split_widget.mapFromGlobal(global_pos)
                if cloned_rect and split_widget.geometry().contains(widget_pos):
                    visible_rect = visible_region.boundingRect()
                    widget_rect = QtCore.QRect(
                        split_widget.mapFromGlobal(cloned_rect.topLeft()),
                        split_widget.mapFromGlobal(cloned_rect.bottomRight()))
                    if not visible_rect.intersected(widget_rect).isEmpty():
                        break
                elif visible_region.contains(widget_pos):
                    break
            else:
                split_widget = None
            if split_widget:
                break

        # Handle a drag outside of any split tab widget.
        if not split_widget:
            if self.window().frameGeometry().contains(global_pos):
                return miss
            else:
                return (None, self._HS_OUTSIDE, None)

        # Go through each tab widget.
        pos = split_widget.mapFromGlobal(global_pos)
        for tw in split_widget.findChildren(_TabWidget):
            if tw.geometry().contains(tw.parent().mapFrom(split_widget, pos)):
                break
        else:
            return miss

        # See if the hotspot is in the widget area.
        widg = tw.currentWidget()
        if widg is not None:

            # Get the widget's position relative to its parent.
            wpos = widg.parent().mapFrom(split_widget, pos)

            if widg.geometry().contains(wpos):
                # Get the position of the widget relative to itself (ie. the
                # top left corner is (0, 0)).
                p = widg.mapFromParent(wpos)
                x = p.x()
                y = p.y()
                h = widg.height()
                w = widg.width()

                # Get the global position of the widget.
                gpos = widg.mapToGlobal(widg.pos())
                gx = gpos.x()
                gy = gpos.y()

                # The corners of the widget belong to the north and south
                # sides.
                if y < h / 4:
                    return (tw, self._HS_NORTH, (gx, gy, w, h / 4))

                if y >= (3 * h) / 4:
                    return (tw, self._HS_SOUTH, (gx, gy + (3*h) / 4, w, h / 4))

                if x < w / 4:
                    return (tw, self._HS_WEST, (gx, gy, w / 4, h))

                if x >= (3 * w) / 4:
                    return (tw, self._HS_EAST, (gx + (3*w) / 4, gy, w / 4, h))

                return miss

        # See if the hotspot is in the tab area.
        tpos = tw.mapFrom(split_widget, pos)
        tab_bar = tw.tabBar()
        top_bottom = tw.tabPosition() in (QtGui.QTabWidget.North, 
                                          QtGui.QTabWidget.South)
        for i in range(tw.count()):
            rect = tab_bar.tabRect(i)

            if rect.contains(tpos):
                w = rect.width()
                h = rect.height()

                # Get the global position.
                gpos = tab_bar.mapToGlobal(rect.topLeft())
                gx = gpos.x()
                gy = gpos.y()

                if top_bottom:
                    off = pos.x() - rect.x()
                    ext = w
                    gx -= w / 2
                else:
                    off = pos.y() - rect.y()
                    ext = h
                    gy -= h / 2

                # See if it is in the left (or top) half or the right (or
                # bottom) half.
                if off < ext / 2:
                    return (tw, i, (gx, gy, w, h))

                if top_bottom:
                    gx += w
                else:
                    gy += h

                if i + 1 == tw.count():
                    return (tw, self._HS_AFTER_LAST_TAB, (gx, gy, w, h))

                return (tw, i + 1, (gx, gy, w, h))
        else:
            rect = tab_bar.rect()
            if rect.contains(tpos):
                gpos = tab_bar.mapToGlobal(rect.topLeft())
                gx = gpos.x()
                gy = gpos.y()
                w = rect.width() 
                h = rect.height()
                if top_bottom:
                    tab_widths = sum(tab_bar.tabRect(i).width()
                        for i in range(tab_bar.count()))
                    w -= tab_widths
                    gx += tab_widths
                else:
                    tab_heights = sum(tab_bar.tabRect(i).height()
                        for i in range(tab_bar.count()))
                    h -= tab_heights
                    gy -= tab_heights
                return (tw, self._HS_AFTER_LAST_TAB, (gx, gy, w, h))
                
        return miss
    
    def mouseDoubleClickEvent(self, event):
        """
        Add an empty editor when the tab bar is double clicked
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.tabCreateRequest.emit()
        
    def moveCurrentTabLeft(self):
        raise NotImplementedError("Not implemented yet")   

    def moveCurrentTabRight(self):
        raise NotImplementedError("Not implemented yet")
    
    def focusNextTab(self):
        self._move_right(self._current_tab_w, self._current_tab_idx)
    
    def focusPreviousTab(self):
        self._move_left(self._current_tab_w, self._current_tab_idx)
        