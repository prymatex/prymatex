#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import shutil
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from prymatex.qt import QtCore, QtGui

from prymatex.core.profile import PrymatexProfile
from prymatex.core.config import PMX_PROFILES_PATH
from prymatex.core import PrymatexComponent

from prymatex.models.profiles import ProfilesListModel

from prymatex.gui.dialogs.profile import ProfileDialog

# The very very first manager
class ProfileManager(PrymatexComponent, QtCore.QObject):
    # ------------- Settings
    SETTINGS = 'ProfileManager'
    PMX_PROFILES_FILE = "profiles.ini"
    DEFAULT_PROFILE_NAME = "default"

    def __init__(self, **kwargs):
        super(ProfileManager, self).__init__(**kwargs)
        
        self.profilesListModel = ProfilesListModel(self)
        
        self.__current_profile = None
        self.__dontAsk = True
        
        self.profilesFile = os.path.join(PMX_PROFILES_PATH, self.PMX_PROFILES_FILE)
        config = configparser.RawConfigParser()
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

    # --------------- Profile
    def saveProfiles(self):
        config = configparser.RawConfigParser()
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
            if path is None:
                path = os.path.abspath(os.path.join(PMX_PROFILES_PATH, name))
            profile = PrymatexProfile(name, path)
            self.profilesListModel.addProfile(profile)
            self.setDefaultProfile(profile)
            self.saveProfiles()
            return profile

    def install(self):
        suggested = self.application().options.profile
        if suggested is None or not self.__dontAsk:
            self.__current_profile = ProfileDialog.selectStartupProfile(self)
        elif suggested == "":
            self.__current_profile = self.defaultProfile()
        else:
            self.__current_profile = self.profilesListModel.findProfileByName(suggested)
        if self.__current_profile is None:
            self.__current_profile = self.createProfile(suggested, default = True)
        self.__current_profile.ensure_paths()
    
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
        return [ p.PMX_PROFILE_NAME for p in self.profilesListModel.profiles() ]

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

    def profileForClass(self, componentClass):
        return self.currentProfile()
            
    def currentProfile(self):
        return self.__current_profile

    def defaultProfile(self):
        for profile in self.profilesListModel.profiles():
            if profile.PMX_PROFILE_DEFAULT:
                return profile

