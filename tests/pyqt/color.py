import sys
from PyQt4 import QtCore, QtGui

class SomeQtWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.colorDialog = QtGui.QColorDialog(self)
        self.colorDialog.setOption(QtGui.QColorDialog.ShowAlphaChannel, True)
        self.button = QtGui.QPushButton(self)
        self.button.pressed.connect(self.on_button_pressed)
        
    def on_colorDialog_currentColorChanged(self):
        print hex(self.colorDialog.currentColor().rgba()).upper()[2:-1]
        
    def on_button_pressed(self):
        self.colorDialog.open(self.on_colorDialog_currentColorChanged)
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = SomeQtWidget()
    window.show()
    sys.exit(app.exec_())
