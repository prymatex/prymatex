import os, sys
sys.path.append(os.path.abspath('..'))

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from prymatex.core.config import PMXSettings
from prymatex.mvc.proxies import PMXFlatBaseProxyModel
import prymatex.res_rc

if __name__ == "__main__":
    from prymatex.optargs import parser
    app = QApplication([])
    app.settings = PMXSettings.getSettingsForProfile("default")
    options, open_args = parser.parse_args([])
    app.options = options
    from prymatex.gui.bundles.manager import PMXSupportModelManager
    app.supportManager = PMXSupportModelManager()
    app.supportManager.addNamespace('prymatex', os.path.abspath('../bundles/prymatex'))
    app.supportManager.loadSupport()
    from prymatex.gui.bundles.editor import PMXBundleEditor
    m = PMXBundleEditor()
    m.show()
    app.exec_()
