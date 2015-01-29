# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dialogs/treewidget.ui'
#
# Created: Thu Jan 29 12:30:37 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TreeWidgetDialog(object):
    def setupUi(self, TreeWidgetDialog):
        TreeWidgetDialog.setObjectName("TreeWidgetDialog")
        TreeWidgetDialog.resize(900, 600)
        TreeWidgetDialog.setMinimumSize(QtCore.QSize(900, 600))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(TreeWidgetDialog)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setContentsMargins(6, 6, 3, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtWidgets.QSplitter(TreeWidgetDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.treeLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.treeLayout.setSpacing(2)
        self.treeLayout.setContentsMargins(0, 3, 0, 3)
        self.treeLayout.setObjectName("treeLayout")
        self.lineEditFilter = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.treeLayout.addWidget(self.lineEditFilter)
        self.treeView = QtWidgets.QTreeView(self.verticalLayoutWidget)
        self.treeView.setHeaderHidden(True)
        self.treeView.setObjectName("treeView")
        self.treeLayout.addWidget(self.treeView)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.widgetsLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.widgetsLayout.setSpacing(6)
        self.widgetsLayout.setContentsMargins(3, -1, -1, -1)
        self.widgetsLayout.setObjectName("widgetsLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textLabelTitle = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textLabelTitle.setFont(font)
        self.textLabelTitle.setObjectName("textLabelTitle")
        self.horizontalLayout.addWidget(self.textLabelTitle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.textLabelPixmap = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.textLabelPixmap.setText("")
        self.textLabelPixmap.setObjectName("textLabelPixmap")
        self.horizontalLayout.addWidget(self.textLabelPixmap)
        self.widgetsLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.widgetsLayout.addWidget(self.line)
        self.verticalLayout_3.addWidget(self.splitter)

        self.retranslateUi(TreeWidgetDialog)
        QtCore.QMetaObject.connectSlotsByName(TreeWidgetDialog)

    def retranslateUi(self, TreeWidgetDialog):
        _translate = QtCore.QCoreApplication.translate
        self.textLabelTitle.setText(_translate("TreeWidgetDialog", "TextLabel"))

