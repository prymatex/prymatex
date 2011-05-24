# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/settings.ui'
#
# Created: Tue May 24 09:44:31 2011
#      by: PyQt4 UI code generator 4.8.3
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
        PMXSettingsDialog.resize(725, 225)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PMXSettingsDialog.sizePolicy().hasHeightForWidth())
        PMXSettingsDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(PMXSettingsDialog)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(PMXSettingsDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(-1)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelFilter = QtGui.QLabel(self.layoutWidget)
        self.labelFilter.setObjectName(_fromUtf8("labelFilter"))
        self.horizontalLayout.addWidget(self.labelFilter)
        self.lineFilter = QtGui.QLineEdit(self.layoutWidget)
        self.lineFilter.setObjectName(_fromUtf8("lineFilter"))
        self.horizontalLayout.addWidget(self.lineFilter)
        self.pushClearFilter = QtGui.QPushButton(self.layoutWidget)
        self.pushClearFilter.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/edit-delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushClearFilter.setIcon(icon)
        self.pushClearFilter.setObjectName(_fromUtf8("pushClearFilter"))
        self.horizontalLayout.addWidget(self.pushClearFilter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeView = PMXConfigTreeView(self.layoutWidget)
        self.treeView.setMinimumSize(QtCore.QSize(250, 0))
        self.treeView.setLineWidth(0)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)
        self.mainContainer = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainContainer.sizePolicy().hasHeightForWidth())
        self.mainContainer.setSizePolicy(sizePolicy)
        self.mainContainer.setMinimumSize(QtCore.QSize(470, 0))
        self.mainContainer.setObjectName(_fromUtf8("mainContainer"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.mainContainer)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.labelTitle = QtGui.QLabel(self.mainContainer)
        self.labelTitle.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.labelTitle.setFont(font)
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.verticalLayout_3.addWidget(self.labelTitle)
        self.container = QtGui.QWidget(self.mainContainer)
        self.container.setObjectName(_fromUtf8("container"))
        self.verticalLayout_3.addWidget(self.container)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushClose = QtGui.QPushButton(self.mainContainer)
        self.pushClose.setStyleSheet(_fromUtf8("QPushButton {\n"
"padding: 8%;\n"
"}"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/process-stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushClose.setIcon(icon1)
        self.pushClose.setObjectName(_fromUtf8("pushClose"))
        self.horizontalLayout_2.addWidget(self.pushClose)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(PMXSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(PMXSettingsDialog)

    def retranslateUi(self, PMXSettingsDialog):
        PMXSettingsDialog.setWindowTitle(QtGui.QApplication.translate("PMXSettingsDialog", "Prymatex Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFilter.setText(QtGui.QApplication.translate("PMXSettingsDialog", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTitle.setText(QtGui.QApplication.translate("PMXSettingsDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushClose.setText(QtGui.QApplication.translate("PMXSettingsDialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))

from prymatex.gui.config.widgets import PMXConfigTreeView
import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PMXSettingsDialog = QtGui.QDialog()
    ui = Ui_PMXSettingsDialog()
    ui.setupUi(PMXSettingsDialog)
    PMXSettingsDialog.show()
    sys.exit(app.exec_())

