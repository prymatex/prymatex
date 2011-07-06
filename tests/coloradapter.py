import os, sys
sys.path.append(os.path.abspath('..'))

if __name__ == "__main__":
    from PyQt4 import QtGui
    from prymatex.gui.support.qtadapter import RGBA2QColor, QColor2RGBA
    try:
        color = RGBA2QColor('#ee5533ff')
        print color.rgba()
        rgba = QColor2RGBA(color.rgba())
        print rgba
    except Exception, e:
        print e
    raw_input()
    