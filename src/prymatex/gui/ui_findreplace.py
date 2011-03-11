# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/findreplace.ui'
#
# Created: Fri Mar 11 16:23:36 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(676, 75)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushReplaceAlll = QtGui.QPushButton(Form)
        self.pushReplaceAlll.setObjectName(_fromUtf8("pushReplaceAlll"))
        self.gridLayout.addWidget(self.pushReplaceAlll, 1, 4, 1, 1)
        self.pushReplaceAndFindNext = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nimbus Mono L"))
        font.setWeight(75)
        font.setBold(True)
        self.pushReplaceAndFindNext.setFont(font)
        self.pushReplaceAndFindNext.setObjectName(_fromUtf8("pushReplaceAndFindNext"))
        self.gridLayout.addWidget(self.pushReplaceAndFindNext, 1, 3, 1, 1)
        self.pushReplaceAndFindPrevious = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nimbus Mono L"))
        font.setWeight(75)
        font.setBold(True)
        self.pushReplaceAndFindPrevious.setFont(font)
        self.pushReplaceAndFindPrevious.setObjectName(_fromUtf8("pushReplaceAndFindPrevious"))
        self.gridLayout.addWidget(self.pushReplaceAndFindPrevious, 1, 2, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.labelReplaceWith = QtGui.QLabel(Form)
        self.labelReplaceWith.setObjectName(_fromUtf8("labelReplaceWith"))
        self.gridLayout.addWidget(self.labelReplaceWith, 1, 0, 1, 1)
        self.pushClose = QtGui.QPushButton(Form)
        self.pushClose.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/process-stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushClose.setIcon(icon)
        self.pushClose.setFlat(True)
        self.pushClose.setObjectName(_fromUtf8("pushClose"))
        self.gridLayout.addWidget(self.pushClose, 0, 6, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 1, 1)
        self.pushOptions = QtGui.QPushButton(Form)
        self.pushOptions.setObjectName(_fromUtf8("pushOptions"))
        self.gridLayout.addWidget(self.pushOptions, 0, 4, 1, 1)
        self.pushReplace = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nimbus Mono L"))
        font.setWeight(75)
        font.setBold(True)
        self.pushReplace.setFont(font)
        self.pushReplace.setObjectName(_fromUtf8("pushReplace"))
        self.gridLayout.addWidget(self.pushReplace, 0, 3, 1, 1)
        self.pushFindPrevious = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nimbus Mono L"))
        font.setWeight(75)
        font.setBold(True)
        self.pushFindPrevious.setFont(font)
        self.pushFindPrevious.setObjectName(_fromUtf8("pushFindPrevious"))
        self.gridLayout.addWidget(self.pushFindPrevious, 0, 2, 1, 1)
        self.lineFind = QtGui.QLineEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineFind.sizePolicy().hasHeightForWidth())
        self.lineFind.setSizePolicy(sizePolicy)
        self.lineFind.setMinimumSize(QtCore.QSize(300, 0))
        self.lineFind.setObjectName(_fromUtf8("lineFind"))
        self.gridLayout.addWidget(self.lineFind, 0, 1, 1, 1)
        self.labelFind = QtGui.QLabel(Form)
        self.labelFind.setObjectName(_fromUtf8("labelFind"))
        self.gridLayout.addWidget(self.labelFind, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushClose, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.hide)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushReplaceAlll.setText(QtGui.QApplication.translate("Form", "Replace All", None, QtGui.QApplication.UnicodeUTF8))
        self.pushReplaceAndFindNext.setText(QtGui.QApplication.translate("Form", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.pushReplaceAndFindPrevious.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Replace &amp; Find Previous</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushReplaceAndFindPrevious.setText(QtGui.QApplication.translate("Form", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.labelReplaceWith.setText(QtGui.QApplication.translate("Form", "Replace with:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushOptions.setText(QtGui.QApplication.translate("Form", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.pushReplace.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Next</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushReplace.setText(QtGui.QApplication.translate("Form", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.pushFindPrevious.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Previous</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushFindPrevious.setText(QtGui.QApplication.translate("Form", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFind.setText(QtGui.QApplication.translate("Form", "FInd:", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

