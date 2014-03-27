#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import prymatex

from prymatex.qt import QtCore, QtGui
from prymatex.qt import API, qt_version_str, pyqt_version_str, sip_version_str, pyside_version_str
from prymatex import resources
from prymatex.core.components import PrymatexDialog

from prymatex.ui.about import Ui_AboutDialog

informationHtml = '''<style>dt {{ font-weight: bold; }}</style><dl>
<dt>Home Page</dt><dd><a href="{pmx_url}">{pmx_url}</a></dd>
<dt>Source</dt><dd><a href="{pmx_url}">{pmx_source}</a></dd>
<dt>Version</dt><dd>{pmx_version}</dd>
<dt>Command Line</dt><dd>{commandline}</dd>
<dt>Python</dt><dd>{python_version}</dd>
<dt>Qt</dt><dd>{qt_version}</dd>'''

if API == "pyqt":
    informationHtml += '''<dt>Sip</dt><dd>{sip_version}</dd>
<dt>PyQt4</dt><dd>{pyqt_version}</dd>'''
else:
    informationHtml += '<dt>PySide</dt><dd>{pyside_version}</dd>'
informationHtml += '''<dt>Ponyguruma</dt><dd>{pony_version}</dd>
<dt>Regex</dt><dd>{regex_version}</dd>
<dt>ZMQ Version</dt><dd>{zmq_version}</dd></dl>'''

class AboutDialog(PrymatexDialog, Ui_AboutDialog, QtGui.QDialog):
    def __init__(self, **kwargs):
        super(AboutDialog, self).__init__(**kwargs)
        self.setupUi(self)
        self.labelLogo.setPixmap(resources.getImage("logo"))
        self.textInformation.setReadOnly(True)
        self.fillVersionInfo()
        
    def fillVersionInfo(self):
        self.textInformation.setHtml(informationHtml.format(**{
            'pmx_url': prymatex.__url__,
            'pmx_source': prymatex.__source__,
            'commandline': ' '.join(sys.argv) ,
            'python_version': "%d.%d.%d %s" % sys.version_info[:4],
            'pmx_version': prymatex.__version__,
            'zmq_version': self.zmqVersion(),
            'pony_version': self.ponygurumaVersion(),
            'regex_version': self.regexVersion(),
            'qt_version': qt_version_str,
            'sip_version': sip_version_str,
            'pyqt_version': pyqt_version_str,
            'pyside_version': pyside_version_str
        }))

    def zmqVersion(self):
        try:
            import zmq
            return zmq.__version__
        except ImportError:
            return "Not installed"
        return "Error"

    def ponygurumaVersion(self):
        try:
            import ponyguruma
            return '.'.join(map(str, ponyguruma.VERSION))
        except ImportError:
            return "Not installed"
        return "Error"

    def regexVersion(self):
        try:
            import regex
            return regex.__version__
        except ImportError:
            return "Not installed"
        return "Error"