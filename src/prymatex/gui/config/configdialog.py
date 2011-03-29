from ui_settings import Ui_PMXSettingsDialog
from PyQt4.Qt import *
from prymatex.gui.editor import center

class PMXSettingsItem(QStandardItem):
    def __init__(self, name, widget_index, parent = None):
        if isinstance(parent, QStandardItem):
            super(PMXSettingsItem, self).__init__(parent)
        else:
            super(PMXSettingsItem, self).__init__()
            
        self.setText(name)
        self.setEditable(False)
        self.widget_index = widget_index
        

class PMXNetworkConfigWidget(QWidget):
    def __init__(self):
        super(PMXNetworkConfigWidget, self).__init__()
        



class PMXSettingsDialog(QDialog, Ui_PMXSettingsDialog):
    def __init__(self):
        super(PMXSettingsDialog, self).__init__()
        self.setupUi(self)
        self.model = QStandardItemModel()
        self.model = QStandardItemModel(self)
        
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        
        self.treeView.setModel(self.proxy_model)
        self.treeView.setModel(self.model)
        self.treeView.widgetChanged.connect(self.changeWidget)
        #self.model.setHeaderData(0, Qt.Horizontal, self.trUtf8("Option"))
        self.stackLayout = QStackedLayout()
        self.container.setLayout(self.stackLayout)
        
        self.lineFilter.textChanged.connect(self.filterItems)
        
    def filterItems(self, txt):
        self.proxy_model.setFilterRegExp(QRegExp(txt, Qt.CaseInsensitive))
    
    def exec_(self):
        center(self)
        index = self.model.index(0, 0)
        self.model.itemFromIndex(index)
        self.treeView.setCurrentIndex(index)
        
        super(PMXSettingsDialog, self).exec_()
    
    def changeWidget(self, index):
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
        self.model.appendRow(item)
        

