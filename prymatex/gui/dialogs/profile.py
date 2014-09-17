#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.core.components import PrymatexDialog

from prymatex.utils.i18n import ugettext as _
from prymatex.ui.dialogs.profile import Ui_ProfileDialog

DELETE_MESSAGE = """Deleting a profile will remove the profile from the list of available profiles and cannot be undone.
You may also choose to delete the profile data files, including your settings and other user-related data. This option will delete the folder %s and cannot be undone.
Would you like to delete the profile data files?"""

RENAME_MESSAGE = """Rename the profile %s to:"""

CREATE_MESSAGE = """Enter new profile name:"""

class ProfileDialog(PrymatexDialog, Ui_ProfileDialog, QtWidgets.QDialog):
    
    def __init__(self, **kwargs):
        super(ProfileDialog, self).__init__(**kwargs)
        self.setupUi(self)

    def setProfileManager(self, manager):
        self.manager = manager
        self.listViewProfiles.setModel(self.manager.profilesListModel)
        self.checkDontAsk.setChecked(self.manager.dontAsk())
        
    def initialize(self, **kwargs):
        super(ProfileDialog, self).initialize(**kwargs)
        self.setProfileManager(self.application().profileManager)
    
    def on_checkDontAsk_clicked(self):
        self.manager.setDontAsk(self.checkDontAsk.isChecked())
        
    def on_buttonExit_pressed(self):
        QtGui.QApplication.exit(0)
        
    def on_buttonStartPrymatex_pressed(self):
        self.accept()

    def on_buttonCreate_pressed(self):
        profileName, ok = QtGui.QInputDialog.getText(self, _("Create profile"), _(CREATE_MESSAGE))
        while profileName in self.manager.profileNames():
            profileName, ok = QtGui.QInputDialog.getText(self, _("Create profile"), _(CREATE_MESSAGE))
        if ok:
            self.manager.createProfile(profileName, default = True)


    def on_buttonRename_pressed(self):
        profile = self.manager.profilesListModel.profile(self.listViewProfiles.currentIndex())
        profileNewName, ok = QtGui.QInputDialog.getText(self, _("Rename profile"), _(RENAME_MESSAGE) % profile.PMX_PROFILE_NAME, text=profile.PMX_PROFILE_NAME)
        while profileNewName in self.manager.profileNames():
            profileNewName, ok = QtGui.QInputDialog.getText(self, _("Rename profile"), _(RENAME_MESSAGE) % profile.PMX_PROFILE_NAME, text=profileNewName)
        if ok:
            self.manager.renameProfile(profile, profileNewName)


    def on_buttonDelete_pressed(self):
        profile = self.manager.profilesListModel.profile(self.listViewProfiles.currentIndex())
        result = QtGui.QMessageBox.question(self, _("Delete Profile"),
            _(DELETE_MESSAGE) % profile.PMX_PROFILE_NAME,
            buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.Ok | QtGui.QMessageBox.Discard,
            defaultButton = QtGui.QMessageBox.Ok)
        if result != QtGui.QMessageBox.Discard:
            self.manager.deleteProfile(profile, result == QtGui.QMessageBox.Yes)

            
    def switchProfile(self, title="Switch profile"):
        currentProfileName = self.manager.defaultProfile().PMX_PROFILE_NAME
        self.setWindowTitle(title)
        self.buttonStartPrymatex.setText("Restart Prymatex")
        self.buttonExit.setVisible(False)
        return self.exec_()


    @classmethod
    def selectStartupProfile(cls, profileManager):
        dlg = cls()
        dlg.setProfileManager(profileManager)
        if dlg.exec_() == cls.Accepted:
            return dlg.manager.defaultProfile()
