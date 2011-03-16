from prymatex.gui.panes import PaneDockBase
from prymatex.gui.panes.ui_browser import Ui_BrowserPane

class PMXBrowserPaneDock(PaneDockBase, Ui_BrowserPane):
    def __init__(self, parent):
        PaneDockBase.__init__(self, parent)
        self.setupUi(self)

    def setHtml(self, string):
        self.webView.setHtml(string)

