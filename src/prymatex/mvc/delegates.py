# encoding: utf-8
from PyQt4.Qt import QItemDelegate, QComboBox

class PMXChoiceItemDelegate(QItemDelegate):
    ''' Mimic django choice field '''
    CHOICES = ()
    
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        print "Creando editor"
        for display_text, data in self.CHOICES:
            editor.addItem(display_text, data)
        return editor

    def setEditorData(self, editor, index):
        data = index.data().toPyObject()
        editor.setCurrentIndex(editor.findData(data))

    def setModelData(self, editor, model, index):
        #return PyQt4.Qt.QItemDelegate.setModelData(self, *args, **kwargs)
        data = editor.itemData(editor.currentIndex())
        model.setData(index, data)
