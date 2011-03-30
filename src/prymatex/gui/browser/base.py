 
from PyQt4.QtWebKit import *
from PyQt4.Qt import *
import sys

class PMXWebBrowserWindow(QWidget):
    def __init__(self, parent = None):
        super(PMXWebBrowserWindow, self).__init__(parent)
        self.setupGui()
        
    def setupGui(self):
        layout = QVBoxLayout()
        self.webView = QWebView()
        self.webView.setUrl(QUrl("http://pinguinox.com.ar"))
        layout.addWidget(QLabel("Prymatex Web View"))
        layout.addWidget(self.webView)
        layout.setSpacing(1) 
        layout.setContentsMargins(0,0,0,0) 
        self.setLayout(layout)
        #layout.addLayout()
        


def main():
    a = QApplication(sys.argv)
    w = PMXWebBrowserWindow()
    w.show()
    return a.exec_()

if __name__ == '__main__':
    main()