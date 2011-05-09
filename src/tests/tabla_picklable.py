# encoding: utf-8
from PyQt4.Qt import *
if __name__ == "__main__":
    import sys, os
    path = os.path.dirname(os.path.abspath(__file__))
    import_path = os.path.abspath(os.path.join(path, '..', ))
    sys.path.insert(0, import_path)
    
    
from prymatex.core.exceptions import APIUsageError
from prymatex.models import *

from pprint import pprint
import pickle
import os

def sanitize_data(data):
    if isinstance(data, (QString, QByteArray, )):
        return unicode(data)
    return data

class MiTablaDeBundles(PMXTableBase):
    uuid = PMXTableField(title = "UUID", editable = False)
    name = PMXTableField(title = "Name")
    MY_FILE = '/tmp/data.data'
    
    def get_list(self):
        lista_de_cosas = []
        for i in xrange(self.rowCount()):
            
            diccionario_fila = {}
            for n, field in enumerate(self._meta.fields):
                data = self.data(self.index(i, n)).toPyObject()
                diccionario_fila[ field.name ] = sanitize_data(data)
                
            lista_de_cosas.append(diccionario_fila)
        #pprint(lista_de_cosas)
        return lista_de_cosas
    
    def pickle(self):
        try:
            pickle.dump(self.get_list(), file(self.MY_FILE, 'w'))
        except IOError:
            print "Sin cache!"
    
    def unpickle(self):
        '''
        @return: True si pudo despicklear, False en caso contrario
        '''
        if os.path.isfile(self.MY_FILE):
            try:
                lista = pickle.load(file(self.MY_FILE))
                print lista
                for diccionario in lista:
                    self.addRowFromKwargs(**diccionario)
                return True
            except Exception, e:
                print "Error de depickleado", e
        return False
                
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = QTableView()
    model = MiTablaDeBundles()
    win.setModel(model)
    model.setColumnDelegatesFromFields(win)
    
    if not win.model().unpickle():
        print "No despickleo nada"
        model.addRowFromKwargs(uuid = '000-2--3-3-4-4', name = "Python")
        model.addRowFromKwargs(uuid = '000-2--3-3-4-5', name = "Ruby")
        model.addRowFromKwargs(uuid = '000-2--3-3-4-6', name = "Perl")
        model.addRowFromKwargs(uuid = '000-2--3-3-4-6', name = "HTML")
    #model.addRowFromKwargs(nombre = "Nahuel", apellido = u"Defossé", direccion = "Moreno 46")
    #model.addRowFromKwargs(nombre = "Pablo Enrrique", apellido = "Petenello", direccion = "Moreno 46")
    #model.addRowFromKwargs(nombre = "Diego Marco", apellido = "van Haaster", direccion = "Moreno 46")
    #model.sort('apellido')
    
    QApplication.instance().aboutToQuit.connect(model.pickle)
    
    
    
    win.setWindowTitle(unicode(model.__class__.__name__))
    win.setGeometry(400,200, 400, 400)
    print model._meta
    win.show()
    sys.exit(app.exec_())
    