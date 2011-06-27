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
        #Settings
        self.settings = self.pmxApp.settings.getGroup('Editor')

        #Manager and Modelo
        self.manager = self.pmxApp.supportManager
        self.tableView.setModel(self.manager.themeStyleProxyModel)
        
        #Combo Theme
        for theme in self.pmxApp.supportManager.getAllThemes():
            self.comboThemes.addItem(theme.name, QtCore.QVariant(theme.uuid))
        self.comboThemes.currentIndexChanged[int].connect(self.themesChanged)
        
        self.colorDialog = QtGui.QColorDialog(self)
        self.colorDialog.setOption(QtGui.QColorDialog.ShowAlphaChannel, True)
        
        self.pushForeground.pressed.connect(lambda element = 'foreground': self.on_pushColor_pressed(element))
        self.pushBackground.pressed.connect(lambda element = 'background': self.on_pushColor_pressed(element))
        self.pushSelection.pressed.connect(lambda element = 'selection': self.on_pushColor_pressed(element))
        self.pushInvisibles.pressed.connect(lambda element = 'invisibles': self.on_pushColor_pressed(element))
        self.pushLineHighlight.pressed.connect(lambda element = 'lineHighlight': self.on_pushColor_pressed(element))
        self.pushCaret.pressed.connect(lambda element = 'caret': self.on_pushColor_pressed(element))
        
        self.syncFont()
        
    def on_pushChangeFont_pressed(self):
        font, ok = QtGui.QFontDialog.getFont(QtGui.QFont(), self, self.trUtf8("Select editor font"))
        if ok:
            self.settings.setValue('font', font)
            self.syncFont()
    
    def on_colorDialog_currentColorChanged(self, element):
        uuid = self.comboThemes.itemData(self.comboThemes.currentIndex()).toPyObject()
        theme = self.manager.getTheme(unicode(uuid))
        rgba = self.colorDialog.currentColor()
        theme.update({'settings': { element: rgba }})
        self.setThemeSettings(theme)
    
    def on_pushColor_pressed(self, element):
        uuid = self.comboThemes.itemData(self.comboThemes.currentIndex()).toPyObject()
        theme = self.manager.getTheme(unicode(uuid))
        settings = theme.settings
        self.colorDialog.setCurrentColor(settings[element])
        self.colorDialog.open(lambda element = element: self.on_colorDialog_currentColorChanged(element))
    
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
    
    def getRGB(self, color):
        rgba = hex(color.rgba())[2:-1]
        values = []
        for index in range(0, len(rgba), 2):
            values.append(str(int(rgba[index:index + 2], 16)))
        return values[1:]
    
    def setThemeSettings(self, theme):
        settings = theme.settings
        self.pushForeground.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['foreground'])) + ");")
        self.pushBackground.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['background'])) + ");")
        self.pushSelection.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['selection'])) + ");")
        self.pushInvisibles.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['invisibles'])) + ");")
        self.pushLineHighlight.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['lineHighlight'])) + ");")
        self.pushCaret.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['caret'])) + ");")
        self.manager.themeStyleProxyModel.setFilterRegExp(unicode(theme.uuid))
        self.settings.setValue('theme', unicode(theme.uuid))
    
    def themesChanged(self, index):
        uuid = self.comboThemes.itemData(index).toPyObject()
        theme = self.manager.getTheme(unicode(uuid))
        self.setThemeSettings(theme)
        