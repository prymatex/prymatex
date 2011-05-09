# encoding: utf-8
'''
Created on 07/05/2011

@author: defo
'''

if __name__ == "__main__":
    import sys, os
    path = os.path.dirname(os.path.abspath(__file__))
    import_path = os.path.abspath(os.path.join(path, '..', ))
    sys.path.insert(0, import_path)
    
from PyQt4.Qt import *    
import prymatex
from prymatex.core.exceptions import APIUsageError
from prymatex.models import *
    
class PMXTableModelItemX(QStandardItemModel):
    pass

class PMXChoiceItemDelegate(QItemDelegate):
    CHOICES = ()
    
    def createEditor(self, parent, option, index):
        #window = QWidget()
        #window.setLayout(QVBoxLayout())
        #window.layout().addWidget(QLabel("Seleccione un tipo"))
        editor = QComboBox(parent)
        #window.layout().addWidget(editor)
        
        for display_text, data in self.CHOICES:
            editor.addItem(display_text, data)
        print "Editor"
        return editor

    def setEditorData(self, editor, index):
        data = index.data().toPyObject()
        editor.setCurrentIndex(editor.findData(data))
        


    def setModelData(self, editor, model, index):
        #return PyQt4.Qt.QItemDelegate.setModelData(self, *args, **kwargs)
        data = editor.itemData(editor.currentIndex())
        print "Setting data to model %s" % data
        model.setData(index, data)

class PMXDecoupledDialog(QWidget):
    def __init__(self, title, editor):
        super(PMXDecoupledDialog, self).__init__()
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(QLabel("Press <b>Esc</b> to cancel"))
        self.editor = editor
        layout.addWidget(self.editor)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        #cancel_btn = QPushButton("Cancel")
        #cancel_btn.pressed.connect(window.reject)
        ok_btn = QPushButton("OK")
        ok_btn.pressed.connect(self.close)#self.accept)
        button_layout.addWidget(ok_btn)
        #button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        #self.setModal(True)
        self.setLayout(layout)
    
    #def exec_(self):
    #    self.normal = True
    #    super(PMXDecoupledDialog, self).exec_()
    
    #normal = False
    #def setVisible(self, visible):
    #    if not self.normal:
    #        return self.exec_()
    #    else:
    #        return super(PMXDecoupledDialog, self).setVisible(visible)
    def showEvent(self, event):
        retval = super(PMXDecoupledDialog, self).showEvent(event)
        self.editor.setFocus()
        return retval
    
    
class PMXDecoupledEditorDelegate(QItemDelegate):
    ''' Edit a long text '''
    def createEditor(self, parent, option, index):
        column_title = index.model()._meta.fields[index.column()].title
        window = PMXDecoupledDialog(unicode(self.trUtf8("Edit %s")) % column_title,
                                    editor = QTextEdit())
        #window.editor.setFocus()
        #window.exec_()
        return window
    
    def setEditorData(self, window, index):
        data = index.data().toPyObject()
        window.editor.setPlainText( data )
        
    def setModelData(self, window, model, index):
        data = window.editor.toPlainText()
        model.setData(index, data)
    

class SexoItemDelegate(PMXChoiceItemDelegate):

    CHOICES = [('Sinppet', 1),
               ('Command', 2),
               ('Syntax', 3),
               ('Macro', 4),
               
               ]

class PMXTableTest(PMXTableBase):
    # Order matters
    nombre = PMXTableField(required = False, editable = False)
    apellido = PMXTableField(required = True, editable = False)
    direccion = PMXTableField(required = True, title = u"Dirección")
    type_ = PMXTableField(required = True, default = 1, title = "Bundle Type", 
                         delegate_class=SexoItemDelegate)
    descripcion = PMXTableField(required = False, 
                                delegate_class=PMXDecoupledEditorDelegate)
    
    def __init__(self, parent = None):
        super(PMXTableTest, self).__init__(parent)
        self.setup()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = QTableView()
    model = PMXTableTest()
    win.setModel(model)
    model.setColumnDelegatesFromFields(win)
    model.addRowFromKwargs(nombre = "Nahuel", apellido = u"Defossé", direccion = "Moreno 46")
    model.addRowFromKwargs(nombre = "Pablo Enrrique", apellido = "Petenello", direccion = "Moreno 46")
    model.addRowFromKwargs(nombre = "Diego Marco", apellido = "van Haaster", direccion = "Moreno 46")
    model.sort('apellido')
    win.setWindowTitle(unicode(model.__class__.__name__))
    win.setGeometry(400,200, 600, 400)
    print model._meta
    win.show()
    sys.exit(app.exec_())