# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/trace.ui'
#
# Created: Sun Apr  3 23:47:11 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TracebackDialog(object):
    def setupUi(self, TracebackDialog):
        TracebackDialog.setObjectName(_fromUtf8("TracebackDialog"))
        TracebackDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(TracebackDialog)
        self.verticalLayout.setContentsMargins(1, 2, 1, 1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelTitle = QtGui.QLabel(TracebackDialog)
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.verticalLayout.addWidget(self.labelTitle)
        self.textStackTrace = QtGui.QPlainTextEdit(TracebackDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textStackTrace.sizePolicy().hasHeightForWidth())
        self.textStackTrace.setSizePolicy(sizePolicy)
        self.textStackTrace.setReadOnly(True)
        self.textStackTrace.setObjectName(_fromUtf8("textStackTrace"))
        self.verticalLayout.addWidget(self.textStackTrace)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(TracebackDialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushCopy = QtGui.QPushButton(TracebackDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/edit-copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCopy.setIcon(icon)
        self.pushCopy.setObjectName(_fromUtf8("pushCopy"))
        self.horizontalLayout.addWidget(self.pushCopy)
        self.pushClose = QtGui.QPushButton(TracebackDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/process-stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushClose.setIcon(icon1)
        self.pushClose.setObjectName(_fromUtf8("pushClose"))
        self.horizontalLayout.addWidget(self.pushClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TracebackDialog)
        QtCore.QObject.connect(self.pushClose, QtCore.SIGNAL(_fromUtf8("clicked()")), TracebackDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TracebackDialog)

    def retranslateUi(self, TracebackDialog):
        TracebackDialog.setWindowTitle(QtGui.QApplication.translate("TracebackDialog", "Traceback", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTitle.setText(QtGui.QApplication.translate("TracebackDialog", "Exception Text", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("TracebackDialog", "&View exception", None, QtGui.QApplication.UnicodeUTF8))
        self.pushCopy.setText(QtGui.QApplication.translate("TracebackDialog", "&Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.pushClose.setText(QtGui.QApplication.translate("TracebackDialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))

import prymatex.res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TracebackDialog = QtGui.QDialog()
    ui = Ui_TracebackDialog()
    ui.setupUi(TracebackDialog)
    TracebackDialog.show()
    sys.exit(app.exec_())

