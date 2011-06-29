from PyQt4 import QtCore, QtGui
from prymatex.gui.config.ui_themes import Ui_FontThemeConfig
from prymatex.gui.config.widgets import PMXConfigBaseWidget
from prymatex.core.base import PMXObject

class PMXThemeConfigWidget(PMXConfigBaseWidget, Ui_FontThemeConfig, PMXObject):
    '''
    Changes font and theme
    '''
    DEFAULTS = {'settings': {'background': '#FFFFFF',
                             'caret': '#000000',
                             'foreground': '#000000',
                             'invisibles': '#BFBFBF',
                             'lineHighlight': '#00000012',
                             'selection': '#A6CBFF' },
                #Names and scopes
                'styles': [ ('Comment', 'comment'),
                            ('String', 'string'),
                            ('Number', 'constant.numeric'),
                            ('Built-in constant', 'constant.language'),
                            ('User-defined constant', 'constant.character, constant.other'),
                            ('Variable', 'variable.language, variable.other'),
                            ('Keyword', 'keyword'),
                            ('Storage', 'storage'),
                            ('Class name', 'entity.name.class'),
                            ('Inherited class', 'entity.other.inherited-class'),
                            ('Function name', 'entity.name.function'),
                            ('Function argument', 'variable.parameter'),
                            ('Tag name', 'entity.name.tag'),
                            ('Tag attribute', 'entity.other.attribute-name'),
                            ('Library function', 'support.function'),
                            ('Library constant', 'support.constant'),
                            ('Library class/type', 'support.type, support.class'),
                            ('Library variable', 'support.other.variable'),
                            ('Invalid', 'invalid')]
                }

    def __init__(self, parent = None):
        super(PMXThemeConfigWidget, self).__init__(parent)
        self.setupUi(self)
        #Settings
        self.settings = self.pmxApp.settings.getGroup('Editor')

        #Manager
        self.manager = self.pmxApp.supportManager
        
        self.configComboBoxThemes()
        self.configTableView()
        self.configPushButton()
    
    #==========================================================
    # ComboBoxThemes
    #==========================================================
    def on_comboBoxThemes_Changed(self, index):
        uuid = self.comboBoxThemes.itemData(index).toPyObject()
        theme = self.manager.getTheme(unicode(uuid))
        self.setThemeSettings(theme)
        
    def configComboBoxThemes(self):
        #Combo Theme
        for theme in self.manager.getAllThemes():
            self.comboBoxThemes.addItem(theme.name, QtCore.QVariant(str(theme.uuid).upper()))
        self.comboBoxThemes.currentIndexChanged[int].connect(self.on_comboBoxThemes_Changed)
        uuid = self.settings.value('theme')
        self.comboBoxThemes.setCurrentIndex(self.comboBoxThemes.findData(QtCore.QVariant(uuid.upper())))
    
    #==========================================================
    # TableView
    #==========================================================
    def on_tableView_Activated(self, index):
        style = self.manager.themeStyleProxyModel.mapToSource(index).internalPointer()
        self.comboBoxScope.setEditText(style.scope) 
    
    def on_comboBoxScope_changed(self, string):
        print string
    
    def configTableView(self):
        self.tableView.setModel(self.manager.themeStyleProxyModel)
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableView.activated.connect(self.on_tableView_Activated)
        self.tableView.pressed.connect(self.on_tableView_Activated)
        #Conectar
        for _, scope in self.DEFAULTS['styles']:
            self.comboBoxScope.addItem(scope)
        self.comboBoxScope.currentIndexChanged[str].connect(self.on_comboBoxScope_changed)
        self.comboBoxScope.editTextChanged.connect(self.on_comboBoxScope_changed)
    
    #==========================================================
    # Push Button
    #==========================================================
    def configPushButton(self):
        #Colors
        self.pushButtonForeground.pressed.connect(lambda element = 'foreground': self.on_pushButtonColor_pressed(element))
        self.pushButtonBackground.pressed.connect(lambda element = 'background': self.on_pushButtonColor_pressed(element))
        self.pushButtonSelection.pressed.connect(lambda element = 'selection': self.on_pushButtonColor_pressed(element))
        self.pushButtonInvisibles.pressed.connect(lambda element = 'invisibles': self.on_pushButtonColor_pressed(element))
        self.pushButtonLineHighlight.pressed.connect(lambda element = 'lineHighlight': self.on_pushButtonColor_pressed(element))
        self.pushButtonCaret.pressed.connect(lambda element = 'caret': self.on_pushButtonColor_pressed(element))
        #Font
        self.pushButtonChangeFont.pressed.connect(self.on_pushButtonChangeFont_pressed)
        font = self.settings.value('font')
        self.lineFont.setFont(font)
        self.lineFont.setText("%s, %d" % (font.family(), font.pointSize()))
    
    def on_pushButtonChangeFont_pressed(self):
        font = self.settings.value('font')
        font, ok = QtGui.QFontDialog.getFont(font, self, self.trUtf8("Select editor font"))
        if ok:
            self.settings.setValue('font', font)
            self.lineFont.setFont(font)
            self.lineFont.setText("%s, %d" % (font.family(), font.pointSize()))
    
    def on_pushButtonColor_pressed(self, element):
        uuid = self.comboBoxThemes.itemData(self.comboBoxThemes.currentIndex()).toPyObject()
        theme = self.manager.getTheme(unicode(uuid))
        settings = theme.settings
        color = QtGui.QColorDialog.getColor(settings[element], self)
        if color:
            theme.update({'settings': { element: color }})
            self.setThemeSettings(theme)
    
    def getRGB(self, color):
        rgba = hex(color.rgba())[2:-1]
        values = []
        for index in range(0, len(rgba), 2):
            values.append(str(int(rgba[index:index + 2], 16)))
        return values[1:]
    
    def setThemeSettings(self, theme):
        settings = theme.settings
        self.pushButtonForeground.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['foreground'])) + ");")
        self.pushButtonBackground.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['background'])) + ");")
        self.pushButtonSelection.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['selection'])) + ");")
        self.pushButtonInvisibles.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['invisibles'])) + ");")
        self.pushButtonLineHighlight.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['lineHighlight'])) + ");")
        self.pushButtonCaret.setStyleSheet("background-color: rgb(" + ", ".join(self.getRGB(settings['caret'])) + ");")
        self.manager.themeStyleProxyModel.setFilterRegExp(unicode(theme.uuid))
        self.settings.setValue('theme', unicode(theme.uuid))
        