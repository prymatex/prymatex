# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/support/editor.ui'
#
# Created: Thu Sep 18 09:56:55 2014
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

class Ui_BundleEditorDialog(object):
    def setupUi(self, BundleEditorDialog):
        BundleEditorDialog.setObjectName(_fromUtf8("BundleEditorDialog"))
        BundleEditorDialog.resize(900, 600)
        BundleEditorDialog.setMinimumSize(QtCore.QSize(900, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/prymatex/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BundleEditorDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(BundleEditorDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(BundleEditorDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.treeLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.treeLayout.setSpacing(2)
        self.treeLayout.setMargin(0)
        self.treeLayout.setObjectName(_fromUtf8("treeLayout"))
        self.comboBoxItemFilter = QtGui.QComboBox(self.verticalLayoutWidget)
        self.comboBoxItemFilter.setEditable(True)
        self.comboBoxItemFilter.setObjectName(_fromUtf8("comboBoxItemFilter"))
        self.treeLayout.addWidget(self.comboBoxItemFilter)
        self.treeView = QtGui.QTreeView(self.verticalLayoutWidget)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeLayout.addWidget(self.treeView)
        self.toolbarLayout = QtGui.QHBoxLayout()
        self.toolbarLayout.setSpacing(2)
        self.toolbarLayout.setObjectName(_fromUtf8("toolbarLayout"))
        self.pushButtonAdd = QtGui.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.toolbarLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-remove"))
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.toolbarLayout.addWidget(self.pushButtonRemove)
        spacerItem = QtGui.QSpacerItem(98, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.toolbarLayout.addItem(spacerItem)
        self.pushButtonFilter = QtGui.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("view-filter"))
        self.pushButtonFilter.setIcon(icon)
        self.pushButtonFilter.setObjectName(_fromUtf8("pushButtonFilter"))
        self.toolbarLayout.addWidget(self.pushButtonFilter)
        self.treeLayout.addLayout(self.toolbarLayout)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.editorsLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.editorsLayout.setMargin(0)
        self.editorsLayout.setObjectName(_fromUtf8("editorsLayout"))
        self.labelTitle = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.editorsLayout.addWidget(self.labelTitle)
        self.basicFormLayout = QtGui.QFormLayout()
        self.basicFormLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.basicFormLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.basicFormLayout.setSpacing(2)
        self.basicFormLayout.setObjectName(_fromUtf8("basicFormLayout"))
        self.labelActivation = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.labelActivation.setObjectName(_fromUtf8("labelActivation"))
        self.basicFormLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelActivation)
        self.labelScopeSelector = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.labelScopeSelector.setObjectName(_fromUtf8("labelScopeSelector"))
        self.basicFormLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelScopeSelector)
        self.lineEditScopeSelector = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditScopeSelector.setObjectName(_fromUtf8("lineEditScopeSelector"))
        self.basicFormLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditScopeSelector)
        self.labelActivation_3 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.labelActivation_3.setObjectName(_fromUtf8("labelActivation_3"))
        self.basicFormLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelActivation_3)
        self.lineEditTabTriggerActivation = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditTabTriggerActivation.setObjectName(_fromUtf8("lineEditTabTriggerActivation"))
        self.basicFormLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEditTabTriggerActivation)
        self.labelActivation_4 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.labelActivation_4.setObjectName(_fromUtf8("labelActivation_4"))
        self.basicFormLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelActivation_4)
        self.labelActivation_5 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.labelActivation_5.setObjectName(_fromUtf8("labelActivation_5"))
        self.basicFormLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelActivation_5)
        self.lineEditSemanticClass = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditSemanticClass.setObjectName(_fromUtf8("lineEditSemanticClass"))
        self.basicFormLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEditSemanticClass)
        self.lineEditName = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.basicFormLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditName)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEditKeyEquivalentActivation = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditKeyEquivalentActivation.setObjectName(_fromUtf8("lineEditKeyEquivalentActivation"))
        self.horizontalLayout.addWidget(self.lineEditKeyEquivalentActivation)
        self.pushButtonCleanKeyEquivalent = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.pushButtonCleanKeyEquivalent.setMaximumSize(QtCore.QSize(32, 16777215))
        self.pushButtonCleanKeyEquivalent.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("edit-clear-locationbar-rtl"))
        self.pushButtonCleanKeyEquivalent.setIcon(icon)
        self.pushButtonCleanKeyEquivalent.setFlat(True)
        self.pushButtonCleanKeyEquivalent.setObjectName(_fromUtf8("pushButtonCleanKeyEquivalent"))
        self.horizontalLayout.addWidget(self.pushButtonCleanKeyEquivalent)
        self.basicFormLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.editorsLayout.addLayout(self.basicFormLayout)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(BundleEditorDialog)
        QtCore.QMetaObject.connectSlotsByName(BundleEditorDialog)

    def retranslateUi(self, BundleEditorDialog):
        BundleEditorDialog.setWindowTitle(_translate("BundleEditorDialog", "Bundle Editor", None))
        self.pushButtonFilter.setText(_translate("BundleEditorDialog", "Filter", None))
        self.labelTitle.setText(_translate("BundleEditorDialog", "No item selected", None))
        self.labelActivation.setText(_translate("BundleEditorDialog", "Name:", None))
        self.labelScopeSelector.setText(_translate("BundleEditorDialog", "Scope Selector:", None))
        self.labelActivation_3.setText(_translate("BundleEditorDialog", "Tab Trigger:", None))
        self.labelActivation_4.setText(_translate("BundleEditorDialog", "Key Equivalent:", None))
        self.labelActivation_5.setText(_translate("BundleEditorDialog", "Semantic Class:", None))

