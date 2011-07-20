from PyQt4.Qt import QComboBox
import os


class PMXBookmarksPathComboBox(QComboBox):
    '''
    '''

    def pathChanged(self, newPath):
        print "*"* 40
        parts = unicode(newPath).split(os.sep)
        print parts