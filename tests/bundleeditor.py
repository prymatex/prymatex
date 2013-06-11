import os, sys
sys.path.append(os.path.abspath('..'))

from prymatex.qt import QtCore, QtGui
from prymatex.qt.QtCore import *
from prymatex.qt.QtGui import *
from prymatex.core.config import PMXSettings
from prymatex.mvc.proxies import PMXFlatBaseProxyModel
import prymatex.res_rc

if __name__ == "__main__":
    from prymatex.optargs import parser
    app = QApplication([])
    app.settings = PMXSettings.getSettingsForProfile("default")
    options, open_args = parser.parse_args([])
    app.options = options
    from prymatex.gui.support.manager import PMXSupportModelManager
    app.supportManager = PMXSupportModelManager()
    app.supportManager.addNamespace('prymatex', os.path.abspath('../prymatex/share'))
    app.supportManager.addNamespace('user', os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex')))
    app.supportManager.loadSupport()
    from prymatex.gui.support.bundleeditor import PMXBundleEditor
    m = PMXBundleEditor()
    m.show()
    app.exec_()
