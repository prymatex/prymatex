from PyQt4.QtGui import *
from prymatex.lib.i18n import ugettext as _

class PMXStatusBar(QStatusBar):
    def __init__(self, parent ):
        QStatusBar.__init__(self, parent)
        self.lineLabel = QLabel(_("Line: %6d", 0), self)
        self.columnLabel = QLabel(_("Column: %6d", 0), self)
        self.langComboBox = QComboBox(self)
        self.indentModeComboBox = QComboBox(self)
        self.indentModeComboBox.addItem("Soft Tab")
        self.indentModeComboBox.addItem("Hard Tab")
        self.indentWidthComboBox = QComboBox(self)
        for w in [1,2, 3, 4, 8]:
            self.indentWidthComboBox.addItem(str(w))
        
        self.addPermanentWidget(self.lineLabel)
        self.addPermanentWidget(self.columnLabel)
        self.addPermanentWidget(self.langComboBox)
        self.addPermanentWidget(self.indentModeComboBox)
        self.addPermanentWidget(self.indentWidthComboBox)
        self.showMessage("Alfa", 4000)