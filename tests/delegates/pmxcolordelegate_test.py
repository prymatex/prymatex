from PyQt4.Qt import *
import os, sys
sys.path.append(os.path.abspath('../..'))

from prymatex.mvc.delegates import PMXColorDelegate

def main(argv = sys.argv):
    
    app = QApplication(argv)
    win = QWidget()
    win.setWindowTitle("Color delegate sample")
    layout = QVBoxLayout()
    win.setLayout(layout)
    tableView = QTableView()
    layout.addWidget(tableView)
    model = QStandardItemModel(1, 4)
    model.setHeaderData(0, Qt.Horizontal, "Foreground")
    tableView.setModel(model)
    for i in range(model.columnCount()):
        print "Setting delegate for column: %d" % i
        delegate = PMXColorDelegate()
        delegate.setParent(tableView)
        tableView.setItemDelegateForColumn(i, delegate)
        
    win.show()
    return app.exec_()

if __name__ == "__main__":
    import sys
    sys.exit(main())