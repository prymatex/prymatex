import elementtree.ElementTree as ET
import time
from todo import parser

def segmentedBarGraph(bars, height=300, width=400):
    assert len(bars) > 0
    root = makeSVGRoot(height, width)
    graph = ET.SubElement(root, 'g', transform='translate(0 10)')
    longestLabel = max([len(s[0]) for s in bars])
    if longestLabel > 9:
        stagger = True
        barHeight = height - 50
    else:
        stagger = False
        barHeight = height - 40
    maxVal, ticks = getTicks(max([sum(s[1]) for s in bars]))
    graph.append(yaxis(ticks, barHeight, width))
    width = width - 40#factor out yaxis
    barWidth = width/len(bars)
    scale = barHeight/float(maxVal)
    barsEl = ET.SubElement(graph, 'g', id='bars', transform='translate(40 0)')
    for i, item in enumerate(bars):
	barGroup = ET.SubElement(barsEl, 'g',
				 transform='translate(%d 0)' % (i * barWidth))
	barGroup.append(bar([s * scale for s in item[1]], barHeight, barWidth))
        if stagger:
            if i % 2:
                labelPos = barHeight + 15
            else:
                labelPos = barHeight - 5
        else:
            labelPos = barHeight
	barGroup.append(barLabel(item[0], labelPos, barWidth))
    return root

def getTicks(maxVal):
    if maxVal <= 5:
	return maxVal, ['0', '%d' % maxVal]
    else:
	maxVal = maxVal + (10 - (maxVal % 10))
	return maxVal, ['0', '%d' % (maxVal/2), '%d' % (maxVal)]
    

def barLabel(label, height, width):
    el = ET.Element('text', x='%d' % (width /2),  y='%d' % (height + 20))
    el.attrib['class'] = 'label'
    el.text = label
    return el

def bar(segments, height, width):
    barGroup = ET.Element('g')
    prevSeg = 0
    size = len(segments)
    for i, seg in enumerate(segments):
	barGroup.append(ET.Element('rect',
				   x='%d' % (width/8),
				   y='%d' % (height - prevSeg - seg),
				   width='%d' % (width * 6 / 8),
				   height='%d' % seg))
	barGroup[-1].attrib['class'] = 'segment%d' % (i + 1)
	prevSeg = seg
    return barGroup

def yaxis(labelledTicks, height=600, width=800):
    spacing = height/float(len(labelledTicks) - 1)
    axisGroup = ET.Element('g', id='yaxis')
    axis = ET.SubElement(axisGroup, 'line',
			x1='40', x2='40',
			y1='-10', y2='%d' % height)
    axis.attrib['class'] = 'axis'
    for i, labelText in enumerate(labelledTicks):
	y = height - (i * spacing)
	label = ET.SubElement(axisGroup, 'text', y='%d' % (y+5), x='2')
	label.text = labelText
	tick = ET.SubElement(axisGroup, 'line',
		      x1='20', x2='%d' % width,
		      y1='%d' % y, y2='%d' % y)
	tick.attrib['class'] = 'tick'
	
    return axisGroup
    
def makeSVGRoot(height, width):
    return ET.Element('svg', width='%d' % width, height='%d' % height,
		      version='1.1', xmlns='http://www.w3.org/2000/svg')

def lineGraph(lines, labelIntervals, labelCreator, width=400, height=300):
    root = makeSVGRoot(height, width)
    g = ET.SubElement(root, 'g', transform='translate(0 10)')
    height = height - 20
    maxYVal, ticks = getTicks(max([max(l[1]) for l in lines]))
    g.append(yaxis(ticks, height - 15, width))
    width = width - 40
    maxNumLabels = width/75
    maxXVal = lines[-1][0]
    minXVal = lines[0][0]
    xRange = maxXVal - minXVal
    labelInterval = labelIntervals[-1]
    for interval in labelIntervals:
	if xRange/float(interval) <= maxNumLabels:
	    labelInterval = interval
	    break
    xpixelsPerVal = width/xRange
    labelEl = ET.SubElement(g, 'g', id='labels', transform='translate(40 0)')
    labelVal = minXVal + (labelInterval  - (minXVal % labelInterval))
    while labelVal < maxXVal:
	x = '%d' % ((labelVal - minXVal) * xpixelsPerVal)
	el = ET.SubElement(labelEl, 'text', x=x,  y='%d' % (height))
	el.attrib['class'] = 'label'
	el.text = labelCreator(labelVal)
	tick = ET.SubElement(labelEl, 'line', x1=x, x2=x, y2='%d' % (height - 15), y1='%d' % (height - 25))
	tick.attrib['class'] = 'tick'
	labelVal = labelVal + labelInterval
    height = height - 15
    ypixelsPerVal = height/float(maxYVal)
    numLines = len(lines[0][1])
    linesEl = ET.SubElement(g, 'g', id='lines', transform='translate(40 0)')
    for i in range(numLines):
	line = polyline([((x - minXVal) * xpixelsPerVal, height - y[i] * ypixelsPerVal) for x, y in lines])
	line.attrib['class'] = 'line%d' % (i + 1)
	linesEl.append(line)
    return root

def polyline(points):
    pline = ET.Element('polyline')
    pline.attrib['points'] = ' '.join(['%d,%d' % (p[0], p[1]) for p in points])
    return pline

def makeOpenProjGraph(writer, todos):
    openTodos = parser.groupByProj(parser.filter(todos, doneOn=None))
    openSegments = {}
    for k, v in openTodos.iteritems():
	openSegments[k] = [len(v),]
    openSegments = list(openSegments.iteritems())
    openSegments.sort()
    writeStylesheetPI(writer)
    writer(ET.tostring(segmentedBarGraph(openSegments,
                                         width=calcBarGraphWidth(len(openTodos)))))

def calcOpenProjWidth(todos):
    return calcBarGraphWidth(len(parser.groupByProj(parser.filter(todos, doneOn=None))))

def makeOpenContextGraph(writer, todos):
    openTodos = parser.groupByContext(parser.filter(todos, doneOn=None))
    openSegments = {}
    for k, v in openTodos.iteritems():
	openSegments[k] = [len(v),]
    openSegments = list(openSegments.iteritems())
    openSegments.sort()
    writeStylesheetPI(writer)
    writer(ET.tostring(segmentedBarGraph(openSegments,
                                         width=calcBarGraphWidth(len(openTodos)))))

def calcOpenContextWidth(todos):
    return calcBarGraphWidth(len(parser.groupByContext(parser.filter(todos, doneOn=None))))

def calcBarGraphWidth(numBars):
    if numBars > 10:
        numBars = 10
    return 20 + numBars * 50

def makeBarsForAllGraph(todos):
    openTodos = parser.groupByProj(parser.filter(todos, doneOn=None))
    closedTodos = parser.groupByProj([todo for todo in todos if todo.doneOn])
    bars = {}
    for k in openTodos.keys():
	bars[k] = [len(openTodos[k]), len(closedTodos.get(k, []))]
    for k in closedTodos.keys():
	if not k in openTodos:
	    bars[k] = [0, len(closedTodos[k])]	
    bars = list(bars.iteritems())
    bars.sort(lambda x, y:sum(x[1]).__cmp__(sum(y[1])))
    bars.reverse()
    return bars[:10]

def makeAllProjGraph(writer, todos):
    bars = makeBarsForAllGraph(todos)
    writeStylesheetPI(writer)
    writer(ET.tostring(segmentedBarGraph(bars,
                                         width=calcBarGraphWidth(len(bars)))))

def calcAllProjWidth(todos):
    return calcBarGraphWidth(len(makeBarsForAllGraph(todos)))

def makeTimeGraph(writer, statusByTime):
    if not statusByTime:
	writer('''<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
<text x="10" y="100">report.txt is empty so I can't make this graph</text>
</svg>''')
	return
    writeStylesheetPI(writer)
    labelIntervals = [3600 * 24 * days for days in [1, 2, 3, 7, 14, 30]]
    labelCreator = lambda x : time.strftime('%Y-%m-%d', time.localtime(x))
    writer(ET.tostring(lineGraph(statusByTime, labelIntervals, labelCreator)))
    
def writeStylesheetPI(writer):
    writer('<?xml-stylesheet href="graph.css" type="text/css"?>\n')

    
