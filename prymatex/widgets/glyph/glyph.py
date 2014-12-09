#!/usr/bin/env python

from prymatex.qt import QtCore, QtGui

def load_codepoints(font_name):
    name = font_name.replace("-", "_")
    module = "prymatex.widgets.glyph.codepoints.%s" % name.lower()
    try:
        mod = __import__(module, globals(), locals(), [name], 0)
        return getattr(mod, name)
    except Exception as ex:
        print(ex)
        return {}

#The font-glyphicon painter
class QtGlyphCharIconPainter(object):
    def paint(self, glyph, painter, rect, mode, state, options):
        painter.save()

        #set the correct color
        color = options.get("color")
        text = options.get("text")

        if mode == QtGui.QIcon.Disabled:
            color = options.get("color-disabled")
            alt = options.get("text-disabled") 
            if alt:
                text = "%s" % alt
        elif mode == QtGui.QIcon.Active:
            color = options.get("color-active")
            alt = options.get("text-active")
            if alt:
                text = "%s" % alt
        elif mode == QtGui.QIcon.Selected:
            color = options.get("color-selected")
            alt = options.get("text-selected")
            if alt:
                text = "%s" % alt
            
        painter.setPen(color)

        # add some 'padding' around the icon
        drawSize = QtCore.qRound(rect.height() * options.get("scale-factor"))
        painter.setFont(glyph.font(drawSize))
        painter.drawText(rect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, text)
        painter.restore()

#The painter icon engine.
class QtGlyphIconPainterIconEngine(QtGui.QIconEngine):
    def __init__(self, glyph, painter, options):
        super(QtGlyphIconPainterIconEngine, self).__init__()
        self.glyph = glyph
        self.painter = painter
        self.options = options
    
    def clone(self):
        return QtGlyphIconPainterIconEngine(self.glyph, self.painter, self.options)
    
    def paint(self, painter, rect, mode, state):
        self.painter.paint( self.glyph, painter, rect, mode, state, self.options )

    def pixmap(self, size, mode, state):
        pm = QtGui.QPixmap(size)
        pm.fill( QtCore.Qt.transparent )
        painter = QtGui.QPainter()
        painter.begin(pm)
        self.paint(painter, QtCore.QRect(QtCore.QPoint(0,0),size), mode, state)
        return pm

#The main class for managing icons
#This class requires a 2-phase construction. You must first create the class and then initialize it via an init* method
class QtGlyph(QtCore.QObject):
    fontIds = {}
    def __init__(self, font_name, parent = None):
        super(QtGlyph, self).__init__(parent)
        self._font_name = font_name
        self._codepoints = load_codepoints(font_name)
        
        # initialize the default options
        self.default_options = {
            "color": QtGui.QColor(50,50,50),
            "color-disabled": QtGui.QColor(70,70,70,60),
            "color-active": QtGui.QColor(10,10,10),
            "color-selected": QtGui.QColor(10,10,10),
            "scale-factor": 0.9,
            "text": None, 
            "text-disabled": None,
            "text-active": None,
            "text-selected": None
        }
        
        self._painter_map = {}

        self._font_icon_painter = QtGlyphCharIconPainter()
    
    def name(self):
        return self._font_name
        
    def codepoints(self):
        return self._codepoints

    def setDefaultOption(self, name, value):
        self.default_options[name] = value
    
    def defaultOption(self, name):
        return self.default_options[name]

    # Creates an icon with the given name
    # You can use the icon names as defined on http://fortawesome.github.io/Font-Awesome/design.html withour the 'icon-' prefix
    def icon(self, name, **options):
        options.update(self.default_options)
        if name in self._codepoints:
            options["text"] = self._codepoints[name]
            return self._icon( self._font_icon_painter, **options)
    
        if len(name) == 1:
            options["text"] = name
            return self._icon( self._font_icon_painter, **options)

        #this method first tries to retrieve the icon
        painter = self._painter_map.get(name)
        if not painter:
            return QtGui.QIcon()

        return self._icon(painter, **options)

    #Create a dynamic icon by simlpy supplying a painter object
    #The ownership of the painter is NOT transfered.
    def _icon(self, painter, **options):
        #Warning, when you use memoryleak detection. You should turn it of for the next call
        #QIcon's placed in gui items are often cached and not deleted when my memory-leak detection checks for leaks.
        # I'm not sure if it's a Qt bug or something I do wrong
        engine = QtGlyphIconPainterIconEngine(self, painter, options)
        return QtGui.QIcon(engine)
    
    # Adds a named icon-painter to the QtGlyph icon map
    # As the name applies the ownership is passed over to QtGlyph
    #
    # @param name the name of the icon
    # @param painter the icon painter to add for this name
    def give(self, name, painter):
        if name in self._painter_map:
            p = self._painter_map.pop(name) # delete the old one
            p.deleteLater()
        self._painter_map[name] = painter

    #Creates/Gets the icon font with a given size in pixels. This can be usefull to use a label for displaying icons
    #Example:
    #
    #QLabel* label = new QLabel( QChar( icon_group ) );
    #label.setFont( glyph.font(16) )
    def font(self, size):
        font = QtGui.QFont(self._font_name)
        font.setPixelSize(size)
        return font
