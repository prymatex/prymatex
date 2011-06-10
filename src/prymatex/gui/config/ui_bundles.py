# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/bundles.ui'
#
# Created: Fri Jun 10 17:01:31 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

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
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/folder-sync.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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

