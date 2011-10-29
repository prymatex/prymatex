# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/multiclose.ui'
#
# Created: Fri Oct 28 21:42:07 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SaveMultipleDialog(object):
    def setupUi(self, SaveMultipleDialog):
        SaveMultipleDialog.setObjectName(_fromUtf8("SaveMultipleDialog"))
        SaveMultipleDialog.resize(400, 186)
        SaveMultipleDialog.setWindowTitle(_('Close Multiple Files'))
        self.verticalLayout = QtGui.QVBoxLayout(SaveMultipleDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(SaveMultipleDialog)
        self.label.setText(_('Some files have been altered since they were opened. \nDo you want to save them?'))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tableView = QtGui.QTableView(SaveMultipleDialog)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushDontSave = QtGui.QPushButton(SaveMultipleDialog)
        self.pushDontSave.setText(_('Do &not save'))
        self.pushDontSave.setObjectName(_fromUtf8("pushDontSave"))
        self.horizontalLayout.addWidget(self.pushDontSave)
        self.pushSaveSelected = QtGui.QPushButton(SaveMultipleDialog)
        self.pushSaveSelected.setText(_('Save &Selected'))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-save-all.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushSaveSelected.setIcon(icon)
        self.pushSaveSelected.setObjectName(_fromUtf8("pushSaveSelected"))
        self.horizontalLayout.addWidget(self.pushSaveSelected)
        self.pushCancel = QtGui.QPushButton(SaveMultipleDialog)
        self.pushCancel.setText(_('&Cancel'))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/dialog-cancel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCancel.setIcon(icon1)
        self.pushCancel.setObjectName(_fromUtf8("pushCancel"))
        self.horizontalLayout.addWidget(self.pushCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SaveMultipleDialog)
        QtCore.QObject.connect(self.pushCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), SaveMultipleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SaveMultipleDialog)

    def retranslateUi(self, SaveMultipleDialog):
        pass

from prymatex import resources_rc
