#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

class BundleFilterDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(BundleFilterDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.proxy = QtCore.QSortFilterProxyModel(self)
        self.listBundleItems.setModel(self.proxy)
        
    def setModel(self, model):
        self.proxy.setSourceModel(model)

    def setupUi(self, BundleFilter):
        BundleFilter.setObjectName("BundleFilter")
        BundleFilter.resize(330, 400)
        BundleFilter.setMinimumSize(QtCore.QSize(330, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(BundleFilter)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(6,6,6,6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listBundleItems = QtWidgets.QListView(BundleFilter)
        self.listBundleItems.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listBundleItems.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listBundleItems.setObjectName("listBundleItems")
        self.verticalLayout.addWidget(self.listBundleItems)
        self.labelHelp = QtWidgets.QLabel(BundleFilter)
        self.labelHelp.setWordWrap(True)
        self.labelHelp.setObjectName("labelHelp")
        self.verticalLayout.addWidget(self.labelHelp)
        self.retranslateUi(BundleFilter)

    def setHelpVisible(self, visible):
        self.labelHelp.setVisible(visible)

    def retranslateUi(self, BundleFilter):
        BundleFilter.setWindowTitle('Enable/Disable bundles')
        self.labelHelp.setText('You should keep the Source, Text and TextMate bundles enabled, as these provide base functionality relied upon by other bundles.')
