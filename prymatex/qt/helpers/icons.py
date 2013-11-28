#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.utils import text

__all__ = [ "combine_icons", "get_std_icon", "text2iconname" ]

def text2iconname(source, sufix = "", prefix = ""):
    """&Text Button name -> %{prefix}-text-button-name-%{sufix}"""
    source = [ text.to_alphanumeric(chunk) for chunk in text.lower_case(source).split() ]
    if prefix:
        source.insert(0, prefix)
    if sufix:
        source.append( sufix )
    return '-'.join(source)

def combine_icons(icon1, icon2, scale = 1):
    newIcon = QtGui.QIcon()
    sizes = icon1.availableSizes()
    if not sizes:
        sizes = [ QtCore.QSize(16, 16), QtCore.QSize(22, 22), QtCore.QSize(32, 32), QtCore.QSize(48, 48) ]
    for size in sizes:
        pixmap1 = icon1.pixmap(size)
        pixmap2 = icon2.pixmap(size)
        pixmap2 = pixmap2.scaled(pixmap1.width() * scale, pixmap1.height() * scale)
        result = QtGui.QPixmap(size)
        result.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(result)
        painter.drawPixmap(0, 0, pixmap1)
        painter.drawPixmap(pixmap1.width() - pixmap2.width(), pixmap1.height() - pixmap2.height(), pixmap2)
        painter.end()
        newIcon.addPixmap(result)
    return newIcon

def get_std_icon(name):
    """Get standard platform icon Call 'show_std_icons()' for details"""
    if not name.startswith('SP_'):
        name = 'SP_' + name
    standardIconName = getattr(QtGui.QStyle, name, None)
    if standardIconName is not None:
        return QtGui.QWidget().style().standardIcon( standardIconName )

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
                label.setPixmap(icon.pixmap(16, 16))
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
    app = QtGui.QApplication([])
    dialog = ShowStdIcons(None)
    print(get_std_icon("cacho"))
    dialog.show()
    import sys
    sys.exit(app.exec_())


if __name__ == "__main__":
    show_std_icons()