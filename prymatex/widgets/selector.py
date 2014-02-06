#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.delegates.items import HtmlItemDelegate

class SelectorWidget(QtGui.QLineEdit):
    def __init__(self, parent = None):
        QtGui.QLineEdit.__init__(self, parent)
        
        # Completer
        listView = QtGui.QListView()
        listView.setAlternatingRowColors(True)
        listView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        listView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        listView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        listView.setItemDelegate(HtmlItemDelegate(listView))
        #self.completer.setPopup(listView)

    def select(self, model):
        completer = QtGui.QCompleter(model, self)
        self.setCompleter(completer)
        #self.completer().complete()
        print("arranca completer")
