# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/browser.ui'
#
# Created: Thu Dec 11 08:36:22 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Browser(object):
    def setupUi(self, Browser):
        Browser.setObjectName("Browser")
        Browser.resize(592, 404)
        self.verticalLayout = QtWidgets.QVBoxLayout(Browser)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(Browser)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_3.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setContentsMargins(6, 6, 6, 6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEditHomePage = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditHomePage.setObjectName("lineEditHomePage")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditHomePage)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(Browser)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(6, 6, 6, 6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.checkBoxDeveloperExtrasEnabled = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxDeveloperExtrasEnabled.setObjectName("checkBoxDeveloperExtrasEnabled")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.checkBoxDeveloperExtrasEnabled)
        self.checkBoxAutoLoadImages = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxAutoLoadImages.setObjectName("checkBoxAutoLoadImages")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.checkBoxAutoLoadImages)
        self.checkBoxJavaEnabled = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxJavaEnabled.setObjectName("checkBoxJavaEnabled")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.checkBoxJavaEnabled)
        self.checkBoxPrivateBrowsingEnabled = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxPrivateBrowsingEnabled.setObjectName("checkBoxPrivateBrowsingEnabled")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.checkBoxPrivateBrowsingEnabled)
        self.checkBoxJavascriptEnabled = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxJavascriptEnabled.setObjectName("checkBoxJavascriptEnabled")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.checkBoxJavascriptEnabled)
        self.checkBoxPluginsEnabled = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxPluginsEnabled.setObjectName("checkBoxPluginsEnabled")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.checkBoxPluginsEnabled)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(Browser)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(6, 6, 6, 6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName("formLayout")
        self.labelProxy = QtWidgets.QLabel(self.groupBox)
        self.labelProxy.setObjectName("labelProxy")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.labelProxy)
        self.lineEditProxyAddress = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditProxyAddress.setObjectName("lineEditProxyAddress")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEditProxyAddress)
        self.radioButtonNoProxy = QtWidgets.QRadioButton(self.groupBox)
        self.radioButtonNoProxy.setObjectName("radioButtonNoProxy")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.radioButtonNoProxy)
        self.radioButtonSystemProxy = QtWidgets.QRadioButton(self.groupBox)
        self.radioButtonSystemProxy.setObjectName("radioButtonSystemProxy")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.radioButtonSystemProxy)
        self.radioButtonManualProxy = QtWidgets.QRadioButton(self.groupBox)
        self.radioButtonManualProxy.setObjectName("radioButtonManualProxy")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.radioButtonManualProxy)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Browser)
        QtCore.QMetaObject.connectSlotsByName(Browser)

    def retranslateUi(self, Browser):
        _translate = QtCore.QCoreApplication.translate
        Browser.setWindowTitle(_translate("Browser", "Browser"))
        self.groupBox_3.setTitle(_translate("Browser", "Behavior"))
        self.label_3.setText(_translate("Browser", "Home page:"))
        self.groupBox_2.setTitle(_translate("Browser", "Source"))
        self.checkBoxDeveloperExtrasEnabled.setText(_translate("Browser", "Developer extras enabled"))
        self.checkBoxAutoLoadImages.setText(_translate("Browser", "Auto load images"))
        self.checkBoxJavaEnabled.setText(_translate("Browser", "Java enabled"))
        self.checkBoxPrivateBrowsingEnabled.setText(_translate("Browser", "Private browsing enabled"))
        self.checkBoxJavascriptEnabled.setText(_translate("Browser", "Javascript enabled"))
        self.checkBoxPluginsEnabled.setText(_translate("Browser", "Plugins enabled"))
        self.groupBox.setTitle(_translate("Browser", "Connection"))
        self.labelProxy.setText(_translate("Browser", "Proxy address:"))
        self.radioButtonNoProxy.setText(_translate("Browser", "No proxy"))
        self.radioButtonSystemProxy.setText(_translate("Browser", "Use system proxy settings"))
        self.radioButtonManualProxy.setText(_translate("Browser", "Manual proxy configuration"))

