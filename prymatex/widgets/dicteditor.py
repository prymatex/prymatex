#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex import resources

class DictDelegate(QtGui.QItemDelegate):
    """DictEditor Item Delegate"""
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.inplace = inplace
        self._editors = {} # keep references on opened editors
        
    def get_value(self, index):
        if index.isValid():
            return index.model().get_value(index)
    
    def set_value(self, index, value):
        if index.isValid():
            index.model().set_value(index, value)

    def createEditor(self, parent, option, index):
        """Overriding method createEditor"""
        if index.column() < 3:
            return None
        try:
            value = self.get_value(index)
        except Exception, msg:
            QMessageBox.critical(self.parent(), _("Edit item"),
                                 _("<b>Unable to retrieve data.</b>"
                                   "<br><br>Error message:<br>%s"
                                   ) % unicode(msg))
            return
        key = index.model().get_key(index)
        readonly = isinstance(value, tuple) or self.parent().readonly \
                   or not is_known_type(value)
        #---editor = DictEditor
        if isinstance(value, (list, tuple, dict)) and not self.inplace:
            editor = DictEditor()
            editor.setup(value, key, icon=self.parent().windowIcon(),
                         readonly=readonly)
            self.create_dialog(editor, dict(model=index.model(), editor=editor,
                                            key=key, readonly=readonly))
            return None
        #---editor = ArrayEditor
        elif isinstance(value, (ndarray, MaskedArray))\
             and ndarray is not FakeObject and not self.inplace:
            if value.size == 0:
                return None
            editor = ArrayEditor(parent)
            if not editor.setup_and_check(value, title=key, readonly=readonly):
                return
            self.create_dialog(editor, dict(model=index.model(), editor=editor,
                                            key=key, readonly=readonly))
            return None
        #---showing image
        elif isinstance(value, Image) and ndarray is not FakeObject \
             and Image is not FakeObject:
            arr = array(value)
            if arr.size == 0:
                return None
            editor = ArrayEditor(parent)
            if not editor.setup_and_check(arr, title=key, readonly=readonly):
                return
            conv_func = lambda arr: Image.fromarray(arr, mode=value.mode)
            self.create_dialog(editor, dict(model=index.model(), editor=editor,
                                            key=key, readonly=readonly,
                                            conv=conv_func))
            return None
        #---editor = QDateTimeEdit
        elif isinstance(value, datetime.datetime) and not self.inplace:
            editor = QDateTimeEdit(value, parent)
            editor.setCalendarPopup(True)
            editor.setFont(get_font('dicteditor'))
            self.connect(editor, SIGNAL("returnPressed()"),
                         self.commitAndCloseEditor)
            return editor
        #---editor = QDateEdit
        elif isinstance(value, datetime.date) and not self.inplace:
            editor = QDateEdit(value, parent)
            editor.setCalendarPopup(True)
            editor.setFont(get_font('dicteditor'))
            self.connect(editor, SIGNAL("returnPressed()"),
                         self.commitAndCloseEditor)
            return editor
        #---editor = QTextEdit
        elif isinstance(value, (str, unicode)) and len(value)>40:
            editor = TextEditor(value, key)
            self.create_dialog(editor, dict(model=index.model(), editor=editor,
                                            key=key, readonly=readonly))
            return None
        #---editor = QLineEdit
        elif self.inplace or is_editable_type(value):
            editor = QLineEdit(parent)
            editor.setFont(get_font('dicteditor'))
            editor.setAlignment(Qt.AlignLeft)
            self.connect(editor, SIGNAL("returnPressed()"),
                         self.commitAndCloseEditor)
            return editor
        #---editor = DictEditor for an arbitrary object
        else:
            editor = DictEditor()
            editor.setup(value, key, icon=self.parent().windowIcon(),
                         readonly=readonly)
            self.create_dialog(editor, dict(model=index.model(), editor=editor,
                                            key=key, readonly=readonly))
            return None
            
    def create_dialog(self, editor, data):
        self._editors[id(editor)] = data
        self.connect(editor, SIGNAL('accepted()'),
                     lambda eid=id(editor): self.editor_accepted(eid))
        self.connect(editor, SIGNAL('rejected()'),
                     lambda eid=id(editor): self.editor_rejected(eid))
        editor.show()
        
    def editor_accepted(self, editor_id):
        data = self._editors[editor_id]
        if not data['readonly']:
            index = data['model'].get_index_from_key(data['key'])
            value = data['editor'].get_value()
            conv_func = data.get('conv', lambda v: v)
            self.set_value(index, conv_func(value))
        self._editors.pop(editor_id)
        
    def editor_rejected(self, editor_id):
        self._editors.pop(editor_id)

    def commitAndCloseEditor(self):
        """Overriding method commitAndCloseEditor"""
        editor = self.sender()
        self.emit(SIGNAL("commitData(QWidget*)"), editor)
        self.emit(SIGNAL("closeEditor(QWidget*)"), editor)

    def setEditorData(self, editor, index):
        """Overriding method setEditorData
Model --> Editor"""
        value = self.get_value(index)
        if isinstance(editor, QLineEdit):
            if not isinstance(value, basestring):
                value = repr(value)
            editor.setText(value)
        elif isinstance(editor, QDateEdit):
            editor.setDate(value)
        elif isinstance(editor, QDateTimeEdit):
            editor.setDateTime(QDateTime(value.date(), value.time()))

    def setModelData(self, editor, model, index):
        """Overriding method setModelData
Editor --> Model"""
        if not hasattr(model, "set_value"):
            # Read-only mode
            return
        
        if isinstance(editor, QLineEdit):
            value = editor.text()
            try:
                value = display_to_value(to_qvariant(value),
                                         self.get_value(index),
                                         ignore_errors=False)
            except Exception, msg:
                raise
                QMessageBox.critical(editor, _("Edit item"),
                                     _("<b>Unable to assign data to item.</b>"
                                       "<br><br>Error message:<br>%s"
                                       ) % str(msg))
                return
        elif isinstance(editor, QDateEdit):
            qdate = editor.date()
            value = datetime.date( qdate.year(), qdate.month(), qdate.day() )
        elif isinstance(editor, QDateTimeEdit):
            qdatetime = editor.dateTime()
            qdate = qdatetime.date()
            qtime = qdatetime.time()
            value = datetime.datetime( qdate.year(), qdate.month(),
                                       qdate.day(), qtime.hour(),
                                       qtime.minute(), qtime.second() )
        else:
            # Should not happen...
            raise RuntimeError("Unsupported editor widget")
        self.set_value(index, value)

class DictEditorTableView(QtGui.QTableView):
    pass
