#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex import resources

class ProfilesListModel(QtCore.QAbstractListModel):
    def __init__(self, profileManager, parent = None): 
        QtCore.QAbstractListModel.__init__(self, parent)
        self.profileManager = profileManager
        self.__profiles = []


    # ------------------ QtCore.QAbstractListModel methods
    def rowCount(self, parent = None):
        return len(self.__profiles)


    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        profile = self.__profiles[index.row()]
        if role == QtCore.Qt.DisplayRole:
            return profile.PMX_PROFILE_NAME
        elif role == QtCore.Qt.CheckStateRole:
            if profile.PMX_PROFILE_DEFAULT:
                return 2
            return 0
        elif role == QtCore.Qt.ToolTipRole:
            return profile.PMX_PROFILE_PATH
        elif role == QtCore.Qt.DecorationRole:
            return resources.getIcon("user-identity")


    def setData(self, index, data, role):
        profile = self.__profiles[index.row()]
        if role == QtCore.Qt.CheckStateRole and profile.PMX_PROFILE_DEFAULT == False:
            self.profileManager.setDefaultProfile(profile)
            self.layoutChanged.emit()
            return True


    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable


    # ------------------ Custom functions
    def profiles(self):
        return self.__profiles


    def findProfileByName(self, name):
        for profile in self.__profiles:
            if profile.PMX_PROFILE_NAME == name:
                return profile


    def profile(self, index):
        return self.__profiles[index.row()]


    def selectedProfile(self):
        for profile in self.__profiles:
            if profile.PMX_PROFILE_DEFAULT:
                return profile


    # ------------------ Add remove keywords
    def addProfile(self, profile):
        self.__profiles.append(profile)
        self.layoutChanged.emit()
        
    def removeProfile(self, profile):
        self.__profiles.remove(profile)
        self.layoutChanged.emit()
