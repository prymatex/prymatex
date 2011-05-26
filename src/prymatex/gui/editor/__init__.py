from PyQt4.QtCore import QRect

def center(widget, respect_to):
    my_geo = widget.geometry()
    my_width, my_height = widget.width(), widget.height()
    width, height = respect_to.width(), respect_to.height()
    
    geo = QRect(
                (width - my_width) / 2,
                (height - my_height) / 2,
                my_width,
                my_height
    )
    widget.setGeometry(geo)
    
