'''
A simple django-models like API for Qt's TableModel.
It allows to handle things by name insted of index.
Some caching is peformed for some operations.

For sample usage check prymatex test folder in the source
tree inside the tablemodels

'''
from PyQt4.QtGui import QStandardItem, QItemDelegate, QStandardItemModel
from PyQt4.QtCore import Qt, pyqtSignal, pyqtWrapperType, QVariant, QString, QModelIndex
from prymatex.core.exceptions import APIUsageError, InvalidField

class PMXTableField(object):
    '''
    Table fields define table strcuture. Their definition is stored
    in a PMXTableBase instance inside a _meta attibute.

    '''
    _creation_counter = 0
    _name = None
    
    def __init__(self, 
                 name = None, 
                 required = False,
                 title = None,
                 hidden = False,
                 default = None,
                 editable = True,
                 fget_from_bundle = None, 
                 item_class = QStandardItem,
                 delegate_class = QItemDelegate):
        '''
        Field costructor, all fields are optional but name.
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
        self.hidden = hidden
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
    def fieldNames(self):
        ''' Return a list of field names '''
        return [f.name for f in self.fields]
    
    @property
    def requiredFieldNames(self):
        ''' Returns a list of required fields '''
        return [f.name for f in self.fields if f.required ]
    
    def fieldName(self, col_number):
        ''' Returns integer index for col '''
        return self.fieldNames.index(col_number)
    
    def colNumber(self, name):
        ''' Returns integer index for a column name '''
        for n, field in enumerate(self.fields):
            if name == field.name:
                return n
        raise KeyError("%s not found in %s" % (name, self))
    
    def colsNumber(self, names):
        return map(self.colNumber, names)
    
    @property
    def editableCols(self):
        ''' Returns editable columns '''
        cols = []
        for n, field in enumerate(self.fields):
            if field.editable:
                cols.append(n)
        return cols
    
    def allValidNames(self, names):
        '''
        @return: True if all name are in the meta's field definition, False otherwise
        '''
        valid_names = self.fieldNames
        return all(map(lambda fname: fname in valid_names, names))
    
    
    @property
    def visibleColumnsNames(self):
        return [ f.name for f in self.fields if not f.hidden ]
    
    @property
    def hiddenColumnsNames(self):
        return [ f.name for f in self.fields if f.hidden ]
    
    
    def checkHasNames(self, names):
        '''
        @raise InvalidField: If not valid field
        '''
        valid_names = self.fieldNames
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
    '''
    The model
    '''
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
        required = self._meta.requiredFieldNames
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
        assert self._configured, APIUsageError("configure() not called")
        if isinstance(col, (str, unicode)):
            #print "Cambio"
            col = self._meta.colNumber(col)
        return super(PMXTableBase, self).sort(col, ordering)
    
    # http://www.osgeo.org/pipermail/qgis-developer/2009-February/006203.html
    def flags(self, index):
        ''' 
        Read only fields are handled here
        '''
        baseflags = super(PMXTableBase, self).flags(index)
        col = index.column()
        if not col in self._meta.editableCols:
            return baseflags & ~Qt.ItemIsEditable
        return baseflags
    
    def setShownColumnsForView(self, view, column_names = []):
        '''
        Defines which columns have to be shown
        '''
        if not column_names:
            column_names = self._meta.visibleColumnsNames
            print "Hidding"
            print column_names
        else:
            self._meta.checkHasNames(column_names)
        
        for n, field in enumerate(self._meta.fields):
            view.setColumnHidden(n, not field.name in column_names)
    
    
    def index(self, row, column, parent = QModelIndex()):
        ''' Accepts names as well as ints'''
        if isinstance(column, (basestring, QString)):
            column = self._meta.colNumber(column)
        return super(PMXTableBase, self).index(row, column, parent)
        
    

    #===========================================================================
    # Persistance
    #===========================================================================
    
    #===========================================================================
    # Python API
    #===========================================================================
    
    def __setitem__(self, key, value):
        ''' Enable simple access '''
        if isinstance(key, tuple) and len(key) == 2:
            row, col = key
            index = self.index(row, col)
            self.setData(index, QVariant(value))
        else:
            raise APIUsageError("Only tuples can be used")
        print "Set"
        
        
class PMXModelIterator(object):
    ''' Python iteration of Qt models '''
    
    def __init__(self, model, typeSubstitution = {(QString, unicode): str}):
        print model
        self.model = model
        self.currentRow = 0
        self.typeSubstitution = typeSubstitution
        
    def next(self):
        if self.currentRow >= self.model.rowCount():
            raise StopIteration()
        data = []
        for c in range(self.model.columnCount()):
            data.append( self.model.data(self.model.index(self.currentRow, c)))
        self.currentRow += 1
        return map(self.typeConversion, data)

    def typeConversion(self, data):
        if isinstance(data, QVariant):
            data = data.toPyObject()
        for types, substitution in self.typeSubstitution:
            if isinstance(data, types):
                return substitution(data)
        return data
