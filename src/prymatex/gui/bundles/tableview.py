from PyQt4.Qt import *
from prymatex.core.base import PMXObject
from prymatex.models.base import PMXTableBase


class PMXBundleItemTableView(QTableView):
    showStateChanged = pyqtSignal(bool)
    
    def closeEvent(self, event):
        self.showStateChanged.emit(False)
        super(PMXBundleItemTableView, self).closeEvent(event)
        
    def showEvent(self, event):
        self.showStateChanged.emit(True)
        super(PMXBundleItemTableView, self).showEvent(event)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            return
        super(PMXBundleItemTableView, self).keyPressEvent(event)
    
    def setModel(self, model):
        super(PMXBundleItemTableView, self).setModel(model)
        model.rowsInserted.connect(self.resizeColumnsAndRows)
        model.rowsRemoved.connect(self.resizeColumnsAndRows)
        # Setup
        if isinstance(model, PMXTableBase):
            model.setColumnDelegatesFromFields(self)

        
    def resizeColumnsAndRows(self, *largs):
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        #self.resizeRowsToContents()
        
    
        

class PMXFilterBundleItem(QSortFilterProxyModel):
    '''
    Filters from user input
    '''
    #def filterAcceptsRow(self, sourceRow, parent):
        #print sourceRow
    #    return True
    
    def setFilteringProxy(self, value):
        print value
    

class PMXBundleItemSelector(QDialog, PMXObject):
    '''
    This dialog allow the user to search through commands and snippets
    easily. An instance is hold in the main window and triggered with
    an action. 
    '''
    def __init__(self, parent = None):
        
        super(PMXBundleItemSelector, self).__init__(parent)
        self.setupUi()
        #self.hideUnusedColumns()
        self.setModal(True)
        self.lineFilter.textChanged.connect(self.proxyFilteringModel.setFilteringProxy)
    
    def exec_(self):
        # Geo is not known until the mainwindow is shown, so we 
        # must accept it
        geo = self.mainwindow.geometry()
        w  = geo.width() * .8
        h = geo.height() * .4
        geo.setX(geo.x() + (geo.width() - w)/2)
        geo.setY(geo.y() + (geo.height() - h)/2)
        geo.setWidth(w)
        geo.setHeight(h)
        self.setGeometry(geo)
        self.lineFilter.setFocus()
        super(PMXBundleItemSelector, self).exec_()
        
    def hideUnusedColumns(self):
        model = self.tableView.model()
        for n, name in enumerate(model.ELEMENTS):

            if name in ('name', 'tabTrigger'):
                self.tableView.setColumnHidden(n, False)
            else:
                self.tableView.setColumnHidden(n, True)
            
        
    def setupUi(self):
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        self.lineFilter = QLineEdit(self)
        layout.addWidget(self.lineFilter)
        self.tableView = QTableView(self)
        
        self.proxyFilteringModel = PMXFilterBundleItem()
        self.proxyFilteringModel.setSourceModel(QApplication.instance().bundleItemModel)
        self.tableView.setModel(self.proxyFilteringModel)
        
        self.tableView.resizeColumnToContents(1)
        self.tableView.resizeRowsToContents()
        self.tableView.verticalHeader().setVisible(False)

        layout.addWidget(self.tableView)
        
        self.setLayout(layout)
        self.setContentsMargins(-1, -1, -1, -1)