#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

class BundleFilterDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.proxy = QtGui.QSortFilterProxyModel(self)
        self.listBundleItems.setModel(self.proxy)
        
    def setModel(self, model):
        self.proxy.setSourceModel(model)

    def setupUi(self, BundleFilter):
        BundleFilter.setObjectName("BundleFilter")
        BundleFilter.resize(330, 400)
        BundleFilter.setMinimumSize(QtCore.QSize(330, 400))
        self.verticalLayout = QtGui.QVBoxLayout(BundleFilter)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listBundleItems = QtGui.QListView(BundleFilter)
        self.listBundleItems.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.listBundleItems.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.listBundleItems.setObjectName("listBundleItems")
        self.verticalLayout.addWidget(self.listBundleItems)
        self.labelHelp = QtGui.QLabel(BundleFilter)
        self.labelHelp.setWordWrap(True)
        self.labelHelp.setObjectName("labelHelp")
        self.verticalLayout.addWidget(self.labelHelp)
        self.retranslateUi(BundleFilter)

    def setHelpVisible(self, visible):
        self.labelHelp.setVisible(visible)

    def retranslateUi(self, BundleFilter):
        BundleFilter.setWindowTitle('Enable/Disable bundles')
        self.labelHelp.setText('You should keep the Source, Text and TextMate bundles enabled, as these provide base functionality relied upon by other bundles.')
