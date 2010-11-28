#!/usr/bin/env python
import os
import sys

from os import path

line_changers = ['app', 'append', 'del', 'do', 'p', 'prep', 'prepend', 'pri', 'replace', 'rm']
undo_breakers = ['archive', 'remdup', 'report']

def findTodoFile(config):
    '''returns the path to todo.txt

This just uses os.popen to source config and print out the values of
$TODO_FILE.  If it isn't set in config an IndexError will be raised.
If config can't be found, a IOError will be raised'''
    echoout = os.popen('''. %s
echo $TODO_FILE''' % config)
    loc = echoout.read().split('\n')[0]
    echoout.close()
    return loc

def dropLastLine(fileName):
    lines = open(fileName).readlines()
    out = open(fileName, 'w')
    for line in lines[:-1]:
        out.write(line)
    out.close()
    return lines[-1][:-1]

def quoteArgs(argList):
    args = []
    for arg in argList:
	if '"' in arg:
	    args.append("'%s'" % arg)
	else:
	    args.append('"%s"' % arg)
    return ' '.join(args)

def findAction(args):
    for i, arg in enumerate(args):
	if arg.startswith('-') or args[i - 1] == '-d':
	    continue
	return arg
    return None

def findConfig(args):
    for i, arg in enumerate(args):
	if args[i - 1] == '-d':
	    return arg
    return '~/.todo'

action = findAction(sys.argv[1:])
config = findConfig(sys.argv[1:])
histFile = '%s/%s_undo_history' % (os.environ['HOME'], path.basename(config))

if action == 'undo':
    histlines =  open(histFile).readlines()
    if len(histlines) == 0:
	print 'Nothing in %s to undo' % histFile
	sys.exit(-1)
    lasthist = histlines[-1][:-1]
    todoFile = findTodoFile(config)
    action = lasthist.split(' ')[0]
    if action == 'add' or action == 'a':
	print 'Dropped "%s" from todo.txt' % (dropLastLine(todoFile))
	dropLastLine(histFile)
    elif action in line_changers:
	lineNumStr = lasthist.split(' ')[1]
	lineNum = int(lineNumStr) - 1
	before = lasthist[lasthist.index(lineNumStr) + len(lineNumStr) + 1:]
	todoLines = open(todoFile).readlines()
	out = open(todoFile, 'w')
	if len(todoLines) == 0:
	    out.write(before + '\n')
	for i, line in enumerate(todoLines):
	    if i == lineNum:
		out.write(before + '\n')
		if action == 'del' or action == 'rm':
		    out.write(line)
	    else:
		out.write(line)
	out.close()
	dropLastLine(histFile)
	print 'Restored "%s" on line %s' % (before, lineNumStr)
    else:
	print 'Unrecognized action %s in %s' % (action, histFile)
	dropLastLine(histFile)
	sys.exit(-1)
    sys.exit(0)

#If the action is one that changes the content of a particular line, grab its 
#contents before todo.sh changes it
if action in line_changers:
    todoLines = open(findTodoFile(config)).readlines()
    try:
	lineNum = int(sys.argv[sys.argv.index(action) + 1])
	curLine = todoLines[lineNum - 1]
    except:
    #command is malformed if action is in the above list and argv[2]
    #isn't a number.  Let todo.sh take care of it
	pass

result = os.system('todo.sh %s' % (quoteArgs(sys.argv[1:])))
if not result == 0:
    sys.exit(result)

if action in undo_breakers:
    #Empty hist file
    open(histFile, 'w').close()
    sys.exit(0)

hist = open(histFile, 'a')
if action == 'add' or action == 'a':
    hist.write('%s\n' % action)
elif action in line_changers:
    hist.write('%s %s %s' % (action, lineNum, curLine))
hist.close()
