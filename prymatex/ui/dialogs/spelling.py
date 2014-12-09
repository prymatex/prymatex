# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dialogs/spelling.ui'
#
# Created: Tue Dec  9 16:01:53 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SpellingDialog(object):
    def setupUi(self, SpellingDialog):
        SpellingDialog.setObjectName("SpellingDialog")
        SpellingDialog.resize(482, 313)
        SpellingDialog.setMinimumSize(QtCore.QSize(482, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/prymatex/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SpellingDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SpellingDialog)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditNotFound = QtWidgets.QLineEdit(SpellingDialog)
        self.lineEditNotFound.setObjectName("lineEditNotFound")
        self.gridLayout.addWidget(self.lineEditNotFound, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(SpellingDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.pushButtonChange = QtWidgets.QPushButton(SpellingDialog)
        self.pushButtonChange.setObjectName("pushButtonChange")
        self.gridLayout.addWidget(self.pushButtonChange, 0, 1, 1, 1)
        self.pushButtonFindNext = QtWidgets.QPushButton(SpellingDialog)
        self.pushButtonFindNext.setObjectName("pushButtonFindNext")
        self.gridLayout.addWidget(self.pushButtonFindNext, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listWidgetCorrections = QtWidgets.QListWidget(SpellingDialog)
        self.listWidgetCorrections.setObjectName("listWidgetCorrections")
        self.gridLayout_2.addWidget(self.listWidgetCorrections, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButtonIgnore = QtWidgets.QPushButton(SpellingDialog)
        self.pushButtonIgnore.setObjectName("pushButtonIgnore")
        self.verticalLayout.addWidget(self.pushButtonIgnore)
        self.pushButtonLearn = QtWidgets.QPushButton(SpellingDialog)
        self.pushButtonLearn.setObjectName("pushButtonLearn")
        self.verticalLayout.addWidget(self.pushButtonLearn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.comboBoxDictionary = QtWidgets.QComboBox(SpellingDialog)
        self.comboBoxDictionary.setObjectName("comboBoxDictionary")
        self.gridLayout_2.addWidget(self.comboBoxDictionary, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.retranslateUi(SpellingDialog)
        QtCore.QMetaObject.connectSlotsByName(SpellingDialog)

    def retranslateUi(self, SpellingDialog):
        _translate = QtCore.QCoreApplication.translate
        SpellingDialog.setWindowTitle(_translate("SpellingDialog", "Spelling"))
        self.label.setText(_translate("SpellingDialog", "This word was not found in the spelling dictionary."))
        self.pushButtonChange.setText(_translate("SpellingDialog", "Change"))
        self.pushButtonFindNext.setText(_translate("SpellingDialog", "Find Next"))
        self.pushButtonIgnore.setText(_translate("SpellingDialog", "Ignore"))
        self.pushButtonLearn.setText(_translate("SpellingDialog", "Learn"))

