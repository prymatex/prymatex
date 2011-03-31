from PyQt4.QtGui import *
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

#===============================================================================
# 
#===============================================================================
CONFIG_WIDGETS = (QLineEdit, QSpinBox, QCheckBox,)

filter_config_widgets = lambda ws: filter(lambda w: isinstance(w, CONFIG_WIDGETS), ws)

class PMXConfigBaseWidget(QWidget):
    _widgets = None
    
    @property
    def all_widgets(self):
        if not self._widgets:
            self._widgets = filter_config_widgets(self.children())
        return self._widgets

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
        
from ui_network import Ui_Network
class PMXNetworkWidget(PMXConfigBaseWidget, Ui_Network):
    def __init__(self, parent = None):
        super(PMXNetworkWidget, self).__init__(parent)
        self.setupUi(self)
        self.comboProxyType.currentIndexChanged[QString].connect(self.changeProxyType)
   
    
    def changeProxyType(self, proxy_type):
        proxy_type = unicode(proxy_type).lower()
        
        if proxy_type.count("no proxy"):
            map(lambda w: w.setEnabled(False), self.all_widgets)
        else:
            map(lambda w: w.setEnabled(True), self.all_widgets)
        
