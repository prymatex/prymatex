# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/editorwidget.ui'
#
# Created: Thu Jan  6 09:44:54 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_EditorWidget(object):
    def setupUi(self, EditorWidget):
        EditorWidget.setObjectName("EditorWidget")
        EditorWidget.resize(715, 482)
        self.verticalLayout = QtGui.QVBoxLayout(EditorWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.codeEdit = PMXCodeEdit(EditorWidget)
        self.codeEdit.setObjectName("codeEdit")
        self.verticalLayout.addWidget(self.codeEdit)
        self.widget = QtGui.QWidget(EditorWidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtGui.QSpinBox(self.widget)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.pushButton = QtGui.QPushButton(self.widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/go-next-view.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setAutoDefault(True)
        self.pushButton.setDefault(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtGui.QSpacerItem(154, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushCloseFindreplace_2 = QtGui.QPushButton(self.widget)
        self.pushCloseFindreplace_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/resources/actions/process-stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCloseFindreplace_2.setIcon(icon1)
        self.pushCloseFindreplace_2.setFlat(True)
        self.pushCloseFindreplace_2.setObjectName("pushCloseFindreplace_2")
        self.horizontalLayout.addWidget(self.pushCloseFindreplace_2)
        self.verticalLayout.addWidget(self.widget)
        self.findreplaceWidget = QtGui.QWidget(EditorWidget)
        self.findreplaceWidget.setObjectName("findreplaceWidget")
        self.gridLayout = QtGui.QGridLayout(self.findreplaceWidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelFind = QtGui.QLabel(self.findreplaceWidget)
        self.labelFind.setObjectName("labelFind")
        self.gridLayout.addWidget(self.labelFind, 0, 0, 1, 1)
        self.pushFindPrevious = QtGui.QPushButton(self.findreplaceWidget)
        font = QtGui.QFont()
        font.setFamily("Nimbus Mono L")
        font.setWeight(75)
        font.setBold(True)
        self.pushFindPrevious.setFont(font)
        self.pushFindPrevious.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/actions/resources/actions/go-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushFindPrevious.setIcon(icon2)
        self.pushFindPrevious.setObjectName("pushFindPrevious")
        self.gridLayout.addWidget(self.pushFindPrevious, 0, 3, 1, 1)
        self.pushReplace = QtGui.QPushButton(self.findreplaceWidget)
        font = QtGui.QFont()
        font.setFamily("Nimbus Mono L")
        font.setWeight(75)
        font.setBold(True)
        self.pushReplace.setFont(font)
        self.pushReplace.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/actions/resources/actions/go-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushReplace.setIcon(icon3)
        self.pushReplace.setAutoDefault(True)
        self.pushReplace.setObjectName("pushReplace")
        self.gridLayout.addWidget(self.pushReplace, 0, 4, 1, 1)
        self.pushOptions = QtGui.QPushButton(self.findreplaceWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/actions/resources/actions/configure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushOptions.setIcon(icon4)
        self.pushOptions.setObjectName("pushOptions")
        self.gridLayout.addWidget(self.pushOptions, 0, 5, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 6, 1, 1)
        self.pushCloseFindreplace = QtGui.QPushButton(self.findreplaceWidget)
        self.pushCloseFindreplace.setText("")
        self.pushCloseFindreplace.setIcon(icon1)
        self.pushCloseFindreplace.setFlat(True)
        self.pushCloseFindreplace.setObjectName("pushCloseFindreplace")
        self.gridLayout.addWidget(self.pushCloseFindreplace, 0, 7, 1, 1)
        self.labelReplaceWith = QtGui.QLabel(self.findreplaceWidget)
        self.labelReplaceWith.setObjectName("labelReplaceWith")
        self.gridLayout.addWidget(self.labelReplaceWith, 1, 0, 1, 1)
        self.pushReplaceAndFindPrevious = QtGui.QPushButton(self.findreplaceWidget)
        font = QtGui.QFont()
        font.setFamily("Nimbus Mono L")
        font.setWeight(75)
        font.setBold(True)
        self.pushReplaceAndFindPrevious.setFont(font)
        self.pushReplaceAndFindPrevious.setText("")
        self.pushReplaceAndFindPrevious.setIcon(icon2)
        self.pushReplaceAndFindPrevious.setObjectName("pushReplaceAndFindPrevious")
        self.gridLayout.addWidget(self.pushReplaceAndFindPrevious, 1, 3, 1, 1)
        self.pushReplaceAndFindNext = QtGui.QPushButton(self.findreplaceWidget)
        font = QtGui.QFont()
        font.setFamily("Nimbus Mono L")
        font.setWeight(75)
        font.setBold(True)
        self.pushReplaceAndFindNext.setFont(font)
        self.pushReplaceAndFindNext.setText("")
        self.pushReplaceAndFindNext.setIcon(icon3)
        self.pushReplaceAndFindNext.setObjectName("pushReplaceAndFindNext")
        self.gridLayout.addWidget(self.pushReplaceAndFindNext, 1, 4, 1, 1)
        self.pushReplaceAll = QtGui.QPushButton(self.findreplaceWidget)
        self.pushReplaceAll.setFlat(True)
        self.pushReplaceAll.setObjectName("pushReplaceAll")
        self.gridLayout.addWidget(self.pushReplaceAll, 1, 5, 1, 1)
        self.comboFind = PMXFindBox(self.findreplaceWidget)
        self.comboFind.setMinimumSize(QtCore.QSize(300, 0))
        self.comboFind.setEditable(True)
        self.comboFind.setObjectName("comboFind")
        self.gridLayout.addWidget(self.comboFind, 0, 2, 1, 1)
        self.comboReplace = PMXReplaceBox(self.findreplaceWidget)
        self.comboReplace.setEditable(True)
        self.comboReplace.setObjectName("comboReplace")
        self.gridLayout.addWidget(self.comboReplace, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.findreplaceWidget)

        self.retranslateUi(EditorWidget)
        QtCore.QObject.connect(self.pushCloseFindreplace_2, QtCore.SIGNAL("pressed()"), self.widget.hide)
        QtCore.QMetaObject.connectSlotsByName(EditorWidget)

    def retranslateUi(self, EditorWidget):
        EditorWidget.setWindowTitle(QtGui.QApplication.translate("EditorWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("EditorWidget", "Go to line:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("EditorWidget", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFind.setText(QtGui.QApplication.translate("EditorWidget", "Find:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushFindPrevious.setToolTip(QtGui.QApplication.translate("EditorWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Previous</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushReplace.setToolTip(QtGui.QApplication.translate("EditorWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Find Next</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushOptions.setText(QtGui.QApplication.translate("EditorWidget", "&Options", None, QtGui.QApplication.UnicodeUTF8))
        self.labelReplaceWith.setText(QtGui.QApplication.translate("EditorWidget", "Replace with:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushReplaceAndFindPrevious.setToolTip(QtGui.QApplication.translate("EditorWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Replace &amp; Find Previous</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushReplaceAll.setText(QtGui.QApplication.translate("EditorWidget", "Replace &All", None, QtGui.QApplication.UnicodeUTF8))

from base import PMXCodeEdit
from searchwidgets import PMXReplaceBox, PMXFindBox
import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    EditorWidget = QtGui.QWidget()
    ui = Ui_EditorWidget()
    ui.setupUi(EditorWidget)
    EditorWidget.show()
    sys.exit(app.exec_())

