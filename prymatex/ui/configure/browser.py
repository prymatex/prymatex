# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/configure/browser.ui'
#
# Created: Tue May 14 21:59:08 2013
#      by: PyQt4 UI code generator snapshot-4.10.2-6f54723ef2ba
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Browser(object):
    def setupUi(self, Browser):
        Browser.setObjectName(_fromUtf8("Browser"))
        Browser.resize(592, 404)
        self.verticalLayout = QtGui.QVBoxLayout(Browser)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(Browser)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setMargin(6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEditHomePage = QtGui.QLineEdit(self.groupBox_3)
        self.lineEditHomePage.setObjectName(_fromUtf8("lineEditHomePage"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEditHomePage)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtGui.QGroupBox(Browser)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setMargin(6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.checkBoxDeveloperExtrasEnabled = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxDeveloperExtrasEnabled.setObjectName(_fromUtf8("checkBoxDeveloperExtrasEnabled"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBoxDeveloperExtrasEnabled)
        self.checkBoxAutoLoadImages = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxAutoLoadImages.setObjectName(_fromUtf8("checkBoxAutoLoadImages"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBoxAutoLoadImages)
        self.checkBoxJavaEnabled = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxJavaEnabled.setObjectName(_fromUtf8("checkBoxJavaEnabled"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.checkBoxJavaEnabled)
        self.checkBoxPrivateBrowsingEnabled = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxPrivateBrowsingEnabled.setObjectName(_fromUtf8("checkBoxPrivateBrowsingEnabled"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.checkBoxPrivateBrowsingEnabled)
        self.checkBoxJavascriptEnabled = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxJavascriptEnabled.setObjectName(_fromUtf8("checkBoxJavascriptEnabled"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.checkBoxJavascriptEnabled)
        self.checkBoxPluginsEnabled = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxPluginsEnabled.setObjectName(_fromUtf8("checkBoxPluginsEnabled"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.FieldRole, self.checkBoxPluginsEnabled)
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
        self.lineEditProxyAddress = QtGui.QLineEdit(self.groupBox)
        self.lineEditProxyAddress.setObjectName(_fromUtf8("lineEditProxyAddress"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEditProxyAddress)
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
        Browser.setWindowTitle(_translate("Browser", "Browser", None))
        self.groupBox_3.setTitle(_translate("Browser", "Behavior", None))
        self.label_3.setText(_translate("Browser", "Home page:", None))
        self.groupBox_2.setTitle(_translate("Browser", "Source", None))
        self.checkBoxDeveloperExtrasEnabled.setText(_translate("Browser", "Developer extras enabled", None))
        self.checkBoxAutoLoadImages.setText(_translate("Browser", "Auto load images", None))
        self.checkBoxJavaEnabled.setText(_translate("Browser", "Java enabled", None))
        self.checkBoxPrivateBrowsingEnabled.setText(_translate("Browser", "Private browsing enabled", None))
        self.checkBoxJavascriptEnabled.setText(_translate("Browser", "Javascript enabled", None))
        self.checkBoxPluginsEnabled.setText(_translate("Browser", "Plugins enabled", None))
        self.groupBox.setTitle(_translate("Browser", "Connection", None))
        self.labelProxy.setText(_translate("Browser", "Proxy address:", None))
        self.radioButtonNoProxy.setText(_translate("Browser", "No proxy", None))
        self.radioButtonSystemProxy.setText(_translate("Browser", "Use system proxy settings", None))
        self.radioButtonManualProxy.setText(_translate("Browser", "Manual proxy configuration", None))

