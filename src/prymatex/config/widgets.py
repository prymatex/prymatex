from PyQt4.Qt import *
from prymatex.lib.i18n import ugettext as _



class PMXBasicConfTitileWidget(QWidget):
    '''
    
    '''
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        label = QLabel(_("General configuration"))
        layout.addWidget(label)
        layout.addStretch()
        self.setStyleSheet('''
        QLabel {
            font-size: 17pt;
            padding-left: 10%;    
            font-weight: bold;
            border-bottom: 1px solid #ccc;
            }
        ''')
        self.hide()
    
