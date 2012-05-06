#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui

from prymatex.ui.dialogs.profile import Ui_ProfileDialog

class PMXProfileDialog(QtGui.QDialog, Ui_ProfileDialog):
    def __init__(self, profilesFilePath, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.application = QtGui.QApplication.instance()
        self.profilesFilePath = profilesFilePath
        self.config = ConfigParser()
        if not self.config.read(profilesFilePath):
            self.config.add_section("General")
            self.config.add_section("Profile0")
            self.config.set("General", "DontAskAtStartup", 0)
            self.config.set("Profile0", "Name", self.application.settings.PMX_PROFILE_NAME)
            self.config.set("Profile0", "Path", self.application.settings.PMX_PROFILE_PATH)
            self.config.set("Profile0", "Default", 1)
            self.saveProfile()
        self.setupListProfiles()

    def setupListProfiles(self):
        self.listProfiles.clear()
        for section in self.config.sections():
            if section.startswith("Profile"):
                self.listProfiles.addItem(QtGui.QListWidgetItem(self.config.get(section, "Name")))
        self.checkDontAsk.setCheckState(int(self.config.get("General", "DontAskAtStartup")))
        
    def on_checkDontAsk_stateChanged(self, state):
        self.config.set("General", "DontAskAtStartup", state)
        self.saveProfile()

    def on_buttonExit_pressed(self):
        QtGui.QApplication.exit(0)
        
    def on_buttonStartPrymatex_pressed(self):
        print self.config.sections()
        self.accept()
    
    def saveProfile(self):
        f = open(self.profilesFilePath, "w")
        self.config.write(f)
        f.close()

    @classmethod
    def switchProfile(cls, profilesFilePath, parent = None):
        dlg = cls(profilesFilePath, parent = parent)
        if dlg.exec_() == cls.Accepted:
            return "default"
