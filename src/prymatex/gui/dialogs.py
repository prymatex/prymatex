
from PyQt4.Qt import QDialog, QVBoxLayout, QPushButton, QFileDialog, QVariant
from PyQt4.QtCore import pyqtSignal, QDir
from PyQt4.Qt import SIGNAL
from PyQt4.QtGui import QCompleter, QFileSystemModel, QMessageBox
from os.path import isdir, abspath
from prymatex.core.base import PMXObject
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

class NewFromTemplateDialog(QDialog, Ui_NewFromTemplateDialog, PMXObject):
    newFileCreated = pyqtSignal(str)
    
    def __init__(self, parent):
        super(NewFromTemplateDialog, self).__init__(parent)
        self.setupUi(self)
        model = QFileSystemModel(self)
        model.setRootPath("")
        model.setFilter(QDir.Dirs)
        self.completerFileSystem = QCompleter(model, self)
        self.lineLocation.setCompleter(self.completerFileSystem)
        for template in self.pmxApp.bundleManager.getAllTemplates():
            self.comboTemplates.addItem(template.name, userData = QVariant(template))
        self.buttonCreate.setDefault(True)
    
    def on_buttonChoose_pressed(self):
        path = QFileDialog.getExistingDirectory(self, self.trUtf8("Choose Location for Template"))
        if path:
            self.lineLocation.setText(path)

    def on_buttonCreate_pressed(self):
        #TODO: Validar que los lineEdit tengan texto
        template = self.comboTemplates.itemData(self.comboTemplates.currentIndex()).toPyObject()
        environment = template.buildEnvironment(directory = unicode(self.lineLocation.text()), name = unicode(self.lineFileName.text()))
        if not template:
            QMessageBox.question(self, "Information requiered", 
                                 "You did not suply all the information required "
                                 "for the file", 
                                 buttons=QMessageBox.Cancel | QMessageBox.Retry, 
                                 defaultButton=QMessageBox.NoButton)
        template.resolve(environment)
        self.newFileCreated.emit(environment['TM_NEW_FILE'])
        self.close()
    
    def check_valid_location(self):
        ''' Disable file '''
        location = unicode(self.lineLocation.text())
        if not isdir(location):
            self.buttonCreate.setEnabled(False)
            return
        filename = unicode(self.lineFileName)
        if not filename:
            self.buttonCreate.setEnabled(False)
            return
        self.buttonCreate.setEnabled(True)
             
    def on_lineFileName_textChanged(self, text):
        self.check_valid_location()
    
    def on_lineLocation_textChanged(self, text):
        self.check_valid_location()
            
    def on_buttonClose_pressed(self):
        self.close()
    
    def exec_(self):
        self.lineFileName.setText('')
        start_directory = qApp.instance().startDirectory()
        start_directory = abspath(start_directory)
        self.lineLocation.setText(start_directory)
        self.check_valid_location()
        super(NewFromTemplateDialog, self).exec_()
        
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