# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prymatex\resources\ui\multiclose.ui'
#
# Created: Fri Jul 01 12:35:46 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.translation import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SaveMultipleDialog(object):
    def setupUi(self, SaveMultipleDialog):
        SaveMultipleDialog.setObjectName(_fromUtf8("SaveMultipleDialog"))
        SaveMultipleDialog.resize(400, 186)
        self.verticalLayout = QtGui.QVBoxLayout(SaveMultipleDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(SaveMultipleDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tableView = QtGui.QTableView(SaveMultipleDialog)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushSaveSelected = QtGui.QPushButton(SaveMultipleDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/document-save-all.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushSaveSelected.setIcon(icon)
        self.pushSaveSelected.setObjectName(_fromUtf8("pushSaveSelected"))
        self.horizontalLayout.addWidget(self.pushSaveSelected)
        self.pushDontSave = QtGui.QPushButton(SaveMultipleDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/edit-delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushDontSave.setIcon(icon1)
        self.pushDontSave.setObjectName(_fromUtf8("pushDontSave"))
        self.horizontalLayout.addWidget(self.pushDontSave)
        self.pushCancel = QtGui.QPushButton(SaveMultipleDialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/process-stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCancel.setIcon(icon2)
        self.pushCancel.setObjectName(_fromUtf8("pushCancel"))
        self.horizontalLayout.addWidget(self.pushCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SaveMultipleDialog)
        QtCore.QObject.connect(self.pushCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), SaveMultipleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SaveMultipleDialog)

    def retranslateUi(self, SaveMultipleDialog):
        SaveMultipleDialog.setWindowTitle(_('Close Multiple Files'))
        self.label.setText(_('Some files have been altered since they were opened. \nDo you want to save them?'))
        self.pushSaveSelected.setText(_('Save &Selected'))
        self.pushDontSave.setText(_('Do &not save'))
        self.pushCancel.setText(_('&Cancel'))

from prymatex import res_rc
