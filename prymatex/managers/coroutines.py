#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PyQt4 based coroutines implementation.
#
# GNU LGPL v. 2.1
# Kirill Kostuchenko <ddosoff@gmail.com>

import sys
import datetime
import traceback
from collections import deque
from types import GeneratorType

from prymatex.qt import QtCore
from prymatex.core import PrymatexComponent

# Reduce scheduler overhead
# Iterate in the Task.run, while calling subcoroutines
MAX_TASK_ITERATIONS = 3

# Scheduler longIteration signal warning
MAX_ITERATION_TIME = datetime.timedelta( milliseconds = 300 )

# Average scheduler runtime between qt loops
AVERAGE_SCHEDULER_TIME = datetime.timedelta( milliseconds = 30 )

# Max scheduler iterations between qt loops
MAX_SCHEDULER_ITERATIONS = 10

# Usage: 
#   yield Return( v1, v2, .. )
class Return( object ):
    def __init__( self, *args ):
        if not args:
            raise Exception( "Please use 'return' keyword, instead of 'yield Return()'" )

        if len( args ) == 1:
            # v = yield subCoroutine()
            self.value = args[ 0 ]
        else:
            # a,b,c = yield subCoroutine()
            self.value = args

# Inherit your asynchronous calls,
# like Sleep below.
class AsynchronousCall( QtCore.QObject ):
    def handle( self ):
        raise Exception( 'Not Implemented' )
    
    # will be called by scheduler, before handle()
    def setContext( self, task, scheduler ):
        self.task = task
        self.scheduler = scheduler

    # continue execution
    def wakeup( self, result = None ):
        if isinstance( result, Exception ):
            if not isinstance( result, CoException ):
                # Construct CoException to
                # save subcoroutines stack
                result = CoException( result )
                # exception is not raised naturally, format top of the stack manually
                result.updateStack( traceback.format_stack( limit = 2 )[ -2 ] )
            self.task.exception = result
        else:
            self.task.sendval = result

        # Wake up execution of the caller's task
        self.scheduler.schedule( self.task )

# Asynchronous call example
#
# Usage:
#   yield Sleep( 100 )   # sleep 100ms
class Sleep( AsynchronousCall ):
    def __init__( self, ms ):
        AsynchronousCall.__init__( self )
        # save params for the future use
        self.ms = ms

    def handle( self ):
        # QtCore.QObject is the QT library class. SytemCall inherits QtCore.QObject.
        # QtCore.QObject.timerEvent will be called after self.ms milliseconds
        self.timerId = QtCore.QObject.startTimer( self, self.ms )

    # This is overloaded QtCore.QObject.timerEvent
    # and will be called by the Qt event loop.
    def timerEvent( self, e ):
        QtCore.QObject.killTimer( self, self.timerId )
        self.wakeup( None )

# Wait task, until it's done!
#
# Usage:
#   res = yield WaitTask( task )   # res - task return value or raises Exception from task
class WaitTask( AsynchronousCall ):
    def __init__( self, waitTask ):
        AsynchronousCall.__init__( self )
        # save params for the future use
        self.waitTask = waitTask

    def handle( self ):
        if self.waitTask.state == Task.RUNNING:
            # When task is done, it emits signal done(Return)
            self.waitTask.done.connect( self.passParam )
        elif self.waitTask.state == Task.DONE:
            # repeat last return value
            self.wakeup( self.waitTask.result.value )
        elif self.waitTask.state == Task.EXCEPTION:
            # raise exception in the waiter
            self.wakeup( self.waitTask.exception )
        else:
            raise Exception( 'Unknown %s state %d' % (self.waitTask, self.waitTask.state) )

    def passParam( self, resReturn ):
        # expand Return to it's value
        self.wakeup( resReturn.value )


# Wait, until first task is done or Exception!
#
# Usage:
#   task = WaitFirstTask( [task1, task2, ... ], [timeout] )
class WaitFirstTask( AsynchronousCall ):
    def __init__( self, iterableTasks, timeoutMs = 0 ):
        AsynchronousCall.__init__( self )
        # save params for the future use
        self.tasks = iterableTasks
        assert self.tasks
        self.timeoutMs = timeoutMs

    def handle( self ):
        connected = []
        for t in self.tasks:
            if t.state == Task.RUNNING:
                t.done.connect( self.passParam )
                connected.append( t )
            elif t.state == Task.DONE or t.state == Task.EXCEPTION:
                [u.done.disconnect( self.passParam ) for u in connected ]
                self.wakeup( t )
                return
            else:
                raise Exception( 'Unknown %s state %d' % (t, t.state) )

        # timoeut passed?
        if self.timeoutMs:
            self.timerId = QtCore.QObject.startTimer( self, self.timeoutMs )

    # tasks done signal
    def passParam( self, resReturn ):
        for t in self.tasks:
            t.done.disconnect( self.passParam )

        # expand Return to it's value
        self.wakeup( self.sender() )

    def timerEvent( self, e ):
        for t in self.tasks:
            t.done.disconnect( self.passParam )

        QtCore.QObject.killTimer( self, self.timerId )
        self.wakeup( None )

# Exception with the coroutines stack
class CoException( Exception ):
    def __init__( self, orig ):
        # coroutines traceback
        self.tb = deque()
        # original Exception
        self.orig = orig
    
    def updateStack( self, preformatted = None ):
        if preformatted:
            self.tb.appendleft( preformatted )
        else:
            formattedList = traceback.format_tb( sys.exc_info()[2] )
            if len(formattedList) > 1:
                formattedList.reverse()
                for e in formattedList[:-1]:
                    self.tb.appendleft( e )
            else:
                self.tb.appendleft( traceback.format_tb( sys.exc_info()[2] )[0] )

    def __repr__( self ):
        res = ''
        for l in self.tb:
            res += l
        strExc = str(self.orig)
        res += strExc + '\n' + '-' * len(strExc) + '\n\n'
        return res

    def __str__( self ):
        return self.__repr__()

class WaitTasksTimeout( Exception ):
    """ When tasks coroutines works too long """
    def __init__( tasks, maxTimeoutMs ):
        Exception.__init__( '%d tasks (%s) works longer, then %d ms.' % \
                            (len(tasks), tasks, maxTimeoutMs) )

class Runnable(QtCore.QObject):
    # States
    NEW = 0
    RUNNING = 1
    DONE = 2
    EXCEPTION = 3
    CANCELED = 4
    STATES = {
        NEW: "NEW",
        RUNNING: "RUNNING",
        DONE: "DONE",
        EXCEPTION: "EXCEPTION",
        CANCELED: "CANCELED"
    }
    
    def __init__(self, parent = None):
        super(Runnable, self).__init__(parent)
        self.state = Runnable.NEW
    
    def cancelled(self):
        return self.state == Runnable.CANCELED

    def done(self):
        return self.state in ( Runnable.DONE, Runnable.EXCEPTION, Runnable.CANCELED )

    def running(self):
        return self.state == Runnable.RUNNING

    def cancel(self):
        self.state = Runnable.CANCELED

    def stateStr( self ):
        if self.state in self.STATES:
            return self.STATES[self.state]
        else:
            raise Exception( 'Unknown state %s' % self.state )

# Coroutine based task
class Task( Runnable ):
    # Return.value is task result, if no unhandled Exceptions occured.
    # Emmited on Exception with Exception as Return.value, if emitUnhandled set.
    # Do not emmited with exception, if emitUnhandled is False. Pass exceptions to main loop.
    done = QtCore.Signal( Return )
    finished = QtCore.Signal()

    def __init__( self, coroutine, parent = None, **kwargs):
        super(Task, self).__init__(parent)
        
        self.stack = deque()                          # stack for subcoroutines
        self.coroutine = coroutine                    # task coroutine / top subcoroutine
        self.sendval = kwargs.get("sendval", None)    # value to send into coroutine
        self.exception = None                         # save exceptions here
        self.result = Return( None )                  # default return value
        # Do not route exceptions to Scheduler
        self.emitUnhandled = False                    # emits done with unhandled exception as Return.value

    # Do not pass exceptions to scheduler.
    #
    # Useful with WaitTask of WaitFirstTask calls.
    def setEmitUnhandled( self, val = True ):
        self.emitUnhandled = val

    def formatBacktrace( self ):
        # TODO: implement full trace
        return 'File "%s", line %d' % \
               (self.coroutine.gi_code.co_filename, self.coroutine.gi_frame.f_lineno)

    def value( self ):
        if self.state == Runnable.DONE:
            return self.result.value
        if self.state == Runnable.EXCEPTION:
            return self.exception.orig
        else:
            assert False, "Can't get result. State: %d" % self.state

    # Run a task until it hits the next yield statement
    def run( self ):
        for i in range( MAX_TASK_ITERATIONS ):
            try:
                if self.exception:
                    self.result = self.coroutine.throw( self.exception.orig )
                    self.exception = None
                elif self.state == Runnable.CANCELED:
                    self.coroutine.close()
                elif self.coroutine.gi_frame is not None and self.coroutine.gi_frame.f_lasti == -1:
                    # just-started generator
                    self.result = self.coroutine.send(None)
                else:
                    # save result into self to protect from gc
                    self.result = self.coroutine.send(self.sendval)

                # simple trap? (yield)
                if self.result is None:
                    # go back to the scheduler
                    return

                # yield AsynchronousCall(..)
                if isinstance( self.result, AsynchronousCall ): 
                    # handled by scheduler
                    return self.result

                # yield subcoroutine(..)
                if isinstance( self.result, GeneratorType ):
                    # save current coroutine in stack
                    self.stack.append( self.coroutine )
                    self.coroutine = self.result
                    self.sendval = None
                    continue
                
                # yield Return(..)
                if isinstance( self.result, Return ):
                    raise StopIteration()

                # Unknown result type!?
                raise TypeError( '%s\n\nWrong type %s yielded.' % \
                                 (self.formatBacktrace(), type(self.result)) )

            except StopIteration:
                if self.state == Runnable.CANCELED:
                    self.finished.emit()
                    raise

                # old exceptions handled
                self.exception = None

                if not isinstance( self.result, Return ):
                    # replace previous yield
                    self.result = Return( None )

                # end of task?
                if not self.stack:
                    self.state = Runnable.DONE
                    self.finished.emit()
                    self.done.emit( self.result )
                    raise

                # end of subcoroutine
                self.sendval = self.result.value
                del self.coroutine
                self.coroutine = self.stack.pop()

            except Exception as e:
                if self.exception is None:
                    self.exception = CoException( e )

                # exception was catched, but new one raised?
                if self.exception.orig != e:
                    self.exception = CoException( e )

                # calc own backtrace
                self.exception.updateStack()

                if not self.stack:
                    self.state = Runnable.EXCEPTION
                    if self.emitUnhandled:
                        self.done.emit( Return(self.exception) )
                        raise StopIteration()
                    else:
                        raise self.exception

                del self.coroutine
                self.coroutine = self.stack.pop()

class SchedulerManager(PrymatexComponent, QtCore.QObject):
    longIteration = QtCore.Signal( datetime.timedelta, Task )
    done = QtCore.Signal()

    def __init__( self, **kwargs):
        super(SchedulerManager, self).__init__(**kwargs)

        self._current_task = None
        self._tasks = 0
        self.ready = deque()
        self.timerId = None
        self.printCoException = True

    # Schedule coroutine as Task
    def task( self, coroutine, **kwargs):
        kwargs.setdefault("parent", self)
        t = Task(coroutine, **kwargs)
        t.destroyed.connect(self._task_destroyed)
        self._tasks += 1

        t.state = Task.RUNNING
        self.schedule( t )
        return t

    def schedule( self, t ):
        self.ready.appendleft( t )

        if self.timerId is None:
            self.timerId = self.startTimer(0)

    def _task_destroyed( self, task ):
        self._tasks -= 1

        if not self._tasks:
            self.done.emit()

    # paramsList - list( *argv1, *argv2, ... )
    # will start coTask( *argv1 ), coTask( *argv2 )... and returns tasks set
    def tasks(self, coTask, tasksParams, emitUnhandled=True):
        tasks = set()
        for argv in tasksParams:
            t = self.task(coTask(argv))
            if emitUnhandled:
                t.setEmitUnhandled()
    
            tasks.add(t)

        return tasks

    def checkRuntime( self, task ):
        t = datetime.datetime.now()
        l = self.lastIterationTime
        self.lastIterationTime = t

        # task iteration too long?
        if t - l > MAX_ITERATION_TIME:
            self.longIteration.emit( t - l, task )
            return True

        # scheduler iterating too long? 
        if t - self.startIterationTime > AVERAGE_SCHEDULER_TIME:
            return True
        
        return False

    # Show coroutines stack
    def formatException( self ):
        assert isinstance( self._current_task, Task )
        assert isinstance( self._current_task.exception, CoException )

        return '\nUNHANDLED COROUTINE EXCEPTION BACKTRACE (self.printCoException is True)!\n%s' % self._current_task.exception

    # The scheduler loop!
    def timerEvent( self, e ):
        # Do not iterate too much.. 
        self.startIterationTime = datetime.datetime.now()
        self.lastIterationTime = self.startIterationTime
        timeout = False
        for i in range( MAX_SCHEDULER_ITERATIONS ):
            if timeout or not self.ready:
                break

            self._current_task = self.ready.pop()
            try:
                result = self._current_task.run()
                
                if isinstance( result, AsynchronousCall ):
                    result.setContext( self._current_task, self )
                    result.handle()

                    # AsynchronousCall will resume execution later
                    continue
                     
            except Exception as e:
                self._current_task.deleteLater()

                if isinstance( e, StopIteration ):
                    continue

                if isinstance( e, CoException ) and self.printCoException:
                    sys.stdout.write( self.formatException() )

                # this is unknown exception!
                # stop iterating timer, if all tasks done
                if not self.ready:
                    self.killTimer( self.timerId )
                    self.timerId = None

                # forward exception to the main event loop
                raise

            finally:
                timeout = self.checkRuntime( self._current_task )

            # continue this task later
            self.ready.appendleft( self._current_task )

        # do not lopp, if all tasks done
        if not self.ready:
            self.killTimer( self.timerId )
            self.timerId = None

        self._current_task = None

# Wait until many tasks done
def coWaitTasks( tasks, maxTimeoutMs, breakFunc = lambda tasks, t: False ):
    """ Wait until all coroutines from tasks 
        done with result or exception. """
    while tasks:
        t = yield WaitFirstTask( tasks, maxTimeoutMs )

        # Timeout?
        if not t:
            raise WaitTasksTimeout( tasks, maxTimeoutMs )

        tasks.remove( t )

        if breakFunc( tasks, t ):
            break




if __name__ == '__main__':
    import sys
    import random
    from prymatex.qt.QtGui import QApplication

    def valueReturner( name ):
        print('%s valueReturner()' % name)
        v = 'valueReturner!'
        yield Return( v )
        print('never print it')

    def multipleValueReturner( name ):
        print('%s multipleValueReturner()' % name)
        v1 = 'multipleValueReturner!'
        v2 = 2

        # exception test
        if not random.randint( 0, 2 ):
            raise Exception( 'multipleValueReturner ooops!' )

        yield Return( v1, v2 )

    def subcoroutinesTest( name ):

        # Sleep system call example
        ms = random.randint( 1000, 2000 )
        print('%s Sleep( %d )' % (name, ms))
        yield Sleep( ms )

        # exception test
        try:
            print('%s subcoroutinesTest()' % name)

            # return values and subcoroutines test
            v1, v2 = yield multipleValueReturner( name )
            v = yield valueReturner( name )
        except Exception as e:
            print("%s exception '%s' handled!" % (name, e ))
        else:
            print('%s v = %s, v1 = %s, v2 = %s' % (name, v, v1, v2))

            # signal done test
            yield Return( name, v, v1, v2 )

    class TaskReturnValueTest( QtCore.QObject ):
        def slotDone( self, res ):
            print('slotDone():', res.value)

    a = QApplication( sys.argv )
    s = Scheduler( a )

    # call QApplication.quit() when all coroutines done
    s.done.connect( a.quit )

    d = TaskReturnValueTest()

    # start tasks
    for i in range( 0, 3 ):
        t = s.task( subcoroutinesTest('task %d' % i) )
        t.done.connect( d.slotDone )

    # start qt event loop
    a.exec_()
