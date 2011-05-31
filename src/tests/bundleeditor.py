import os, sys
sys.path.append(os.path.abspath('..'))

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from prymatex.support.manager import PMXSupportManager
from prymatex.core.config import PMXSettings

if __name__ == "__main__":
    from prymatex.optargs import parser
    app = QApplication([])
    app.settings = PMXSettings.getSettingsForProfile("default")
    options, open_args = parser.parse_args([])
    app.options = options  
    from prymatex.gui.bundles.editor import PMXBundleEditor
    manager = PMXSupportManager()
    manager.addNamespace('prymatex', os.path.abspath('../bundles/prymatex'))
    manager.loadSupport()
    m = PMXBundleEditor(manager)
    m.show()
    app.exec_()
