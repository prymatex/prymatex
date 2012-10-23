#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

def get_std_icon(name, size=None):
    """Get standard platform icon
    Call 'show_std_icons()' for details"""
    if not name.startswith('SP_'):
        name = 'SP_'+name
    icon = QtGui.QWidget().style().standardIcon( getattr(QtGui.QStyle, name) )
    if size is None:
        return icon
    else:
        return QtGui.QIcon( icon.pixmap(size, size) )
        
class ShowStdIcons(QtGui.QWidget):
    """
    Dialog showing standard icons
    """
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QHBoxLayout()
        row_nb = 14
        cindex = 0
        for child in dir(QtGui.QStyle):
            if child.startswith('SP_'):
                if cindex == 0:
                    col_layout = QtGui.QVBoxLayout()
                icon_layout = QtGui.QHBoxLayout()
                icon = get_std_icon(child)
                label = QtGui.QLabel()
                label.setPixmap(icon.pixmap(32, 32))
                icon_layout.addWidget( label )
                icon_layout.addWidget( QtGui.QLineEdit(child.replace('SP_', '')) )
                col_layout.addLayout(icon_layout)
                cindex = (cindex+1) % row_nb
                if cindex == 0:
                    layout.addLayout(col_layout)                    
        self.setLayout(layout)
        self.setWindowTitle('Standard Platform Icons')
        self.setWindowIcon(get_std_icon('TitleBarMenuButton'))


def show_std_icons():
    """
    Show all standard Icons
    """
    app = qapplication()
    dialog = ShowStdIcons(None)
    dialog.show()
    import sys
    sys.exit(app.exec_())


if __name__ == "__main__":
    show_std_icons()