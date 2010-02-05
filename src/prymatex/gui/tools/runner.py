#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 05/02/2010 by defo

'''
Definitions
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_runner import Ui_PMXRunnerWidget

# No utilizamos subproccess, sino QProcess porque es eventual
#from subprocess import Popen, PIPE

class PMXRunnerWidget(Ui_PMXRunnerWidget, QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        CMD = "python hola.py"
        # Popen(args, bufsize, executable, 
        # stdin, stdout, stderr, 
        # preexec_fn, close_fds, shell, cwd, env, 
        # universal_newlines, startupinfo, creationflags)
        self.proc = QProcess(self)
        self.connect(self.proc, SIGNAL("readyReadStandardOutput ()"), self.readStdout)
        self.connect(self.proc, SIGNAL("readyReadStandardError ()"), self.readStderr)
        
        self.proc.start("/usr/bin/python", ["test.py", ])
        self.proc.waitForStarted()
        
        self.proc.write("23\n")
        self.proc.waitForReadyRead()
        self.proc.waitForFinished()
        #print self.proc.readAll()
        #print "OK"
        
    def readStdout(self):
        self.textOutput.append(u"%s" % self.proc.readAllStandardOutput())
        print "Read"
        
    
    def readStderr(self):
        self.textOutput.append(u"%s" % self.proc.readAllStandardError())
        print "Error"
        
# Test code

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = PMXRunnerWidget()
    win.show()
    sys.exit(app.exec_())