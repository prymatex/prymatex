# Some search widgets


from PyQt4.QtGui import QComboBox
from PyQt4.QtCore import Qt

class PMXCommonSearchBox(QComboBox):
    '''
    Common behaviour between the search and replace widgtets
    '''
    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key_Escape:
            self.parent().hide()
        super(PMXCommonSearchBox, self).keyPressEvent(key_event)

class PMXFindBox(PMXCommonSearchBox):
    pass


class PMXReplaceBox(PMXCommonSearchBox):
    pass