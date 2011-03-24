# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/settings.ui'
#
# Created: Sat Mar 19 09:58:19 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PMXSettingsDialog(object):
    def setupUi(self, PMXSettingsDialog):
        PMXSettingsDialog.setObjectName(_fromUtf8("PMXSettingsDialog"))
        PMXSettingsDialog.resize(680, 401)
        self.verticalLayout_2 = QtGui.QVBoxLayout(PMXSettingsDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(PMXSettingsDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelFilter = QtGui.QLabel(self.widget)
        self.labelFilter.setObjectName(_fromUtf8("labelFilter"))
        self.horizontalLayout.addWidget(self.labelFilter)
        self.lineFilter = QtGui.QLineEdit(self.widget)
        self.lineFilter.setObjectName(_fromUtf8("lineFilter"))
        self.horizontalLayout.addWidget(self.lineFilter)
        self.pushClearFilter = QtGui.QPushButton(self.widget)
        self.pushClearFilter.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/edit-delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushClearFilter.setIcon(icon)
        self.pushClearFilter.setObjectName(_fromUtf8("pushClearFilter"))
        self.horizontalLayout.addWidget(self.pushClearFilter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeView = QtGui.QTreeView(self.widget)
        self.treeView.setMinimumSize(QtCore.QSize(250, 0))
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushExpand = QtGui.QPushButton(self.widget)
        self.pushExpand.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/list-add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushExpand.setIcon(icon1)
        self.pushExpand.setObjectName(_fromUtf8("pushExpand"))
        self.horizontalLayout_2.addWidget(self.pushExpand)
        self.pushShrink = QtGui.QPushButton(self.widget)
        self.pushShrink.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/list-remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushShrink.setIcon(icon2)
        self.pushShrink.setObjectName(_fromUtf8("pushShrink"))
        self.horizontalLayout_2.addWidget(self.pushShrink)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.container = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.container.sizePolicy().hasHeightForWidth())
        self.container.setSizePolicy(sizePolicy)
        self.container.setMinimumSize(QtCore.QSize(470, 0))
        self.container.setObjectName(_fromUtf8("container"))
        self.verticalLayout_2.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(PMXSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(PMXSettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PMXSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PMXSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PMXSettingsDialog)

    def retranslateUi(self, PMXSettingsDialog):
        PMXSettingsDialog.setWindowTitle(QtGui.QApplication.translate("PMXSettingsDialog", "Prymatex Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFilter.setText(QtGui.QApplication.translate("PMXSettingsDialog", "Filter", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PMXSettingsDialog = QtGui.QDialog()
    ui = Ui_PMXSettingsDialog()
    ui.setupUi(PMXSettingsDialog)
    PMXSettingsDialog.show()
    sys.exit(app.exec_())

