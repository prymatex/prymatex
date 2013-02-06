#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import shutil
from ConfigParser import ConfigParser

from prymatex.qt import QtCore, QtGui

from prymatex.core.profile import PMXProfile as PrymatexProfile
from prymatex.core.config import PMX_HOME_PATH

from prymatex.models.profiles import ProfilesListModel
from prymatex.models.settings import SettingsTreeModel
from prymatex.models.settings import SortFilterSettingsProxyModel

from prymatex.gui.dialogs.profile import ProfileDialog

# The very very first manager
class ProfileManager(QtCore.QObject):
    PRYMATEX_PROFILES_NAME = "profiles.ini"
    
    def __init__(self, application):
        QtCore.QObject.__init__(self)
        self.application = application
        
        self.profilesListModel = ProfilesListModel(self)
        
        self.defaultProfileName = "default"
        self.dontask = True
        
        self.profilesFile = os.path.join(PMX_HOME_PATH, self.PRYMATEX_PROFILES_NAME)
        config = ConfigParser()
        if os.path.exists(self.profilesFile):
            config.read(self.profilesFile)
            for section in config.sections():
                if section.startswith("Profile"):
                    name = config.get(section, "name")
                    path = config.get(section, "path")
                    default = config.getboolean(section, "default")
                    if default:
                        self.defaultProfileName = name
                    profile = PrymatexProfile(name, path, default)
                    self.profilesListModel.addProfile(profile)
            self.dontask = config.getboolean("General", "dontask")

        # Setting models        
        self.settingsTreeModel = SettingsTreeModel(self)
        self.sortFilterSettingsProxyModel = SortFilterSettingsProxyModel(self)
        self.sortFilterSettingsProxyModel.setSourceModel(self.settingsTreeModel)


    # --------------- Profile
    def build_prymatex_profile(self, path):
        os.makedirs(path)
        os.makedirs(os.path.join(path, 'tmp'), 0700)
        os.makedirs(os.path.join(path, 'log'), 0700)
        os.makedirs(os.path.join(path, 'cache'), 0700)
        os.makedirs(os.path.join(path, 'screenshot'), 0700)


    def get_or_create_profile(self, name, path = None):
        name = name.lower()
        profile = self.profilesListModel.findProfileByName(name)
        if profile is not None:
            return profile, False
        path = path if path is not None else os.path.abspath(os.path.join(PMX_HOME_PATH, name))
        if not os.path.exists(path):
            self.build_prymatex_profile(path)
        profile = PrymatexProfile(name, path)
        self.profilesListModel.addProfile(profile)
        self.saveProfiles()
        return profile, True

        
    def saveProfiles(self):
        config = ConfigParser()
        config.add_section("General")
        config.set("General", "dontask", str(self.dontask))
        for index, profile in enumerate(self.profilesListModel.profiles()):
            section = "Profile%d" % index
            config.add_section(section)
            config.set(section, "name", profile.PMX_PROFILE_NAME)
            config.set(section, "path", profile.PMX_PROFILE_PATH)
            config.set(section, "default", profile.PMX_PROFILE_DEFAULT)
        f = open(self.profilesFile, "w")
        config.write(f)
        f.close()


    def createProfile(self, name):
        profile, created = self.get_or_create_profile(name)
        return profile


    def currentProfile(self, name = None):
        if name is None or (name == "" and not self.dontask):
            #Select profile
            name = ProfileDialog.selectStartupProfile(self)
        elif name == "":
            name = self.defaultProfileName

        return self.createProfile(name)


    def renameProfile(self, profile, newName):
        newName = newName.lower()
        profile = self.profilesListModel.findProfileByName(profile.PMX_PROFILE_NAME)
        profile.PMX_PROFILE_NAME = newName.lower()
        #self.profilesListModel[profile.PMX_PROFILE_NAME] = profile
        self.saveProfiles()
        return newName


    def deleteProfile(self, profile, files = False):
        profile = self.profilesListModel.removeProfile(profile)
        if files:
            shutil.rmtree(profile.PMX_PROFILE_PATH)
        self.saveProfiles()

    def profileNames(self):
        return map(lambda p: p.PMX_PROFILE_NAME, self.profilesListModel.profiles())
        
    # ------------------- Settings
    def registerSettingsWidget(self, widget):
        self.settingsTreeModel.addConfigNode(widget)


    def loadSettings(self):
        self.settingsTreeModel.loadSettings()