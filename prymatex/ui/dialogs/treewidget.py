# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/dialogs/treewidget.ui'
#
# Created: Tue Jul 30 11:11:59 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TreeWidgetDialog(object):
    def setupUi(self, TreeWidgetDialog):
        TreeWidgetDialog.setObjectName(_fromUtf8("TreeWidgetDialog"))
        TreeWidgetDialog.resize(900, 600)
        TreeWidgetDialog.setMinimumSize(QtCore.QSize(900, 600))
        self.verticalLayout_3 = QtGui.QVBoxLayout(TreeWidgetDialog)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setContentsMargins(6, 6, 3, 3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.splitter = QtGui.QSplitter(TreeWidgetDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.treeLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.treeLayout.setSpacing(2)
        self.treeLayout.setContentsMargins(0, 3, 0, 3)
        self.treeLayout.setObjectName(_fromUtf8("treeLayout"))
        self.lineEditFilter = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEditFilter.setObjectName(_fromUtf8("lineEditFilter"))
        self.treeLayout.addWidget(self.lineEditFilter)
        self.treeView = QtGui.QTreeView(self.verticalLayoutWidget)
        self.treeView.setHeaderHidden(True)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeLayout.addWidget(self.treeView)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.widgetsLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.widgetsLayout.setSpacing(6)
        self.widgetsLayout.setContentsMargins(3, -1, -1, -1)
        self.widgetsLayout.setObjectName(_fromUtf8("widgetsLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textLabelTitle = QtGui.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textLabelTitle.setFont(font)
        self.textLabelTitle.setObjectName(_fromUtf8("textLabelTitle"))
        self.horizontalLayout.addWidget(self.textLabelTitle)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.textLabelPixmap = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.textLabelPixmap.setText(_fromUtf8(""))
        self.textLabelPixmap.setObjectName(_fromUtf8("textLabelPixmap"))
        self.horizontalLayout.addWidget(self.textLabelPixmap)
        self.widgetsLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(self.verticalLayoutWidget_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.widgetsLayout.addWidget(self.line)
        self.verticalLayout_3.addWidget(self.splitter)

        self.retranslateUi(TreeWidgetDialog)
        QtCore.QMetaObject.connectSlotsByName(TreeWidgetDialog)

    def retranslateUi(self, TreeWidgetDialog):
        self.textLabelTitle.setText(QtGui.QApplication.translate("TreeWidgetDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

