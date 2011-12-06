# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/project/newproject.ui'
#
# Created: Tue Dec  6 17:12:48 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NewProject(object):
    def setupUi(self, NewProject):
        NewProject.setObjectName(_fromUtf8("NewProject"))
        NewProject.setWindowModality(QtCore.Qt.WindowModal)
        NewProject.resize(450, 134)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/Prymatex_Logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NewProject.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(NewProject)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(NewProject)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineProjectName = QtGui.QLineEdit(NewProject)
        self.lineProjectName.setObjectName(_fromUtf8("lineProjectName"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineProjectName)
        self.label_2 = QtGui.QLabel(NewProject)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lineLocation = QtGui.QLineEdit(NewProject)
        self.lineLocation.setEnabled(False)
        self.lineLocation.setObjectName(_fromUtf8("lineLocation"))
        self.horizontalLayout_5.addWidget(self.lineLocation)
        self.buttonChoose = QtGui.QPushButton(NewProject)
        self.buttonChoose.setEnabled(False)
        self.buttonChoose.setObjectName(_fromUtf8("buttonChoose"))
        self.horizontalLayout_5.addWidget(self.buttonChoose)
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.checkBoxUseDefaultLocation = QtGui.QCheckBox(NewProject)
        self.checkBoxUseDefaultLocation.setChecked(True)
        self.checkBoxUseDefaultLocation.setObjectName(_fromUtf8("checkBoxUseDefaultLocation"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBoxUseDefaultLocation)
        self.label_3 = QtGui.QLabel(NewProject)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBoxWorkingSet = QtGui.QComboBox(NewProject)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxWorkingSet.sizePolicy().hasHeightForWidth())
        self.comboBoxWorkingSet.setSizePolicy(sizePolicy)
        self.comboBoxWorkingSet.setEditable(True)
        self.comboBoxWorkingSet.setObjectName(_fromUtf8("comboBoxWorkingSet"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBoxWorkingSet)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCreate = QtGui.QPushButton(NewProject)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-development-new-template.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCreate.setIcon(icon1)
        self.buttonCreate.setObjectName(_fromUtf8("buttonCreate"))
        self.horizontalLayout.addWidget(self.buttonCreate)
        self.buttonCancel = QtGui.QPushButton(NewProject)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/dialog-cancel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCancel.setIcon(icon2)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewProject)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), NewProject.reject)
        QtCore.QMetaObject.connectSlotsByName(NewProject)
        NewProject.setTabOrder(self.lineProjectName, self.lineLocation)
        NewProject.setTabOrder(self.lineLocation, self.buttonChoose)
        NewProject.setTabOrder(self.buttonChoose, self.buttonCreate)

    def retranslateUi(self, NewProject):
        NewProject.setWindowTitle(_('New Project'))
        self.label.setText(_('Project Name:'))
        self.label_2.setText(_('Location:'))
        self.buttonChoose.setText(_('Ch&oose'))
        self.checkBoxUseDefaultLocation.setText(_('Use default location'))
        self.label_3.setText(_('Working Set'))
        self.buttonCreate.setText(_('&Create'))
        self.buttonCancel.setText(_('C&ancel'))

from prymatex import resources_rc
