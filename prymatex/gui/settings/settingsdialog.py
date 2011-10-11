#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.ui.settingsdialog import Ui_SettingsDialog

class PMXSettingsItem(QtGui.QStandardItem):
    def __init__(self, name, widget_index, parent = None):
        if isinstance(parent, QtGui.QStandardItem):
            super(PMXSettingsItem, self).__init__(parent)
        else:
            super(PMXSettingsItem, self).__init__()
            
        self.setText(name)
        self.setEditable(False)
        self.widget_index = widget_index
        

class PMXNetworkConfigWidget(QtGui.QWidget):
    def __init__(self):
        super(PMXNetworkConfigWidget, self).__init__()

class PMXSettingsDialog(QtGui.QDialog, Ui_SettingsDialog, PMXObject):
    '''
    Settings dialog, it's hold by the application under
    configdialog property
    '''
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.model = QtGui.QStandardItemModel(self)
        
        self.proxy_model = QtGui.QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        
        self.treeViewSettings.setModel(self.proxy_model)
        self.treeViewSettings.setModel(self.model)
        #self.model.setHeaderData(0, Qt.Horizontal, self.trUtf8("Option"))
        self.stackLayout = QtGui.QStackedLayout()
        self.container.setLayout(self.stackLayout)
        
        # Focus first item
    
    def focusFirst(self):
        index = self.model.index(0, 0)
        self.model.itemFromIndex(index)
        self.treeViewSettings.setCurrentIndex(index)
    
    def on_lineEditFilter_textChanged(self, text):
        self.proxy_model.setFilterRegExp(QtCore.QRegExp(text, Qt.CaseInsensitive))
    
    def on_treeViewSettings_activated(self, index):
        print "Cambiando al widget"
        self.container.layout().setCurrentIndex(index)
        title = self.container.layout().currentWidget().windowTitle()
        self.labelTitle.setText( title )
        
    def _register(self, name, widget):
        
        index = self.stackLayout.addWidget(widget)
        #item.setD
        item = PMXSettingsItem(name, widget_index = index)
        self.model.appendRow(item)
        
    def register(self, widget, parent_node = None):
        '''
        Takes title form widget's windowTitle
        '''
        index = self.stackLayout.addWidget(widget)
        item = PMXSettingsItem(widget.windowTitle(), widget_index = index)
        icon = widget.windowIcon()
        if not icon.isNull():
            item.setIcon(icon)
        self.model.appendRow(item)
        
    def on_pushClose_pressed(self):
        self.reject()
    
    @property
    def currentWidget(self):
        return self.container.layout().currentWidget()
    
    def on_pushDiscard_pressed(self):
        self.currentWidget.discard()
        
        #QMessageBox.information(self, "Discard", "Discards changes<br/>TODO")
        
    def on_pushApply_pressed(self):
        self.currentWidget.apply()
        #QMessageBox.information(self, "Apply", "Apply changes<br/>TODO")

