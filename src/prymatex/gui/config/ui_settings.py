# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/settings.ui'
#
# Created: Mon Mar 28 14:21:46 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PMXSettingsDialog(object):
    def setupUi(self, PMXSettingsDialog):
        PMXSettingsDialog.setObjectName("PMXSettingsDialog")
        PMXSettingsDialog.resize(733, 401)
        self.verticalLayout_2 = QtGui.QVBoxLayout(PMXSettingsDialog)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtGui.QSplitter(PMXSettingsDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(-1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelFilter = QtGui.QLabel(self.layoutWidget)
        self.labelFilter.setObjectName("labelFilter")
        self.horizontalLayout.addWidget(self.labelFilter)
        self.lineFilter = QtGui.QLineEdit(self.layoutWidget)
        self.lineFilter.setObjectName("lineFilter")
        self.horizontalLayout.addWidget(self.lineFilter)
        self.pushClearFilter = QtGui.QPushButton(self.layoutWidget)
        self.pushClearFilter.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushClearFilter.setIcon(icon)
        self.pushClearFilter.setObjectName("pushClearFilter")
        self.horizontalLayout.addWidget(self.pushClearFilter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeView = PMXConfigTreeView(self.layoutWidget)
        self.treeView.setMinimumSize(QtCore.QSize(250, 0))
        self.treeView.setLineWidth(0)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.mainContainer = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainContainer.sizePolicy().hasHeightForWidth())
        self.mainContainer.setSizePolicy(sizePolicy)
        self.mainContainer.setMinimumSize(QtCore.QSize(470, 0))
        self.mainContainer.setObjectName("mainContainer")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.mainContainer)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelTitle = QtGui.QLabel(self.mainContainer)
        self.labelTitle.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.labelTitle.setFont(font)
        self.labelTitle.setObjectName("labelTitle")
        self.verticalLayout_3.addWidget(self.labelTitle)
        self.container = QtGui.QWidget(self.mainContainer)
        self.container.setObjectName("container")
        self.verticalLayout_3.addWidget(self.container)
        self.verticalLayout_2.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(PMXSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(PMXSettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), PMXSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), PMXSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PMXSettingsDialog)

    def retranslateUi(self, PMXSettingsDialog):
        PMXSettingsDialog.setWindowTitle(QtGui.QApplication.translate("PMXSettingsDialog", "Prymatex Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFilter.setText(QtGui.QApplication.translate("PMXSettingsDialog", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTitle.setText(QtGui.QApplication.translate("PMXSettingsDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

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

