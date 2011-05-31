# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/editor.ui'
#
# Created: Tue May 31 14:54:03 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_bundleEditor(object):
    def setupUi(self, bundleEditor):
        bundleEditor.setObjectName(_fromUtf8("bundleEditor"))
        bundleEditor.resize(594, 507)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(bundleEditor)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboBoxItemFilter = QtGui.QComboBox(bundleEditor)
        self.comboBoxItemFilter.setObjectName(_fromUtf8("comboBoxItemFilter"))
        self.verticalLayout.addWidget(self.comboBoxItemFilter)
        self.treeView = QtGui.QTreeView(bundleEditor)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btn_new_bundle = QtGui.QPushButton(bundleEditor)
        self.btn_new_bundle.setObjectName(_fromUtf8("btn_new_bundle"))
        self.horizontalLayout_3.addWidget(self.btn_new_bundle)
        self.btn_del_bundle = QtGui.QPushButton(bundleEditor)
        self.btn_del_bundle.setObjectName(_fromUtf8("btn_del_bundle"))
        self.horizontalLayout_3.addWidget(self.btn_del_bundle)
        spacerItem = QtGui.QSpacerItem(98, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn_filter = QtGui.QPushButton(bundleEditor)
        self.btn_filter.setObjectName(_fromUtf8("btn_filter"))
        self.horizontalLayout_3.addWidget(self.btn_filter)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(bundleEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.widget = QtGui.QWidget(bundleEditor)
        self.widget.setStyleSheet(_fromUtf8("image: url(:/icons/resources/icons/Prymatex_Logo.png);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_3.addWidget(self.widget)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(bundleEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.comboBox_3 = QtGui.QComboBox(bundleEditor)
        self.comboBox_3.setEnabled(False)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.horizontalLayout_4.addWidget(self.comboBox_3)
        self.line_activation = QtGui.QLineEdit(bundleEditor)
        self.line_activation.setEnabled(False)
        self.line_activation.setObjectName(_fromUtf8("line_activation"))
        self.horizontalLayout_4.addWidget(self.line_activation)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_3 = QtGui.QLabel(bundleEditor)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.line_scope = QtGui.QLineEdit(bundleEditor)
        self.line_scope.setEnabled(False)
        self.line_scope.setObjectName(_fromUtf8("line_scope"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.line_scope)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.retranslateUi(bundleEditor)
        QtCore.QMetaObject.connectSlotsByName(bundleEditor)

    def retranslateUi(self, bundleEditor):
        bundleEditor.setWindowTitle(QtGui.QApplication.translate("bundleEditor", "Bundle Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_new_bundle.setText(QtGui.QApplication.translate("bundleEditor", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_del_bundle.setText(QtGui.QApplication.translate("bundleEditor", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_filter.setText(QtGui.QApplication.translate("bundleEditor", "Filter List", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("bundleEditor", "No item selected", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("bundleEditor", "Activation:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.setItemText(0, QtGui.QApplication.translate("bundleEditor", "Key Equivalent", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.setItemText(1, QtGui.QApplication.translate("bundleEditor", "Tab Trigger", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("bundleEditor", "Scope Selector:", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    bundleEditor = QtGui.QWidget()
    ui = Ui_bundleEditor()
    ui.setupUi(bundleEditor)
    bundleEditor.show()
    sys.exit(app.exec_())

