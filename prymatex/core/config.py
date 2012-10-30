#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""
Application configuration based on Qt's QSettings module.
"""
import sys, os, plistlib
from prymatex.utils.misc import get_home_dir

#==============================================================================
# Debug helpers
#==============================================================================
STDOUT = sys.stdout
STDERR = sys.stderr
DEBUG = True

#==============================================================================
# Configuration paths
#==============================================================================
USER_HOME_PATH = get_home_dir()
PRYMATEX_HOME_NAME = ".prymatex"
TEXTMATE_WEBPREVIEW_NAME = "com.macromates.textmate.webpreview.plist"
TEXTMATE_PREFERENCE_NAMES = ["Library", "Preferences"]

def get_prymatex_app_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_prymatex_home_path():
    path = os.path.join(USER_HOME_PATH, PRYMATEX_HOME_NAME)
    if not os.path.exists(path):
        os.makedirs(path)
    #Create extra paths
    for extra in ['Bundles', 'Themes', 'Plugins']:
        extraPath = os.path.join(path, extra)
        if not os.path.exists(extraPath):
            os.makedirs(extraPath, 0700)
    return path

def get_textmate_preferences_user_path():
    path = os.path.join(USER_HOME_PATH, *TEXTMATE_PREFERENCE_NAMES)
    if not os.path.exists(path):
        os.makedirs(path)
    #Create extra files
    webpreview = os.path.join(path, TEXTMATE_WEBPREVIEW_NAME)
    if not os.path.exists(webpreview):
        plistlib.writePlist({"SelectedTheme": "bright"}, webpreview)
    return path

def get_conf_path(filename=None):
    """Return absolute path for configuration file with specified filename"""
    # TODO: Hacerlo para el profile
    from prymatex.utils.misc import get_home_dir
    conf_dir = os.path.join(get_home_dir(), PRYMATEX_HOME_NAME)
    if not os.path.isdir(conf_dir):
        os.mkdir(conf_dir)
    if filename is None:
        return conf_dir
    else:
        return os.path.join(conf_dir, filename)

#==============================================================================
# Namespace Browser (Variable Explorer) configuration management
#==============================================================================
def get_supported_types():
    """Return a dictionnary containing types lists supported by the 
    namespace browser:
    dict(picklable=picklable_types, editable=editables_types)
         
    See:
    get_remote_data function in spyderlib/widgets/externalshell/monitor.py
    get_internal_shell_filter method in namespacebrowser.py"""
    from datetime import date
    editable_types = [int, long, float, list, dict, tuple, str, unicode, date]
    try:
        from numpy import ndarray, matrix
        editable_types += [ndarray, matrix]
    except ImportError:
        pass
    picklable_types = editable_types[:]
    try:
        from prymatex.utils.pil_patch import Image
        editable_types.append(Image.Image)
    except ImportError:
        pass
    return dict(picklable=picklable_types, editable=editable_types)
