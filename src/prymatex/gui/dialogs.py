
from PyQt4.Qt import QDialog, QVBoxLayout, QPushButton, QFileDialog, QVariant
from PyQt4.QtCore import pyqtSignal
from PyQt4.Qt import SIGNAL
from prymatex.bundles import PMXBundle
from prymatex.gui.ui_multiclose import Ui_SaveMultipleDialog
from prymatex.gui.ui_newtemplate import Ui_NewFromTemplateDialog

if __name__ == '__main__':
    import sys
    from os.path import abspath, dirname, join
    path = join(abspath(dirname(__file__)), '..', )
    print path
    sys.path.append( path )
    
class MultiCloseDialog(QDialog, Ui_SaveMultipleDialog):
    def __init__(self, parent):
        super(MultiCloseDialog, self).__init__(parent)
        self.setupUi(self)

from PyQt4.Qt import QDialog

class NewFromTemplateDialog(QDialog, Ui_NewFromTemplateDialog):
    newFileCreated = pyqtSignal(str)
    
    def __init__(self, parent):
        super(NewFromTemplateDialog, self).__init__(parent)
        self.setupUi(self)
        for template in PMXBundle.TEMPLATES:
            self.comboTemplates.addItem(template.name, userData = QVariant(template))
    
    def on_buttonChoose_pressed(self):
        path = QFileDialog.getExistingDirectory(self, self.trUtf8("Choose Location for Template"))
        self.lineLocation.setText(path)

    def on_buttonCreate_pressed(self):
        #TODO: Validar que los lineEdit tengan texto
        template = self.comboTemplates.itemData(self.comboTemplates.currentIndex()).toPyObject()
        environment = template.buildEnvironment(directory = unicode(self.lineLocation.text()), name = unicode(self.lineFileName.text()))
        template.resolve(environment)
        self.newFileCreated.emit(environment['TM_NEW_FILE'])
        self.close()

    def on_buttonClose_pressed(self):
        self.close()
        
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