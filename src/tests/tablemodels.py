# encoding: utf-8
'''
Created on 07/05/2011

@author: defo
'''
from PyQt4.Qt import *
from prymatex.core.exceptions import APIUsageError

class PMXTableField(object):
    
    _creation_counter = 0
    _name = None
    
    def __init__(self, 
                 name = None, 
                 required = False,
                 title = None,
                 default = None,
                 editable = True,
                 fget_from_bundle = None, 
                 item_class = QStandardItem,
                 delegate_class = QItemDelegate):
        '''
        @param name: The field name
        @param required: Is the field requirerd
        @param title: Field's title
        @param fget_from_bundle: How to get data from bundle, maight be dropped soon
        @param item_ctor: The item class that
        @param delegate_class: A delegate class, not an instance!
        '''
        self.title = title
        self.name = name
        self.required = required
        self.item_class = item_class
        self.delegate_class = delegate_class
        self.default = default
        self.editable = editable
        # For sorting
        PMXTableField._creation_counter += 1
        self._creation_counter = PMXTableField._creation_counter
        
    def __str__(self):
        return "<%s field (%d)>" % (self.name, self._creation_counter)
    
    __repr__ = __str__
    

class PMXTableMeta(object):
    '''
    Stores field in order
    '''
    fields = []
    
    def __init__(self, fields):
        self.fields = fields
    
    @property
    def field_names(self):
        return [f.name for f in self.fields]
    
    @property
    def required_field_names(self):
        return [f.name for f in self.fields if f.required ]
    
    def col_number(self, name):
        for n, field in enumerate(self.fields):
            if name == field.name:
                return n
        raise KeyError("%s not found in %s" % (name, self))
    
    @property
    def editable_cols(self):
        cols = []
        for n, field in enumerate(self.fields):
            if field.editable:
                cols.append(n)
        return cols  
    

class PMXTableMetaclass(pyqtWrapperType):
    def __new__(cls, name, bases, attrs):
        
        fields = []
        field_names = []
        for attr_name in attrs:
            attr = attrs[attr_name]
            if isinstance(attr, PMXTableField):
                field = attr
                field.name = attr_name
                field.title = field.title or attr_name.title()
                field_names.append(attr_name)
                fields.append(field)
                
                #print field, attr_name
        # Remove fields!
        map(lambda n: attrs.pop(n), field_names)
            
        fields.sort(lambda a, b: cmp(a._creation_counter, b._creation_counter))
        attrs['_meta'] = PMXTableMeta(fields)
        
        new_class = super(PMXTableMetaclass, cls).__new__(cls, name, bases, attrs)
        return new_class

class PMXTableBase(QStandardItemModel):
    __metaclass__ = PMXTableMetaclass 
    _configured = False
    
    @property
    def configured(self):
        return self._configured
    
    def __init__(self, parent = None):
        super(PMXTableBase, self).__init__()
        self.setup()
        
    def setup(self):
        '''
        Configure 
        '''
        self.setColumnCount(len(self._meta.fields))
        self.fillHeadersFromFields()
        self._configured = True
    
    def fillHeadersFromFields(self):
        for n, field in enumerate(self._meta.fields):
            #QStandardItemModel.setHeaderData(self, n, Qt.Horizontal, field.title)
            title = field.title
            self.setHeaderData(n, Qt.Horizontal, title)
    
    def setColumnDelegatesFromFields(self, view):
        if view.model() is not self:
            raise APIUsageError("Atteped to setup item delegates for wrong model")
        for n, field in enumerate(self._meta.fields):
            item_delegate = field.delegate_class()
            view.setItemDelegateForColumn(n, item_delegate)
    
    def addRowFromKwargs(self, **kwargs):
        required = self._meta.required_field_names
        if not map(lambda name: name in required, kwargs):
            raise APIUsageError("Not all required fields provided!")
        items = []
        for field in self._meta.fields:
            data = kwargs.get(field.name, '')
            if not data and field.default:
                data = field.default
            item = field.item_class(data)
            items.append(item)
        QStandardItemModel.appendRow(self, items)
    
    def sort(self, col, ordering = Qt.AscendingOrder):
        print col
        if isinstance(col, (str, unicode)):
            print "Cambio"
            col = self._meta.col_number(col)
        return super(PMXTableBase, self).sort(col, ordering)
    # http://www.osgeo.org/pipermail/qgis-developer/2009-February/006203.html
    def flags(self, index):
        ''' '''
        baseflags = super(PMXTableBase, self).flags(index)
        col = index.column()
        if not col in self._meta.editable_cols:
            return baseflags & ~Qt.ItemIsEditable
        return baseflags  
    
class PMXTableModelItemX(QStandardItemModel):
    pass

class PMXChoiceItemDelegate(QItemDelegate):
    CHOICES = ()
    
    def createEditor(self, parent, option, index):
        window = QWidget()
        window.setLayout(QVBoxLayout())
        window.layout().addWidget(QLabel("Seleccione un tipo"))
        editor = QComboBox()
        window.layout().addWidget(editor)
        
        for display_text, data in self.CHOICES:
            editor.addItem(display_text, data)
            
        return window

    def setEditorData(self, editor, index):
        data = index.data().toPyObject()
        editor.setCurrentIndex(editor.findData(data))
        


    def setModelData(self, editor, model, index):
        #return PyQt4.Qt.QItemDelegate.setModelData(self, *args, **kwargs)
        data = editor.itemData(editor.currentIndex())
        print "Setting data to model %s" % data
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
    tipo = PMXTableField(required = True, default = 1, 
                         delegate_class=SexoItemDelegate)
    
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
    win.setGeometry(400,200, 400, 400)
    print model._meta
    win.show()
    sys.exit(app.exec_())