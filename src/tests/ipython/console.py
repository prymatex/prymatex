#!/usr/bin/env python
import sys

from IPython.frontend.qt.kernelmanager import QtKernelManager
from IPython.frontend.qt.console.ipython_widget import IPythonWidget

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMainWindow, QApplication


class MainWin(QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    self.resize(1000,1000)

    self.kernel = QtKernelManager()
    self.kernel.start_kernel()
    self.kernel.start_channels()

    self.console = IPythonWidget()
    self.console.kernel_manager = self.kernel
    self.setCentralWidget(self.console)

def main():
    app = QApplication(sys.argv)

    main_win = MainWin()
    main_win.show()
    main_win.activateWindow()

    app.exec_()

if __name__ == '__main__':
    main()