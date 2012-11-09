# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/browser.ui'
#
# Created: Fri Nov  9 18:10:45 2012
#      by: PyQt4 UI code generator snapshot-4.9.6-95094339d25b
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BrowserWidget(object):
    def setupUi(self, BrowserWidget):
        BrowserWidget.setObjectName(_fromUtf8("BrowserWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(BrowserWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBoxDeveloperExtras = QtGui.QCheckBox(BrowserWidget)
        self.checkBoxDeveloperExtras.setObjectName(_fromUtf8("checkBoxDeveloperExtras"))
        self.verticalLayout.addWidget(self.checkBoxDeveloperExtras)
        self.groupBox = QtGui.QGroupBox(BrowserWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radioButtonNoProxy = QtGui.QRadioButton(self.groupBox)
        self.radioButtonNoProxy.setObjectName(_fromUtf8("radioButtonNoProxy"))
        self.verticalLayout_2.addWidget(self.radioButtonNoProxy)
        self.radioButtonSystemProxy = QtGui.QRadioButton(self.groupBox)
        self.radioButtonSystemProxy.setObjectName(_fromUtf8("radioButtonSystemProxy"))
        self.verticalLayout_2.addWidget(self.radioButtonSystemProxy)
        self.radioButtonManualProxy = QtGui.QRadioButton(self.groupBox)
        self.radioButtonManualProxy.setObjectName(_fromUtf8("radioButtonManualProxy"))
        self.verticalLayout_2.addWidget(self.radioButtonManualProxy)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelProxy = QtGui.QLabel(self.groupBox)
        self.labelProxy.setObjectName(_fromUtf8("labelProxy"))
        self.horizontalLayout.addWidget(self.labelProxy)
        self.lineEditProxy = QtGui.QLineEdit(self.groupBox)
        self.lineEditProxy.setObjectName(_fromUtf8("lineEditProxy"))
        self.horizontalLayout.addWidget(self.lineEditProxy)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(BrowserWidget)
        QtCore.QMetaObject.connectSlotsByName(BrowserWidget)

    def retranslateUi(self, BrowserWidget):
        BrowserWidget.setWindowTitle(_('Browser'))
        self.checkBoxDeveloperExtras.setText(_('Enable developer extras'))
        self.groupBox.setTitle(_('Connection'))
        self.radioButtonNoProxy.setText(_('No proxy'))
        self.radioButtonSystemProxy.setText(_('Use system proxy settings'))
        self.radioButtonManualProxy.setText(_('Manual proxy configuration:'))
        self.labelProxy.setText(_('Proxy:'))

