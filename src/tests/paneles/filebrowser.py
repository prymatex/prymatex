from PyQt4.QtCore import *
from PyQt4.QtGui import *
from os.path import join, abspath, isfile, isdir, dirname
import sys
import os

    
         
class myTree(QTreeView):
    def __init__(self, parent = None):
        super(myTree, self).__init__(parent)
        
        self.modelo = QFileSystemModel()
        self.modelo.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.AllEntries)
        self.modelo.setNameFilterDisables(False)
        self.setModel(self.modelo)
        
        self.setRoot()
        self.setupActions()
        self.ocultarColumnas()
    
    def setRoot(self):
        start_dir = os.getcwd()
        self.setRootIndex(self.model().index(start_dir))
        self.modelo.setRootPath(start_dir)
        
    def ocultarColumnas(self):
        #ocultamos el header 
        self.setHeaderHidden(True)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

    def setupActions(self):
        self.actionOcultar = QAction(self.trUtf8("Ocultar"), self )
        self.connect(self.actionOcultar, SIGNAL("triggered()"), self.ocultar)
        
        self.actionSetRootPath = QAction(self.trUtf8("Set as root"), self)
        self.connect(self.actionSetRootPath, SIGNAL("triggered()"), self.setRootPath)
        
        self.actionGoUp = QAction(self.trUtf8("Go Up"), self)
        self.connect(self.actionGoUp, SIGNAL("triggered()"), self.goUp)
        
        self.actionCreateNewFolder = QAction(self.trUtf8("Folder"), self)
        self.connect(self.actionCreateNewFolder, SIGNAL("triggered()"), self.CreateNewFolder)
        
    def contextMenuEvent(self, event):
        '''slot'''
        self.index_at = self.indexAt(event.pos())
        menu = QMenu(self)
        
        
        menu.addAction(self.actionGoUp)
        menu.addAction(self.actionOcultar)
        
        #Si el index del modelo es una carpeta
        #mostramos la opcion de setear ese dir como root
        if os.path.isdir(self.modelo.filePath(self.currentIndex())):
            menu.addAction(self.actionSetRootPath)
        
        menu.addSeparator()
        
        sub_menu_new = QMenu(self)
        sub_menu_new.setTitle('New')
        sub_menu_new.addAction(self.actionCreateNewFolder)
        menu.addMenu(sub_menu_new)
        
        menu.exec_(event.globalPos())
        
        del menu
        del sub_menu_new
        
    def ocultar(self):
        '''slot'''
        print self.modelo.filePath(self.currentIndex())
        
    def setRootPath(self):
        '''slot'''
        self.setRootIndex(self.currentIndex())
        self.modelo.setRootPath(self.modelo.filePath(self.currentIndex()))
    
    def CreateNewFolder(self):
        '''slot'''
        #obtenemos el path para crear la nueva carpeta
        
        if os.path.isdir(self.modelo.filePath(self.currentIndex())):
            path = self.modelo.filePath(self.currentIndex())
        else:
            path = self.modelo.rootPath()
        dialogo = NewFileDialog()
        salida = dialogo.exec_()
        print salida
        
            
    def goUp(self):
        
        current_top = unicode(self.model().filePath(self.rootIndex()))
        #self.tree.setRootIndex(self.tree.model().index(QDir.currentPath()))
        upper = abspath(join(current_top, '..'))
        
        self.setRootIndex(self.model().index(upper))
        self.modelo.setRootPath(self.modelo.filePath(self.model().index(upper)))
    
    def filtrar(self, texto):
        filtro = texto.__str__();
        if filtro:
            self.modelo.setNameFilters(filtro.split(' '))
        else:
            self.modelo.setNameFilters(['*.*'])
            

class myFilterEdit(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
    
    def event(self, event):
        if (event.type()==QEvent.KeyRelease):
            self.emit(SIGNAL("estanTecleando"))
        return QLineEdit.event(self, event)



class miVentana(object):
    
    def setupUi(self, myParent):
        myParent.setObjectName("MyWidget")
        myParent.resize(300, 600)
        
        #the vertical box layouy
        self.vbox = QVBoxLayout(myParent)
        #-------------------------------------
        # HEADER
        
        #ahora creo el footer que es un label y un lineEdit 
        #para el filtro del filebrowser
        self.header = QHBoxLayout()
        self.lb_filtro = QLabel("Filtro:")
        self.filtro  = myFilterEdit()
        myParent.connect(self.filtro, SIGNAL("estanTecleando"), self.filtrar)
        
        self.header.addWidget(self.lb_filtro)
        self.header.addWidget(self.filtro)
        
        #self.vbox.addWidget()
        self.vbox.addLayout(self.header)
        
        
        #-------------------------------------
        # CONTENT: TreeView
        
        
        self.tree = myTree(myParent)
                
        self.vbox.addWidget(self.tree)
        #-------------------------------------
        # FOOTER: 
        self.btn_exit = QPushButton()
        self.btn_exit.setText("Exit")
        self.vbox.addWidget(self.btn_exit)
        myParent.connect(self.btn_exit, SIGNAL("clicked()"),self.onExit)
        
        #-------------------------------------
    
    def onExit(self):
        sys.exit()
        
    def filtrar(self):
        self.tree.filtrar(self.filtro.text())
        
    


class NewFileDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        #self.setModal(True)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        
        #----
        #HEADER
        self.header = QHBoxLayout()
        self.lb_folder = QLabel("Folder name:")
        self.ql_folder = myFilterEdit()
        self.header.addWidget(self.lb_folder)
        self.header.addWidget(self.ql_folder)
        
        self.vbox.addLayout(self.header)
        
        #----
        #FOOTER
        self.footer = QHBoxLayout()
        
        self.btn_accept = QPushButton("Accept")
        self.btn_accept.setEnabled(False)
        self.btn_cancel = QPushButton("Cancel")
        
        self.footer.addWidget(self.btn_cancel)
        self.footer.addWidget(self.btn_accept)
        
        self.vbox.addLayout(self.footer)
        
        
        #-----
        #Conexiones
        #self.connect(self.ql_folder, SIGNAL("textEdited()"), self.cambio_el_texto)
        self.connect(self.ql_folder, SIGNAL("estanTecleando"), self.cambio_el_texto)
        self.connect(self.btn_cancel, SIGNAL("clicked()"), self.cancelar)
        self.connect(self.btn_accept, SIGNAL("clicked()"), self.aceptar)
        
    def cambio_el_texto(self):
        '''
        Se encarga de activar o desactivar el boton de aceptar
        en caso de que exista texto en el QlineEdit
        '''
        
        texto =  self.ql_folder.text()
        if texto:
            if not self.btn_accept.isEnabled():
                self.btn_accept.setEnabled(True)
        else:
            print texto
            self.btn_accept.setEnabled(False);
        
    def cancelar(self):
        self.reject()
        
    def aceptar(self):
        retorno = super(NewFileDialog, self).exec_()
        if retorno == QDialog.Accepted:
            return self.ql_folder.text()
        
        
        
        
        

def testDialog():
    app = QApplication(sys.argv)
    MyWidget = QWidget()
    dialogo = NewFileDialog(MyWidget)
    MyWidget.show()
    sys.exit(app.exec_())
    
    #dialogo.setLayout(QVBoxLayout(self))
    #label = QLabel("Folder name:")
        
def main():
    app = QApplication(sys.argv)
    MyWidget = QWidget()
    ui = miVentana()
    
    ui.setupUi(MyWidget)
    MyWidget.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    #testDialog()
    main()
    
    
    
"""
13:56:23) nahuel.defosse@gmail.com:     def exec_(self):
       
            
            
"""

    