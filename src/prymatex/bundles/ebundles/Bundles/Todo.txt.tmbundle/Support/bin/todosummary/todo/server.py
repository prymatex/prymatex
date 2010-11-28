import sys
import web
from beaker import session

urls = (
  '/', 'Index',
  '/(\w+).svg', 'SVGMaker',
  '/(graph.(css))', 'Files',
  '/(gradient.(png))', 'Files',
  '/(timeline.(html))', 'Files',
  '/events.xml', 'Events'
)

multiuser = False

if __name__ == '__main__':
    from os.path import dirname, abspath
    sys.path.append(dirname(dirname(abspath(__file__))))
    def createSession(x):
        return session.SessionMiddleware(x, key='todo')
    web.run(urls, createSession, web.reloader)

from todo import svg, parser, html, timeline

typeToMime = {'css':'text/css', 'png':'image/png', 'html':'text/html'}

class Files:
    def GET(self, name, type):
        web.header('Content-Type', typeToMime[type])
        print open(name).read()

form = '''<form action="." method="POST" enctype="multipart/form-data">
<h3>todo.txt</h3>
<input type="file" name="open" />
<h3>done.txt</h3>
<input type="file" name="done" />
<h3>report.txt</h3>
<input type="file" name="report" />
<input value="Upload File(s)" type="submit" />  
</form>'''

def getSingleuserTodos():
    openFile, doneFile, reportFile = parser.findTodoFiles()
    return parser.makeTodos(open(openFile)) + parser.makeTodos(open(doneFile))
    

class Index:
    def GET(self):
	web.header('Content-Type', 'text/html')
	session =  web.ctx.environ['beaker.session']
        if not multiuser:
            contents = html.makeSVGAndTables(getSingleuserTodos())
        elif 'todos' in session:
            contents = html.makeSVGAndTables(session['todos']) + '<a href="timeline.html">Timeline</a>' + form
        else:
            contents = form
	print html.makePage(contents)

    def POST(self):
	session =  web.ctx.environ['beaker.session']
	i = web.input()
	if 'done' in i or 'open' in i:
	    session['todos'] = []
	for ctxName in ['done', 'open']:
	    if i[ctxName]:
		newTodos = parser.makeTodos(i[ctxName].split('\n'))
		session['todos'].extend((newTodos))
	if i['report']:
	    session['report'] = parser.parseReport(i['report'].split('\n'))
	session.save()
	self.GET()    

class SVGMaker:
    def GET(self, graph):
	web.header('Content-Type', 'image/svg+xml')
	session =  web.ctx.environ['beaker.session']
        if graph in ['OpenProj', 'AllProj', 'OpenContext']:
            if not multiuser:
                todos = getSingleuserTodos()
            else:
                todos = session['todos']
            getattr(svg, 'make%sGraph' % graph)(web.output, todos)
	elif graph == 'Time':
            if not multiuser:
                openFile, doneFile, reportFile = parser.findTodoFiles()
                report = parser.parseReport(open(reportFile))
            else:
                report = session['report']
	    svg.makeTimeGraph(web.output, report)
	else:
	    print '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
<text x="10" y="100">not a known graph type</text>
</svg>'''
	    

class Events:
    def GET(self):
	web.header('Content-Type', 'text/xml')
	if multiuser:
	    todos = web.ctx.environ['beaker.session']['todos']
	else:
	    todos = getSingleuserTodos()
	timeline.makeEvents(web.output, todos)
