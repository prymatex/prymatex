#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import datetime
from collections import deque
from PyQt4.QtCore import QObject
from satchmo.common_lib.coroutines import AsynchronousCall, Return, Sleep



class Acquirer( AsynchronousCall ):
    def handle( self ):
        # we're quiet :)
        # Task will scheduled from Semaphore
        pass



# Semaphore
class Semaphore:
    def __init__( self, semVal ):
        assert semVal > 0

        self.initial = semVal
        self.available = semVal

        # waiting acquirers here
        self.pending = deque()


    def release( self ):
        if self.pending:
            self.pending.pop().wakeup( self.available )
            assert self.available == 0
            return self.available

        assert self.available >= 0
        self.available += 1
        assert self.available <= self.initial

        return self.available



    def __repr__( self ):
        return 'Семафор( свободно %d из %d, в очереди %d )' % ( self.available, self.initial, len(self.pending) )


    # Usage:
    #   yield sem.acquire()
    def acquire( self ):
        start = datetime.datetime.now()
        done = start
        if self.available:
            self.available -= 1
        else:
            # sleep, until released..
            acquirer = Acquirer()
            self.pending.appendleft( acquirer )
            # sleep, until available
            yield acquirer
            done = datetime.datetime.now()

        yield Return( self.available, done - start )



if __name__ == '__main__':
    import random
    from PyQt4.QtGui import QApplication
    from satchmo.common_lib.coroutines import Scheduler


    def coWorker( name, sem ):
        sys.stdout.write( '\n' + str(name) + ' acquiring() ... ' )
        semVal, delay = yield sem.acquire()
        sys.stdout.write( '%d avail, %s delay\n' % (semVal, delay) )
        ms = random.randint( 1500, 3000 )
        print name, 'Sleep(): %d ms..' % ms
        yield Sleep( ms )
        print name, 'release()', sem.release()


    a = QApplication( sys.argv )
    s = Scheduler( a )
    s.done.connect( a.quit )

    sem = Semaphore( 3 )
    for i in xrange( 5 ):
        s.newTask( coWorker(i, sem) )

    a.exec_()
