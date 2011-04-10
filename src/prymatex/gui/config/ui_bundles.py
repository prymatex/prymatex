# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/bundles.ui'
#
# Created: Sat Apr  9 13:42:44 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Bundles(object):
    def setupUi(self, Bundles):
        Bundles.setObjectName("Bundles")
        Bundles.resize(400, 359)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/folder-sync.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Bundles.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Bundles)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtGui.QLabel(Bundles)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(Bundles)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.linePath = QtGui.QLineEdit(Bundles)
        self.linePath.setObjectName("linePath")
        self.horizontalLayout_2.addWidget(self.linePath)
        self.pushAddPath = QtGui.QPushButton(Bundles)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/resources/actions/list-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushAddPath.setIcon(icon1)
        self.pushAddPath.setObjectName("pushAddPath")
        self.horizontalLayout_2.addWidget(self.pushAddPath)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.listWidget = QtGui.QListWidget(Bundles)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushEdit = QtGui.QPushButton(Bundles)
        self.pushEdit.setObjectName("pushEdit")
        self.horizontalLayout.addWidget(self.pushEdit)
        self.pushRemove = QtGui.QPushButton(Bundles)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/actions/resources/actions/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushRemove.setIcon(icon2)
        self.pushRemove.setObjectName("pushRemove")
        self.horizontalLayout.addWidget(self.pushRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Bundles)
        QtCore.QMetaObject.connectSlotsByName(Bundles)

    def retranslateUi(self, Bundles):
        Bundles.setWindowTitle(QtGui.QApplication.translate("Bundles", "Bundle Paths", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Bundles", "Bundle paths", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Bundles", "Path", None, QtGui.QApplication.UnicodeUTF8))
        self.linePath.setToolTip(QtGui.QApplication.translate("Bundles", "Bundles contain syntax definition, commands and snippets,\n"
"you can add bundles to this directory but make sure you\n"
"include the upper level folder containing the .tmBundle\n"
"directory.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushAddPath.setText(QtGui.QApplication.translate("Bundles", "Add path", None, QtGui.QApplication.UnicodeUTF8))
        self.pushEdit.setText(QtGui.QApplication.translate("Bundles", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushRemove.setText(QtGui.QApplication.translate("Bundles", "Remove", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Bundles = QtGui.QWidget()
    ui = Ui_Bundles()
    ui.setupUi(Bundles)
    Bundles.show()
    sys.exit(app.exec_())

