# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_bundle_editor import Ui_bundleEditor
import os, sys, re, plistlib
from glob import glob
from copy import copy, deepcopy
from xml.parsers.expat import ExpatError

from prymatex.gui.editor import center
from prymatex.gui.mixins.common import CenterWidget


try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

BUNDLES_DIRECTORY = "/home/blackbox/codigos/svn-textmate/Bundles/"

BUNDLE_ELEMENTS = (('Syntax', 'Syntaxes/*.tmLanguage',),
                   ('Snippet', 'Snippets/*.tmSnippet',),
                   ('Macro', 'Macros/*.tmMacro',),
                   ('Command', 'Commands/*.tmCommand',),
                   ('Preference', 'Preferences/*.tmPreferences',),
                   ('Template', 'Templates/*', ),
                   )


"""
class myQSortFilterProxyModel(QSortFilterProxyModel):
    pass
"""
class myQSortFilterProxyModel(QSortFilterProxyModel):
    pass
        
    #def filterAcceptsRow(self, sourceRow, parent):

        #item =  parent.internalPointer()
        #print self.sourceModel()
        #print item.cosas()
        
        #import ipdb;ipdb.set_trace()
        #print dir(item)
        #print item.tipo
        #return 1

class PMXBundleEditor(Ui_bundleEditor, QWidget):
    '''
        Primatex Bundle Editor
    '''
    def __init__(self):
        super(PMXBundleEditor, self).__init__()
        self.setupUi(self)
        self.stackLayout = QStackedLayout()
        self.configSelectTop()
        self.configTreeView()
        self.connect(self.btn_apply, SIGNAL("clicked()"),self.onApply)
        self.connect(self.select_top, SIGNAL("currentIndexChanged(int)"), self.selectTopChange)
        self.setWindowTitle(QApplication.translate("bundleEditor", "Bundle Editor", None, QApplication.UnicodeUTF8))
        

    def selectTopChange(self, index):
        if index == 0:
            self.proxyModel.setFilterRegExp("")
        elif index == 1:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(Sy)|Syntax"))
        elif index == 2:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(Sn)|Snippets"))
        elif index == 3:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(M)|Macros"))
        elif index == 4:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(C)|Command"))
        elif index == 5:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(P)|Preference"))
        elif index == 6:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(T)|Template"))
            
        #self.proxyModel.setFilterKeyColumn(0)
            
        
        
    def configSelectTop(self):
        self.select_top.removeItem(0)
        self.select_top.removeItem(0)
        
        self.select_top.addItem(_fromUtf8("Show all"))
        self.select_top.addItem(_fromUtf8("  Syntaxs"))
        self.select_top.addItem(_fromUtf8("  Snippets"))
        self.select_top.addItem(_fromUtf8("  Macros"))
        self.select_top.addItem(_fromUtf8("  Command"))
        self.select_top.addItem(_fromUtf8("  Preference"))
        self.select_top.addItem(_fromUtf8("  Template"))
    
    def configTreeView(self):
                
        self.sourceModel = myModel()
        self.proxyModel = myQSortFilterProxyModel() 
        self.proxyModel.setSourceModel(self.sourceModel)
        
        self.treeView.setModel(self.proxyModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        
        
    def setCentralWidget(self, objeto):
        pass
    
    def setStatusBar(self, objeto):
        pass

    def onApply(self):
        #self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(s)|Syntax"))
        #self.proxyModel.setFilterKeyColumn(0)
        print "Apply!!"
        


# //////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////

class myTreeItem(QAbstractItemModel):
    
    def __init__(self, obj, tipo, parentItem):
        super(myTreeItem, self).__init__()
        self.obj = obj
        self.parentItem = parentItem
        self.tipo = tipo
        self.childItems = []
    
    def appendChild(self, item):
        self.childItems.append(item)
    
    def __str__(self):
        return "HOLA SOY DIOS"
    
    def cosas(self):
        return "asdasdsadasda"
    
    def child(self, row):
        return self.childItems[row]
    
    def childCount(self):
        return len(self.childItems)
    
    def columnCount(self):
        return 1
    
    def data(self, column):
        if self.obj == None:
            return QVariant(self.tipo)
        else:
            if self.tipo[0] == "S":
                text = "(%s%s) %s" % (self.tipo[0],self.tipo[1],self.obj.name)
            else:
                text = "(%s) %s" % (self.tipo[0],self.obj.name)
            
            return QVariant(text)
        return QVariant()

    def parent(self):
        return self.parentItem
    
    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0




# //////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////        
class myModel(QAbstractItemModel):
    def __init__(self, parent = None):
        super(myModel, self).__init__(parent)
        self.treeView = parent
        self.headers = ['Bundles']
        self.columms = 1
        
        #creamos algunos items
        #self.rootItem = myTreeItem(None, "ALL", None)
        #self.parents = {0 : self.rootItem}
        self.setupModelData()
    
    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(self.headers)
    
    def rowCount(self, parent = QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()
    
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            print "ACA"
            return QModelIndex()
        
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()
    
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        
        childItem = index.internalPointer()
        if not childItem:
            return QModelIndex()
        
        parentItem = childItem.parent()
        
        if parentItem == self.rootItem:
            return QModelIndex()
        
        return self.createIndex(parentItem.row(), 0, parentItem)
    
    def __str__(self):
        return "myModel"
    
    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()
        
        item = index.internalPointer()
        
        if role == Qt.DisplayRole:
            return item.data(index.column())
        
        if role == Qt.UserRole:
            if item:
                return item
        
        return QVariant()

    
    def setupModelData(self, filtro_tipo = None):
        pass
        """
        self.rootItem = myTreeItem(None, "Bundles", None)
        self.parents = {0 : self.rootItem}
        
        
        for bundle_name in LOS_BUNDLES:
            bundle = LOS_BUNDLES[bundle_name]
            root_bundle = myTreeItem(bundle,"bundle", self.rootItem)
            self.rootItem.appendChild(root_bundle)
            
                        
            for tipo in bundle.tipos:
                
                
                objetos = bundle.tipos[tipo]
                
                if objetos:
                    root_bundle_tipo = myTreeItem(None, tipo, root_bundle)    
                    root_bundle.appendChild(root_bundle_tipo)
                    for objeto_nombre in objetos:
                        objeto = objetos[objeto_nombre]
                        item = myTreeItem(objeto, tipo, root_bundle_tipo)
                        root_bundle_tipo.appendChild(item)
    """
    
         


    

    
    

    