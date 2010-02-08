#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 08/02/2010 by defo
from PyQt4.Qt import *
from prymatex.lib.i18n import ugettext as _
from ui_configdialog import Ui_ConfigDialog

class PMXTitleLabel(QLabel):
    def __init__(self, text, parent = None):
        QLabel.__init__(self, text, parent)
        self.setStyleSheet('''
            QLabel {
                font-weight: bolder;
                font-size: 15px;
                text-align: center;
            }
        ''')
        
        

class PMXConfigDialog(QDialog, Ui_ConfigDialog):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setupTree()
        self.splitter.setSizes([150, 300])
        
    def setupTree(self):
        model = QStandardItemModel(0, 1, self)
        self.itemGeneral = QStandardItem(_("General"))
        self.itemGeneral.setEditable(False)
        
        self.itemGeneral.widgetToShow = PMXTitleLabel(_("General Configuration"))
        
        model.appendRow(self.itemGeneral)
        
        
        model.setHorizontalHeaderItem(0, QStandardItem(_('Config Section')))
        self.itemEditor = QStandardItem(_("Editor"))
        #self.
        self.itemEditor.setEditable(False)
        self.itemGeneral.appendRow(self.itemEditor)
        self.itemOpenClose = QStandardItem(_("Open/Close"))
        self.itemOpenClose.setEditable(False)
        self.itemGeneral.appendRow(self.itemOpenClose)
        self.itemTextMate = QStandardItem(_("TextMate"))
        
        self.itemTextMate.setEditable(False)
        self.itemGeneral.appendRow(self.itemTextMate)
        self.itemLookAndFeel = QStandardItem(_("Look and Feel"))
        self.itemLookAndFeel.setEditable(False)
        self.itemGeneral.appendRow(self.itemLookAndFeel)
        self.itemPanes = QStandardItem(_("Panes"))
        self.itemPanes.setEditable(False)
        self.itemPanesFSPane = QStandardItem(_("FS Pane"))
        self.itemPanes.appendRow(self.itemPanesFSPane)
        model.appendRow(self.itemPanes)
        
        self.treeView.setModel(model)
        # Visibles
        self.treeView.setExpanded(model.indexFromItem(self.itemGeneral), True)
        self.treeView.setExpanded(model.indexFromItem(self.itemPanes), True)
    
        self.null_object = QWidget(self.treeView)
    
    def on_treeView_clicked(self, index):
        #print self.treeView.model().index(index).toPyObject()
        model = self.treeView.model()
        item = model.itemFromIndex(index)
        # Devolver la propiedad al llamador
        self.oldWidget = self.scrollArea.takeWidget()
        if hasattr(item, 'widgetToShow'):
            widget = item.widgetToShow
        else:
            widget = self.null_object
        
        self.scrollArea.setWidget(widget)
        
        