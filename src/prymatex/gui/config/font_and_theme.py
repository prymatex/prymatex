from PyQt4 import QtCore, QtGui
from prymatex.gui.config.ui_font_and_theme import Ui_FontThemeConfig
from prymatex.gui.config.widgets import PMXConfigBaseWidget
from prymatex.core.base import PMXObject

class PMXThemeConfigWidget(PMXConfigBaseWidget, Ui_FontThemeConfig, PMXObject):
    '''
    Changes font and theme
    '''
    def __init__(self, parent = None):
        super(PMXThemeConfigWidget, self).__init__(parent)
        self.setupUi(self)
        self.manager = self.pmxApp.supportManager
        
        #Modelo
        self.tableView.setModel(self.manager.themeStyleProxyModel)
        
        self.settings = self.pmxApp.settings.getGroup('Editor')
        uuid = self.settings.value('theme')
        
        #Combo Theme
        for index, theme in enumerate(self.pmxApp.supportManager.getAllThemes()):
            self.comboThemes.addItem(theme.name, QtCore.QVariant(theme.uuid))
            if theme.uuid == uuid:
                self.comboThemes.setCurrentIndex(index)
        self.comboThemes.currentIndexChanged[int].connect(self.themesChanged)
        self.syncFont()
        
    def on_pushChangeFont_pressed(self):
        font, ok = QtGui.QFontDialog.getFont(QtGui.QFont(), self, self.trUtf8("Select editor font"))
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
            #print "Can't get settings font"
            font = QtGui.QFont()
        self.lineFont.setFont(font)
        self.lineFont.setText("%s, %d" % (font.family(), font.pointSize()))
    
    def themesChanged(self, index):
        uuid = self.comboThemes.itemData(index).toPyObject()
        self.settings.setValue('theme', unicode(uuid))
