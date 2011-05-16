'''
Created on 15/05/2011

@author: diego
'''
from PyQt4 import QtCore
from prymatex.gui.config.ui_envvars import Ui_EnvVariables
from prymatex.gui.config.widgets import PMXConfigBaseWidget
from prymatex.core.base import PMXObject

class PMXEnvVariablesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, settingGroup, parent = None):
        super(PMXEnvVariablesTableModel, self).__init__(parent)
        self.values = [[], [], []]
        self.settingGroup = settingGroup
        shellVariables = self.settingGroup.value('shellVariables')
        for var in shellVariables:
            self.values[0].append(var['variable'])
            self.values[1].append(var['value'])
            self.values[2].append(var['enabled'])
    
    def rowCount(self, parent):
        return len(self.values[0])

    def columnCount(self, parent):
        return 2
    
    def data(self, index, role):
        if not index.isValid: return QtCore.QVariant()

        if role == QtCore.Qt.CheckStateRole:
            return QtCore.Qt.Unchecked if self.values[index.column()][index.row()] else QtCore.Qt.Checked 
        elif role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.values[index.column()][index.row()])
    
    def flags(self, index):
        result = super(PMXEnvVariablesTableModel, self).flags(index);
        if index.column() == 0:
            result |= QtCore.Qt.ItemIsUserCheckable
        return result

class PMXEnvVariablesWidgets(PMXConfigBaseWidget, Ui_EnvVariables, PMXObject):
    '''
    Variables
    '''
    def __init__(self, parent = None):
        super(PMXEnvVariablesWidgets, self).__init__(parent)
        self.setupUi(self)
        self.configure()
        self.model = PMXEnvVariablesTableModel(self.pmxApp.settings.getGroup('Manager'))
        self.tableView.setModel(self.model)
        
    def on_pushAdd_pressed(self):
        #r = self.tableView.insertRow(0)
        #print r
        pass
        
    def on_pushRemove_pressed(self):
        pass
