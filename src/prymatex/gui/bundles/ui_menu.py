# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/menu.ui'
#
# Created: Mon May 30 14:59:38 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(458, 349)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeView = QtGui.QTreeView(Form)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.horizontalLayout_2.addWidget(self.treeView)
        self.listView = QtGui.QListView(Form)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.horizontalLayout_2.addWidget(self.listView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

