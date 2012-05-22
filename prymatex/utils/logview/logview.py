#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2011 by Vinay Sajip. All rights reserved. See accompanying LICENSE.txt for details.
"""
A program to view logs sent via TCP and UDP sockets.
"""
from qt import QtCore, QtGui, Qt
from ui_mainwindow import Ui_MainWindow

import about
import bisect
import collections
import colprefs
try:
    import json
except ImportError:
    import simplejson as json
import listeners
import logging
from logging.handlers import DEFAULT_TCP_LOGGING_PORT, DEFAULT_UDP_LOGGING_PORT
import optparse
import os
try:
    import cPickle as pickle
except ImportError:
    import pickle
import re
import sys
import textinfo
import threading
from urllib import quote, unquote
try:
    import zmq
except ImportError:
    print sys.exc_info()[1]
    zmq = None

appname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
logger = logging.getLogger(appname)

MessageRole = Qt.UserRole

invindex = QtCore.QModelIndex()

class TreeNode(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.children = []

    @property
    def path(self):
        result = [self.name]
        parent = self.parent
        if parent and parent.parent:
            result.insert(0, parent.path)
        return '.'.join(result)

    @property
    def row(self):
        result = 0
        parent = self.parent
        if parent:
            result = parent.children.index(self)
        return result
        
class LoggerModel(QtCore.QAbstractItemModel):
    def __init__(self, parent):
        super(LoggerModel, self).__init__(parent)
        self._root = TreeNode(None, '')
        self._registry = {
            '': self._root,
        }

    def columnCount(self, parent):
        return 1

    def index(self, row, column, parent):
        try:
            if not parent.isValid():
                #logger.debug('creating root index')
                result = self.createIndex(row, column, self._root)
            else:
                node = parent.internalPointer()
                #logger.debug('creating index for %r', node.path)
                result = self.createIndex(row, column, node.children[row])
        except IndexError:
            result = invindex
        return result

    def parent(self, index):
        result = invindex
        if index.isValid():
            node = index.internalPointer()
            if node.parent is not None:
                result = self.createIndex(node.parent.row, 0, node.parent)
        return result

    def rowCount(self, parent):
        if not parent.isValid():
            result = 1
        else:
            node = parent.internalPointer()
            result = len(node.children)
        return result

    def data(self, index, role=Qt.DisplayRole):
        result = None
        if index.isValid():
            node = index.internalPointer()
            if role == Qt.DisplayRole:
                try:
                    result = node.name
                    if not node.parent:
                        result = 'Root logger'
                except Exception:
                    pass
            elif role == Qt.ToolTipRole:
                result = node.path
        return result

    def headerData(self, section, orientation, role):
        result = None
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            result = 'Logger name'
        return result

    def register_logger(self, name):
        if name in self._registry:
            result = self._registry[name]
        else:
            parts = name.rsplit('.', 1)
            nodename = parts[-1]
            if len(parts) == 1:
                parent = self._root
            else:
                parent = self.register_logger(parts[0])
            pindex = self.createIndex(0, 0, parent)
            names = [c.name for c in parent.children]
            pos = bisect.bisect(names, nodename)
            result = TreeNode(parent, nodename)
            self._registry[name] = result
            self.beginInsertRows(pindex, pos, pos)
            parent.children.insert(pos, result)
            self.endInsertRows()
        return result

    def clear(self):
        self._registry = {}
        self._root.children = []
        self.reset()

class Column(object):
    def __init__(self, name, title, visible=True):
        self.name = name
        self.title = title
        self.visible = visible

class LogRecordModel(QtCore.QAbstractTableModel):

    foreground_map = {
        logging.ERROR: QtGui.QColor(255, 0, 0),
        logging.CRITICAL: QtGui.QColor(255, 255, 255),
    }

    background_map = {
        logging.DEBUG: QtGui.QColor(192, 255, 255),
        logging.WARNING: QtGui.QColor(255, 255, 192),
        #logging.ERROR: QtGui.QColor(255, 192, 192),
        logging.CRITICAL: QtGui.QColor(255, 0, 0),
    }

    style_map = {
        logging.ERROR: 'bold',
        logging.CRITICAL: 'bold',
    }

    def __init__(self, parent, records, columns, capacity=0):
        super(LogRecordModel, self).__init__(parent)
        self._records = records
        self._columns = columns
        self.font = parent.font()
        self._capacity = capacity

    def columnCount(self, index):
        if index.isValid():
            result = 0
        else:
            visible = [col for col in self._columns if col.visible]
            result = len(visible)
        return result

    def rowCount(self, index):
        if self._records is None or index.isValid():
            result = 0
        else:
            result = len(self._records)
        return result

    def data(self, index, role=Qt.DisplayRole):
        result = None
        if index.isValid():
            record = self._records[index.row()]
            if role == Qt.DisplayRole:
                try:
                    viscols = [c for c in self._columns if c.visible]
                    col = viscols[index.column()]
                    v = getattr(record, col.name)
                    result = v
                except Exception:
                    logger.exception('Error')
            elif role == Qt.BackgroundColorRole:
                result = self.background_map.get(record.levelno)
            elif role == Qt.TextColorRole:
                result = self.foreground_map.get(record.levelno)
            elif role == Qt.FontRole:
                QFont = QtGui.QFont
                result = None
                style = self.style_map.get(record.levelno)
                if style:
                    result = QFont(self.font)
                    if 'bold' in style:
                        result.setWeight(QFont.Bold)
                    if 'italic' in style:
                        result.setStyle(QFont.StyleItalic)
            elif role == MessageRole: # special role used for searching
                result = record.message
        return result

    def headerData(self, section, orientation, role):
        result = None
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                visible = [col.title for col in self._columns if col.visible]
                result = visible[section]
            except IndexError:
                pass
        return result

    def add_record(self, record):
        pos = len(self._records)
        if self._capacity and pos >= self._capacity:
            self.beginRemoveRows(invindex, 0, 0)
            self._records.popleft()
            self.endRemoveRows()
            pos -= 1
        self.beginInsertRows(invindex, pos, pos)
        self._records.append(record)
        self.endInsertRows()

    def clear(self):
        if hasattr(self._records, 'clear'):
            self._records.clear()
        else:
            del self._records[:]
        self.reset()

    def get_record(self, pos):
        return self._records[pos]

ATTRS = [
    'asctime',
    'name',
    'levelname',
    'message',
    'pathname',
    'lineno',
    'funcName',
    'exc_text',
    'module',
]

def attrcmp(k1, k2):
    if k1 not in ATTRS and k2 not in ATTRS:
        result = cmp(k1, k2)
    elif k2 not in ATTRS:
        result = -1
    elif k1 not in ATTRS:
        result = 1
    else:
        result = cmp(ATTRS.index(k1), ATTRS.index(k2))
    return result

class PropertySheetModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, record=None):
        super(PropertySheetModel, self).__init__(parent)
        self.record = record

    def _get_record(self):
        return self._record

    def _set_record(self, value):
        self._record = value
        if value is None:
            self._keys = []
        else:
            self._keys = sorted(vars(value), cmp=attrcmp)
        self.reset()

    record = property(_get_record, _set_record)

    def columnCount(self, index):
        return 3

    def rowCount(self, index):
        return len(self._keys)

    def headerData(self, section, orientation, role):
        result = None
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                result = ('Name', 'Value', '')[section]
            except IndexError:
                pass
        return result

    def data(self, index, role=Qt.DisplayRole):
        result = None
        if index.isValid():
            row = index.row()
            col = index.column()
            if role == Qt.DisplayRole:
                try:
                    key = self._keys[row]
                    if col == 0:
                        v = key
                    elif col == 1:
                        v = getattr(self._record, key)
                    else:
                        v = getattr(self._record, key)
                        if '\n' in str(v):
                            v = '...'
                        else:
                            v = ''
                    result = v
                except Exception:
                    logger.exception('Error getting LogRecord attribute')
            elif role == Qt.ToolTipRole and col == 1:
                try:
                    key = self._keys[row]
                    if key == 'exc_text':
                        result = getattr(self._record, key)
                except Exception:
                    logger.exception('Error getting exception text')
            elif role == Qt.TextAlignmentRole:
                if col == 2:
                    result = Qt.AlignHCenter
                else:
                    result = Qt.AlignLeft
        return result

class FilterModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent):
        super(FilterModel, self).__init__(parent)
        self.tree = parent.tree
        self.wanted = set([logging.DEBUG, logging.INFO, logging.WARNING,
                           logging.ERROR, logging.CRITICAL])

    def filterAcceptsRow(self, row, pindex):
        result = True
        record = self.sourceModel().get_record(row)
        if record.levelno not in self.wanted:
            result = False
        else:
            tindex = self.tree.currentIndex()
            if tindex.isValid():
                path = tindex.internalPointer().path
                if path:
                    if record.name == path:
                        result = True
                    elif record.name.startswith(path + '.'):
                        result = True
                    else:
                        result = False
        return result

def get_addr(s, default_port):
    if ':' not in s:
        result = s, default_port
    else:
        h, p = s.split(':')
        result = h, int(p)
    return result


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    DEFAULT_COLUMNS = [
        Column('asctime', 'Creation time'),
        Column('name', 'Logger name'),
        Column('levelname', 'Level'),
        Column('message', 'Message'),
        Column('funcName', 'Function', False),
        Column('pathname', 'Path name', False),
        Column('filename', 'File name', False),
        Column('lineno', 'Line no.', False),
        Column('module', 'Module', False),
        Column('process', 'Process ID', False),
        Column('processName', 'Process name', False),
        Column('thread', 'Thread ID', False),
        Column('threadName', 'Thread name', False),
    ]

    def __init__(self, options=None):
        super(MainWindow, self).__init__()
        self.settings = QtCore.QSettings()
        self.options = options

        self._sindex = 0
        self.expand_tree = True
        self.moved_to_bottom = False
        self.split_sizes = {}
        self.setupUi(self)
        self.start_listeners()

    def start_listeners(self):
        options = self.options
        if options:
            self.tcp_addr = get_addr(options.tcphost, DEFAULT_TCP_LOGGING_PORT)
        s = listeners.LoggingTCPServer(self.tcp_addr, self.on_record, 0.5)
        self.tcp_server = s
        self.tcp_thread = t = threading.Thread(target=s.serve_until_stopped)
        self._lock = threading.RLock()
        t.setDaemon(True)
        t.start()

        if options:
            self.udp_addr = get_addr(options.udphost, DEFAULT_UDP_LOGGING_PORT)
        s = listeners.LoggingUDPServer(self.udp_addr, self.on_record, 0.5)
        self.udp_server = s
        self.udp_thread = t = threading.Thread(target=s.serve_until_stopped)
        t.setDaemon(True)
        t.start()

        if zmq:
            if options:
                self.zmq_addr = options.zmqhost
            s = listeners.LoggingZMQServer('tcp://%s' % self.zmq_addr,
                                           self.on_record, 0.5)
            self.zmq_server = s
            self.zmq_thread = t = threading.Thread(target=s.serve_until_stopped)
            t.setDaemon(True)
            t.start()

    def setupUi(self, w):
        super(MainWindow, self).setupUi(w)
        self.load_settings()

        if not sys.platform.startswith('darwin'):
            self.setWindowIcon(QtGui.QIcon('logview.ico'))

        connect = self.connect
        SIGNAL = QtCore.SIGNAL
        QHeaderView = QtGui.QHeaderView

        connect(self.action_About, SIGNAL('triggered(bool)'), self.on_help_about)
        split = self.cSplit
        split.setStretchFactor(0, 2)
        split.setStretchFactor(1, 5)
        split = self.mSplit
        split.setStretchFactor(0, 5)
        split.setStretchFactor(1, 3)
        self.records = collections.deque()
        self.tmodel = LoggerModel(self)
        self.tree.setModel(self.tmodel)
        if not self.options:
            capacity = 0
        else:
            capacity = self.options.capacity
        self.lmodel = lmodel = LogRecordModel(self, self.records, self.columns,
                                              capacity)
        if self.background_map:
            lmodel.background_map = self.background_map
        if self.foreground_map:
            lmodel.foreground_map = self.foreground_map
        if self.style_map:
            lmodel.style_map = self.style_map
        self.flmodel = m = FilterModel(self)
        m.setSourceModel(lmodel)
        self.master.setModel(m)
        self.pmodel = PropertySheetModel(self)
        self.detail.setModel(self.pmodel)
        h = self.stretch_last(self.master)
        h.setMovable(True)
        h = self.detail.horizontalHeader()
        h.setResizeMode(1, QHeaderView.Stretch)
        h.setResizeMode(2, QHeaderView.Fixed)
        h.resizeSection(2, 30)
        h.resizeSection(0, 120)
        #self.tbmaster.hide()
        self.tbtree.hide()

        self.connect(self.master.selectionModel(), SIGNAL('selectionChanged(QItemSelection,QItemSelection)'), self.on_master_selection_changed)
        self.mvbar = vbar = self.master.verticalScrollBar()
        connect(vbar, SIGNAL('rangeChanged(int,int)'), self.on_master_range)
        connect(vbar, SIGNAL('sliderMoved(int)'), self.on_master_slide)
        connect(self.lmodel, SIGNAL('modelReset()'), self.on_lmodel_reset)
        connect(self.lmodel, SIGNAL('rowsInserted(QModelIndex,int,int)'), self.on_master_data_change)
        connect(self.tmodel, SIGNAL('rowsInserted(QModelIndex,int,int)'), self.on_tree_rows_inserted)
        connect(self.tree.selectionModel(), SIGNAL('selectionChanged(QItemSelection,QItemSelection)'), self.on_tree_selection_changed)

        connect(self.detail, SIGNAL('clicked(QModelIndex)'), self.on_detail_click)
        connect(self.wantDebug, SIGNAL('stateChanged(int)'), self.on_want_changed)
        connect(self.wantInfo, SIGNAL('stateChanged(int)'), self.on_want_changed)
        connect(self.wantWarning, SIGNAL('stateChanged(int)'), self.on_want_changed)
        connect(self.wantError, SIGNAL('stateChanged(int)'), self.on_want_changed)
        connect(self.wantCritical, SIGNAL('stateChanged(int)'), self.on_want_changed)
        connect(self.wantAll, SIGNAL('stateChanged(int)'), self.on_want_changed)

        connect(self.clearAll, SIGNAL('clicked(bool)'), self.on_clear)
        connect(self.colprefs, SIGNAL('clicked(bool)'), self.on_columns)

        connect(self.match, SIGNAL('textEdited(QString)'), self.on_text_changed)
        connect(self.match, SIGNAL('returnPressed()'), self.on_search)
        connect(self.search, SIGNAL('clicked(bool)'), self.on_search)

        connect(self.cSplit, SIGNAL('doubleClicked(int,int)'), self.on_csplit_dclick)
        connect(self.mSplit, SIGNAL('doubleClicked(int,int)'), self.on_msplit_dclick)

        self.validate()

    def enable_control(self, button, reason):
        button.setToolTip(reason or '')
        button.setEnabled(reason is None)

    @property
    def match_text(self):
        return self.match.text().strip()

    def validate(self):
        reason = None
        if not self.match_text:
            reason = 'Nothing to search for'
        elif not self.records:
            reason = 'Nothing to search in'
        self.enable_control(self.search, reason)
        reason = None
        if not self.records:
            reason = 'Nothing to clear'
        self.enable_control(self.clearAll, reason)

    def show_status_message(self, s):
        self.statusbar.showMessage(s, 2000)

    def load_colors(self, mapping, key):
        settings = self.settings
        settings.beginGroup(key)
        for k in settings.childKeys():
            v = settings.value(k)
            v = [int(i) for i in v.split(',')]
            v = QtGui.QColor(*v)
            k = getattr(logging, k)
            mapping[k] = v
        settings.endGroup()

    def load_strings(self, mapping, key):
        settings = self.settings
        settings.beginGroup(key)
        for k in settings.childKeys():
            v = settings.value(k)
            k = getattr(logging, k)
            mapping[k] = v
        settings.endGroup()

    def load_columns(self, cols, key):
        settings = self.settings
        settings.beginGroup(key)
        ncols = settings.beginReadArray('columns')
        for i in range(ncols):
            settings.setArrayIndex(i)
            info = settings.value('info')
            name, title, vis = info.split(',')
            title = unquote(title)
            vis = bool(vis != '0')
            cols.append(Column(name, title, vis))
        settings.endArray()
        settings.endGroup()

    def load_networks(self):
        settings = self.settings
        settings.beginGroup('network')
        s = settings.value('tcphost', '0.0.0.0')
        self.tcp_addr = get_addr(s, DEFAULT_TCP_LOGGING_PORT)
        s = settings.value('udphost', '0.0.0.0')
        self.udp_addr = get_addr(s, DEFAULT_UDP_LOGGING_PORT)
        if zmq:
            self.zmq_addr = settings.value('zmqhost', 'localhost:9024')
        settings.endGroup()
        
    def load_settings(self):
        settings = self.settings
        settings.beginGroup('mainwindow')
        pos = settings.value('pos')
        size = settings.value('size')
        if pos:
            self.move(pos)
        if size:
            self.resize(size)
        settings.endGroup()
        columns = []
        self.load_columns(columns, 'records')
        if not columns:
            columns = self.DEFAULT_COLUMNS
        self.columns = columns
        self.background_map = d = {}
        self.load_colors(d, 'records/background')
        self.foreground_map = d = {}
        self.load_colors(d, 'records/foreground')
        self.style_map = d = {}
        self.load_strings(d, 'records/style')
        settings.beginGroup('records')
        v = settings.value('stick_to_bottom', '1')
        self.stick_to_bottom = bool(int(v))
        settings.endGroup()
        self.load_networks()

    def save_colors(self, mapping, key):
        settings = self.settings
        settings.beginGroup(key)
        for k in mapping:
            v = ','.join([str(i) for i in mapping[k].getRgb()])
            settings.setValue(logging.getLevelName(k), v)
        settings.endGroup()

    def save_strings(self, mapping, key):
        settings = self.settings
        settings.beginGroup(key)
        for k in mapping:
            settings.setValue(logging.getLevelName(k), mapping[k])
        settings.endGroup()

    def save_columns(self, cols, key):
        settings = self.settings
        settings.beginGroup(key)
        settings.beginWriteArray('columns')
        for i, col in enumerate(cols):
            settings.setArrayIndex(i)
            v = ','.join([col.name, quote(col.title), str(int(col.visible))])
            settings.setValue('info', v)
        settings.endArray()
        settings.endGroup()

    def save_network(self):
        settings = self.settings
        settings.beginGroup('network')
        settings.setValue('tcphost', '%s:%d' % self.tcp_addr)
        settings.setValue('udphost', '%s:%d' % self.udp_addr)
        if zmq:
            settings.setValue('zmqhost', self.zmq_addr)
        settings.endGroup()

    def save_settings(self):
        settings = self.settings
        settings.beginGroup('mainwindow')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
        settings.endGroup()
        self.save_columns(self.columns, 'records')
        self.save_colors(self.lmodel.background_map, 'records/background')
        self.save_colors(self.lmodel.foreground_map, 'records/foreground')
        self.save_strings(self.lmodel.style_map, 'records/style')
        settings.beginGroup('records')
        settings.setValue('stick_to_bottom', int(self.stick_to_bottom))
        settings.endGroup()
        self.save_network()

    def closeEvent(self, event):
        self.tcp_server.stop()
        self.tcp_thread.join()
        self.udp_server.stop()
        self.udp_thread.join()
        if zmq:
            self.zmq_server.stop()
            self.zmq_thread.join()
        self.save_settings()
        event.accept()

    def on_search(self, checked=False):
        model = self.flmodel
        start = model.index(self._sindex, 0, invindex)
        s = self.match_text
        if self.useRegexp.isChecked():
            flags = Qt.MatchRegExp
            if not s.startswith('.*'):
                s = '.*%s' % s
            if not s.endswith('.*'):
                s = '%s.*' % s
        else:
            flags = Qt.MatchContains
        hits = model.match(start, MessageRole, s, 1, Qt.MatchWrap | flags)
        if not hits:
            self.show_status_message("No matches found for '%s'." % self.match_text)
        else:
            result = hits[0]
            self.set_search_start(result)
            self.master.scrollTo(result)
            self.master.setCurrentIndex(result)

    def set_search_start(self, index):
        rc = self.flmodel.rowCount(invindex)
        if rc == 0:
            self._sindex = 0
        else:
            self._sindex = (1 + index.row()) % rc

    def reset_master(self):
        self.master.setCurrentIndex(invindex)
        self._sindex = 0
        self.lmodel.reset()

    def on_text_changed(self, s):
        self.validate()

    def on_help_about(self, checked=False):
        dlg = about.AboutDialog(self)
        dlg.show()

    def process_record(self, record):
        self.lmodel.add_record(record)
        tmodel = self.tmodel
        tmodel.register_logger(record.name)
        self.validate()

    def on_record(self, record):
        self._lock.acquire()
        try:
            self.process_record(record)
        finally:
            self._lock.release()

    def on_master_selection_changed(self, sel, desel):
        self.update_detail()

    def on_master_data_change(self, index, first, last):
        view = self.master
        for i in range(self.lmodel.columnCount(invindex)):
            view.resizeColumnToContents(i)
        self.stretch_last(self.master)

    def stretch_last(self, view):
        h = view.horizontalHeader()
        h.setStretchLastSection(True)
        return h

    def on_lmodel_reset(self):
        self.stretch_last(self.master)
        self.update_detail()
        self.moved_to_bottom = False

    def update_detail(self):
        index = self.master.currentIndex()
        self.set_search_start(index)
        sindex = self.flmodel.mapToSource(index)
        if sindex.isValid():
            record = self.lmodel.get_record(sindex.row())
        else:
            record = None
        self.pmodel.record = record

    def on_tree_selection_changed(self, sel, desel):
        self.reset_master()

    def on_tree_rows_inserted(self, pindex, start, end):
        if self.expand_tree:
            tree = self.tree
            tmodel = self.tmodel
            tree.expand(pindex)
            name = tmodel.data(pindex)
            node = pindex.internalPointer()
            while start <= end:
                index = tmodel.index(start, 0, pindex)
                assert index.isValid()
                tree.expand(index)
                start += 1
            #logger.debug('Expanded: %s (%s)', name, node.path)

    def on_want_changed(self, state):
        sender = self.sender()
        if sender is self.wantAll:
            buttons = (self.wantDebug, self.wantInfo, self.wantWarning,
                       self.wantError, self.wantCritical)
            if state:
                state = Qt.Checked
            else:
                state = Qt.Unchecked
            for button in buttons:
                button.blockSignals(True)
                button.setCheckState(state)
                button.blockSignals(False)
        wanted = set()
        if self.wantDebug.isChecked():
            wanted.add(logging.DEBUG)
        if self.wantInfo.isChecked():
            wanted.add(logging.INFO)
        if self.wantWarning.isChecked():
            wanted.add(logging.WARNING)
        if self.wantError.isChecked():
            wanted.add(logging.ERROR)
        if self.wantCritical.isChecked():
            wanted.add(logging.CRITICAL)
        self.flmodel.wanted = wanted
        self.reset_master()

    def on_clear(self, checked=False):
        QMessageBox = QtGui.QMessageBox
        dlg = QMessageBox(QMessageBox.Question, 'Clear All Records?',
                          'Are you sure you want to clear all %d collected records?' % len(self.records),
                          QMessageBox.Yes | QMessageBox.No)
        dlg.setInformativeText('This action cannot be undone.')
        rc = dlg.exec_()
        if rc == QMessageBox.Yes:
            self._lock.acquire()
            try:
                self.lmodel.clear()
                self.tmodel.clear()
                self.pmodel.reset()
            finally:
                self._lock.release()
                self.validate()

    def on_columns(self, checked=False):
        dlg = colprefs.ColPrefsDialog(self, self.columns)
        rc = dlg.exec_()
        if rc:
            self._lock.acquire()
            try:
                self.columns[:] = dlg.columns
                self.lmodel.reset()
            finally:
                self._lock.release()

    def on_detail_click(self, index):
        model = self.pmodel
        col1 = model.data(model.index(index.row(), 0))
        col2 = model.data(model.index(index.row(), 1))
        if '\n' in col2 and index.column() == 2:
            dlg = textinfo.TextInfoDialog(self, col2)
            dlg.exec_()

    def on_master_range(self, min, max):
        if self.stick_to_bottom and self.moved_to_bottom:
            self.mvbar.setValue(max)

    def on_master_slide(self, pos):
        self.moved_to_bottom = (pos == self.mvbar.maximum())

    def left_collapse(self, splitter):
        sizes = splitter.sizes()
        name = splitter.objectName()
        d = self.split_sizes
        saved_size = d.get(name, 0)
        if sizes[0] == 0 and saved_size > 0:
            sizes[0] = saved_size
            sizes[1] -= sizes[0]
            d[name] = 0
        else:
            d[name] = sizes[0]
            sizes[1] += sizes[0]
            sizes[0] = 0
        splitter.setSizes(sizes)

    def right_collapse(self, splitter):
        sizes = splitter.sizes()
        name = splitter.objectName()
        d = self.split_sizes
        saved_size = d.get(name, 0)
        if sizes[-1] == 0 and saved_size > 0:
            sizes[-1] = saved_size
            sizes[-2] -= sizes[-1]
            d[name] = 0
        else:
            d[name] = sizes[-1]
            sizes[-2] += sizes[-1]
            sizes[-1] = 0
        splitter.setSizes(sizes)

    def on_csplit_dclick(self, index, buttons):
        if buttons & Qt.LeftButton:
            self.left_collapse(self.cSplit)
        else:
            self.right_collapse(self.cSplit)

    def on_msplit_dclick(self, index, buttons):
        if buttons & Qt.LeftButton:
            self.left_collapse(self.mSplit)
        else:
            self.right_collapse(self.mSplit)


def main():
    parser = optparse.OptionParser()
    parser.add_option('-c', '--capacity', default=0, type='int', dest='capacity',
                      help='Maximum number of messages to hold')
    parser.add_option('-t', '--tcp', default='0.0.0.0', dest='tcphost',
                      help='Where to listen for TCP traffic (host[:port])')
    parser.add_option('-u', '--udp', default='0.0.0.0', dest='udphost',
                      help='Where to listen for UDP traffic (host[:port])')
    parser.add_option('-z', '--zmq', default='localhost:9024', dest='zmqhost',
                      help='Where to listen for UDP traffic (host[:port])')

    # On a packaged OS X system, a '-psn' argument is passed which we
    # don't care about
    args = [arg for arg in sys.argv[1:] if not arg.startswith('-psn')]
    options, args = parser.parse_args(args)

    app = QtGui.QApplication(sys.argv)
    QCoreApplication = QtCore.QCoreApplication
    QCoreApplication.setApplicationName('LogView')
    QCoreApplication.setApplicationVersion('0.1')
    QCoreApplication.setOrganizationName('Vinay Sajip')
    QCoreApplication.setOrganizationDomain('www.red-dove.com')

    main = MainWindow(options)
    main.show()
    # On OS X, this call is needed to bring the application window to the
    # front.
    if sys.platform.startswith('darwin'):
        main.raise_()
    app.exec_()

if __name__ == '__main__':
    root = logging.getLogger()
    h = logging.FileHandler('logview.log', 'w')
    root.addHandler(h)
    root.setLevel(logging.DEBUG)
    main()
