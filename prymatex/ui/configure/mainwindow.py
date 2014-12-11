# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/configure/mainwindow.ui'
#
# Created: Thu Dec 11 08:36:23 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(838, 266)
        self.verticalLayout = QtWidgets.QVBoxLayout(MainWindow)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(MainWindow)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_3.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setContentsMargins(6, 6, 6, 6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName("formLayout_3")
        self.checkBoxAskAboutModifiedEditors = QtWidgets.QCheckBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setItalic(False)
        self.checkBoxAskAboutModifiedEditors.setFont(font)
        self.checkBoxAskAboutModifiedEditors.setObjectName("checkBoxAskAboutModifiedEditors")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.checkBoxAskAboutModifiedEditors)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(MainWindow)
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_4)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(6, 6, 6, 6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBoxTitleTemplate = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBoxTitleTemplate.setEditable(True)
        self.comboBoxTitleTemplate.setObjectName("comboBoxTitleTemplate")
        self.comboBoxTitleTemplate.addItem("")
        self.comboBoxTitleTemplate.addItem("")
        self.comboBoxTitleTemplate.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxTitleTemplate)
        self.checkBoxShowTabsIfMoreThanOne = QtWidgets.QCheckBox(self.groupBox_4)
        font = QtGui.QFont()
        font.setItalic(False)
        self.checkBoxShowTabsIfMoreThanOne.setFont(font)
        self.checkBoxShowTabsIfMoreThanOne.setObjectName("checkBoxShowTabsIfMoreThanOne")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.checkBoxShowTabsIfMoreThanOne)
        self.verticalLayout.addWidget(self.groupBox_4)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "General"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Behavior"))
        self.checkBoxAskAboutModifiedEditors.setText(_translate("MainWindow", "Ask about modified editors on exit?"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Interface"))
        self.label_3.setText(_translate("MainWindow", "Title:"))
        self.comboBoxTitleTemplate.setItemText(0, _translate("MainWindow", "$TM_DISPLAYNAME - $PMX_APP_NAME"))
        self.comboBoxTitleTemplate.setItemText(1, _translate("MainWindow", "$TM_DISPLAYNAME - $PMX_APP_NAME ($PMX_VERSION)"))
        self.comboBoxTitleTemplate.setItemText(2, _translate("MainWindow", "$TM_DISPLAYNAME${TM_FILEPATH/.+/ ($0)/} - $PMX_APP_NAME ($PMX_VERSION)"))
        self.checkBoxShowTabsIfMoreThanOne.setText(_translate("MainWindow", "Show tabs only if there are more than one"))

