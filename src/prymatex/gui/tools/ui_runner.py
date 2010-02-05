# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/runner.ui'
#
# Created: Fri Feb  5 15:56:11 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PMXRunnerWidget(object):
    def setupUi(self, PMXRunnerWidget):
        PMXRunnerWidget.setObjectName("PMXRunnerWidget")
        PMXRunnerWidget.resize(534, 487)
        PMXRunnerWidget.setStyleSheet("""QTextEdit#textOutput {
  border: 1px solid #CCC;
  /*padding: 4px;*/
  margin: 4px;
  background: rgba(23, 23, 23, 23);
}

QLabel#heading {
    font-weight: bold;
    margin: 10px;
    font-size: 18pt;
}
QComboBox {
    color: red;
}""")
        self.verticalLayout = QtGui.QVBoxLayout(PMXRunnerWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.heading = QtGui.QLabel(PMXRunnerWidget)
        self.heading.setObjectName("heading")
        self.horizontalLayout.addWidget(self.heading)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboBox = QtGui.QComboBox(PMXRunnerWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_2 = QtGui.QPushButton(PMXRunnerWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(PMXRunnerWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textOutput = QtGui.QTextEdit(PMXRunnerWidget)
        self.textOutput.setObjectName("textOutput")
        self.verticalLayout.addWidget(self.textOutput)

        self.retranslateUi(PMXRunnerWidget)
        QtCore.QMetaObject.connectSlotsByName(PMXRunnerWidget)

    def retranslateUi(self, PMXRunnerWidget):
        PMXRunnerWidget.setWindowTitle(QtGui.QApplication.translate("PMXRunnerWidget", "Runner", None, QtGui.QApplication.UnicodeUTF8))
        self.heading.setText(QtGui.QApplication.translate("PMXRunnerWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setToolTip(QtGui.QApplication.translate("PMXRunnerWidget", "Theme", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("PMXRunnerWidget", "Dark", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("PMXRunnerWidget", "Clean", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("PMXRunnerWidget", "Mac", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("PMXRunnerWidget", "Xplode", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(4, QtGui.QApplication.translate("PMXRunnerWidget", "Galactic", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("PMXRunnerWidget", "Copy to Clipboard", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("PMXRunnerWidget", "Paste to...", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PMXRunnerWidget = QtGui.QWidget()
    ui = Ui_PMXRunnerWidget()
    ui.setupUi(PMXRunnerWidget)
    PMXRunnerWidget.show()
    sys.exit(app.exec_())

