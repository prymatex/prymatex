# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dialogs/search.ui'
#
# Created: Thu Jan 29 12:30:37 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SearchDialog(object):
    def setupUi(self, SearchDialog):
        SearchDialog.setObjectName("SearchDialog")
        SearchDialog.resize(482, 243)
        SearchDialog.setMinimumSize(QtCore.QSize(482, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/prymatex/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SearchDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(SearchDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(SearchDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(6, 6, 6, 6)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBoxContainingText = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxContainingText.sizePolicy().hasHeightForWidth())
        self.comboBoxContainingText.setSizePolicy(sizePolicy)
        self.comboBoxContainingText.setEditable(True)
        self.comboBoxContainingText.setObjectName("comboBoxContainingText")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxContainingText)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBoxFilePatterns = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFilePatterns.sizePolicy().hasHeightForWidth())
        self.comboBoxFilePatterns.setSizePolicy(sizePolicy)
        self.comboBoxFilePatterns.setEditable(True)
        self.comboBoxFilePatterns.setObjectName("comboBoxFilePatterns")
        self.comboBoxFilePatterns.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBoxFilePatterns)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBoxRecursive = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxRecursive.setObjectName("checkBoxRecursive")
        self.horizontalLayout_4.addWidget(self.checkBoxRecursive)
        self.checkBoxHidden = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxHidden.setObjectName("checkBoxHidden")
        self.horizontalLayout_4.addWidget(self.checkBoxHidden)
        self.checkBoxFollowLinks = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxFollowLinks.setObjectName("checkBoxFollowLinks")
        self.horizontalLayout_4.addWidget(self.checkBoxFollowLinks)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(SearchDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButtonWorkspace = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButtonWorkspace.setChecked(True)
        self.radioButtonWorkspace.setObjectName("radioButtonWorkspace")
        self.verticalLayout_2.addWidget(self.radioButtonWorkspace)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButtonWorkingSet = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButtonWorkingSet.setObjectName("radioButtonWorkingSet")
        self.horizontalLayout.addWidget(self.radioButtonWorkingSet)
        self.comboBoxWorkingSet = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBoxWorkingSet.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxWorkingSet.sizePolicy().hasHeightForWidth())
        self.comboBoxWorkingSet.setSizePolicy(sizePolicy)
        self.comboBoxWorkingSet.setEditable(True)
        self.comboBoxWorkingSet.setObjectName("comboBoxWorkingSet")
        self.horizontalLayout.addWidget(self.comboBoxWorkingSet)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_3.addWidget(self.radioButton)
        self.lineLocation = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineLocation.setEnabled(False)
        self.lineLocation.setObjectName("lineLocation")
        self.horizontalLayout_3.addWidget(self.lineLocation)
        self.buttonChoose = QtWidgets.QPushButton(self.groupBox_2)
        self.buttonChoose.setEnabled(False)
        self.buttonChoose.setObjectName("buttonChoose")
        self.horizontalLayout_3.addWidget(self.buttonChoose)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.buttonSearch = QtWidgets.QPushButton(SearchDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/actions/edit-find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonSearch.setIcon(icon1)
        self.buttonSearch.setObjectName("buttonSearch")
        self.horizontalLayout_2.addWidget(self.buttonSearch)
        self.buttonCancel = QtWidgets.QPushButton(SearchDialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/actions/dialog-cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCancel.setIcon(icon2)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout_2.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(SearchDialog)
        QtCore.QMetaObject.connectSlotsByName(SearchDialog)

    def retranslateUi(self, SearchDialog):
        _translate = QtCore.QCoreApplication.translate
        SearchDialog.setWindowTitle(_translate("SearchDialog", "Search"))
        self.groupBox.setTitle(_translate("SearchDialog", "Search"))
        self.label.setText(_translate("SearchDialog", "Containing text"))
        self.label_3.setText(_translate("SearchDialog", "File name patterns"))
        self.comboBoxFilePatterns.setItemText(0, _translate("SearchDialog", "*.*"))
        self.checkBoxRecursive.setText(_translate("SearchDialog", "Recursive"))
        self.checkBoxHidden.setText(_translate("SearchDialog", "Hidden"))
        self.checkBoxFollowLinks.setText(_translate("SearchDialog", "Follow links"))
        self.groupBox_2.setTitle(_translate("SearchDialog", "Scope"))
        self.radioButtonWorkspace.setText(_translate("SearchDialog", "Workspace"))
        self.radioButtonWorkingSet.setText(_translate("SearchDialog", "Working set"))
        self.radioButton.setText(_translate("SearchDialog", "Location"))
        self.buttonChoose.setText(_translate("SearchDialog", "Ch&oose"))
        self.buttonSearch.setText(_translate("SearchDialog", "&Search"))
        self.buttonCancel.setText(_translate("SearchDialog", "C&ancel"))

