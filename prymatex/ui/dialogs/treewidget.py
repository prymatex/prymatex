# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dialogs/treewidget.ui'
#
# Created: Mon Feb 13 20:59:54 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TreeWidgetDialog(object):
    def setupUi(self, TreeWidgetDialog):
        TreeWidgetDialog.setObjectName(_fromUtf8("TreeWidgetDialog"))
        TreeWidgetDialog.resize(317, 218)
        self.verticalLayout_3 = QtGui.QVBoxLayout(TreeWidgetDialog)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.splitter = QtGui.QSplitter(TreeWidgetDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.treeLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.treeLayout.setSpacing(2)
        self.treeLayout.setMargin(0)
        self.treeLayout.setObjectName(_fromUtf8("treeLayout"))
        self.lineEditFilter = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEditFilter.setObjectName(_fromUtf8("lineEditFilter"))
        self.treeLayout.addWidget(self.lineEditFilter)
        self.treeView = QtGui.QTreeView(self.verticalLayoutWidget)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeLayout.addWidget(self.treeView)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.widgetsLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.widgetsLayout.setSpacing(2)
        self.widgetsLayout.setMargin(0)
        self.widgetsLayout.setObjectName(_fromUtf8("widgetsLayout"))
        self.textLabelTitle = QtGui.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.textLabelTitle.setFont(font)
        self.textLabelTitle.setObjectName(_fromUtf8("textLabelTitle"))
        self.widgetsLayout.addWidget(self.textLabelTitle)
        self.line = QtGui.QFrame(self.verticalLayoutWidget_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.widgetsLayout.addWidget(self.line)
        self.verticalLayout_3.addWidget(self.splitter)

        self.retranslateUi(TreeWidgetDialog)
        QtCore.QMetaObject.connectSlotsByName(TreeWidgetDialog)

    def retranslateUi(self, TreeWidgetDialog):
        TreeWidgetDialog.setWindowTitle(_('Dialog'))
        self.textLabelTitle.setText(_('TextLabel'))

