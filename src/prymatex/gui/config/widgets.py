from PyQt4.QtGui import *
from PyQt4.Qt import QString, Qt

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
        
CODECS = '''
ascii    646, us-ascii    English
big5    big5-tw, csbig5    Traditional Chinese
big5hkscs    big5-hkscs, hkscs    Traditional Chinese
cp037    IBM037, IBM039    English
cp424    EBCDIC-CP-HE, IBM424    Hebrew
cp437    437, IBM437    English
cp500    EBCDIC-CP-BE, EBCDIC-CP-CH, IBM500    Western Europe
cp720         Arabic
cp737         Greek
cp775    IBM775    Baltic languages
cp850    850, IBM850    Western Europe
cp852    852, IBM852    Central and Eastern Europe
cp855    855, IBM855    Bulgarian, Byelorussian, Macedonian, Russian, Serbian
cp856         Hebrew
cp857    857, IBM857    Turkish
cp858    858, IBM858    Western Europe
cp860    860, IBM860    Portuguese
cp861    861, CP-IS, IBM861    Icelandic
cp862    862, IBM862    Hebrew
cp863    863, IBM863    Canadian
cp864    IBM864    Arabic
cp865    865, IBM865    Danish, Norwegian
cp866    866, IBM866    Russian
cp869    869, CP-GR, IBM869    Greek
cp874         Thai
cp875         Greek
cp932    932, ms932, mskanji, ms-kanji    Japanese
cp949    949, ms949, uhc    Korean
cp950    950, ms950    Traditional Chinese
cp1006         Urdu
cp1026    ibm1026    Turkish
cp1140    ibm1140    Western Europe
cp1250    windows-1250    Central and Eastern Europe
cp1251    windows-1251    Bulgarian, Byelorussian, Macedonian, Russian, Serbian
cp1252    windows-1252    Western Europe
cp1253    windows-1253    Greek
cp1254    windows-1254    Turkish
cp1255    windows-1255    Hebrew
cp1256    windows-1256    Arabic
cp1257    windows-1257    Baltic languages
cp1258    windows-1258    Vietnamese
euc_jp    eucjp, ujis, u-jis    Japanese
euc_jis_2004    jisx0213, eucjis2004    Japanese
euc_jisx0213    eucjisx0213    Japanese
euc_kr    euckr, korean, ksc5601, ks_c-5601, ks_c-5601-1987, ksx1001, ks_x-1001    Korean
gb2312    chinese, csiso58gb231280, euc- cn, euccn, eucgb2312-cn, gb2312-1980, gb2312-80, iso- ir-58    Simplified Chinese
gbk    936, cp936, ms936    Unified Chinese
gb18030    gb18030-2000    Unified Chinese
hz    hzgb, hz-gb, hz-gb-2312    Simplified Chinese
iso2022_jp    csiso2022jp, iso2022jp, iso-2022-jp    Japanese
iso2022_jp_1    iso2022jp-1, iso-2022-jp-1    Japanese
iso2022_jp_2    iso2022jp-2, iso-2022-jp-2    Japanese, Korean, Simplified Chinese, Western Europe, Greek
iso2022_jp_2004    iso2022jp-2004, iso-2022-jp-2004    Japanese
iso2022_jp_3    iso2022jp-3, iso-2022-jp-3    Japanese
iso2022_jp_ext    iso2022jp-ext, iso-2022-jp-ext    Japanese
iso2022_kr    csiso2022kr, iso2022kr, iso-2022-kr    Korean
latin_1    iso-8859-1, iso8859-1, 8859, cp819, latin, latin1, L1    West Europe
iso8859_2    iso-8859-2, latin2, L2    Central and Eastern Europe
iso8859_3    iso-8859-3, latin3, L3    Esperanto, Maltese
iso8859_4    iso-8859-4, latin4, L4    Baltic languages
iso8859_5    iso-8859-5, cyrillic    Bulgarian, Byelorussian, Macedonian, Russian, Serbian
iso8859_6    iso-8859-6, arabic    Arabic
iso8859_7    iso-8859-7, greek, greek8    Greek
iso8859_8    iso-8859-8, hebrew    Hebrew
iso8859_9    iso-8859-9, latin5, L5    Turkish
iso8859_10    iso-8859-10, latin6, L6    Nordic languages
iso8859_13    iso-8859-13, latin7, L7    Baltic languages
iso8859_14    iso-8859-14, latin8, L8    Celtic languages
iso8859_15    iso-8859-15, latin9, L9    Western Europe
iso8859_16    iso-8859-16, latin10, L10    South-Eastern Europe
johab    cp1361, ms1361    Korean
koi8_r         Russian
koi8_u         Ukrainian
mac_cyrillic    maccyrillic    Bulgarian, Byelorussian, Macedonian, Russian, Serbian
mac_greek    macgreek    Greek
mac_iceland    maciceland    Icelandic
mac_latin2    maclatin2, maccentraleurope    Central and Eastern Europe
mac_roman    macroman    Western Europe
mac_turkish    macturkish    Turkish
ptcp154    csptcp154, pt154, cp154, cyrillic-asian    Kazakh
shift_jis    csshiftjis, shiftjis, sjis, s_jis    Japanese
shift_jis_2004    shiftjis2004, sjis_2004, sjis2004    Japanese
shift_jisx0213    shiftjisx0213, sjisx0213, s_jisx0213    Japanese
utf_32    U32, utf32    all languages
utf_32_be    UTF-32BE    all languages
utf_32_le    UTF-32LE    all languages
utf_16    U16, utf16    all languages
utf_16_be    UTF-16BE    all languages (BMP only)
utf_16_le    UTF-16LE    all languages (BMP only)
utf_7    U7, unicode-1-1-utf-7    all languages
utf_8    U8, UTF, utf8    all languages
utf_8_sig         all languages'''.split('\n')

CODECS = filter(len, CODECS)
CODECS_CODEC_ALIAS_LANG = []
for codline in CODECS:
    code, alias, lang = codline.split('    ')
    #print code.upper().replace('_', '-'), '(', alias, ')', lang.strip().title()
    CODECS_CODEC_ALIAS_LANG.append( (code.upper().replace('_', '-').strip(), 
                                     alias.strip(), 
                                     lang.strip().title(), ) 
    )

from ui_save import Ui_Save 
class PMXSaveWidget(QWidget, Ui_Save):
    def __init__(self, parent = None):
        super(PMXSaveWidget, self).__init__(parent)
        self.setupUi(self)
        for code, alias, lang in CODECS_CODEC_ALIAS_LANG:
            name = "%s%s %s" % (code, alias and " (%s)" % alias or '', lang)
            self.comboEncodings.addItem(name, None)
        
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



    
from ui_envvars import Ui_EnvVariables
class PMXEnvVariablesWidgets(PMXConfigBaseWidget, Ui_EnvVariables):
    '''
    Variables
    '''
    def __init__(self, parent = None):
        super(PMXEnvVariablesWidgets, self).__init__(parent)
        self.setupUi(self)
        self.tableVariables.setColumnCount(2)
        self.tableVariables.setHorizontalHeaderItem(0, 
                                                    QTableWidgetItem(self.trUtf8("Name")))
        self.tableVariables.setHorizontalHeaderItem(1, 
                                                    QTableWidgetItem(self.trUtf8("Value")))
        self.tableVariables.setUpdatesEnabled(True)
        self.tableVariables.cellChanged.connect(self.updateCellWidths)
        #self.tableVariables.model().setHeaderData(0, Qt.Horizontal, self.trUtf8("Name"))
        #self.tableVariables.model().setHeaderData(1, Qt.Horizontal, self.trUtf8("Value"))
        
    def updateCellWidths(self, _row, _column):
        self.tableVariables.resizeColumnsToContent(0)
        
    def on_pushAdd_pressed(self):
        r = self.tableVariables.insertRow(0)
        print r
        
    def on_pushRemove_pressed(self):
        pass


