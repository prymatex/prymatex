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

from prymatex.ui.support.bundle import Ui_Menu
from prymatex.utils import zeromqt

class PMXBundleWidget(QtGui.QWidget, Ui_Menu):
    TYPE = 'bundle'
    BUNDLEITEM = 0
    SEPARATOR = 1
    SUBMENU = 2
    NEWGROUP = 3
    NEWSEPARATOR = 4
    def __init__(self, manager, parent = None):
        from prymatex.gui.support.models import PMXMenuTreeModel
        from prymatex.gui.support.models import PMXExcludedListModel
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.context = zeromqt.ZeroMQTContext(parent = self)
        self.socket = self.context.socket(zeromqt.REP)
        self.socket.bind('tcp://127.0.0.1:10001')
        self.socket.readyRead.connect(self.socketReadyRead)
        self.socket.readyWrite.connect(self.socketReadyWrite)
        self.publisher = self.context.socket(zeromqt.PUB)
        self.publisher.bind('tcp://127.0.0.1:10002')
        
        self.manager = manager
        self.treeModel = PMXMenuTreeModel(manager)
        self.listModel = PMXExcludedListModel(manager)
        self.treeMenuView.setModel(self.treeModel)
        self.treeMenuView.setAcceptDrops(True)
        self.treeMenuView.setDropIndicatorShown(True)
        self.listExcludedView.setModel(self.listModel)
        self.treeMenuView.collapsed.connect(self.nodeCollapsed) 

    def socketReadyWrite(self):
        print "puedo mandar"
        self.socket.send("oka")
        
    def socketReadyRead(self):
        print self.socket.recv()
    
    def nodeCollapsed(self, index):
        print "send"
        self.publisher.send_pyobj({"Node": index.data(), "Row": index.row(), "Column": index.column()})
    
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