# -*- encoding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.Qt import QStandardItemModel, QModelIndex
from PyQt4.Qt import QStandardItem, QIcon, QPixmap
from PyQt4.Qt import Qt, QListView, QTableView, pyqtSignal
from os.path import expanduser, exists
import os
import thread
from urllib import unquote, unquote_plus
from prymatex.core.base import PMXObject

class PMXBookmarksBaseModel(QStandardItemModel):
    def __init__(self, parent = None):
        super(PMXBookmarksBaseModel, self).__init__(0, 2, parent)
        self.loadBookmarks()
        
    def loadBookmarks(self):
        '''
        This method should populate the model
        '''
        raise NotImplementedError()
    
    def addItem(self, text, path, icon = QIcon() ):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)
        item.setIcon(icon)
        item.setToolTip(path)
        self.appendRow([item, QStandardItem(path)])

class PMXBookmarksEmptyModel(PMXBookmarksBaseModel):
    def loadBookmarks(self):
        pass

class PMXBookmarkModelFactory(PMXObject):
    
    __model = None
    @property
    def bookmarksModel(self):
        if not self.__model:
            try:
                self.__model = PMXBookmarksKDE4Model(self)
            except:
                self.__model = PMXBookmarksEmptyModel(self)
        return self.__model
        
    
class PMXBookmarksKDE4Model(PMXBookmarksBaseModel):
    #thread.start_new(self.loadBookmarks, (bookmarks_path, ))
    
    def findIconInMetadata(self, bookmark):
        icon = ''
        for mdata in bookmark.find('info/metadata'):
            if mdata.tag.endswith('icon'):
                icon = mdata.attrib['name']
                break
        #TODO: Obterner el icono de donde corresponde
        return icon
    
    def getKDEBookmarksPath(self):
        ''' @return: kde bookmark XML file '''
        path = expanduser('~/.kde/share/apps/kfileplaces/bookmarks.xml')
        if not exists(path):
            from prymatex.core.exceptions import FileDoesNotExistError
            raise FileDoesNotExistError("Can't read KDE 4 bookmarks :(")
        return path
                
    def loadBookmarks(self):
        path = self.getKDEBookmarksPath()
        from lxml import etree
        bookmarks_tree = etree.parse(path)
        for bookmark in bookmarks_tree.findall('bookmark'):
            href = bookmark.attrib['href']
            if not href.startswith('file://'):
                #print "%s not supported", href
                continue
            path = unquote_plus(href.replace('file://', '').encode('utf-8'))
            icon = self.findIconInMetadata(bookmark)
            
            title = bookmark.find('title').text
            self.addItem(title, path, icon)
    

class PMXBookmarksListView(QListView):
    '''
    Bookmarks view
    '''
    pathChangeRequested = QtCore.pyqtSignal(str)
    
    def __init__(self, parent = None):
        super(PMXBookmarksListView, self).__init__(parent)
        self.modelFactory = PMXBookmarkModelFactory(self)
        self.setModel(self.modelFactory.bookmarksModel)
        self.doubleClicked.connect(self.itemDoubleClicked)
    
    def itemDoubleClicked(self, index):
        path = self.model().index(index.row(), 1).data()
        self.pathChangeRequested.emit(path)
        
        
if __name__ == "__main__":
    from PyQt4.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    def test_signal(path):
        print "You clicked ", path
    win = PMXBookmarksListView()
    win.pathChangeRequested.connect(test_signal)
    win.show()
    
    sys.exit(app.exec_())
    