# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/general.ui'
#
# Created: Sun May 22 16:02:57 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_General(object):
    def setupUi(self, General):
        General.setObjectName(_fromUtf8("General"))
        General.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/Prymatex_Logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        General.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(General)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox = QtGui.QCheckBox(General)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtGui.QCheckBox(General)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.verticalLayout.addWidget(self.checkBox_2)
        self.groupBox = QtGui.QGroupBox(General)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.comboTabVisibility = QtGui.QComboBox(self.groupBox)
        self.comboTabVisibility.setObjectName(_fromUtf8("comboTabVisibility"))
        self.gridLayout.addWidget(self.comboTabVisibility, 3, 1, 1, 3)
        self.labelTabVisibility = QtGui.QLabel(self.groupBox)
        self.labelTabVisibility.setObjectName(_fromUtf8("labelTabVisibility"))
        self.gridLayout.addWidget(self.labelTabVisibility, 3, 0, 1, 1)
        self.pushInsertAppName = QtGui.QPushButton(self.groupBox)
        self.pushInsertAppName.setObjectName(_fromUtf8("pushInsertAppName"))
        self.gridLayout.addWidget(self.pushInsertAppName, 2, 1, 1, 1)
        self.pushInsertProject = QtGui.QPushButton(self.groupBox)
        self.pushInsertProject.setObjectName(_fromUtf8("pushInsertProject"))
        self.gridLayout.addWidget(self.pushInsertProject, 2, 2, 1, 1)
        self.pushInsertFile = QtGui.QPushButton(self.groupBox)
        self.pushInsertFile.setObjectName(_fromUtf8("pushInsertFile"))
        self.gridLayout.addWidget(self.pushInsertFile, 2, 3, 1, 1)
        self.comboApplicationTitle = QtGui.QComboBox(self.groupBox)
        self.comboApplicationTitle.setEditable(True)
        self.comboApplicationTitle.setObjectName(_fromUtf8("comboApplicationTitle"))
        self.gridLayout.addWidget(self.comboApplicationTitle, 1, 1, 1, 3)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(General)
        QtCore.QMetaObject.connectSlotsByName(General)

    def retranslateUi(self, General):
        General.setWindowTitle(QtGui.QApplication.translate("General", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("General", "Highlight curent line", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("General", "Show right margin indicator", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("General", "Window Title", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("General", "Title template", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTabVisibility.setText(QtGui.QApplication.translate("General", "Tab visibilty", None, QtGui.QApplication.UnicodeUTF8))
        self.pushInsertAppName.setText(QtGui.QApplication.translate("General", "Application Name", None, QtGui.QApplication.UnicodeUTF8))
        self.pushInsertProject.setText(QtGui.QApplication.translate("General", "Project Name", None, QtGui.QApplication.UnicodeUTF8))
        self.pushInsertFile.setText(QtGui.QApplication.translate("General", "File Name", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    General = QtGui.QWidget()
    ui = Ui_General()
    ui.setupUi(General)
    General.show()
    sys.exit(app.exec_())

