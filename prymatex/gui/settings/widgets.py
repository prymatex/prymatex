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

CONFIG_WIDGETS = (QtGui.QLineEdit, QtGui.QSpinBox, QtGui.QCheckBox,)

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
    def __init__(self, parent = None):
        super(PMXFileManagerSettings, self).__init__(parent)
        self.setupUi(self)
        self.loadEncodings()
    
#    for codline in constants.TM_CODECS:
#    code, alias, lang = codline.split('    ')
#    #print code.upper().replace('_', '-'), '(', alias, ')', lang.strip().title()
#    CODECS_CODEC_ALIAS_LANG.append( (code.upper().replace('_', '-').strip(), 
#                                     alias.strip(), 
#                                     lang.strip().title(), ) 
#    )
        
    def loadEncodings(self):
        from constants import TM_CODECS
        
        for codec_line in TM_CODECS.split('\n'):
            print ">>>", codec_line
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
    class Meta:
        settings = 'network'
        
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
     
