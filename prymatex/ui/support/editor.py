# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/editor.ui'
#
# Created: Mon Oct 27 12:36:55 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BundleEditorDialog(object):
    def setupUi(self, BundleEditorDialog):
        BundleEditorDialog.setObjectName("BundleEditorDialog")
        BundleEditorDialog.resize(900, 600)
        BundleEditorDialog.setMinimumSize(QtCore.QSize(900, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/prymatex/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BundleEditorDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(BundleEditorDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(BundleEditorDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.treeLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.treeLayout.setSpacing(2)
        self.treeLayout.setContentsMargins(0, 0, 0, 0)
        self.treeLayout.setObjectName("treeLayout")
        self.comboBoxItemFilter = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBoxItemFilter.setEditable(True)
        self.comboBoxItemFilter.setObjectName("comboBoxItemFilter")
        self.treeLayout.addWidget(self.comboBoxItemFilter)
        self.treeView = QtWidgets.QTreeView(self.verticalLayoutWidget)
        self.treeView.setObjectName("treeView")
        self.treeLayout.addWidget(self.treeView)
        self.toolbarLayout = QtWidgets.QHBoxLayout()
        self.toolbarLayout.setSpacing(2)
        self.toolbarLayout.setObjectName("toolbarLayout")
        self.pushButtonAdd = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.toolbarLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.toolbarLayout.addWidget(self.pushButtonRemove)
        spacerItem = QtWidgets.QSpacerItem(98, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.toolbarLayout.addItem(spacerItem)
        self.pushButtonFilter = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon.fromTheme("view-filter")
        self.pushButtonFilter.setIcon(icon)
        self.pushButtonFilter.setObjectName("pushButtonFilter")
        self.toolbarLayout.addWidget(self.pushButtonFilter)
        self.treeLayout.addLayout(self.toolbarLayout)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.editorsLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.editorsLayout.setContentsMargins(0, 0, 0, 0)
        self.editorsLayout.setObjectName("editorsLayout")
        self.labelTitle = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.labelTitle.setObjectName("labelTitle")
        self.editorsLayout.addWidget(self.labelTitle)
        self.basicFormLayout = QtWidgets.QFormLayout()
        self.basicFormLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.basicFormLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.basicFormLayout.setSpacing(2)
        self.basicFormLayout.setObjectName("basicFormLayout")
        self.labelActivation = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.labelActivation.setObjectName("labelActivation")
        self.basicFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelActivation)
        self.labelScopeSelector = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.labelScopeSelector.setObjectName("labelScopeSelector")
        self.basicFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelScopeSelector)
        self.lineEditScopeSelector = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditScopeSelector.setObjectName("lineEditScopeSelector")
        self.basicFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEditScopeSelector)
        self.labelActivation_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.labelActivation_3.setObjectName("labelActivation_3")
        self.basicFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelActivation_3)
        self.lineEditTabTriggerActivation = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditTabTriggerActivation.setObjectName("lineEditTabTriggerActivation")
        self.basicFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEditTabTriggerActivation)
        self.labelActivation_4 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.labelActivation_4.setObjectName("labelActivation_4")
        self.basicFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelActivation_4)
        self.labelActivation_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.labelActivation_5.setObjectName("labelActivation_5")
        self.basicFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.labelActivation_5)
        self.lineEditSemanticClass = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditSemanticClass.setObjectName("lineEditSemanticClass")
        self.basicFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEditSemanticClass)
        self.lineEditName = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditName.setObjectName("lineEditName")
        self.basicFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditName)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditKeyEquivalentActivation = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditKeyEquivalentActivation.setObjectName("lineEditKeyEquivalentActivation")
        self.horizontalLayout.addWidget(self.lineEditKeyEquivalentActivation)
        self.pushButtonCleanKeyEquivalent = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButtonCleanKeyEquivalent.setMaximumSize(QtCore.QSize(32, 16777215))
        self.pushButtonCleanKeyEquivalent.setText("")
        icon = QtGui.QIcon.fromTheme("edit-clear-locationbar-rtl")
        self.pushButtonCleanKeyEquivalent.setIcon(icon)
        self.pushButtonCleanKeyEquivalent.setFlat(True)
        self.pushButtonCleanKeyEquivalent.setObjectName("pushButtonCleanKeyEquivalent")
        self.horizontalLayout.addWidget(self.pushButtonCleanKeyEquivalent)
        self.basicFormLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.editorsLayout.addLayout(self.basicFormLayout)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(BundleEditorDialog)
        QtCore.QMetaObject.connectSlotsByName(BundleEditorDialog)

    def retranslateUi(self, BundleEditorDialog):
        _translate = QtCore.QCoreApplication.translate
        BundleEditorDialog.setWindowTitle(_translate("BundleEditorDialog", "Bundle Editor"))
        self.pushButtonFilter.setText(_translate("BundleEditorDialog", "Filter"))
        self.labelTitle.setText(_translate("BundleEditorDialog", "No item selected"))
        self.labelActivation.setText(_translate("BundleEditorDialog", "Name:"))
        self.labelScopeSelector.setText(_translate("BundleEditorDialog", "Scope Selector:"))
        self.labelActivation_3.setText(_translate("BundleEditorDialog", "Tab Trigger:"))
        self.labelActivation_4.setText(_translate("BundleEditorDialog", "Key Equivalent:"))
        self.labelActivation_5.setText(_translate("BundleEditorDialog", "Semantic Class:"))

