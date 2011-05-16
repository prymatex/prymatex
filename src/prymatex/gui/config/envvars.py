'''
Created on 15/05/2011

@author: diego
'''
from PyQt4 import QtCore
from prymatex.gui.config.ui_envvars import Ui_EnvVariables
from prymatex.gui.config.widgets import PMXConfigBaseWidget
from prymatex.core.base import PMXObject

class PMXEnvVariablesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, vars = {}, parent = None):
        super(PMXEnvVariablesTableModel, self).__init__(parent)
        self.names = vars.keys()
        self.values = vars.values()
        self.vars = vars
    
    def rowCount(self, parent):
        return len(self.vars)
    
    def columnCount(self, parent):
        return len(self.names)
    
    def data(self, index, role):
        column = index.column()
        row = index.row()
        if column == 0:
            return self.names[row]
        else:
            return self.values[row]
    
    def flags(self, index):
        if index.column() == 0:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable  

class PMXEnvVariablesWidgets(PMXConfigBaseWidget, Ui_EnvVariables, PMXObject):
    '''
    Variables
    '''
    def __init__(self, parent = None):
        super(PMXEnvVariablesWidgets, self).__init__(parent)
        self.setupUi(self)
        self.configure()
        self.model = PMXEnvVariablesTableModel({'pepe': 1, 'pepa': 'algo'})
        self.tableView.setModel(self.model)
        
    def on_pushAdd_pressed(self):
        r = self.tableVariables.insertRow(0)
        print r
        
    def on_pushRemove_pressed(self):
        pass



