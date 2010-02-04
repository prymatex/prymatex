from PyQt4.Qt import *
import sys
app = QApplication(sys.argv)
win = QPushButton("Press Me")
menu = QMenu()
ax = menu.addAction("X")
ax.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_PageDown ))
ay = menu.addAction("Y")
az = menu.addAction("Z")
win.setMenu(menu)
win.show()
app.exec_()