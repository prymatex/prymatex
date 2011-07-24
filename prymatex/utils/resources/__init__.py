import subprocess
import os
from prymatex.utils.deco import memoize

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
    def getIcon(self, iconName, preferedInPath=None):
        if self.cache:
            cacheKey = (iconName, preferedInPath)
            if not self._iconCache.has_key(cacheKey):
                self._iconCache[cacheKey] = self._findIconPath(iconName, preferedInPath)
            else:
                print "Hit!"
            return self._iconCache[cacheKey]
        else:
            return self._findIconPath(iconName, preferedInPath)
    
    @memoize
    def _findIconPath(self, iconName, preferedInPath=None):
        '''
        Gets icon path from KDE resource system
        '''
        if isinstance(preferedInPath, basestring):
            preferedInPath = (preferedInPath, )
        matches = []
        for basePath in self.iconPaths:
            for root, dir, files in os.walk(basePath, followlinks = True):
                for filename in files:
                    name, ext = os.path.splitext(filename)
                    if name == iconName:
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
    print resouceManager.getIcon('folder',)