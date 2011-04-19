# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/bundle_editor.ui'
#
# Created: Tue Apr 19 09:01:10 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BundleEditor(object):
    def setupUi(self, BundleEditor):
        BundleEditor.setObjectName(_fromUtf8("BundleEditor"))
        BundleEditor.setWindowModality(QtCore.Qt.WindowModal)
        BundleEditor.resize(758, 542)
        self.centralwidget = QtGui.QWidget(BundleEditor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.select_top = QtGui.QComboBox(self.centralwidget)
        self.select_top.setObjectName(_fromUtf8("select_top"))
        self.select_top.addItem(_fromUtf8(""))
        self.select_top.addItem(_fromUtf8(""))
        self.gridLayout_3.addWidget(self.select_top, 0, 0, 2, 2)
        self.treeView = QtGui.QTreeView(self.centralwidget)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.gridLayout_3.addWidget(self.treeView, 2, 0, 1, 2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btn_new_bundle = QtGui.QPushButton(self.centralwidget)
        self.btn_new_bundle.setObjectName(_fromUtf8("btn_new_bundle"))
        self.gridLayout_2.addWidget(self.btn_new_bundle, 0, 0, 1, 1)
        self.btn_del_bundle = QtGui.QPushButton(self.centralwidget)
        self.btn_del_bundle.setObjectName(_fromUtf8("btn_del_bundle"))
        self.gridLayout_2.addWidget(self.btn_del_bundle, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(98, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.btn_filter = QtGui.QPushButton(self.centralwidget)
        self.btn_filter.setObjectName(_fromUtf8("btn_filter"))
        self.gridLayout_2.addWidget(self.btn_filter, 0, 3, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 0, 1, 2)
        self.horizontalLayout_2.addLayout(self.gridLayout_3)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem2 = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem2)
        self.label_subtitle = QtGui.QLabel(self.centralwidget)
        self.label_subtitle.setEnabled(False)
        self.label_subtitle.setObjectName(_fromUtf8("label_subtitle"))
        self.verticalLayout.addWidget(self.label_subtitle)
        spacerItem3 = QtGui.QSpacerItem(0, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem3)
        self.editor_bundle = QtGui.QTextEdit(self.centralwidget)
        self.editor_bundle.setObjectName(_fromUtf8("editor_bundle"))
        self.verticalLayout.addWidget(self.editor_bundle)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.comboBox_3 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_3.setEnabled(False)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_3, 0, 1, 1, 2)
        self.line_activation = QtGui.QLineEdit(self.centralwidget)
        self.line_activation.setEnabled(False)
        self.line_activation.setObjectName(_fromUtf8("line_activation"))
        self.gridLayout.addWidget(self.line_activation, 0, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 2)
        self.line_scope = QtGui.QLineEdit(self.centralwidget)
        self.line_scope.setEnabled(False)
        self.line_scope.setObjectName(_fromUtf8("line_scope"))
        self.gridLayout.addWidget(self.line_scope, 1, 2, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.btn_apply = QtGui.QPushButton(self.centralwidget)
        self.btn_apply.setObjectName(_fromUtf8("btn_apply"))
        self.horizontalLayout.addWidget(self.btn_apply)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        BundleEditor.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(BundleEditor)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        BundleEditor.setStatusBar(self.statusbar)

        self.retranslateUi(BundleEditor)
        QtCore.QMetaObject.connectSlotsByName(BundleEditor)

    def retranslateUi(self, BundleEditor):
        BundleEditor.setWindowTitle(QtGui.QApplication.translate("BundleEditor", "Bundle Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.select_top.setItemText(0, QtGui.QApplication.translate("BundleEditor", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.select_top.setItemText(1, QtGui.QApplication.translate("BundleEditor", "Hide All", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_new_bundle.setText(QtGui.QApplication.translate("BundleEditor", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_del_bundle.setText(QtGui.QApplication.translate("BundleEditor", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_filter.setText(QtGui.QApplication.translate("BundleEditor", "Filter List", None, QtGui.QApplication.UnicodeUTF8))
        self.label_subtitle.setText(QtGui.QApplication.translate("BundleEditor", "No item selected", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("BundleEditor", "Activation:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.setItemText(0, QtGui.QApplication.translate("BundleEditor", "key Equivalent", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("BundleEditor", "Scope Selector:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_apply.setText(QtGui.QApplication.translate("BundleEditor", "Apply", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BundleEditor = QtGui.QMainWindow()
    ui = Ui_BundleEditor()
    ui.setupUi(BundleEditor)
    BundleEditor.show()
    sys.exit(app.exec_())

