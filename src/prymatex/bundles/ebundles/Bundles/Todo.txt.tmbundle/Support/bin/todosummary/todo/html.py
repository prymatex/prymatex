import itertools

def writeTablePage(todos):
    sys.stdout.write(makePage(makeTables(todos)))

def writeSVGGraph(name, todos):
    from todo import svg
    writer = open('%s.svg' % name, 'w')
    getattr(svg, 'make%sGraph' % name)(writer.write, todos)
    writer.close()

def makePage(contents):
    return '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
      <title>Todo.txt Summary</title>
      <style>
table{
  padding-right:50px;
  float:left;
}

#header{
background:url(gradient.png) repeat-x bottom;
}

h1{
padding-bottom:15px;
}

h2{
   color:green;
}

td{
padding:5px;
text-align:center;
}

.even{
  background-color:#ececec;
}

th{
   color:white;
   background-color:#666666;
   padding:5px 10px 5px 10px;
   font-weight:bold;
}

.sum{
font-weight:bold;
}

.sum td{
border-top:2px solid #666666;
}

ul{
display:inline;
}

div{
clear:both;
}

      </style>
    </head>
    <body>
    <div id="header">
    <h1>Todo.txt Summary</h1>
    </div>
%s
    </body>
</html>''' % contents

def makeSection(id, title, contents):
    return '''<div id="%s">
            <h2>%s</h2>
%s
</div>''' % (id, title, contents)

def makeSVGAndTables(todos):
    from todo import svg
    g = globals()
    sections = []
    for t in tables:
        obj = makeObject(t[0], 300, getattr(svg, 'calc%sWidth' % t[0])(todos))
        table = g['make%sTable' % t[0]](todos)
        sections.append((t[0], t[1], '%s\n%s' % (table, obj)))
    sections.append(('Time', 'Todo and Done by Time', makeObject('Time', 300, 400)))
    return '\n'.join([makeSection(*section) for section in sections])


def makeObject(name, height, width):
    return '''<object data="%s.svg" type="image/svg+xml" width="%d" height="%d" name="%s" >
</object>''' % (name, width, height, name)

def makeTables(todos):
    g = globals()
    sections = [(t[0], t[1], g['make%sTable' % t[0]](todos)) for t in tables]
    return '\n'.join([makeSection(*section) for section in sections])

def makeOpenProjTable(todos):
    return makeTable(parser.groupByProj(parser.filter(todos, doneOn=None)),
                     openColumns)

def makeAllProjTable(todos):
    return makeTable(parser.groupByProj(todos), allColumns)

def makeOpenContextTable(todos):
    return makeTable(parser.groupByContext(parser.filter(todos, doneOn=None)),
                     openColumns)
    
tables = [('OpenProj', 'Open Todos by Project'),
          ('OpenContext', 'Open Todos by Context'),
          ('AllProj', 'Todo and Done by Project')]

def makeTable(groups, columns, sortFunc=None):
    if sortFunc == None:
        sortFunc = lambda x, y: -cmp(len(x[1]), len(y[1]))#by group length
    groups = list(groups.iteritems())
    groups.sort(sortFunc)
    columnFunc = [c[1] for c in columns]
    rows = []
    for i, group in enumerate(groups):
        if i % 2 == 0:
            rows.append(makeRow(group, columnFunc))
        else:
            rows.append(makeRow(group, columnFunc, 'even'))
    rows.append(makeRow(('All', list(itertools.chain(*[t[1] for t in groups]))),
                        columnFunc,
                        'sum'))
    return '''
<table cellpadding="0" cellspacing="0">
  <tr>
      %s
  </tr>
  %s
</table>
''' % ('\n'.join(['<th>%s</th>' % c[0] for c in columns]), '\n'.join(rows))

def counter(**kwargs):
    def filterCounter(group):
        return len(parser.filter(group[1], **kwargs))
    return filterCounter

def nameExtractor(group):
    return group[0]

def count(group):
    return len(group[1])

def done(group):
    return len([g for g in group[1] if g.doneOn])

openColumns = [('Name', nameExtractor),
               ('Open', count),
               ('A', counter(priority='A')),
               ('B', counter(priority='B')),
               ('C', counter(priority='C')),
               ('Unprioritized', counter(priority=None))]

allColumns = [('Name', nameExtractor),
              ('All', count),
              ('Open', counter(doneOn=None)),
              ('Done', done)]

def makeRow(group, columns, rowClass=''):
    if not rowClass == '':
        rowClass = ' class="%s"' % rowClass
    return '''<tr%s>
    %s
</tr>''' % (rowClass, '\n'.join(['<td>%s</td>' % c(group) for c in columns]))

if __name__ == "__main__":
    import os
    import sys
    import parser
    
    todos = parser.makeTodos(sys.stdin)
    if (os.environ.has_key("TM_DIRECTORY")):
      doneFile = os.environ["TM_DIRECTORY"] + "/done.txt"
      todos += parser.makeTodos(open(doneFile))

    if len(sys.argv) < 2 or sys.argv[1] == 'svg':
        try:
            import elementtree
        except ImportError:
            print "unable to import elementtree so I can't make svg.  Producing html with tables only."
            writeTablePage(todos)
            sys.exit(1)
        from todo import svg
        sys.stdout.write(makePage(makeSVGAndTables(todos)))
        for t in html.tables:
            writeSVGGraph(t[0], todos)
        #html.writeSVGGraph('Time', parser.parseReport(open(reportFile)))
    elif sys.argv[1] == 'html':
        writeTablePage(todos)
    else:
        print 'Usage: python %s [html|svg]' % sys.argv[0]