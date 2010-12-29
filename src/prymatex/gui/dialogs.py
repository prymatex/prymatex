
from PyQt4.Qt import QDialog, QVBoxLayout, QPushButton
from PyQt4.Qt import SIGNAL
if __name__ == '__main__':
    import sys
    from os.path import abspath, dirname, join
    path = join(abspath(dirname(__file__)), '..', )
    print path
    sys.path.append( path )
    
from ui_multiclose import Ui_SaveMultipleDialog

    
class MultiCloseDialog(QDialog, Ui_SaveMultipleDialog):
    def __init__(self, parent):
        super(MultiCloseDialog, self).__init__(parent)
        self.setupUi(self)



def test():
    def multiclose_dialog(p):
        d = MultiCloseDialog(p)
        d.exec_()
    from functools import partial
    from PyQt4.Qt import QApplication, QWidget
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setWindowTitle("Window Title")
    layout = QVBoxLayout()
    pushButton = QPushButton("Multi Save Dialog")
    widget.connect(pushButton, SIGNAL("pressed()"), partial(multiclose_dialog, widget))
    layout.addWidget(pushButton)
    widget.setLayout(layout)
    widget.show()
    
    return app.exec_()

if __name__ == '__main__':
    import sys
    sys.exit(test())