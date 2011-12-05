import os, sys
#Setup qt
import sip
sip.setapi('QDate', 2)
sip.setapi('QTime', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui

import cPickle
import StringIO
from copy import deepcopy

sys.path.append(os.path.abspath('..'))

from prymatex.utils.i18n import ugettext as _
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class PyMimeData(QtCore.QMimeData):
    """ The PyMimeData wraps a Python instance as MIME data.
    """
    # The MIME type for instances.
    MIME_TYPE = 'application/x-ets-qt4-instance'

    def __init__(self, data = None):
        """ Initialise the instance.
        """
        QtCore.QMimeData.__init__(self)

        # Keep a local reference to be returned if possible.
        self._local_instance = data

        if data is not None:
            # We may not be able to pickle the data.
            try:
                pdata = cPickle.dumps(data)
            except:
                return
    
            # This format (as opposed to using a single sequence) allows the
            # type to be extracted without unpickling the data itself.
            self.setData(self.MIME_TYPE, cPickle.dumps(data.__class__) + pdata)

    @classmethod
    def coerce(cls, md):
        """ Coerce a QMimeData instance to a PyMimeData instance if possible.
        """
        # See if the data is already of the right type. If it is then we know
        # we are in the same process.
        if isinstance(md, cls):
            return md

        # See if the data type is supported.
        if not md.hasFormat(cls.MIME_TYPE):
            return None

        nmd = cls()
        nmd.setData(cls.MIME_TYPE, md.data())
        return nmd

    def instance(self):
        """ Return the instance.
        """
        if self._local_instance is not None:
            return self._local_instance

        io = StringIO.StringIO(str(self.data(self.MIME_TYPE)))

        try:
            # Skip the type.
            cPickle.load(io)

            # Recreate the instance.
            return cPickle.load(io)
        except:
            pass

        return None

    def instanceType(self):
        """ Return the type of the instance.
        """
        if self._local_instance is not None:
            return self._local_instance.__class__

        try:
            return cPickle.loads(str(self.data(self.MIME_TYPE)))
        except:
            pass

        return None

class PMXBundleMenuNode(object):
    ITEM = 0
    SUBMENU = 1
    SEPARATOR = 2
    def __init__(self, item, nodeType, parent = None):
        self.item = item
        self.nodeType = nodeType
        self.parent = parent
        self.children = []
        
    def name(self):
        if self.nodeType == self.SEPARATOR:
            return '--------------------------------'
        elif self.nodeType == self.SUBMENU:
            return self.item['name']
        return self.item.name
    
    def appendChild(self, child):
        self.children.append(child)
        child.parent = self

    def removeChild(self, child):
        self.children.remove(child)
        
    def child(self, row):
        if len(self.children) > row:
            return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):
        if self.parent is not None and self in self.parent.children:  
            return self.parent.children.index(self)

    def insertChild(self, index, child):
        self.children.insert(index, child)
        child.parent = self
        
class PMXMenuTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, manager):
        QtCore.QAbstractItemModel.__init__(self)
        self.manager = manager

    def buildMenu(self, items, parent, submenus = {}):
        for uuid in items:
            if uuid.startswith("-"):
                parent.appendChild(PMXBundleMenuNode(uuid, PMXBundleMenuNode.SEPARATOR, parent))
            else:
                item = self.manager.getBundleItem(uuid)
                if item != None:
                    parent.appendChild(PMXBundleMenuNode(item, PMXBundleMenuNode.ITEM, parent))
                elif uuid in submenus:
                    submenu = PMXBundleMenuNode({"uuid": uuid, "name": submenus[uuid]['name']}, PMXBundleMenuNode.SUBMENU, parent)
                    parent.appendChild(submenu)
                    self.buildMenu(submenus[uuid]['items'], submenu, submenus)

    def setMainMenu(self, mainMenu):
        # 'items' 'submenus'
        self.root = PMXBundleMenuNode({ "uuid":"root", "name": "root" }, PMXBundleMenuNode.SUBMENU)
        self.buildMenu(mainMenu['items'], self.root, mainMenu['submenus'])

    def index(self, row, column, parent):
        if not parent.isValid():
            parent = self.root
        else:
            parent = parent.internalPointer()
        
        child = parent.child(row)
        if child:
            return self.createIndex(row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()  

        child = index.internalPointer()  
        parent = child.parent
        row = parent.row()
        
        if parent == self.root or row is None:  
            return QtCore.QModelIndex()

        return self.createIndex(row, 0, parent)
    
    def rowCount(self, parent):
        if parent.column() > 0:  
            return 0  

        if not parent.isValid():  
            parent = self.root  
        else:  
            parent = parent.internalPointer()  

        return parent.childCount()
    
    def columnCount(self, parent):  
        return 1

    def data(self, index, role):
        if role == 0:
            node = index.internalPointer()
            return node.name()
        else:
            return None

    def supportedDropActions(self): 
        return QtCore.Qt.MoveAction     

    def flags(self, index):
        defaultFlags = QtCore.QAbstractItemModel.flags(self, index)
        if index.isValid():
            node = index.internalPointer()
            print node.type()
            if node.type() == 1:
                return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
        return defaultFlags | QtCore.Qt.ItemIsDropEnabled

    def mimeTypes(self):
        return [ 'application/x-ets-qt4-instance' ]

    def mimeData(self, index):
        node = index[0].internalPointer()
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True
        
        if not mimedata.hasFormat("application/x-ets-qt4-instance"):
            return False
        
        dragNode = mimedata.instance()
        
        if not parentIndex.isValid():
            parentNode = self.root
        else:
            parentNode = parentIndex.internalPointer()

        if dragNode.parent == parentNode:
            currentRow = dragNode.row()
            row = row if currentRow >= row else row - 1
            dragNode.parent.removeChild(dragNode)
            dragNode.parent.insertChild(row, dragNode)
        else:
            dragNode.parent.removeChild(dragNode)
            parentNode.insertChild(row, dragNode)
        
        self.layoutChanged.emit()
        return True

class PMXExcludedListModel(QtCore.QAbstractListModel):
    def __init__(self, manager):
        QtCore.QAbstractListModel.__init__(self)
        self.manager = manager
        self.items = [PMXBundleMenuNode({ "uuid":"", "name": "New Group" }, PMXBundleMenuNode.SUBMENU),  PMXBundleMenuNode("-", PMXBundleMenuNode.SEPARATOR)]
    
    def setExcludedItems(self, items):
        pass
    
    def index(self, row, column, parent):
        if not parent.isValid():
            return QtCore.QModelIndex()
        return self.createIndex(row, column, self.items[row])
    
    def rowCount(self, parent):
        return len(self.items)
    
    def data(self, index, role):
        if role == 0:
            node = self.items[index.row()]
            return node.name()
        else:
            return None
    
    def columnCount(self, parent):  
        return 1

    def supportedDropActions(self): 
        return QtCore.Qt.MoveAction     

    def flags(self, index):
        defaultFlags = QtCore.QAbstractItemModel.flags(self, index)
        if index.isValid():
            node = index.internalPointer()
            print node.type()
            if node.type() == 1:
                return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
        return defaultFlags | QtCore.Qt.ItemIsDropEnabled
    
    def mimeTypes(self):
        return [ 'application/x-ets-qt4-instance' ]

    def mimeData(self, index):
        node = index[0].internalPointer()
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True
        
        if not mimedata.hasFormat("application/x-ets-qt4-instance"):
            return False
        
        dragNode = mimedata.instance()
        
        if not parentIndex.isValid():
            parentNode = self.root
        else:
            parentNode = parentIndex.internalPointer()

        if dragNode.parent == parentNode:
            currentRow = dragNode.row()
            row = row if currentRow >= row else row - 1
            dragNode.parent.removeChild(dragNode)
            dragNode.parent.insertChild(row, dragNode)
        else:
            dragNode.parent.removeChild(dragNode)
            parentNode.insertChild(row, dragNode)
        
        self.layoutChanged.emit()
        return True
    
from prymatex.ui.support.bundle import Ui_Menu

class PMXBundleWidget(QtGui.QWidget, Ui_Menu):
    TYPE = 'bundle'
    BUNDLEITEM = 0
    SEPARATOR = 1
    SUBMENU = 2
    NEWGROUP = 3
    NEWSEPARATOR = 4
    def __init__(self, manager, parent = None):
        from prymatex.gui.support.models import PMXMenuTreeModel as RealPMXMenuTreeModel
        from prymatex.gui.support.models import PMXExcludedListModel as RealPMXExcludedListModel
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.manager = manager
        self.treeModel = RealPMXMenuTreeModel(manager)
        self.listModel = RealPMXExcludedListModel(manager)
        self.treeMenuView.setModel(self.treeModel)
        self.treeMenuView.setAcceptDrops(True)
        self.treeMenuView.setDropIndicatorShown(True)
        self.listExcludedView.setModel(self.listModel)

    def edit(self, bundleItem):
        if bundleItem.mainMenu != None:
            self.treeModel.setMainMenu(bundleItem.mainMenu)
            if "excludedItems" in bundleItem.mainMenu:
                self.listModel.setExcludedItems(bundleItem.mainMenu['excludedItems'])

def loadManager():
    from prymatex.support.manager import PMXSupportPythonManager
    def loadCallback(message):
        print message
    manager = PMXSupportPythonManager()
    manager.addNamespace('prymatex', os.path.abspath('../prymatex/share'))
    userPath = os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex'))
    print userPath
    manager.addNamespace('user', userPath)
    manager.loadSupport(loadCallback)
    return manager
    
if __name__ == "__main__":
    from pprint import pprint
    manager = loadManager()
    app = QtGui.QApplication(sys.argv)
    window = PMXBundleWidget(manager)
    html = manager.getBundle("4676FC6D-6227-11D9-BFB1-000D93589AF6")
    window.edit(html)
    window.show()
    sys.exit(app.exec_())