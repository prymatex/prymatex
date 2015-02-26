#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtCore
from prymatex.utils import json, plist

from . import notifier

from prymatex.core.config import (TM_PREFERENCES_PATH,
    PMX_SETTINGS_NAME, PMX_STATE_NAME, TM_SETTINGS_NAME)

class PrymatexProfile(object):
    def __init__(self, name, path, default=True):
        self.PMX_PROFILE_NAME = name
        self.PMX_PROFILE_PATH = path
        self.PMX_PROFILE_DEFAULT = default
        self.PMX_TMP_PATH = os.path.join(self.PMX_PROFILE_PATH, 'tmp')
        self.PMX_LOG_PATH = os.path.join(self.PMX_PROFILE_PATH, 'log')
        self.PMX_CACHE_PATH = os.path.join(self.PMX_PROFILE_PATH, 'cache')
        self.PMX_SCREENSHOT_PATH = os.path.join(self.PMX_PROFILE_PATH, 'screenshot')
        self.PMX_SETTINGS_PATH = os.path.join(self.PMX_PROFILE_PATH, PMX_SETTINGS_NAME)
        self.PMX_STATE_PATH = os.path.join(self.PMX_PROFILE_PATH, PMX_STATE_NAME)
        self.TM_PREFERENCES_PATH = os.path.join(TM_PREFERENCES_PATH, TM_SETTINGS_NAME)
        
    # ------------------------ Paths
    def ensure_paths(self):
        new_paths = filter(lambda p: not os.path.exists(p), (self.PMX_PROFILE_PATH, 
            self.PMX_TMP_PATH, self.PMX_LOG_PATH, self.PMX_CACHE_PATH, self.PMX_SCREENSHOT_PATH))
        for new_path in new_paths:
            os.makedirs(new_path, 0o700)

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return self.settings.get(name, default)
