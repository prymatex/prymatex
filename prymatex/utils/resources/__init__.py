import subprocess
import os

from PyQt4.Qt import QIcon, QThread, QPixmap


class PMXKDE4ResourceManager(object):
    
    KDE_CONFIG_ICON_PATH_CMD = "kde4-config --path icon".split()
    
    def __init__(self, deferredLoading=False, cache = True):
        self.deferredLoading = deferredLoading
        self.cache = cache
    
    _iconPaths = None
    @property
    def iconPaths(self):
        if not self._iconPaths:
            paths = subprocess.check_output(self.KDE_CONFIG_ICON_PATH_CMD)
            self._iconPaths = paths.strip('\n').split(':')
        return self._iconPaths

    _iconCache = {}
    def getIcon(self, iconName):
        if self.cache:
            cacheKey = (iconName, )
            if not self._iconCache.has_key(cacheKey):
                self._iconCache[cacheKey] = self._loadIcon(iconName, )
            return self._iconCache[cacheKey]
        else:
            return QIcon.fromTheme(iconName, fallback=QIcon(QPixmap(iconName)))
        
    def _loadIcon(self, name):
        if os.path.exists(name):
            return QIcon(QPixmap(name))
        else:
            return QIcon.fromTheme(name, fallback = QIcon())
        

def findFileName(searchPaths, fileName, preferedInPath=None, exts=None):
    '''
    Generic function for resouce crawling under a path
    @param searchPaths: Paths where resource should be searched in
    @param fileName: The name, i.e. "folder"
    @param preferedInPath: A string or list of parts expected in the path (i.e. 32x32)
    @param exts: Extensions
    '''
    if isinstance(preferedInPath, basestring):
        preferedInPath = (preferedInPath, )
    if isinstance(exts, basestring):
        exts = (exts, )
    exts = map(lambda s: s.lower(), exts)
        
    matches = []
    for basePath in searchPaths:
        for root, dir, files in os.walk(basePath, followlinks = True):
            for filename in files:
                name, ext = os.path.splitext(filename)
                if name == fileName:
                    if exts and not ext.lower() in exts:
                        continue
                    fullpath = os.path.join(root, filename)
                    if preferedInPath:
                        for part in preferedInPath:
                            if part in root:
                                return fullpath
                            else:
                                matches.append(fullpath)
                    else:
                        return fullpath
    if matches:
        return matches[0]

if __name__ == "__main__":
    resouceManager = PMXKDE4ResourceManager()
    icon =  resouceManager.getIcon('folder',)
    print icon.isNull()
    