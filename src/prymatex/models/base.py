
from PyQt4.Qt import *
from prymatex.core.exceptions import APIUsageError, InvalidField

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
    Stores fields in order
    '''
    fields = []
    
    def __init__(self, fields, name = None):
        self.fields = fields
        self.name = name
    
    @property
    def field_names(self):
        ''' Return a list of field names '''
        return [f.name for f in self.fields]
    
    @property
    def required_field_names(self):
        ''' Returns a list of required fields '''
        return [f.name for f in self.fields if f.required ]
    
    def col_number(self, name):
        ''' Returns integer index for a column name '''
        for n, field in enumerate(self.fields):
            if name == field.name:
                return n
        raise KeyError("%s not found in %s" % (name, self))
    
    @property
    def editable_cols(self):
        ''' Returns editable columns '''
        cols = []
        for n, field in enumerate(self.fields):
            if field.editable:
                cols.append(n)
        return cols
    
    def all_valid_names(self, names):
        '''
        @return: True if all name are in the meta's field definition, False otherwise
        '''
        valid_names = self.field_names
        return all(map(lambda fname: fname in valid_names, names))
        
    
    def check_has_names(self, names):
        '''
        @raise InvalidField: If not valid field
        '''
        valid_names = self.field_names
        for name in names:
            if not name in valid_names:
                raise InvalidField(name, valid_names) 
    
    def __str__(self):
        return "<PMXTableMeta for %s table model>" % self.name
    
    __repr__ = __str__
    

class PMXTableMetaclass(pyqtWrapperType):
    '''
    This metaclass takes fields from PMXTableBase sub-classes and
    sotre thier fields in _meta property.
    PMXTableBase.setup(self) makes extensive usage of the PMXTableMeta
    '''
    def __new__(cls, name, bases, attrs):
        
        fields = []
        field_names = []
        for attr_name in attrs:
            attr = attrs[attr_name]
            if isinstance(attr, PMXTableField):
                # Generate meta
                field = attr
                field.name = attr_name
                field.title = field.title or attr_name.title()
                field_names.append(attr_name)
                fields.append(field)
                
        # Remove fields!
        map(lambda n: attrs.pop(n), field_names)
            
        fields.sort(lambda a, b: cmp(a._creation_counter, b._creation_counter))
        attrs['_meta'] = PMXTableMeta(fields, name)
        
        new_class = super(PMXTableMetaclass, cls).__new__(cls, name, bases, attrs)
        return new_class

class PMXTableBase(QStandardItemModel):
    __metaclass__ = PMXTableMetaclass 
    _configured = False
    
    tableConfigured = pyqtSignal()
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
        #print "Using", self._meta
        self.setColumnCount(len(self._meta.fields))
        self.fillHeadersFromFields()
        self._configured = True
        self.tableConfigured.emit()
    
    def fillHeadersFromFields(self):
        for n, field in enumerate(self._meta.fields):
            #QStandardItemModel.setHeaderData(self, n, Qt.Horizontal, field.title)
            title = field.title
            self.setHeaderData(n, Qt.Horizontal, title)
    
    def setColumnDelegatesFromFields(self, view):
        if view.model() is not self:
            raise APIUsageError("Atteped to setup item delegate for wrong model")
        
        for n, field in enumerate(self._meta.fields):
            if not field.delegate_class is QItemDelegate:
                print "Setting custom delegete for", field.delegate_class, "for field", field
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
            if data is None:
                data = ''
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
    
    def setShownColumnsForView(self, view, column_names):
        '''
        Defines which columns have to be shown
        '''
        self._meta.check_has_names(column_names)
        
        for n, field in enumerate(self._meta.fields):
            view.setColumnHidden(n, not field.name in column_names)

