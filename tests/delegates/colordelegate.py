
from PyQt4.Qt import *


QColor2HTML = lambda color: ("#%2x%2x%2x" % (color.red(), color.green(), color.blue(),)).upper()

def HTML2QColor(htmlColor):
    '''
    @param htmlColor: A html formated color string i.e.: #RRGGBB or #RRGGBBAA
    @return: If htmlColor is a valid color, a QColor isntance
    ''' 
    htmlColor = unicode(htmlColor).strip('#')
    if len(htmlColor) == 3:
        red, green, blue = htmlColor
    elif len(htmlColor) == 6:
        red, green, blue = htmlColor[0:2], htmlColor[2:4], htmlColor[4:6]
    else:
        raise ValueError("Invalid Color")
    return QColor(int(red, 16), int(green, 16), int(blue, 16))
        
    
class QWebColorDelegate(QItemDelegate):
    def createEditor(self, parent, options, index):
        #print("createEditor")
        editor = QColorDialog(parent)
        return editor
    
    def setModelData(self, colorDialog, model, index):
        color = colorDialog.currentColor()
        #print color.lightness()
        HTMLColor = QColor2HTML(color)
        model.setData(index, HTMLColor)
    
    def setEditorData(self, colorDialog, index):
        try:
            color = HTML2QColor( index.data().toString() )
            colorDialog.setCurrentColor(color)
        except ValueError, e:
            print e
    
    def _paint(self, painter, style, index):
        # TODO: Paint it somewere?
        print painter, style, index
        QItemDelegate.paint(self, painter, style, index)
        

def main(argv):
    
    app = QApplication(argv)
    win = QWidget()
    win.setWindowTitle("Color delegate sample")
    layout = QVBoxLayout()
    win.setLayout(layout)
    tableView = QTableView()
    layout.addWidget(tableView)
    model = QStandardItemModel(1, 1)
    model.setHeaderData(0, Qt.Horizontal, "Foreground")
    tableView.setModel(model)
    tableView.setItemDelegateForColumn(0, QWebColorDelegate())
    win.show()
    return app.exec_()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))