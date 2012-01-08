#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

#TODO: en inicialize deberia pasar un proveedro de servicios o otra forma menos directa de que un plguin hable con el core
class PMXBasePlugin(object):
    __app = QtGui.QApplication.instance()
    __mainwindow = None
    __logger = None
    
    def initialize(self):
        pass
    
    #============================================================
    # Shortcut
    #============================================================
    @property
    def mainWindow(self):
        if self.__class__.__mainwindow == None:
            self.__class__.__mainwindow = self
            while self.__class__.__mainwindow.parent() != None:
                self.__class__.__mainwindow = self.__class__.__mainwindow.parent()
        return self.__class__.__mainwindow
    
    @property
    def application(self):
        """
        Shortcut property for PyQt4.QtGui.QApplication.instance().
        """
        return self.__app
    #============================================================
    # Logger
    #============================================================
    @property
    def logger(self):
        from logging import getLogger
        if self.__logger is None:
            t = type(self)
            loggername = '.'.join([t.__module__, t.__name__])
            self.__class__.__logger = getLogger(loggername)
        return self.__logger
    
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg)
    
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg)
    
    def warn(self, msg, *args, **kwargs):
        self.logger.warn(msg)
    
    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg)