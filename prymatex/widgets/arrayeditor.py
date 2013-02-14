#!/usr/bin/env python
# -*- coding: utf-8 -*-


import StringIO

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath("../.."))

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import create_action, add_actions, keybinding
from prymatex.utils.i18n import ugettext as _

from prymatex import resources

# Note: string and unicode data types will be formatted with '%s' (see below)
SUPPORTED_FORMATS = {
    'single': '%.3f',
    'double': '%.3f',
    'float_': '%.3f',
    'longfloat': '%.3f',
    'float32': '%.3f',
    'float64': '%.3f',
    'float96': '%.3f',
    'float128': '%.3f',
    'csingle': '%r',
    'complex_': '%r',
    'clongfloat': '%r',
    'complex64': '%r',
    'complex128': '%r',
    'complex192': '%r',
    'complex256': '%r',
    'byte': '%d',
    'short': '%d',
    'intc': '%d',
    'int_': '%d',
    'longlong': '%d',
    'intp': '%d',
    'int8': '%d',
    'int16': '%d',
    'int32': '%d',
    'int64': '%d',
    'ubyte': '%d',
    'ushort': '%d',
    'uintc': '%d',
    'uint': '%d',
    'ulonglong': '%d',
    'uintp': '%d',
    'uint8': '%d',
    'uint16': '%d',
    'uint32': '%d',
    'uint64': '%d',
    'bool_': '%r',
    'bool8': '%r',
    'bool': '%r',
}

def is_float(ptype):
    """Return True if datatype ptype is a float kind"""
    return isinstance(ptype, float)

def is_number(ptype):
    """Return True is datatype ptype is a number kind"""
    return isinstance(ptype, (int, float))

def get_idx_rect(index_list):
    """Extract the boundaries from a list of indexes"""
    rows, cols = zip(*[(i.row(), i.column()) for i in index_list])
    return ( min(rows), max(rows), min(cols), max(cols) )


class ArrayModel(QtCore.QAbstractTableModel):
    """Array Editor Table Model"""
    def __init__(self, data, format="%.3f", xlabels=None, ylabels=None,
                 readonly=False, parent=None):
        QtCore.QAbstractTableModel.__init__(self)

        self.dialog = parent
        self.changes = {}
        self.xlabels = xlabels
        self.ylabels = ylabels
        self.readonly = readonly
        self.test_array = [0]

        # Backgroundcolor settings
        huerange = [.66, .99] # Hue
        self.sat = .7 # Saturation
        self.val = 1. # Value
        self.alp = .6 # Alpha-channel

        self._data = data
        self.ptype = type(data[0])
        self._format = format
        
        self.vmin = None
        self.vmax = None
        self.hue0 = None
        self.dhue = None
        self.bgcolor_enabled = False
        
        
    def get_format(self):
        """Return current format"""
        # Avoid accessing the private attribute _format from outside
        return self._format

    def get_data(self):
        """Return data"""
        return self._data

    def set_format(self, format):
        """Change display format"""
        self._format = format
        self.reset()

    def columnCount(self, qindex=QtCore.QModelIndex()):
        """Array column number"""
        return 2

    def rowCount(self, qindex=QtCore.QModelIndex()):
        """Array row number"""
        return len(self._data)

    def bgcolor(self, state):
        """Toggle backgroundcolor"""
        self.bgcolor_enabled = state > 0
        self.reset()

    def get_value(self, index):
        i = index.row()
        j = index.column()
        return self.changes.get((i, j), self._data[i][j])

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Cell content"""
        if not index.isValid():
            return None
        value = self.get_value(index)
        if role == QtCore.Qt.DisplayRole:
            return self._format % value
        elif role == QtCore.Qt.TextAlignmentRole:
            return int(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        elif role == QtCore.Qt.BackgroundColorRole and self.bgcolor_enabled\
             and value is not np.ma.masked:
            hue = self.hue0+\
                  self.dhue*(self.vmax-self.color_func(value))\
                  /(self.vmax-self.vmin)
            hue = float(np.abs(hue))
            color = QtGui.QColor.fromHsvF(hue, self.sat, self.val, self.alp)
            return color


    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Cell content change"""
        if not index.isValid() or self.readonly:
            return False
        i = index.row()
        j = index.column()
        if self.ptype == bool:
            try:
                val = bool(float(value))
            except ValueError:
                val = value.lower() == "true"
        elif isinstance(self.ptype, basestring):
            val = value
        else:
            if value.lower().startswith('e') or value.lower().endswith('e'):
                return False
            try:
                val = complex(value)
                if not val.imag:
                    val = val.real
            except ValueError, e:
                QtGui.QMessageBox.critical(self.dialog, "Error",
                                     "Value error: %s" % str(e))
                return False
        try:
            self.test_array[0] = val # will raise an Exception eventually
        except OverflowError, e:
            print type(e.message)
            QtGui.QMessageBox.critical(self.dialog, "Error",
                                 "Overflow error: %s" % e.message)
            return False

        # Add change to self.changes
        self.changes[(i, j)] = val
        self.emit(QtCore.SIGNAL("dataChanged(QtCore.QModelIndex,QtCore.QModelIndex)"),
                  index, index)
        if val > self.vmax:
            self.vmax = val
        if val < self.vmin:
            self.vmin = val
        return True

    def flags(self, index):
        """Set editable flag"""
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemFlags(QtCore.QAbstractTableModel.flags(self, index)|
                            QtCore.Qt.ItemIsEditable)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Set header data"""
        if role != QtCore.Qt.DisplayRole:
            return None
        labels = self.xlabels if orientation == QtCore.Qt.Horizontal else self.ylabels
        if labels is None:
            return int(section)
        else:
            return labels[section]


class ArrayDelegate(QtGui.QItemDelegate):
    """Array Editor Item Delegate"""
    def __init__(self, ptype, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.ptype = ptype

    def createEditor(self, parent, option, index):
        """Create editor widget"""
        model = index.model()
        value = model.get_value(index)
        if self.ptype == bool:
            value = not value
            model.setData(index, value)
            return
        else:
            editor = QtGui.QLineEdit(parent)
            editor.setAlignment(QtCore.Qt.AlignCenter)
            if is_number(self.ptype):
                editor.setValidator(QtGui.QDoubleValidator(editor))
            self.connect(editor, QtCore.SIGNAL("returnPressed()"),
                         self.commitAndCloseEditor)
            return editor

    def commitAndCloseEditor(self):
        """Commit and close editor"""
        editor = self.sender()
        self.emit(QtCore.SIGNAL("commitData(QtGui.QWidget*)"), editor)
        self.emit(QtCore.SIGNAL("closeEditor(QtGui.QWidget*)"), editor)

    def setEditorData(self, editor, index):
        """Set editor widget's data"""
        text = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setText(text)


#TODO: Implement "Paste" (from clipboard) feature
class ArrayView(QtGui.QTableView):
    """Array view class"""
    def __init__(self, parent, model, ptype, shape):
        QtGui.QTableView.__init__(self, parent)

        self.setModel(model)
        self.setItemDelegate(ArrayDelegate(ptype, self))
        total_width = 0
        for k in xrange(shape[1]):
            total_width += self.columnWidth(k)
        self.viewport().resize(min(total_width, 1024), self.height())
        self.shape = shape
        self.menu = self.setup_menu()

    def resize_to_contents(self):
        """Resize cells to contents"""
        size = 1
        for dim in self.shape:
            size *= dim
        if size > 1e5:
            answer = QtGui.QMessageBox.warning(self, _("Array editor"),
                                         _("Resizing cells of a table of such "
                                           "size could take a long time.\n"
                                           "Do you want to continue anyway?"),
                                         QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.No:
                return
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setup_menu(self):
        """Setup context menu"""
        self.copy_action = create_action(self, { 'text':_( "Copy"),
                                         'shortcut':keybinding("Copy"),
                                         'icon':resources.getIcon('editcopy.png'),
                                         'triggered':self.copy,
                                         'context':QtCore.Qt.WidgetShortcut })
        menu = QtGui.QMenu(self)
        add_actions(menu, [self.copy_action, ])
        return menu

    def contextMenuEvent(self, event):
        """Reimplement Qt method"""
        self.menu.popup(event.globalPos())
        event.accept()
        
    def keyPressEvent(self, event):
        """Reimplement Qt method"""
        if event == QtGui.QKeySequence.Copy:
            self.copy()
        else:
            QtGui.QTableView.keyPressEvent(self, event)

    def _sel_to_text(self, cell_range):
        """Copy an array portion to a unicode string"""
        row_min, row_max, col_min, col_max = get_idx_rect(cell_range)
        _data = self.model().get_data()
        output = StringIO.StringIO()
        np.savetxt(output,
                  _data[row_min:row_max+1, col_min:col_max+1],
                  delimiter='\t')
        contents = output.getvalue()
        output.close()
        return contents
    
    def copy(self):
        """Copy text to clipboard"""
        cliptxt = self._sel_to_text( self.selectedIndexes() )
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(cliptxt)


class ArrayEditorWidget(QtGui.QWidget):
    def __init__(self, parent, data, readonly=False,
                 xlabels=None, ylabels=None):
        QtGui.QWidget.__init__(self, parent)
        self.data = data
        self.old_data_shape = None
        ptype = type(self.data[0])
        shape = (1,1)
        format = '%s'
        self.model = ArrayModel(self.data, format=format, xlabels=xlabels,
                                ylabels=ylabels, readonly=readonly, parent=self)
        self.view = ArrayView(self, self.model, ptype, shape)
        
        btn_layout = QtGui.QHBoxLayout()
        btn_layout.setAlignment(QtCore.Qt.AlignLeft)
        btn = QtGui.QPushButton(_( "Format"))
        # disable format button for int type
        btn.setEnabled(is_float(ptype))
        btn_layout.addWidget(btn)
        self.connect(btn, QtCore.SIGNAL("clicked()"), self.change_format)
        btn = QtGui.QPushButton(_( "Resize"))
        btn_layout.addWidget(btn)
        self.connect(btn, QtCore.SIGNAL("clicked()"), self.view.resize_to_contents)
        bgcolor = QtGui.QCheckBox(_( 'Background color'))
        bgcolor.setChecked(self.model.bgcolor_enabled)
        bgcolor.setEnabled(self.model.bgcolor_enabled)
        self.connect(bgcolor, QtCore.SIGNAL("stateChanged(int)"), self.model.bgcolor)
        btn_layout.addWidget(bgcolor)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(btn_layout)        
        self.setLayout(layout)
        
    def accept_changes(self):
        """Accept changes"""
        for (i, j), value in self.model.changes.iteritems():
            self.data[i][j] = value
        if self.old_data_shape is not None:
            self.data.shape = self.old_data_shape
            
    def reject_changes(self):
        """Reject changes"""
        if self.old_data_shape is not None:
            self.data.shape = self.old_data_shape
        
    def change_format(self):
        """Change display format"""
        format, valid = QtGui.QInputDialog.getText(self, _( 'Format'),
                                 _( "Float formatting"),
                                 QtGui.QLineEdit.Normal, self.model.get_format())
        if valid:
            format = str(format)
            try:
                format % 1.1
            except:
                QtGui.QMessageBox.critical(self, _("Error"),
                                     _("Format (%s) is incorrect") % format)
                return
            self.model.set_format(format)    


class ListEditor(QtGui.QDialog):
    """Array Editor Dialog"""    
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        # Destroying the C++ object right after closing the dialog box,
        # otherwise it may be garbage-collected in another QThread
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.data = None
        self.arraywidget = None
        self.stack = None
        self.layout = None
    
    def setup_and_check(self, data, title='', readonly=False,
                        xlabels=None, ylabels=None):
        """
        Setup ListEditor:
        return False if data is not supported, True otherwise
        """
        self.data = data
        is_record_array = False
        is_masked_array = False
        if len(data) == 0:
            self.error(_("List is empty"))
            return False
        
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.setWindowIcon(resources.getIcon('arredit.png'))
        if title:
            title = unicode(title) # in case title is not a string
        else:
            title = _("List editor")
        if readonly:
            title += ' (' + _('read only') + ')'
        self.setWindowTitle(title)
        self.resize(600, 500)
        
        # Stack widget
        self.stack = QtGui.QStackedWidget(self)
        self.stack.addWidget(ArrayEditorWidget(self, data, readonly,
                                                   xlabels, ylabels))
        self.arraywidget = self.stack.currentWidget()
        self.connect(self.stack, QtCore.SIGNAL('currentChanged(int)'),
                     self.current_widget_changed)
        self.layout.addWidget(self.stack, 1, 0)

        # Buttons configuration
        btn_layout = QtGui.QHBoxLayout()
        if is_record_array or is_masked_array:
            if is_record_array:
                btn_layout.addWidget(QtGui.QLabel(_("Record array fields:")))
                names = []
                for name in data.ptype.names:
                    field = data.ptype.fields[name]
                    text = name
                    if len(field) >= 3:
                        title = field[2]
                        if not isinstance(title, basestring):
                            title = repr(title)
                        text += ' - '+title
                    names.append(text)
            else:
                names = [_('Masked data'), _('Data'), _('Mask')]
            ra_combo = QtGui.QComboBox(self)
            self.connect(ra_combo, QtCore.SIGNAL('currentIndexChanged(int)'),
                         self.stack.setCurrentIndex)
            ra_combo.addItems(names)
            btn_layout.addWidget(ra_combo)
            if is_masked_array:
                label = QtGui.QLabel(_("<u>Warning</u>: changes are applied separately"))
                label.setToolTip(_("For performance reasons, changes applied "\
                                   "to masked array won't be reflected in "\
                                   "array's data (and vice-versa)."))
                btn_layout.addWidget(label)
            btn_layout.addStretch()
        bbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.connect(bbox, QtCore.SIGNAL("accepted()"), QtCore.SLOT("accept()"))
        self.connect(bbox, QtCore.SIGNAL("rejected()"), QtCore.SLOT("reject()"))
        btn_layout.addWidget(bbox)
        self.layout.addLayout(btn_layout, 2, 0)
        
        self.setMinimumSize(400, 300)
        
        # Make the dialog act as a window
        self.setWindowFlags(QtCore.Qt.Window)
        
        return True
        
    def current_widget_changed(self, index):
        self.arraywidget = self.stack.widget(index)
        
    def accept(self):
        """Reimplement Qt method"""
        for index in range(self.stack.count()):
            self.stack.widget(index).accept_changes()
        QtGui.QDialog.accept(self)
        
    def get_value(self):
        """Return modified array -- this is *not* a copy"""
        # It is import to avoid accessing Qt C++ object as it has probably
        # already been destroyed, due to the QtCore.Qt.WA_DeleteOnClose attribute
        return self.data

    def error(self, message):
        """An error occured, closing the dialog box"""
        QtGui.QMessageBox.critical(self, _("Array editor"), message)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.reject()

    def reject(self):
        """Reimplement Qt method"""
        if self.arraywidget is not None:
            for index in range(self.stack.count()):
                self.stack.widget(index).reject_changes()
        QtGui.QDialog.reject(self)


def test_edit(data, title="", xlabels=None, ylabels=None,
              readonly=False, parent=None):
    """Test subroutine"""
    dlg = ListEditor(parent)
    if dlg.setup_and_check(data, title, xlabels=xlabels, ylabels=ylabels,
                           readonly=readonly) and dlg.exec_():
        return dlg.get_value()
    else:
        import sys
        sys.exit()


def test():
    """Array editor test"""
    _app = QtGui.QApplication([])
    
    arr = [[1, "kjrekrjkejr"]]
    print "out:", test_edit(arr, "string array")
    arr = [[1, u"kjrekrjkejr"]]
    print "out:", test_edit(arr, "unicode array")
    arr = [[1, 0], [1, 0]]
    print "out:", test_edit(arr, "masked array")
    arr = [[0, 0.0], [0, 0.0], [0, 0.0]]
    print "out:", test_edit(arr, "record array with titles")
    arr_in = [True, False, True]
    print "in:", arr_in
    arr_out = test_edit(arr_in, "bool array")
    print "out:", arr_out
    print arr_in is arr_out
    arr = [1, 2, 3]
    print "out:", test_edit(arr, "int array")


if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath("../.."))
    print sys.path
    test()
