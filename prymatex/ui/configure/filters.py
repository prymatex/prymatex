# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/configure/filters.ui'
#
# Created: Wed Dec 10 13:43:28 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FiltersWidget(object):
    def setupUi(self, FiltersWidget):
        FiltersWidget.setObjectName("FiltersWidget")
        FiltersWidget.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FiltersWidget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listViewFilters = QtWidgets.QListView(FiltersWidget)
        self.listViewFilters.setObjectName("listViewFilters")
        self.horizontalLayout.addWidget(self.listViewFilters)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButtonAdd = QtWidgets.QPushButton(FiltersWidget)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.verticalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonEdit = QtWidgets.QPushButton(FiltersWidget)
        self.pushButtonEdit.setObjectName("pushButtonEdit")
        self.verticalLayout.addWidget(self.pushButtonEdit)
        self.pushButtonRemove = QtWidgets.QPushButton(FiltersWidget)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.verticalLayout.addWidget(self.pushButtonRemove)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(FiltersWidget)
        QtCore.QMetaObject.connectSlotsByName(FiltersWidget)

    def retranslateUi(self, FiltersWidget):
        _translate = QtCore.QCoreApplication.translate
        FiltersWidget.setWindowTitle(_translate("FiltersWidget", "Form"))
        self.pushButtonAdd.setText(_translate("FiltersWidget", "Add"))
        self.pushButtonEdit.setText(_translate("FiltersWidget", "Edit"))
        self.pushButtonRemove.setText(_translate("FiltersWidget", "Remove"))

