#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import prymatex

from prymatex.qt import QtCore, QtGui
from prymatex.qt import API, qt_version_str, pyqt_version_str, sip_version_str, pyside_version_str
from prymatex import resources
from prymatex.core.components import PMXBaseDialog

from prymatex.ui.about import Ui_AboutDialog

informationHtml = '''<style>dt {{ font-weight: bold; }}</style><dl>
<dt>Home Page</dt><dd><a href="{pmx_url}">{pmx_url}</a></dd>
<dt>Source</dt><dd><a href="{pmx_url}">{pmx_source}</a></dd>
<dt>Version</dt><dd>{pmx_version}</dd>
<dt>Command Line</dt><dd>{commandline}</dd>
<dt>Qt</dt><dd>{qt_version}</dd>'''

if API == "pyqt":
    informationHtml += '<dt>Sip</dt><dd>{sip_version}</dd><dt>PyQt4</dt><dd>{pyqt_version}</dd>'
else:
    informationHtml += '<dt>PySide</dt><dd>{pyside_version}</dd>'
informationHtml += '<dt>Ponyguruma Regex Library</dt><dd>{pony_version}</dd><dt>ZMQ Version</dt><dd>{zmq_version}</dd></dl>'

class AboutDialog(QtGui.QDialog, Ui_AboutDialog, PMXBaseDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        self.labelLogo.setPixmap(resources.getImage("logo"))
        self.textInformation.setReadOnly(True)
        self.fillVersionInfo()
        
    def fillVersionInfo(self):
        self.textInformation.setHtml(informationHtml.format(**{
            'pmx_url': prymatex.__url__,
            'pmx_source': prymatex.__source__,
            'commandline': ' '.join(sys.argv) ,
            'pmx_version': prymatex.__version__,
            'zmq_version': self.getZMQVersion(),
            'pony_version': self.getPonygurumaVersion(),
            'qt_version': qt_version_str,
            'sip_version': sip_version_str,
            'pyqt_version': pyqt_version_str,
            'pyside_version': pyside_version_str
        }))

    def getZMQVersion(self):
        try:
            import zmq
            return zmq.__version__ #@UndefinedVariable
        except ImportError:
            return "Not installed"
        return "Error"

    def getPonygurumaVersion(self):
        try:
            import ponyguruma
            return '.'.join(map(str, ponyguruma.VERSION))
        except ImportError:
            return "Not installed."
        return "Error"
