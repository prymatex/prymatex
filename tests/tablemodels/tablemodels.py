# encoding: utf-8
'''
Created on 07/05/2011

@author: defo
'''

if __name__ == "__main__":
    import sys, os
    path = os.path.dirname(os.path.abspath('.'))
    import_path = os.path.abspath(os.path.join(path, '..', ))
    sys.path.insert(0, import_path)
    
from PyQt4.Qt import *
import prymatex
from prymatex.core.exceptions import APIUsageError
from prymatex.models import *


def colorize(some_code):
    ''' python -> html '''
    try:
        from pygments import highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import HtmlFormatter
        return highlight(some_code, PythonLexer(), HtmlFormatter(noclasses = True))
    except ImportError:
        return some_code
    
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
        print("Editor")
        return editor

    def setEditorData(self, editor, index):
        data = index.data().toPyObject()
        editor.setCurrentIndex(editor.findData(data))
        


    def setModelData(self, editor, model, index):
        #return PyQt4.Qt.QItemDelegate.setModelData(self, *args, **kwargs)
        data = editor.itemData(editor.currentIndex())
        print("Setting data to model %s" % data)
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
        window = PMXDecoupledDialog(str(self.trUtf8("Edit %s")) % column_title,
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
    nombre = PMXTableField(required = False)
    apellido = PMXTableField(required = True)
    direccion = PMXTableField(required = True, title = "Dirección")
    type_ = PMXTableField(required = True, default = 1, title = "Bundle Type", 
                         delegate_class=SexoItemDelegate)
    descripcion = PMXTableField(required = False, 
                                delegate_class=PMXDecoupledEditorDelegate)
    
    nombre_apelido = PMXTableField(editable = False)

    
    def __init__(self, parent = None):
        super(PMXTableTest, self).__init__(parent)
        self.setup()
        # Eventos
        self.itemChanged.connect(self._updateItem)
        self.rowsInserted.connect(self.appendToApeNombre)

    def fillNombreApellido(self, row):
        ''' Rellenar una columna a partir de otras dos '''
        values = self.index(row, 'nombre' ).data(), self.index(row, 'apellido' ).data()
        values = [str(x.toPyObject()) for x in values]
        data = " ".join(values)
        self.setData(self.index(row, 'nombre_apelido'), data)
    
    
    def _updateItem(self, item):
        '''
        Si se edita un item, se acutaliza
        '''
        index = item.index()
        row = item.index().row()
        interesting_indexes = self._meta.colsNumber(["nombre", "apellido"])
        #  Se modifico alguna columna interesante? 
        if index.column() in interesting_indexes:
            self.fillNombreApellido(row)
        
    def appendToApeNombre(self, index, start, end):
        ''' Cuando se agrega una columna '''
        for row in range(start, end+1):
            self.fillNombreApellido(row)
        
        
    

def setupModel():
    model = PMXTableTest()
    model.addRowFromKwargs(nombre = "Pepe", apellido = "Grillo", direccion = "Caja de 222 fósforos Patito")
    model.addRowFromKwargs(nombre = "Pinocho", apellido = "Pérez", direccion = "Lata de concentrado de ballena")
    model.addRowFromKwargs(nombre = "Froddo", apellido = "Baggins", direccion = "The fellowship of the ring")
    return model

def exampleCodeLabel():
    html = colorize('''

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

model = PMXTableTest()
model.addRowFromKwargs(nombre = "Pepe", apellido = u"Grillo", direccion = u"Caja de 222 fósforos Patito")
model.addRowFromKwargs(nombre = "Pinocho", apellido = u"Pérez", direccion = "Lata de concentrado de ballena")
model.addRowFromKwargs(nombre = "Froddo", apellido = "Baggins", direccion = "The fellowship of the ring")
model.sort('apellido')
    ''')
    lbl = QLabel(html)
    lbl.setStyleSheet('QLabel {border: 1px solid #000; }')
    return lbl
      
if __name__ == "__main__":
    ''' Create the widget '''
    import sys
    
        
    app = QApplication(sys.argv)
    test_win = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    test_win.setLayout(layout)
    lbl = QLabel('''<h3>PMXTableBase</h3>''')
    lbl.setMargin(3)
    layout.addWidget(lbl)
    layout.addWidget(exampleCodeLabel())
    table = QTableView()
    layout.addWidget(table)
    layout2 = QHBoxLayout()
    layout.addLayout(layout2)
    layout2.addStretch()
    combo = QComboBox()
    
    layout2.addWidget(combo)
    #layout2.addWidget(QPushButton("Save to file"))
    # Create model
    model = setupModel()
    table.setModel(model)
    
    combo.setModel(model)
    #combo.setModelColumn(model._meta.colNumber('nombre_apelido'))
    combo.setModelColumn(model._meta.colNumber('nombre_apelido'))
    # Enable edit features
    model.setColumnDelegatesFromFields(table)
    model.setShownColumnsForView(table,)
    
    
    
    model.sort('nombre_apelido')
    test_win.setWindowTitle(str(model.__class__.__name__))
    test_win.setGeometry(400,200, 600, 560)
    print(model._meta)
    test_win.show()
    sys.exit(app.exec_())
