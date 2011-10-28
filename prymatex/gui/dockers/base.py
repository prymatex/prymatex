from PyQt4 import QtGui

class PMXBaseDock(object):
    MENU_KEY_SEQUENCE = None
    def __init__(self):
        """"""
        if self.MENU_KEY_SEQUENCE:
            keysequence = QtGui.QKeySequence(self.MENU_KEY_SEQUENCE)
            self.toggleViewAction().setShortcut(keysequence)
            
