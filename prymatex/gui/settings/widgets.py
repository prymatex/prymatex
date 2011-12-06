#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import Qt
from PyQt4.QtNetwork import QNetworkProxy
from prymatex.core.base import PMXObject

#from prymatex.ui.configupdates import Ui_Updates
#from prymatex.ui.configsave import Ui_Save
from prymatex.ui.settings.network import Ui_Network
from prymatex.ui.settings.general import Ui_General
#from prymatex.ui.settings.bundles import Ui_Bundles
import constants
from prymatex.ui.settings.filemanager import Ui_FileManagerDialog
from prymatex.core.settings import pmxConfigPorperty

#class PMXConfigTreeView(QtGui.QTreeView):
#    _model = None
#    
#    widgetChanged = QtCore.pyqtSignal(int)
#    
#    def __init__(self, parent = None):
#        super(PMXConfigTreeView, self).__init__(parent)
#        self.setAnimated(True)
#        self.setHeaderHidden(True)
#        raise Exception("X")
#    
#    def currentChanged(self, new, old):
#        model = self.model()#.sourceModel()
#        new, old = map( lambda indx: model.itemFromIndex(indx), (new, old))
#        #print new, old, map(type, [old, new])
#        self.widgetChanged.emit(new.widget_index)
#    
#    
#    def showEvent(self):
#        super(PMXConfigTreeView, self).showEvent()
#        print self.currentIndex()
#===============================================================================
# 
#===============================================================================
CONFIG_WIDGETS = (QtGui.QLineEdit, QtGui.QSpinBox, QtGui.QCheckBox,)

filter_config_widgets = lambda ws: filter(lambda w: isinstance(w, CONFIG_WIDGETS), ws)

class PMXConfigBaseWidget(QtGui.QWidget, PMXObject):
    '''
    Base class for configuration widgets
    '''
    _widgets = None
    
    @property
    def all_widgets(self):
        if not self._widgets:
            self._widgets = filter_config_widgets(self.children())
        return self._widgets
    
    def enableAllWidgets(self, enabled):
        map(lambda w: w.setEnabled(enabled), self.all_widgets)
    
    def apply(self):
        QtGui.QMessageBox.information(self, "Apply %s..." % self.windowTitle(), "Apply settings")
    
    def discard(self):
        QtGui.QMessageBox.information(self, "Discard %s..." % self.windowTitle(), "Discard settings")

# class PMXUpdatesWidget(QtGui.QWidget, Ui_Updates):
#    def __init__(self, parent = None):
#        super(PMXUpdatesWidget, self).__init__(parent)
#        self.setupUi(self)

class PMXConfigBaseWidget(QtGui.QWidget):
    pass

class PMXGeneralWidget(QtGui.QWidget, Ui_General, PMXObject):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        
        #self.comboTabVisibility.addItem("Always shown", PMXTabWidget.TABBAR_ALWAYS_SHOWN)
        #self.comboTabVisibility.addItem("Show when more than one", PMXTabWidget.TABBAR_WHEN_MULTIPLE)
        #self.comboTabVisibility.addItem("Never show", PMXTabWidget.TABBAR_NEVER_SHOWN)
        
        self.tabwidgetSettingsGroup = self.application.settings.getGroup('TabWidget')
        self.mainwindowSettingsGroup = self.application.settings.getGroup('MainWindow')
        
        self.comboTabVisibility.currentIndexChanged.connect(self.tabVisibilityChanged)
        self.comboApplicationTitle.editTextChanged.connect(self.updateMainWindowTitle)
        
    def tabVisibilityChanged(self, index):
        value = self.comboTabVisibility.itemData(index)
        self.tabwidgetSettingsGroup.setValue('showTabBar', value)
    
    def appendToCombo(self, text):
        
        current_index = self.comboApplicationTitle.currentIndex()
        #print "Current index", current_index
        current_text = self.comboApplicationTitle.currentText()
        text = unicode(current_text or '') + unicode(text or '')
        self.comboApplicationTitle.setItemText(current_index, text)
        #print "Settings text", text
    
    def on_pushInsertAppName_pressed(self):
        self.appendToCombo(" $APPNAME")
        
    def on_pushInsertFile_pressed(self):
        self.appendToCombo(" $FILENAME")
        
    def on_pushInsertProject_pressed(self):
        self.appendToCombo(" $PROJECT")
    
    def updateMainWindowTitle(self, text):
        self.mainwindowSettingsGroup.setValue('windowTitleTemplate', unicode(text))
        

 
#class PMXSaveWidget(QtGui.QWidget, Ui_Save):
#    def __init__(self, parent = None):
#        QtGui.QWidget.__init__(self, parent)
#        self.setupUi(self)
#        for code, alias, lang in CODECS_CODEC_ALIAS_LANG:
#            name = "%s%s %s" % (code, alias and " (%s)" % alias or '', lang)
#            self.comboEncodings.addItem(name, None)

class PMXFileManagerSettings(QtGui.QWidget, Ui_FileManagerDialog, PMXObject):
    SETTINGS_GROUP = 'FileSaveSettings'
    #DEFAULTS = {}
    
    @pmxConfigPorperty(default = "unix")
    def lineEndings(self, ending):
        self.comboBoxLineEnding.setCurrentIndex(self.comboBoxLineEnding.findData(ending))

    @pmxConfigPorperty(default = 'utf-8')
    def encoding(self, enc):
        self.comboBoxEncoding.setCurrentIndex(self.comboBoxEncoding.findData(enc))
        
    
    def __init__(self, parent = None):
        super(PMXFileManagerSettings, self).__init__(parent)
        self.setupUi(self)
        self.loadEncodings()
        self.setupLineEndings()
        self.configure()
    

    def setupLineEndings(self):
        ''' Populate line endings '''
        self.comboBoxLineEnding.addItem(r"Unix (\n)", "unix")
        self.comboBoxLineEnding.addItem(r"Windows (\r\n)", "windows")
    
    @QtCore.pyqtSignature("int")
    def on_comboBoxLineEnding_currentIndexChanged(self, index):
        data = self.comboBoxLineEnding.itemData(index)
        self.lineEndings = data
        self.settings.setValue('lineEndings', data)
    
    def loadEncodings(self):
        ''' Populate ComboBox from constants '''
        from constants import TM_CODECS
        
        for codec_line in TM_CODECS.split('\n'):
            if not codec_line:
                continue
            userData, titleInformation = codec_line.split('    ', 1)
            title_data = titleInformation.split('   ')
            if len(title_data) > 1:
                title = "%s (%s)" % (title_data[-1].strip().title(), title_data[0])
            else:
                title = "%s (%s)" % (title_data, userData)
            self.comboBoxEncoding.addItem(title.strip().title(), userData.replace('_', '-'))
    

class PMXNetworkWidget(QtGui.QWidget, Ui_Network, PMXObject):
    '''
    Setup network connection
    '''
    SETTINGS_GROUP = "Network"
        
    def __init__(self, parent = None):
        super(PMXNetworkWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.radioAutomatically.setToolTip("Not implemented yet")
        self.radioAutomatically.setEnabled(False)
        for radio in (
                      self.radioAutomatically,
                      self.radioBasedOnVariables,
                      self.radioDirect,
                      self.radioManual,
                      self.radioPAC,
                      ):
            radio.toggled.connect(self.changeProxyMode)
        
        self.mapping = {
                        self.radioAutomatically: 'automatic',
                        self.radioBasedOnVariables: 'enviroment',
                        self.radioDirect: 'direct',
                        self.radioManual: 'manual',
                        self.radioPAC: 'pac',                
        }
        
        self.comboProxyType.addItem(self.trUtf8("HTTP Proxy"), QNetworkProxy.HttpProxy)
        self.comboProxyType.addItem(self.trUtf8("Socks 5 Proxy"), QNetworkProxy.Socks5Proxy)
        self.configure()
        
    
    def changeProxyMode(self, checked):
        if checked:
            self.proxyType = self.mapping[self.sender()]

    def proxyType(self, value):
        if   value == 'direct':
            if not self.radioDirect.isChecked():
                self.radioDirect.setChecked(True)
            proxy = QNetworkProxy(QNetworkProxy.NoProxy)
            QNetworkProxy.setApplicationProxy(proxy)
        elif value == 'pac':
            if not self.radioPAC.isChecked():
                self.radioPAC.setChecked(True)
        elif value == 'manual':
            if not self.radioManual.isChecked():
                self.radioManual.setChecked(True)
        elif value == 'enviroment':
            if not self.radioBasedOnVariables.isChecked():
                self.radioBasedOnVariables.setChecked(True)
        elif value == 'automatic':
            if not self.radioAutomatically.isChecked():
                self.radioAutomatically.setChecked(True)
        else:
            raise ValueError("%s is not a valid proxyType value" % value)
        
    def proxyManual(self, value):
        url = QtCore.QUrl(value)
        self.lineProxyAddress.setText(url.host())
        self.spinProxyPort.setValue(int(url.port()))
        self._proxyManual = url
    
    def proxyEnviromentVariable(self, value):
        self._proxyEnviromentVariable = value
     
