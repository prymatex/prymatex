# -*- encoding: utf-8 -*-
from PyQt4.Qt import QStandardItemModel
from PyQt4.Qt import QStandardItem, QIcon, QPixmap
from PyQt4.Qt import Qt, QListView, QTableView
from os.path import expanduser, exists
import os
import thread
from prymatex.utils.resources import PMXKDE4ResourceManager

class PMXBookmarksBaseModel(QStandardItemModel):
    pass


class PMXBookmarksKDE4Model(PMXBookmarksBaseModel):
    # In kde we should parse 
    # $USER/.kde/share/apps/kfileplaces
    def __init__(self, parent = None):
        super(PMXBookmarksKDE4Model, self).__init__(parent)
        bookmarks_path = expanduser('~/.kde/share/apps/kfileplaces/bookmarks.xml')
        if not exists(bookmarks_path):
            from prymatex.core.exceptions import FileDoesNotExistError
            raise FileDoesNotExistError("Can't read KDE 4 bookmarks :(")
        self.resourceManager = PMXKDE4ResourceManager()

        #self.loadBookmarks(bookmarks_path)
        thread.start_new(self.loadBookmarks, (bookmarks_path, ))
        
        
    
    
    def findIconInMetadata(self, bookmark):
        icon = ''
        for mdata in bookmark.find('info/metadata'):
            if mdata.tag.endswith('icon'):
                icon = mdata.attrib['name']
                break
        if exists(icon):
            return QIcon(QPixmap(icon))
        else:
            # resource?
            iconPath = self.resourceManager.getIcon(icon, '32x32')
            return QIcon(QPixmap(iconPath))
            
                
    def loadBookmarks(self, path):
        from lxml import etree
        bookmarks_tree = etree.parse(path)
        for bookmark in bookmarks_tree.findall('bookmark'):
            href = bookmark.attrib['href']
            if not href.startswith('file://'):
                #print "%s not supported", href
                continue
            icon = self.findIconInMetadata(bookmark)
            
            title = bookmark.find('title').text
            item = QStandardItem(title) 
            item.setToolTip(href)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if icon:
                item.setIcon(icon)
            self.appendRow(item)
            print "Row"


class PMXBookmarksListView(QListView):
    def __init__(self, parent = None):
        super(PMXBookmarksListView, self).__init__(parent)
        self.setModel(PMXBookmarksKDE4Model(self))
        self.itemDoubleClicked.connect(self.openBookmark)
    
    
        
    
        
    
if __name__ == "__main__":
    from PyQt4.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    win = PMXBookmarksListView()
    win.show()
    
    sys.exit(app.exec_())
    
    

