import sys
from PyQt4 import QtCore, QtGui

class MyThread(QtCore.QThread):
    def __init__(self, parent = None):
        super(MyThread, self).__init__(parent)
        
    def run(self):
        while True:
            print "Ping"
            QtCore.QThread.sleep(1)

class Window(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.thread = MyThread()
        self.thread.start()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
