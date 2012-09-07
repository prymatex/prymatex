# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/support/editor.ui'
#
# Created: Fri Sep  7 14:19:37 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BundleEditor(object):
    def setupUi(self, BundleEditor):
        BundleEditor.setObjectName(_fromUtf8("BundleEditor"))
        BundleEditor.resize(700, 433)
        BundleEditor.setMinimumSize(QtCore.QSize(700, 433))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/prymatex/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BundleEditor.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(BundleEditor)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(BundleEditor)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.treeLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.treeLayout.setSpacing(2)
        self.treeLayout.setMargin(0)
        self.treeLayout.setObjectName(_fromUtf8("treeLayout"))
        self.comboBoxItemFilter = QtGui.QComboBox(self.verticalLayoutWidget)
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
        self.activationLayout = QtGui.QHBoxLayout()
        self.activationLayout.setSpacing(2)
        self.activationLayout.setObjectName(_fromUtf8("activationLayout"))
        self.comboBoxActivation = QtGui.QComboBox(self.verticalLayoutWidget_2)
        self.comboBoxActivation.setObjectName(_fromUtf8("comboBoxActivation"))
        self.activationLayout.addWidget(self.comboBoxActivation)
        self.lineTabTriggerActivation = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.lineTabTriggerActivation.setObjectName(_fromUtf8("lineTabTriggerActivation"))
        self.activationLayout.addWidget(self.lineTabTriggerActivation)
        self.lineKeyEquivalentActivation = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.lineKeyEquivalentActivation.setObjectName(_fromUtf8("lineKeyEquivalentActivation"))
        self.activationLayout.addWidget(self.lineKeyEquivalentActivation)
        self.basicFormLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.activationLayout)
        self.labelScopeSelector = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.labelScopeSelector.setObjectName(_fromUtf8("labelScopeSelector"))
        self.basicFormLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelScopeSelector)
        self.lineEditScope = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEditScope.setObjectName(_fromUtf8("lineEditScope"))
        self.basicFormLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditScope)
        self.editorsLayout.addLayout(self.basicFormLayout)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(BundleEditor)
        QtCore.QMetaObject.connectSlotsByName(BundleEditor)

    def retranslateUi(self, BundleEditor):
        BundleEditor.setWindowTitle(_('Bundle Editor'))
        self.pushButtonFilter.setText(_('Filter'))
        self.labelTitle.setText(_('No item selected'))
        self.labelActivation.setText(_('Activation:'))
        self.labelScopeSelector.setText(_('Scope Selector:'))

