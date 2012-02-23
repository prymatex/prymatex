# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dialogs/search.ui'
#
# Created: Thu Feb 23 07:22:40 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SearchDialog(object):
    def setupUi(self, SearchDialog):
        SearchDialog.setObjectName(_fromUtf8("SearchDialog"))
        self.verticalLayout = QtGui.QVBoxLayout(SearchDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(SearchDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBoxContainingText = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxContainingText.sizePolicy().hasHeightForWidth())
        self.comboBoxContainingText.setSizePolicy(sizePolicy)
        self.comboBoxContainingText.setEditable(True)
        self.comboBoxContainingText.setObjectName(_fromUtf8("comboBoxContainingText"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxContainingText)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBoxFilePatterns = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFilePatterns.sizePolicy().hasHeightForWidth())
        self.comboBoxFilePatterns.setSizePolicy(sizePolicy)
        self.comboBoxFilePatterns.setEditable(True)
        self.comboBoxFilePatterns.setObjectName(_fromUtf8("comboBoxFilePatterns"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBoxFilePatterns)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(SearchDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radioButtonWorkspace = QtGui.QRadioButton(self.groupBox_2)
        self.radioButtonWorkspace.setObjectName(_fromUtf8("radioButtonWorkspace"))
        self.verticalLayout_2.addWidget(self.radioButtonWorkspace)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButtonWorkingSet = QtGui.QRadioButton(self.groupBox_2)
        self.radioButtonWorkingSet.setObjectName(_fromUtf8("radioButtonWorkingSet"))
        self.horizontalLayout.addWidget(self.radioButtonWorkingSet)
        self.comboBoxWorkingSet = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxWorkingSet.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxWorkingSet.sizePolicy().hasHeightForWidth())
        self.comboBoxWorkingSet.setSizePolicy(sizePolicy)
        self.comboBoxWorkingSet.setEditable(True)
        self.comboBoxWorkingSet.setObjectName(_fromUtf8("comboBoxWorkingSet"))
        self.horizontalLayout.addWidget(self.comboBoxWorkingSet)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonCreate = QtGui.QPushButton(SearchDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/edit-find.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCreate.setIcon(icon)
        self.buttonCreate.setObjectName(_fromUtf8("buttonCreate"))
        self.horizontalLayout_2.addWidget(self.buttonCreate)
        self.buttonCancel = QtGui.QPushButton(SearchDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/dialog-cancel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCancel.setIcon(icon1)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout_2.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(SearchDialog)
        QtCore.QMetaObject.connectSlotsByName(SearchDialog)

    def retranslateUi(self, SearchDialog):
        SearchDialog.setWindowTitle(_('Search'))
        self.groupBox.setTitle(_('Search'))
        self.label.setText(_('Containing text'))
        self.label_3.setText(_('File name patterns'))
        self.groupBox_2.setTitle(_('Scope'))
        self.radioButtonWorkspace.setText(_('Workspace'))
        self.radioButtonWorkingSet.setText(_('Working set'))
        self.buttonCreate.setText(_('&Search'))
        self.buttonCancel.setText(_('C&ancel'))

from prymatex import resources_rc
