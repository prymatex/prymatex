#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui

from prymatex.utils.i18n import ugettext as _
from prymatex.ui.dialogs.profile import Ui_ProfileDialog

DELETE_MESSAGE = """Deleting a profile will remove the profile from the list of available profiles and cannot be undone.
You may also choose to delete the profile data files, including your settings and other user-related data. This option will delete the folder %s and cannot be undone.
Would you like to delete the profile data files?"""

RENAME_MESSAGE = """Rename the profile %s to:"""

CREATE_MESSAGE = """Enter new profile name:"""

class PMXProfileDialog(QtGui.QDialog, Ui_ProfileDialog):
    
    def __init__(self, profilesFilePath, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.application = QtGui.QApplication.instance()
        self.profilesFilePath = profilesFilePath
        self.config = ConfigParser()
        self.config.read(self.profilesFilePath)
        self.setupListProfiles()

    def setupListProfiles(self):
        self.profiles = []
        self.listProfiles.clear()
        for section in self.config.sections():
            if section.startswith("Profile"):
                profile = { "name": self.config.get(section, "name"),
                            "path": self.config.get(section, "path"),
                            "default": self.config.get(section, "default")}
                self.listProfiles.addItem(QtGui.QListWidgetItem(profile["name"]))
                self.profiles.append(profile)
        self.checkDontAsk.setCheckState(self.config.getint("General", "dontask"))
        self.listProfiles.setCurrentRow(0)
        
    def on_checkDontAsk_stateChanged(self, state):
        self.config.set("General", "dontask", state)
        self.saveProfile()

    def on_buttonExit_pressed(self):
        QtGui.QApplication.exit(0)
        
    def on_buttonStartPrymatex_pressed(self):
        self.accept()
    
    def on_listProfiles_currentRowChanged(self):
        print self.listProfiles.currentRow()

    def on_buttonCreate_pressed(self):
        profileName, ok = QtGui.QInputDialog.getText(self, _("Create profile"),
            _(CREATE_MESSAGE))
        if ok:
            print "create", profileName
        
    def on_buttonRename_pressed(self):
        index = self.listProfiles.currentRow()
        profileName, ok = QtGui.QInputDialog.getText(self, _("Rename profile"),
            _(RENAME_MESSAGE) % self.profiles[index]["name"])
        if ok:
            self.profiles[index]["name"] = profileName
                
    def on_buttonDelete_pressed(self):
        index = self.listProfiles.currentRow()
        result = QtGui.QMessageBox.question(self, _("Delete Profile"),
            _(DELETE_MESSAGE) % self.profiles[index]["path"],
            buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.Ok | QtGui.QMessageBox.Discard,
            defaultButton = QtGui.QMessageBox.Ok)
        if result == QtGui.QMessageBox.Yes:
            print "eliminar"
        elif result == QtGui.QMessageBox.Ok:
            print "remover"

    def saveProfile(self):
        f = open(self.profilesFilePath, "w")
        self.config.write(f)
        f.close()

    @classmethod
    def switchProfile(cls, profilesFilePath, parent = None):
        dlg = cls(profilesFilePath, parent = parent)
        if dlg.exec_() == cls.Accepted:
            return "default"

    @classmethod
    def selectProfile(cls, profilesFilePath, parent = None):
        dlg = cls(profilesFilePath, parent = parent)
        if dlg.exec_() == cls.Accepted:
            return "default"