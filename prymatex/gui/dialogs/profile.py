#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui

from prymatex.utils.i18n import ugettext as _
from prymatex.core.settings import PMXSettings
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
        self.setupDialogProfiles()
        
    def setupDialogProfiles(self):
        self.profiles = []
        self.listProfiles.clear()
        defaultProfile = None
        for section in self.config.sections():
            if section.startswith("Profile"):
                profile = { "name": self.config.get(section, "name"),
                            "path": self.config.get(section, "path"),
                            "default": self.config.getboolean(section, "default")}
                if profile["default"]:
                    defaultProfile = profile
                self.listProfiles.addItem(QtGui.QListWidgetItem(profile["name"]))
                self.profiles.append(profile)
        self.checkDontAsk.setChecked(self.config.getboolean("General", "dontask"))
        self.listProfiles.setCurrentRow(defaultProfile is not None and self.profiles.index(defaultProfile) or 0)
        
    def on_checkDontAsk_clicked(self):
        self.config.set("General", "dontask", str(self.checkDontAsk.isChecked()))
        self.saveProfiles()

    def on_buttonExit_pressed(self):
        QtGui.QApplication.exit(0)
        
    def on_buttonStartPrymatex_pressed(self):
        index = self.listProfiles.currentRow()
        defaultProfile = self.profiles[index]
        for profile in self.profiles:
            profile["default"] = defaultProfile == profile
        self.saveProfiles()
        self.accept()
    
    def on_buttonCreate_pressed(self):
        profileName, ok = QtGui.QInputDialog.getText(self, _("Create profile"), _(CREATE_MESSAGE))
        while profileName in map(lambda profile: profile["name"], self.profiles):
            profileName, ok = QtGui.QInputDialog.getText(self, _("Create profile"), _(CREATE_MESSAGE))
        if ok:
            profile = { "name": profileName,
                        "path": PMXSettings.get_prymatex_profile_path(profileName),
                        "default": 0}
            self.listProfiles.addItem(QtGui.QListWidgetItem(profile["name"]))
            self.profiles.append(profile)
            self.saveProfiles()

    def on_buttonRename_pressed(self):
        index = self.listProfiles.currentRow()
        rprofile = self.profiles[index]
        profileName, ok = QtGui.QInputDialog.getText(self, _("Rename profile"), _(RENAME_MESSAGE) % rprofile["name"])
        while profileName in map(lambda profile: profile["name"], filter(lambda profile: profile != rprofile, self.profiles)):
            profileName, ok = QtGui.QInputDialog.getText(self, _("Rename profile"), _(RENAME_MESSAGE) % rprofile["name"])
        if ok:
            rprofile["name"] = profileName
            self.saveProfiles()
                
    def on_buttonDelete_pressed(self):
        index = self.listProfiles.currentRow()
        dprofile = self.profiles[index]
        result = QtGui.QMessageBox.question(self, _("Delete Profile"),
            _(DELETE_MESSAGE) % dprofile["path"],
            buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.Ok | QtGui.QMessageBox.Discard,
            defaultButton = QtGui.QMessageBox.Ok)
        if result == QtGui.QMessageBox.Yes:
            shutil.rmtree(dprofile["path"])
            self.profiles = filter(lambda profile: profile != dprofile, self.profiles)
            self.saveProfiles()
        elif result == QtGui.QMessageBox.Ok:
            self.profiles = filter(lambda profile: profile != dprofile, self.profiles)
            self.saveProfiles()

    def saveProfiles(self):
        f = open(self.profilesFilePath, "w")
        for section in self.config.sections():
            if section.startswith("Profile"):
                self.config.remove_section(section)
        for index, profile in enumerate(self.profiles):
            section = "Profile%d" % index
            self.config.add_section(section)
            for key, value in profile.iteritems():
                self.config.set(section, key, str(value))
        self.config.write(f)
        f.close()
        self.setupDialogProfiles()

    @classmethod
    def switchProfile(cls, profilesFilePath, parent = None):
        dlg = cls(profilesFilePath, parent = parent)
        dlg.buttonStartPrymatex.setText("Restart Prymatex")
        dlg.buttonExit.setVisible(False)
        if dlg.exec_() == cls.Accepted:
            QtGui.QApplication.exit(3)

    @classmethod
    def selectProfile(cls, profilesFilePath, parent = None):
        dlg = cls(profilesFilePath, parent = parent)
        if dlg.exec_() == cls.Accepted:
            return dlg.profiles[dlg.listProfiles.currentRow()]["name"]
