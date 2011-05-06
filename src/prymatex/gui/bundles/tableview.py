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
            