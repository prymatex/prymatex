import os, sys
sys.path.append(os.path.abspath('..'))
from PyQt4 import QtGui
if __name__ == "__main__":
    from prymatex.support.manager import PMXSupportManager
    from prymatex.gui.support.qtadapter import buildKeySequence, buildKeyEquivalent
    supportManager = PMXSupportManager()
    supportManager.addNamespace('prymatex', os.path.abspath('../prymatex/share'))
    supportManager.addNamespace('user', os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex')))
    supportManager.loadSupport()
    for item in supportManager.BUNDLE_ITEMS.values():
        if item.keyEquivalent:
            code = buildKeySequence(item.keyEquivalent)
            keyequ = buildKeyEquivalent(code)
            print "%s --> %d --> %s --> %s" % (item.keyEquivalent, code, QtGui.QKeySequence(code).toString(format=QtGui.QKeySequence.NativeText), keyequ)
    
