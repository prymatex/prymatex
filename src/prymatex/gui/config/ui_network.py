# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/network.ui'
#
# Created: Thu Mar 31 09:45:11 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Network(object):
    def setupUi(self, Network):
        Network.setObjectName("Network")
        Network.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/document-open-remote.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Network.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Network)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboProxyType = QtGui.QComboBox(Network)
        self.comboProxyType.setObjectName("comboProxyType")
        self.comboProxyType.addItem("")
        self.comboProxyType.addItem("")
        self.comboProxyType.addItem("")
        self.comboProxyType.addItem("")
        self.verticalLayout.addWidget(self.comboProxyType)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(Network)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineProxyAddress = QtGui.QLineEdit(Network)
        self.lineProxyAddress.setObjectName("lineProxyAddress")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineProxyAddress)
        self.label_2 = QtGui.QLabel(Network)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineProxyPort = QtGui.QLineEdit(Network)
        self.lineProxyPort.setObjectName("lineProxyPort")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineProxyPort)
        self.label_4 = QtGui.QLabel(Network)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineProxyUsername = QtGui.QLineEdit(Network)
        self.lineProxyUsername.setEnabled(False)
        self.lineProxyUsername.setObjectName("lineProxyUsername")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineProxyUsername)
        self.label_3 = QtGui.QLabel(Network)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineProxyPassword = QtGui.QLineEdit(Network)
        self.lineProxyPassword.setEnabled(False)
        self.lineProxyPassword.setObjectName("lineProxyPassword")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineProxyPassword)
        self.label_5 = QtGui.QLabel(Network)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.checkBox = QtGui.QCheckBox(Network)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBox)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Network)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL("toggled(bool)"), self.lineProxyUsername.setEnabled)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL("toggled(bool)"), self.lineProxyPassword.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Network)

    def retranslateUi(self, Network):
        Network.setWindowTitle(QtGui.QApplication.translate("Network", "Network Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.comboProxyType.setItemText(0, QtGui.QApplication.translate("Network", "No Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.comboProxyType.setItemText(1, QtGui.QApplication.translate("Network", "Based on Enviroment variables", None, QtGui.QApplication.UnicodeUTF8))
        self.comboProxyType.setItemText(2, QtGui.QApplication.translate("Network", "HTTP Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.comboProxyType.setItemText(3, QtGui.QApplication.translate("Network", "Socks Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Network", "Address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Network", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Network", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Network", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Network", "Rrequires authentication", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Network = QtGui.QWidget()
    ui = Ui_Network()
    ui.setupUi(Network)
    Network.show()
    sys.exit(app.exec_())

