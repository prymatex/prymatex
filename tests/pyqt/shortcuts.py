import sys
from PyQt4 import QtCore, QtGui

class Docker1(QtGui.QDockWidget):
    def __init__(self, parent = None):
        QtGui.QDockWidget.__init__(self, parent)
        self.copy = QtGui.QShortcut(self)
        self.copy.setKey(QtGui.QKeySequence("Ctrl+C"))
        self.copy.activated.connect(self.on_copy)
        self.copy.activatedAmbiguously.connect(self.on_copy_amb)
        #self.copy.setShortcutContext(QtCore.Qt.WidgetShortcut)

    def on_copy(self):
        print(self)
        
    def on_copy_amb(self):
        print("amb", self)

class Docker2(QtGui.QDockWidget):
    def __init__(self, parent = None):
        QtGui.QDockWidget.__init__(self, parent)
        self.copy = QtGui.QShortcut(self)
        self.copy.setKey(QtGui.QKeySequence("Ctrl+C"))
        self.copy.activated.connect(self.on_copy)
        self.copy.activatedAmbiguously.connect(self.on_copy_amb)
        #self.copy.setShortcutContext(QtCore.Qt.WidgetShortcut)

    def on_copy(self):
        print(self)
        
    def on_copy_amb(self):
        print("amb", self)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.addDockers()
        self.widget = QtGui.QLabel("hola", self)
        self.copy = QtGui.QAction(self.widget)
        self.copy.setShortcut(QtGui.QKeySequence("Ctrl+C"))
        self.copy.triggered.connect(self.on_copy)
        self.addAction(self.copy)
        self.setCentralWidget(self.widget)
        self.copy.setShortcutContext(QtCore.Qt.WidgetShortcut)
        #copy.activatedAmbiguously.connect(self.on_activatedAmbiguously)
        
    def addDockers(self):
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, Docker1(self))
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, Docker2(self))
    
    def on_copy(self):
        print(self)
        
    def on_activatedAmbiguously(self):
        print("amb", self)
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())