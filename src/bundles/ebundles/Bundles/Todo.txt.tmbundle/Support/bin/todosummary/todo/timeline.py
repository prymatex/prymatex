import time
import elementtree.ElementTree as ET
from todo import parser

def makeEvents(writer, todos):
    done = [todo for todo in todos if todo.doneOn]
    root = ET.Element('data')
    for todo in done:
	ev = ET.SubElement(root, 'event', title=todo.task,
			   start=makeTimelineTime(todo.doneOn))
	ev.text = '%s p-%s @%s' % (todo.task, todo.project, todo.context)
    writer(ET.tostring(root))
    
def makeTimelineTime(todoTime):
    struct = time.strptime(todoTime, '%Y-%m-%d')
    return time.strftime('%b %d %Y %H:%M:%S GMT', struct)
