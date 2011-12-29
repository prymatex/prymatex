from prymatex.gui.dockers.base import PMXBaseDock
from PyQt4 import QtGui, QtCore
import os
from prymatex.utils.i18n import ugettext as _

class PMXFileSystemTasks(PMXBaseDock):
    '''
    Groups FileSystem and Project actions, it's a facade of the PMXFileManager
    that displays dialogs and handle common exceptions
    '''
    def createDirectory(self, basePath = None):
        
        basePath = basePath or self.currentPath()
        while True:
            newDirName, accepted = QtGui.QInputDialog.getText(self, _("Create Directory"), 
                                                        _("Please specify the new directory name"), 
                                                        text = _("New Folder"))
            if accepted:
                absNewDirName = os.path.join(basePath, newDirName)
                try:
                    rslt = self.application.fileManager.createDirectory(absNewDirName)
                except Exception as e:
                    continue
                else:
                    print("Created", rslt)
                    break
            else:
                return
    
    def createFileFromTemplate(self, basePath):
        pass
    
    def createFile(self, basePath):
        pass
    
    