#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui

from prymatex.utils.i18n import ugettext as _
from prymatex.core.settings import PMXProfile
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
        self.listProfiles.clear()
        defaultProfile = None
        defaultIndex = 0
        for index, profileName in enumerate(PMXProfile.PMX_PROFILES):
            self.listProfiles.addItem(QtGui.QListWidgetItem(QtGui.QIcon.fromTheme("user-identity"), profileName))
            if PMXProfile.PMX_PROFILE_DEFAULT == profileName:
                defaultIndex = index
        self.checkDontAsk.setChecked(PMXProfile.PMX_PROFILES_DONTASK)
        self.listProfiles.setCurrentRow(defaultIndex)
        
    def on_checkDontAsk_clicked(self):
        PMXProfile.PMX_PROFILES_DONTASK = self.checkDontAsk.isChecked()
        PMXProfile.saveProfiles()
        
    def on_buttonExit_pressed(self):
        QtGui.QApplication.exit(0)
        
    def on_buttonStartPrymatex_pressed(self):
        PMXProfile.PMX_PROFILE_DEFAULT = self.listProfiles.item(self.listProfiles.currentRow()).data(QtCore.Qt.DisplayRole)
        PMXProfile.saveProfiles()
        self.accept()
    
    def on_buttonCreate_pressed(self):
        profileName, ok = QtGui.QInputDialog.getText(self, _("Create profile"), _(CREATE_MESSAGE))
        while profileName in PMXProfile.PMX_PROFILES.keys():
            profileName, ok = QtGui.QInputDialog.getText(self, _("Create profile"), _(CREATE_MESSAGE))
        if ok:
            profileName = PMXProfile.createProfile(profileName)
            self.listProfiles.addItem(QtGui.QListWidgetItem(QtGui.QIcon.fromTheme("user-identity"), profileName))

    def on_buttonRename_pressed(self):
        profileOldName = self.listProfiles.item(self.listProfiles.currentRow()).data(QtCore.Qt.DisplayRole)
        profileNewName, ok = QtGui.QInputDialog.getText(self, _("Rename profile"), _(RENAME_MESSAGE) % profileOldName, text=profileOldName)
        while profileNewName in PMXProfile.PMX_PROFILES.keys():
            profileNewName, ok = QtGui.QInputDialog.getText(self, _("Rename profile"), _(RENAME_MESSAGE) % profileOldName, text=profileNewName)
        if ok:
            newName = PMXProfile.renameProfile(profileOldName, profileNewName)
            self.listProfiles.item(self.listProfiles.currentRow()).setData(QtCore.Qt.DisplayRole, newName)

    def on_buttonDelete_pressed(self):
        item = self.listProfiles.item(self.listProfiles.currentRow())
        profileOldName = item.data(QtCore.Qt.DisplayRole)
        result = QtGui.QMessageBox.question(self, _("Delete Profile"),
            _(DELETE_MESSAGE) % profileOldName,
            buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.Ok | QtGui.QMessageBox.Discard,
            defaultButton = QtGui.QMessageBox.Ok)
        if result != QtGui.QMessageBox.Discard:
            PMXProfile.deleteProfile(profileOldName, result == QtGui.QMessageBox.Yes)
            self.listProfiles.removeItemWidget(item)
            
    @classmethod
    def switchProfile(cls, profilesFilePath, parent = None):
        dlg = cls(profilesFilePath, parent = parent)
        dlg.buttonStartPrymatex.setText("Restart Prymatex")
        dlg.buttonExit.setVisible(False)
        if dlg.exec_() == cls.Accepted:
            return PMXProfile.PMX_PROFILE_DEFAULT

    @classmethod
    def selectProfile(cls, profilesFilePath, parent = None):
        dlg = cls(profilesFilePath, parent = parent)
        if dlg.exec_() == cls.Accepted:
            return PMXProfile.PMX_PROFILE_DEFAULT
