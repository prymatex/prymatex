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
    '''
    Changes font and theme
    '''
    def __init__(self, parent = None):
        super(PMXThemeConfigWidget, self).__init__(parent)
        self.setupUi(self)
        for theme in PMXTheme.THEMES.values():
            self.comboThemes.addItem(theme.name)
        self.comboThemes.currentIndexChanged[QString].connect(self.themesChanged)
        self.settings = qApp.instance().settings.getGroup('editor')
        self.syncFont()
        
    def on_pushChangeFont_pressed(self):
        font, ok = QFontDialog.getFont(QFont(), self, self.trUtf8("Select editor font"))
        if ok:
            self.settings.setValue('font', font)
            self.syncFont()
    
    def syncFont(self):
        '''
        Syncs font with the lineEdit
        '''
        
        try:
            font = self.settings.font
        except Exception, _e:
            print "Can't get settings font"
            font = QFont()
        self.lineFont.setFont(font)
        self.lineFont.setText("%s, %d" % (font.family(), font.pointSize()))
    
    def themesChanged(self, name):
        self.settings.setValue('theme', unicode(name))

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

from ui_bundles import Ui_Bundles
class PMXBundleWidget(PMXConfigBaseWidget, Ui_Bundles):
    def __init__(self, parent = None):
        super(PMXConfigBaseWidget, self).__init__(parent)
        self.setupUi(self)
        
    def on_pushAddPath_pressed(self):
        pth = QFileDialog.getExistingDirectory(self, self.trUtf8("Select bundle dir"))
    
    def on_pushRemove_pressed(self):
        print "Remove"
    
    def on_pushEdit_pressed(self):
        print "Edit"
        
