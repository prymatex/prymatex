# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/emergencytrace.ui'
#
# Created: Fri Oct 28 21:42:07 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TracebackDialog(object):
    def setupUi(self, TracebackDialog):
        TracebackDialog.setObjectName(_fromUtf8("TracebackDialog"))
        TracebackDialog.resize(400, 300)
        TracebackDialog.setWindowTitle(_('Traceback'))
        self.verticalLayout = QtGui.QVBoxLayout(TracebackDialog)
        self.verticalLayout.setContentsMargins(1, 2, 1, 1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelTitle = QtGui.QLabel(TracebackDialog)
        self.labelTitle.setText(_('Exception Text'))
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.verticalLayout.addWidget(self.labelTitle)
        self.textStackTrace = QtGui.QTextEdit(TracebackDialog)
        self.textStackTrace.setObjectName(_fromUtf8("textStackTrace"))
        self.verticalLayout.addWidget(self.textStackTrace)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(TracebackDialog)
        self.pushButton.setText(_('&View exception'))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushCopy = QtGui.QPushButton(TracebackDialog)
        self.pushCopy.setText(_('&Copy'))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/edit-copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCopy.setIcon(icon)
        self.pushCopy.setObjectName(_fromUtf8("pushCopy"))
        self.horizontalLayout.addWidget(self.pushCopy)
        self.pushClose = QtGui.QPushButton(TracebackDialog)
        self.pushClose.setText(_('&Close'))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/dialog-cancel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushClose.setIcon(icon1)
        self.pushClose.setObjectName(_fromUtf8("pushClose"))
        self.horizontalLayout.addWidget(self.pushClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TracebackDialog)
        QtCore.QObject.connect(self.pushClose, QtCore.SIGNAL(_fromUtf8("clicked()")), TracebackDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TracebackDialog)

    def retranslateUi(self, TracebackDialog):
        pass

from prymatex import resources_rc
