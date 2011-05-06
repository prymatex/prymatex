from PyQt4.Qt import *


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

class PMXBundleItemSelector(QDialog):
    def __init__(self, parent = None):
        super(PMXBundleItemSelector, self).__init__(parent)
        self.setupUi()
        self.hideUnusedColumns()
        self.setModal(True)
        
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
        self.lineFilter = QLineEdit(self)
        layout.addWidget(self.lineFilter)
        self.tableView = QTableView(self)
        
        self.tableView.setModel(QApplication.instance().bundleItemModel)
        layout.addWidget(self.tableView)
        
        self.setLayout(layout)
        self.setContentsMargins(-1, -1, -1, -1)