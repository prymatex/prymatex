from PyQt4.Qt import *

from ui_choosetab import Ui_ChooseTab


class ChooseTabDialog(QDialog, Ui_ChooseTab):
    '''
    Choose tab
    '''
    def __init__(self, parent):
        super(ChooseTabDialog, self).__init__(parent)
        self.setupUi(self)
        self.getParentTabs()

    def getParentTabs(self):
        # todo
        pass

    def centerInParent(self):
        ''' Should we implement this? This should be automatic '''
        parent_geo = self.parent().geometry()
        pass