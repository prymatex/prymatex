# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/browser.ui'
#
# Created: Fri Jan 25 10:19:09 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Browser(object):
    def setupUi(self, Browser):
        Browser.setObjectName(_fromUtf8("Browser"))
        Browser.resize(592, 225)
        self.verticalLayout = QtGui.QVBoxLayout(Browser)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(Browser)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setMargin(6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.checkBoxDeveloperExtras = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxDeveloperExtras.setObjectName(_fromUtf8("checkBoxDeveloperExtras"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBoxDeveloperExtras)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(Browser)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelProxy = QtGui.QLabel(self.groupBox)
        self.labelProxy.setObjectName(_fromUtf8("labelProxy"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelProxy)
        self.lineEditProxy = QtGui.QLineEdit(self.groupBox)
        self.lineEditProxy.setObjectName(_fromUtf8("lineEditProxy"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEditProxy)
        self.radioButtonNoProxy = QtGui.QRadioButton(self.groupBox)
        self.radioButtonNoProxy.setObjectName(_fromUtf8("radioButtonNoProxy"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.radioButtonNoProxy)
        self.radioButtonSystemProxy = QtGui.QRadioButton(self.groupBox)
        self.radioButtonSystemProxy.setObjectName(_fromUtf8("radioButtonSystemProxy"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.radioButtonSystemProxy)
        self.radioButtonManualProxy = QtGui.QRadioButton(self.groupBox)
        self.radioButtonManualProxy.setObjectName(_fromUtf8("radioButtonManualProxy"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.radioButtonManualProxy)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Browser)
        QtCore.QMetaObject.connectSlotsByName(Browser)

    def retranslateUi(self, Browser):
        Browser.setWindowTitle(_('Browser'))
        self.groupBox_2.setTitle(_('Source'))
        self.checkBoxDeveloperExtras.setText(_('Enable developer extras'))
        self.groupBox.setTitle(_('Connection'))
        self.labelProxy.setText(_('Proxy:'))
        self.radioButtonNoProxy.setText(_('No proxy'))
        self.radioButtonSystemProxy.setText(_('Use system proxy settings'))
        self.radioButtonManualProxy.setText(_('Manual proxy configuration'))

