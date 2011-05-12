'''
Created on 12/05/2011

@author: diego
'''
from prymatex.models.base import PMXTableBase, PMXTableField

class PMXEnvironmentVariablesModel(PMXTableBase):
    '''
    Store environment Variables
    '''
    variable = PMXTableField()
    value = PMXTableField()
    enabled = PMXTableField()
    
    def appendBundleRow(self, var):
        self.addRowFromKwargs(
                    var['variable'],
                    var['value'],
                    var['enabled'],
                    )