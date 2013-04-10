#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import shutil
from ConfigParser import ConfigParser

from prymatex.qt import QtCore, QtGui

from prymatex.core.profile import PMXProfile as PrymatexProfile
from prymatex.core.config import PMX_HOME_PATH
from prymatex.core import PMXBaseComponent

from prymatex.models.profiles import ProfilesListModel
from prymatex.models.settings import SettingsTreeModel
from prymatex.models.settings import SortFilterSettingsProxyModel

from prymatex.gui.dialogs.profile import ProfileDialog

# The very very first manager
class ProfileManager(QtCore.QObject, PMXBaseComponent):
    PRYMATEX_PROFILES_NAME = "profiles.ini"
    DEFAULT_PROFILE_NAME = "default"

    def __init__(self, application):
        QtCore.QObject.__init__(self, application)
        PMXBaseComponent.__init__(self)
        
        self.profilesListModel = ProfilesListModel(self)
        
        self.__dontAsk = True
        
        self.profilesFile = os.path.join(PMX_HOME_PATH, self.PRYMATEX_PROFILES_NAME)
        config = ConfigParser()
        if os.path.exists(self.profilesFile):
            config.read(self.profilesFile)
            for section in config.sections():
                if section.startswith("Profile"):
                    name = config.get(section, "name")
                    path = config.get(section, "path")
                    default = config.getboolean(section, "default")
                    profile = PrymatexProfile(name, path, default)
                    self.profilesListModel.addProfile(profile)
            self.__dontAsk = config.getboolean("General", "dontAsk")
        else:
            self.createProfile(self.DEFAULT_PROFILE_NAME, default = True)

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


    def saveProfiles(self):
        config = ConfigParser()
        config.add_section("General")
        config.set("General", "dontask", str(self.__dontAsk))
        for index, profile in enumerate(self.profilesListModel.profiles()):
            section = "Profile%d" % index
            config.add_section(section)
            config.set(section, "name", profile.PMX_PROFILE_NAME)
            config.set(section, "path", profile.PMX_PROFILE_PATH)
            config.set(section, "default", profile.PMX_PROFILE_DEFAULT)
        f = open(self.profilesFile, "w")
        config.write(f)
        f.close()


    def createProfile(self, name, path = None, default = False):
        name = name.lower()
        profile = self.profilesListModel.findProfileByName(name)
        if profile is None:
            path = path if path is not None else os.path.abspath(os.path.join(PMX_HOME_PATH, name))
            if not os.path.exists(path):
                self.build_prymatex_profile(path)
            profile = PrymatexProfile(name, path)
            self.profilesListModel.addProfile(profile)
            self.setDefaultProfile(profile)
            self.saveProfiles()
            return profile

    def currentProfile(self, value = None):
        if value is None or not self.__dontAsk:
            return ProfileDialog.selectStartupProfile(self)
        elif value == "":
            return self.defaultProfile()
        profile = self.profilesListModel.findProfileByName(value)
        if profile is None:
            profile = self.createProfile(value, default = True)
        return profile


    def renameProfile(self, profile, newName):
        newName = newName.lower()
        profile = self.profilesListModel.findProfileByName(profile.PMX_PROFILE_NAME)
        
        profile.PMX_PROFILE_NAME = newName.lower()
        self.profilesListModel.layoutChanged.emit()
        self.saveProfiles()
        return newName


    def deleteProfile(self, profile, files = False):
        self.profilesListModel.removeProfile(profile)
        if files:
            shutil.rmtree(profile.PMX_PROFILE_PATH)
        self.saveProfiles()


    def profileNames(self):
        return map(lambda p: p.PMX_PROFILE_NAME, self.profilesListModel.profiles())


    def setDontAsk(self, value):
        self.__dontAsk = value
        self.saveProfiles()

    def dontAsk(self):
        return self.__dontAsk

    def setDefaultProfile(self, profile):
        # Unset all ?
        for p in self.profilesListModel.profiles():
            p.PMX_PROFILE_DEFAULT = False
        profile.PMX_PROFILE_DEFAULT = True
        self.saveProfiles()

    def defaultProfile(self):
        for profile in self.profilesListModel.profiles():
            if profile.PMX_PROFILE_DEFAULT:
                return profile

    # ------------------- Settings
    def registerSettingsWidget(self, widget):
        self.settingsTreeModel.addConfigNode(widget)


    def loadSettings(self):
        self.settingsTreeModel.loadSettings()