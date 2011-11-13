# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configbundles.ui'
#
# Created: Sun Nov 13 18:07:37 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Bundles(object):
    def setupUi(self, Bundles):
        Bundles.setObjectName(_fromUtf8("Bundles"))
        Bundles.resize(400, 359)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/shapes.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Bundles.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Bundles)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(Bundles)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(Bundles)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.linePath = QtGui.QLineEdit(Bundles)
        self.linePath.setObjectName(_fromUtf8("linePath"))
        self.horizontalLayout_2.addWidget(self.linePath)
        self.pushAddPath = QtGui.QPushButton(Bundles)
        self.pushAddPath.setObjectName(_fromUtf8("pushAddPath"))
        self.horizontalLayout_2.addWidget(self.pushAddPath)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.listWidget = QtGui.QListWidget(Bundles)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushEdit = QtGui.QPushButton(Bundles)
        self.pushEdit.setObjectName(_fromUtf8("pushEdit"))
        self.horizontalLayout.addWidget(self.pushEdit)
        self.pushRemove = QtGui.QPushButton(Bundles)
        self.pushRemove.setObjectName(_fromUtf8("pushRemove"))
        self.horizontalLayout.addWidget(self.pushRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Bundles)
        QtCore.QMetaObject.connectSlotsByName(Bundles)

    def retranslateUi(self, Bundles):
        Bundles.setWindowTitle(_('Bundle Paths'))
        self.label_2.setText(_('Bundle paths'))
        self.label.setText(_('Path'))
        self.linePath.setToolTip(_('Bundles contain syntax definition, commands and snippets,\nyou can add bundles to this directory but make sure you\ninclude the upper level folder containing the .tmBundle\ndirectory.'))
        self.pushAddPath.setText(_('Add path'))
        self.pushEdit.setText(_('Edit'))
        self.pushRemove.setText(_('Remove'))

from prymatex import resources_rc
