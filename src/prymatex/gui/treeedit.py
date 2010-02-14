# -*- encoding: utf-8 -*-

'''
Configuration may use this
'''
try:
    from prymatex.lib.i18n import ugettext as _
except:
    _ = lambda s: s
    

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class BoolNode(QStandardItem):
    def __init__(self, root):
        QStandardItem.__init__(self, 1, 2)
        

class IntegerNode(QStandardItem):
    def __init__(self, root):
        QStandardItem.__init__(self, 1, 2)
        self.setData()

class FloatNode(QStandardItem):
    pass

class StrNode(QStandardItem):
    pass

class ListNode(QStandardItem):
    def __init__(self, name, lst):
        QStandardItem.__init__(self, "List")
        for item in lst:
            pass
        
class DictNode(QStandardItem):
    def __init__(self, data, lst):
        QStandardItem.__init__(self, 1, 2)
        self.setText("Dict")
        


class PMXPythonItemModel(QStandardItemModel):
    def __init__(self, data = None):
        QStandardItemModel.__init__(self)
        self.setHorizontalHeaderLabels(["Type", "Value"])
        
        self.setPythonData(data)
        
    def setPythonData(self, data, root = None):
        if not root:
            root = self
        if isinstance(data, dict):
            self.addHash(data, root)
        elif isinstance(data, list):
            self.addList(data, root)
            
    def addHash(self, data, root):
        node = DictNode(data, self)
        self.appendRow(node)
    
    def addList(self, data, root):
        pass
        
            
     

class PMXTreeEdit(QTreeView):
    def __init__(self, parent = None):
        QTreeView.__init__(self, parent)
        self.setWindowTitle("Python Object Editor")
        
        
        
        
if __name__ == "__main__":
    app = QApplication([])
    win = PMXTreeEdit(None)
    model = PMXPythonItemModel({'x': 3, 'b': 3, 'c': [1, 2, 4]})
    win.setModel(model)
    win.show()
    app.exec_()
