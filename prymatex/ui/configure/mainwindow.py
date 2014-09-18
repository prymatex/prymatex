# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/configure/mainwindow.ui'
#
# Created: Thu Sep 18 10:11:59 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(838, 266)
        self.verticalLayout = QtGui.QVBoxLayout(MainWindow)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(MainWindow)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setMargin(6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.checkBoxAskAboutModifiedEditors = QtGui.QCheckBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setItalic(False)
        self.checkBoxAskAboutModifiedEditors.setFont(font)
        self.checkBoxAskAboutModifiedEditors.setObjectName(_fromUtf8("checkBoxAskAboutModifiedEditors"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBoxAskAboutModifiedEditors)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(MainWindow)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_4)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBoxTitleTemplate = QtGui.QComboBox(self.groupBox_4)
        self.comboBoxTitleTemplate.setEditable(True)
        self.comboBoxTitleTemplate.setObjectName(_fromUtf8("comboBoxTitleTemplate"))
        self.comboBoxTitleTemplate.addItem(_fromUtf8(""))
        self.comboBoxTitleTemplate.addItem(_fromUtf8(""))
        self.comboBoxTitleTemplate.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxTitleTemplate)
        self.checkBoxShowTabsIfMoreThanOne = QtGui.QCheckBox(self.groupBox_4)
        font = QtGui.QFont()
        font.setItalic(False)
        self.checkBoxShowTabsIfMoreThanOne.setFont(font)
        self.checkBoxShowTabsIfMoreThanOne.setObjectName(_fromUtf8("checkBoxShowTabsIfMoreThanOne"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.checkBoxShowTabsIfMoreThanOne)
        self.verticalLayout.addWidget(self.groupBox_4)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "General", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Behavior", None))
        self.checkBoxAskAboutModifiedEditors.setText(_translate("MainWindow", "Ask about modified editors on exit?", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Interface", None))
        self.label_3.setText(_translate("MainWindow", "Title:", None))
        self.comboBoxTitleTemplate.setItemText(0, _translate("MainWindow", "$TM_FILENAME${TM_FILENAME/.+/ - /}$PMX_APP_NAME", None))
        self.comboBoxTitleTemplate.setItemText(1, _translate("MainWindow", "$TM_FILENAME${TM_FILENAME/.+/ - /}$PMX_APP_NAME ($PMX_VERSION)", None))
        self.comboBoxTitleTemplate.setItemText(2, _translate("MainWindow", "$TM_FILENAME${TM_FILEPATH/.+/ ($0)/}${TM_FILENAME/.+/ - /}$PMX_APP_NAME ($PMX_VERSION)", None))
        self.checkBoxShowTabsIfMoreThanOne.setText(_translate("MainWindow", "Show tabs only if there are more than one", None))

