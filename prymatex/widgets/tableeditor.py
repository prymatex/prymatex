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

class TableModel(QtCore.QAbstractTableModel):
    """Table Model"""
    def __init__(self, data, types=None, formats=None, xlabels=None, ylabels=None,
            editable=False, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.changes = {}
        self._data = data
        if self._data and not isinstance(self._data[0], (tuple, list)):
            self._fixed = True
            self._data = [ (e, ) for e in self._data ]

        if self._data:        
            firstItem = self._data[0]
            types = types or map(lambda e: type(e), firstItem)
            formats = formats or [ "%s" for _ in firstItem ]
        
        assert types is not None and formats is not None, "Type, format error"
        
        self._columnCount = len(types)
        self._types = types
        self._formats = formats if isinstance(formats, (list, tuple)) else\
            [ str(formats) for _ in range(self._columnCount) ]
        self._xlabels = xlabels
        self._ylabels = ylabels
        self._editable = editable if isinstance(editable, (list, tuple)) else\
            [ bool(editable) for _ in range(self._columnCount) ]
            

    def columnCount(self, qindex=QtCore.QModelIndex()):
        """Array column number"""
        return self._columnCount

    def rowCount(self, qindex=QtCore.QModelIndex()):
        """Array row number"""
        return len(self._data)

    def get_value(self, index):
        i = index.row()
        j = index.column()
        return self.changes.get((i, j), self._data[i][j])

    def get_format(self, index):
        return self._formats[index.column()]

    def is_editable(self, index):
        return self._editable[index.column()]

    def get_background(self, index):
        i = index.row()
        j = index.column()
        color = QtCore.Qt.green if (i, j) in self.changes else QtCore.Qt.red
        return color
        
    def get_type(self, index):
        return self._types[index.column()]
        
    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Cell content"""
        if not index.isValid():
            return None
        value = self.get_value(index)
        if role == QtCore.Qt.DisplayRole:
            format = self.get_format(index)
            return format % value
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
        elif role == QtCore.Qt.BackgroundColorRole:
            return self.get_background(index)


    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Cell content change"""
        if not index.isValid() or not self.is_editable(index):
            return False
        val = None
        ctype = self.get_type(index)
        if ctype in [ bool ]:
            val = value not in [ "false", "False", "0" ]
        else:
            try:
                val = ctype(value)
            except:
                pass
        
        if val is None:
            return False
            
        # Add change to self.changes
        self.changes[(index.row(), index.column())] = val
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        """Set editable flag"""
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        flags = QtCore.QAbstractTableModel.flags(self, index)
        
        if self.is_editable(index):
            flags |= QtCore.Qt.ItemIsEditable
        return flags

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Set header data"""
        if role != QtCore.Qt.DisplayRole:
            return None
        labels = self._xlabels if orientation == QtCore.Qt.Horizontal else self._ylabels
        if labels is None:
            return int(section)
        else:
            return labels[section]


class TableDelegate(QtGui.QItemDelegate):
    """Array Editor Item Delegate"""
    def createEditor(self, parent, option, index):
        """Create editor widget"""
        model = index.model()
        value = model.get_value(index)
        ctype = model.get_type(index)
        if ctype in [ bool ]:
            value = not value
            model.setData(index, value)
        else:
            editor = QtGui.QLineEdit(parent)
            editor.setAlignment(QtCore.Qt.AlignCenter)
            if ctype in [ int, long ]:
                editor.setValidator(QtGui.QDoubleValidator(editor))
            self.connect(editor, QtCore.SIGNAL("returnPressed()"),
                         self.commitAndCloseEditor)
            return editor

    def commitAndCloseEditor(self):
        """Commit and close editor"""
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)

    def setEditorData(self, editor, index):
        """Set editor widget's data"""
        text = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setText(text)


class TableEditorWidget(QtGui.QWidget):
    def __init__(self, data, editable=False, xlabels=None, 
            ylabels=None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.data = data
        formats = '%s'
        self.model = TableModel(self.data, formats=formats, xlabels=xlabels,
                                ylabels=ylabels, editable=editable, parent = self)
        self.view = QtGui.QTableView(self)
        self.view.setModel(self.model)

        btn_layout = QtGui.QHBoxLayout()
        btn_layout.setAlignment(QtCore.Qt.AlignLeft)
        btn = QtGui.QPushButton(_( "Resize"))
        btn_layout.addWidget(btn)
        self.connect(btn, QtCore.SIGNAL("clicked()"), self.resize_to_contents)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(btn_layout)        
        self.setLayout(layout)
    
    def resize_to_contents(self):
        self.view.resizeColumnsToContents()
        self.view.resizeRowsToContents()


    def accept_changes(self):
        """Accept changes"""
        for (i, j), value in self.model.changes.iteritems():
            self.data[i][j] = value


class TableEditorDialog(QtGui.QDialog):
    """Array Editor Dialog"""    
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        # Destroying the C++ object right after closing the dialog box,
        # otherwise it may be garbage-collected in another QThread
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.data = None

    def setup_and_check(self, data, title='', editable=False,
                        xlabels=None, ylabels=None):
        """
        Setup ListEditor:
        return False if data is not supported, True otherwise
        """
        self.data = data
        if len(data) == 0:
            self.error(_("List is empty"))
            return False
        
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        if title:
            title = unicode(title) # in case title is not a string
        else:
            title = _("List editor")
        if editable:
            title += ' (' + _('read only') + ')'
        self.setWindowTitle(title)
        self.resize(600, 500)
        
        # Stack widget
        self.stack = QtGui.QStackedWidget(self)
        self.tablewidget = TableEditorWidget(data, editable, xlabels, ylabels, parent = self)
        self.stack.addWidget(self.tablewidget)
        self.connect(self.stack, QtCore.SIGNAL('currentChanged(int)'),
                     self.current_widget_changed)
        self.layout.addWidget(self.stack, 1, 0)

        # Buttons configuration
        btn_layout = QtGui.QHBoxLayout()
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
        self.tablewidget = self.stack.widget(index)
        
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


def test_edit(data, title="", xlabels=None, ylabels=None,
              editable=False, parent=None):
    """Test subroutine"""
    dlg = TableEditorDialog(parent)
    if dlg.setup_and_check(data, title, xlabels=xlabels, ylabels=ylabels,
                           editable=editable) and dlg.exec_():
        return dlg.get_value()
    else:
        import sys
        sys.exit()


def test():
    """Array editor test"""
    _app = QtGui.QApplication([])
    
    #arr = [(1, "kjrekrjkejr")]
    #print "out:", test_edit(arr, "string array")
    #arr = [(1, u"kjrekrjkejr")]
    #print "out:", test_edit(arr, "unicode array", editable= True)
    #arr = [(1, 0), (1, 0)]
    #print "out:", test_edit(arr, "masked array")
    #arr = [[0, 0.0], [0, 0.0], [0, 0.0]]
    #print "out:", test_edit(arr, "record array with titles")
    arr_in = [True, False, True]
    print "in:", arr_in
    arr_out = test_edit(arr_in, "bool array", editable= True)
    print "out:", arr_out
    print arr_in is arr_out
    arr = [1, 2, 3]
    print "out:", test_edit(arr, "int array")


if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath("../.."))
    print sys.path
    test()
