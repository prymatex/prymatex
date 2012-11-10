# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dialogs/spelling.ui'
#
# Created: Fri Nov  9 18:10:44 2012
#      by: PyQt4 UI code generator snapshot-4.9.6-95094339d25b
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SpellingDialog(object):
    def setupUi(self, SpellingDialog):
        SpellingDialog.setObjectName(_fromUtf8("SpellingDialog"))
        SpellingDialog.resize(482, 313)
        SpellingDialog.setMinimumSize(QtCore.QSize(482, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/prymatex/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SpellingDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SpellingDialog)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEditNotFound = QtGui.QLineEdit(SpellingDialog)
        self.lineEditNotFound.setObjectName(_fromUtf8("lineEditNotFound"))
        self.gridLayout.addWidget(self.lineEditNotFound, 0, 0, 1, 1)
        self.label = QtGui.QLabel(SpellingDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.pushButtonChange = QtGui.QPushButton(SpellingDialog)
        self.pushButtonChange.setObjectName(_fromUtf8("pushButtonChange"))
        self.gridLayout.addWidget(self.pushButtonChange, 0, 1, 1, 1)
        self.pushButtonFindNext = QtGui.QPushButton(SpellingDialog)
        self.pushButtonFindNext.setObjectName(_fromUtf8("pushButtonFindNext"))
        self.gridLayout.addWidget(self.pushButtonFindNext, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.listWidgetCorrections = QtGui.QListWidget(SpellingDialog)
        self.listWidgetCorrections.setObjectName(_fromUtf8("listWidgetCorrections"))
        self.gridLayout_2.addWidget(self.listWidgetCorrections, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButtonIgnore = QtGui.QPushButton(SpellingDialog)
        self.pushButtonIgnore.setObjectName(_fromUtf8("pushButtonIgnore"))
        self.verticalLayout.addWidget(self.pushButtonIgnore)
        self.pushButtonLearn = QtGui.QPushButton(SpellingDialog)
        self.pushButtonLearn.setObjectName(_fromUtf8("pushButtonLearn"))
        self.verticalLayout.addWidget(self.pushButtonLearn)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.comboBoxDictionary = QtGui.QComboBox(SpellingDialog)
        self.comboBoxDictionary.setObjectName(_fromUtf8("comboBoxDictionary"))
        self.gridLayout_2.addWidget(self.comboBoxDictionary, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.retranslateUi(SpellingDialog)
        QtCore.QMetaObject.connectSlotsByName(SpellingDialog)

    def retranslateUi(self, SpellingDialog):
        SpellingDialog.setWindowTitle(_('Spelling'))
        self.label.setText(_('This word was not found in the spelling dictionary.'))
        self.pushButtonChange.setText(_('Change'))
        self.pushButtonFindNext.setText(_('Find Next'))
        self.pushButtonIgnore.setText(_('Ignore'))
        self.pushButtonLearn.setText(_('Learn'))

