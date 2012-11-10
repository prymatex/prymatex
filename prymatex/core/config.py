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

#==============================================================================
# Configuration paths
#==============================================================================
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

def get_module_path(modname):
    """Return module *modname* base path"""
    return os.path.abspath(os.path.dirname(sys.modules[modname].__file__))


def get_module_data_path(modname, relpath=None, attr_name='DATAPATH'):
    """Return module *modname* data path
    Note: relpath is ignored if module has an attribute named *attr_name*
    
    Handles py2exe/cx_Freeze distributions"""
    datapath = getattr(sys.modules[modname], attr_name, '')
    if datapath:
        return datapath
    else:
        datapath = get_module_path(modname)
        parentdir = os.path.join(datapath, os.path.pardir)
        if os.path.isfile(parentdir):
            # Parent directory is not a directory but the 'library.zip' file:
            # this is either a py2exe or a cx_Freeze distribution
            datapath = os.path.abspath(os.path.join(os.path.join(parentdir, os.path.pardir),
                                            modname))
        if relpath is not None:
            datapath = os.path.abspath(os.path.join(datapath, relpath))
        return datapath

def get_module_source_path(modname, basename=None):
    """Return module *modname* source path
    If *basename* is specified, return *modname.basename* path where 
    *modname* is a package containing the module *basename*
    
    *basename* is a filename (not a module name), so it must include the
    file extension: .py or .pyw
    
    Handles py2exe/cx_Freeze distributions"""
    srcpath = get_module_path(modname)
    parentdir = os.path.join(srcpath, os.path.pardir)
    if os.path.isfile(parentdir):
        # Parent directory is not a directory but the 'library.zip' file:
        # this is either a py2exe or a cx_Freeze distribution
        srcpath = os.path.abspath(os.path.join(os.path.join(parentdir, osp.pardir),
                                       modname))
    if basename is not None:
        srcpath = os.path.abspath(os.path.join(srcpath, basename))
    return srcpath

#==============================================================================
# Translations
#==============================================================================
def get_translation(modname, dirname=None):
    """Return translation callback for module *modname*"""
    if dirname is None:
        dirname = modname
    locale_path = get_module_data_path(dirname, relpath="share/Locale",
                                       attr_name='LOCALEPATH')
    # fixup environment var LANG in case it's unknown
    if "LANG" not in os.environ:
        import locale
        lang = locale.getdefaultlocale()[0]
        if lang is not None:
            os.environ["LANG"] = lang
    import gettext
    try:
        _trans = gettext.translation(modname, locale_path, codeset="utf-8")
        lgettext = _trans.lgettext
        def translate_gettext(x):
            if isinstance(x, unicode):
                x = x.encode("utf-8")
            return unicode(lgettext(x), "utf-8")
        return translate_gettext
    except IOError, _e:  # analysis:ignore
        #print "Not using translations (%s)" % _e
        def translate_dumb(x):
            if not isinstance(x, unicode):
                return unicode(x, "utf-8")
            return x
        return translate_dumb

# Translation callback
_ = get_translation("prymatex")

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
