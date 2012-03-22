import sys
from PyQt4 import QtCore, QtGui, Qt
from prymatex.ui.about import Ui_AboutDialog
import prymatex


class PMXAboutDialog(Ui_AboutDialog, QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.textInformation.setReadOnly(True)
        self.labelTitle.append('<br>')
        self.fillVersionInfo()
        
    def fillVersionInfo(self):
        
        commandline = ' '.join(sys.argv) 
        pmx_version = "%s (%s)" % ('.'.join(map(str, prymatex.VERSION)), self.getGitVersion())
        zmq_version = self.getZMQVersion()
        pony_version = self.getPonygurumaVersion()
        pyqt_version = Qt.qVersion()
        self.textInformation.setHtml('''
            <style>
                dt {{ font-weight: bold; }}
                
            </style>
            <dl>
                <dt>Version</dt><dd>{pmx_version}</dd>
                <dt>Command Line</dt><dd>{commandline}</dd>
                <dt>Ponyguruma Regex Library</dt><dd>{pony_version}</dd>
                <dt>ZMQ Version</dt><dd>{zmq_version}</dd>
                <dt>PyQt4</dt><dd>{pyqt_version}</dd>
           </dl>
        '''.format(**locals()))
    
    def getGitVersion(self):
        try:
            return prymatex.get_git_revision()
        except:
            return "GIT-Unknown"
    
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
            