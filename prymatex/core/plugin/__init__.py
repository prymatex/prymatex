#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class PMXBasePlugin(object):
    
    def initialize(self):
        pass
    
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