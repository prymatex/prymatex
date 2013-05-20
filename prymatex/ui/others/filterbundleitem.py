# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/others/filterbundleitem.ui'
#
# Created: Tue May 14 21:59:05 2013
#      by: PyQt4 UI code generator snapshot-4.10.2-6f54723ef2ba
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FilterThroughCommand(object):
    def setupUi(self, FilterThroughCommand):
        FilterThroughCommand.setObjectName(_fromUtf8("FilterThroughCommand"))
        FilterThroughCommand.resize(400, 325)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/resources/actions/view-filter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FilterThroughCommand.setWindowIcon(icon)
        self.verticalLayout_3 = QtGui.QVBoxLayout(FilterThroughCommand)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setMargin(10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(FilterThroughCommand)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboCommand = QtGui.QComboBox(FilterThroughCommand)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboCommand.sizePolicy().hasHeightForWidth())
        self.comboCommand.setSizePolicy(sizePolicy)
        self.comboCommand.setEditable(True)
        self.comboCommand.setObjectName(_fromUtf8("comboCommand"))
        self.horizontalLayout.addWidget(self.comboCommand)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.groupBox = QtGui.QGroupBox(FilterThroughCommand)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radioInputNone = QtGui.QRadioButton(self.groupBox)
        self.radioInputNone.setObjectName(_fromUtf8("radioInputNone"))
        self.verticalLayout_2.addWidget(self.radioInputNone)
        self.radioInputSelection = QtGui.QRadioButton(self.groupBox)
        self.radioInputSelection.setChecked(True)
        self.radioInputSelection.setObjectName(_fromUtf8("radioInputSelection"))
        self.verticalLayout_2.addWidget(self.radioInputSelection)
        self.radioInputDocument = QtGui.QRadioButton(self.groupBox)
        self.radioInputDocument.setObjectName(_fromUtf8("radioInputDocument"))
        self.verticalLayout_2.addWidget(self.radioInputDocument)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(FilterThroughCommand)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radioOutputDiscard = QtGui.QRadioButton(self.groupBox_2)
        self.radioOutputDiscard.setObjectName(_fromUtf8("radioOutputDiscard"))
        self.verticalLayout.addWidget(self.radioOutputDiscard)
        self.radioOutputSelection = QtGui.QRadioButton(self.groupBox_2)
        self.radioOutputSelection.setChecked(True)
        self.radioOutputSelection.setObjectName(_fromUtf8("radioOutputSelection"))
        self.verticalLayout.addWidget(self.radioOutputSelection)
        self.radioOutputDocument = QtGui.QRadioButton(self.groupBox_2)
        self.radioOutputDocument.setObjectName(_fromUtf8("radioOutputDocument"))
        self.verticalLayout.addWidget(self.radioOutputDocument)
        self.radioOutputInsertText = QtGui.QRadioButton(self.groupBox_2)
        self.radioOutputInsertText.setObjectName(_fromUtf8("radioOutputInsertText"))
        self.verticalLayout.addWidget(self.radioOutputInsertText)
        self.radioOutputInsertSnippet = QtGui.QRadioButton(self.groupBox_2)
        self.radioOutputInsertSnippet.setObjectName(_fromUtf8("radioOutputInsertSnippet"))
        self.verticalLayout.addWidget(self.radioOutputInsertSnippet)
        self.radioOutputShowToolTip = QtGui.QRadioButton(self.groupBox_2)
        self.radioOutputShowToolTip.setObjectName(_fromUtf8("radioOutputShowToolTip"))
        self.verticalLayout.addWidget(self.radioOutputShowToolTip)
        self.radioOutputShowAsHTML = QtGui.QRadioButton(self.groupBox_2)
        self.radioOutputShowAsHTML.setObjectName(_fromUtf8("radioOutputShowAsHTML"))
        self.verticalLayout.addWidget(self.radioOutputShowAsHTML)
        self.radioOutputCreateNewDocument = QtGui.QRadioButton(self.groupBox_2)
        self.radioOutputCreateNewDocument.setObjectName(_fromUtf8("radioOutputCreateNewDocument"))
        self.verticalLayout.addWidget(self.radioOutputCreateNewDocument)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(FilterThroughCommand)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(FilterThroughCommand)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FilterThroughCommand.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FilterThroughCommand.reject)
        QtCore.QMetaObject.connectSlotsByName(FilterThroughCommand)

    def retranslateUi(self, FilterThroughCommand):
        FilterThroughCommand.setWindowTitle(_translate("FilterThroughCommand", "Filter Through Command", None))
        self.label.setText(_translate("FilterThroughCommand", "Command", None))
        self.comboCommand.setProperty("className", _translate("FilterThroughCommand", "bigPadding", None))
        self.groupBox.setTitle(_translate("FilterThroughCommand", "Input", None))
        self.radioInputNone.setText(_translate("FilterThroughCommand", "&None", None))
        self.radioInputSelection.setText(_translate("FilterThroughCommand", "&Selection", None))
        self.radioInputDocument.setText(_translate("FilterThroughCommand", "&Document", None))
        self.groupBox_2.setTitle(_translate("FilterThroughCommand", "Output", None))
        self.radioOutputDiscard.setText(_translate("FilterThroughCommand", "D&iscard", None))
        self.radioOutputSelection.setText(_translate("FilterThroughCommand", "Replace Se&lection", None))
        self.radioOutputDocument.setText(_translate("FilterThroughCommand", "Replace D&ocument", None))
        self.radioOutputInsertText.setText(_translate("FilterThroughCommand", "&Insert As Text", None))
        self.radioOutputInsertSnippet.setText(_translate("FilterThroughCommand", "Insert As Sni&ppet", None))
        self.radioOutputShowToolTip.setText(_translate("FilterThroughCommand", "Show As &ToolTip", None))
        self.radioOutputShowAsHTML.setText(_translate("FilterThroughCommand", "Show As &Html", None))
        self.radioOutputCreateNewDocument.setText(_translate("FilterThroughCommand", "Create &New Document", None))

