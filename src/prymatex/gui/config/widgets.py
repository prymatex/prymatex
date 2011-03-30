from PyQt4.QtGui import QTreeView, QWidget, qApp
from PyQt4.Qt import QString

from PyQt4.QtCore import pyqtSignal, pyqtSignature

settings = qApp.instance().settings

class PMXConfigTreeView(QTreeView):
    _model = None
    
    widgetChanged = pyqtSignal(int)
    
    def __init__(self, parent = None):
        super(PMXConfigTreeView, self).__init__(parent)
        self.setAnimated(True)
        self.setHeaderHidden(True)
        
    def currentChanged(self, new, old):
        model = self.model()#.sourceModel()
        new, old = map( lambda indx: model.itemFromIndex(indx), (new, old))
        print new, old, map(type, [old, new])
        self.widgetChanged.emit(new.widget_index)

from ui_font_and_theme import Ui_FontThemeConfig
from prymatex.bundles import PMXTheme

class PMXThemeConfigWidget(QWidget, Ui_FontThemeConfig):
    def __init__(self, parent = None):
        super(PMXThemeConfigWidget, self).__init__(parent)
        self.setupUi(self)
        for theme in PMXTheme.THEMES.values():
            self.comboThemes.addItem(theme.name)
        self.comboThemes.currentIndexChanged[QString].connect(self.themesChanged)
                                 
    def themesChanged(self, name):
        settings.editor.theme_name = unicode(name)

from ui_updates import Ui_Updates
class PMXUpdatesWidget(QWidget, Ui_Updates):
    def __init__(self, parent = None):
        super(PMXUpdatesWidget, self).__init__(parent)
        self.setupUi(self)
        
from ui_general import Ui_General
class PMXGeneralWidget(QWidget, Ui_General):
    def __init__(self, parent = None):
        super(PMXGeneralWidget, self).__init__(parent)
        self.setupUi(self)
        
        
from ui_save import Ui_Save 
class PMXSaveWidget(QWidget, Ui_Save):
    def __init__(self, parent = None):
        super(PMXSaveWidget, self).__init__(parent)
        self.setupUi(self)