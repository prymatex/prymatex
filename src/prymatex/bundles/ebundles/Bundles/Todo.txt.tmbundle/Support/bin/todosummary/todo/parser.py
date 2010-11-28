import itertools
import os
import time 
import re
from datetime import timedelta

startWithProjPattern = re.compile('^p?[:\-\+](\w+) ')
projInTodoPattern = re.compile(' p?[:\-\+](\w+)')
contextInTodoPattern = re.compile(' @(\w+)')
startWithContextPattern = re.compile('^@(\w+) ')
donePattern = re.compile('^x ([\d]{4}-[\d]{2}-[\d]{2}) ')
priorityPattern = re.compile('^\(([ABC])\) ')

#done pattern must be processed before priority since it expects to be at the
#beginning of the line
todoArgToPattern = [('project', [startWithProjPattern, projInTodoPattern]),
		    ('context', [startWithContextPattern, contextInTodoPattern]),
		    ('doneOn', [donePattern]),
		    ('priority', [priorityPattern])]

def makeTodos(iter=None):
    '''returns a list of todo objects for each line in iter using makeTodo

If iter is unspecified, all of the todos from todo.txt and done.txt as
returned by findTodoFiles are used'''
    if not iter:
       todo, done, report = findTodoFiles()
       return makeTodos(open(todo)) + makeTodos(open(done))
    return [makeTodo(line) for line in iter]

def makeTodo(line):
    '''makes a Todo object from a single line in todo.txt or done.txt.

If the line contains project, context, priority or finish time
information, those fields will be filled in in the Todo object,
otherwise they will be none.  The task in Todo is equal to whatever is
left after pulling out the information for the other fields

If no actual task is left after the meta information is parsed out, a
ValueError will be raised'''
    kwargs = {}
    for argName, patterns in todoArgToPattern:
        for pattern in patterns:
            match = pattern.search(line)
            if match:
                kwargs[argName] = match.group(1)
	        line = line[:match.start()] + line[match.end():]
                break
    if line.strip() == '' and len(kwargs):
	raise ValueError('Line with %s and no actual task!' % kwargs)
    return Todo(line, **kwargs)

def findTodoFiles():
    '''returns a 3 tuple of the paths to todo.txt, done.txt and report.txt

This just uses os.popen to source ~/.todo and print out the values of
$TODO_FILE, $DONE_FILE and $REPORT_FILE.  If one of those isn't set in
~/.todo an IndexError will be raised.  If ~/.todo can't be found, a
IOError will be raised'''
    echoout = os.popen('''. ~/.todo
echo $TODO_FILE
echo $DONE_FILE
echo $REPORT_FILE''')
    locs = echoout.read().split('\n')[:-1]
    echoout.close()
    return locs

def groupByProj(todos):
    projGroups = {}
    for todo in todos:
	proj = todo.project
	if proj == None:
	    proj = "None"
	if not proj in projGroups:
	    projGroups[proj] = []
	projGroups[proj].append(todo)
    return projGroups


def groupByContext(todos):
    projGroups = {}
    for todo in todos:
	proj = todo.context
	if proj == None:
	    proj = "None"
	if not proj in projGroups:
	    projGroups[proj] = []
	projGroups[proj].append(todo)
    return projGroups

def parseReport(iter=None):
    if not iter:
	iter = open(findTodoFiles()[-1])
    reports = []
    for line in iter:
	if line.strip() == '': continue
	try:
	    timeStr, todo, done = line.split(' ')
	except ValueError:
	    print 'Unable to parse %s' % line
	    raise ValueError
	timetuple = time.strptime(timeStr, '%Y-%m-%d-%H:%M:%S')
	reports.append((time.mktime(timetuple), [int(todo), int(done)]))
    return reports

def filter(todos, **kwargs):
    return [todo for todo in todos if todo.matches(**kwargs)]

class Todo(object):
    def __init__(self, task, priority=None, project=None, context=None, doneOn=None):
        self.fields = ['task', 'priority', 'project', 'context', 'doneOn']
	self.task = task
	self.priority = priority
	self.project = project
	self.context = context
	self.doneOn = doneOn

    def matches(self, **kwargs):
	for k, v in kwargs.iteritems():
	    if not k in self.fields:
		raise ValueError('No such field %s on Todos' % k)
	    if not getattr(self, k) == v:
		return False
	return True

    def __cmp__(self, other):
	for f in self.fields:
	    if not hasattr(other, f):
		return -1
	    fcmp = cmp(getattr(self, f), getattr(other, f))
	    if fcmp != 0:
		return fcmp
	return 0

    def __hash__(self):
	hash = 0
	for f in self.fields:
	    hash += getattr(self, f).__hash__()
	return hash

    def __repr__(self):
	d = {}
	for f in self.fields:
	    d[f] = getattr(self, f)
	return 'Todo: %s' % d
