#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is based on the source of pyqterm from Henning Schroeder (henning.schroeder@gmail.com)
# License: GPL2

import sys
import os
import fcntl
import threading
import time
import termios
import pty
import signal
import struct
import select
import subprocess

from vt100 import Terminal

def synchronized(func):
    def wrapper(self, *args, **kwargs):
        try:
            self.lock.acquire()
        except AttributeError:
            self.lock = threading.RLock()
            self.lock.acquire()
        try:
            result = func(self, *args, **kwargs)
        finally:
            self.lock.release()
        return result
    return wrapper




class Multiplexer(object):


    def __init__(self, queue, cmd="/bin/bash", env_term = "xterm-color", timeout=60*60*24):
        # Set Linux signal handler
        if sys.platform in ("linux2", "linux3"):
            self.sigchldhandler = signal.signal(signal.SIGCHLD, signal.SIG_IGN)
            
        # Session
        self.session = {}
        self.queue = queue
        self.cmd = cmd
        self.env_term = env_term
        self.timeout = timeout

        # Supervisor thread
        self.signal_stop = 0
        self.thread = threading.Thread(target = self.proc_thread)
        self.thread.start()


    def stop(self):
        # Stop supervisor thread
        self.signal_stop = 1
        self.thread.join()


    def proc_resize(self, sid, w, h):
        fd = self.session[sid]['fd']
        # Set terminal size
        try:
            fcntl.ioctl(fd,
                struct.unpack('i',
                    struct.pack('I', termios.TIOCSWINSZ)
                )[0],
                struct.pack("HHHH", h, w, 0, 0))
        except (IOError, OSError):
            pass
        self.session[sid]['term'].set_size(w, h)
        self.session[sid]['w'] = w
        self.session[sid]['h'] = h


    @synchronized
    def proc_keepalive(self, sid, w, h, cmd=None):
        if not sid in self.session:
            # Start a new session
            self.session[sid] = {
                'state':'unborn',
                'term':	Terminal(w, h),
                'time':	time.time(),
                'w':	w,
                'h':	h}
            return self.proc_spawn(sid, cmd)
        elif self.session[sid]['state'] == 'alive':
            self.session[sid]['time'] = time.time()
            # Update terminal size
            if self.session[sid]['w'] != w or self.session[sid]['h'] != h:
                self.proc_resize(sid, w, h)
            return True
        else:
            return False


    def proc_spawn(self, sid, cmd=None):
        # Session
        self.session[sid]['state'] = 'alive'
        w, h = self.session[sid]['w'], self.session[sid]['h']
        # Fork new process
        try:
            pid, fd = pty.fork()
        except (IOError, OSError):
            self.session[sid]['state'] = 'dead'
            return False
        if pid == 0:
            cmd = cmd or self.cmd
            # Safe way to make it work under BSD and Linux
            try:
                ls = os.environ['LANG'].split('.')
            except KeyError:
                ls = []
            if len(ls) < 2:
                ls = ['en_US', 'UTF-8']
            try:
                os.putenv('COLUMNS', str(w))
                os.putenv('LINES', str(h))
                os.putenv('TERM', self.env_term)
                os.putenv('PATH', os.environ['PATH'])
                os.putenv('LANG', ls[0] + '.UTF-8')
                #os.system(cmd)
                p = subprocess.Popen(cmd, shell=False)
                #print "called with subprocess", p.pid
                child_pid, sts = os.waitpid(p.pid, 0)
                #print "child_pid", child_pid, sts
            except (IOError, OSError):
                pass
            # self.proc_finish(sid)
            os._exit(0)
        else:
            # Store session vars
            self.session[sid]['pid'] = pid
            self.session[sid]['fd'] = fd
            # Set file control
            fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
            # Set terminal size
            self.proc_resize(sid, w, h)
            return True


    def proc_waitfordeath(self, sid):
        try:
            os.close(self.session[sid]['fd'])
        except (KeyError, IOError, OSError):
            pass
        if sid in self.session:
            if 'fd' in self.session[sid]:
                del self.session[sid]['fd']
        try:
            os.waitpid(self.session[sid]['pid'], 0)
        except (KeyError, IOError, OSError):
            pass
        if sid in self.session:
            if 'pid' in self.session[sid]:
                del self.session[sid]['pid']
        self.session[sid]['state'] = 'dead'
        return True


    def proc_bury(self, sid):
        if self.session[sid]['state'] == 'alive':
            try:
                os.kill(self.session[sid]['pid'], signal.SIGTERM)
            except (IOError, OSError):
                pass
        self.proc_waitfordeath(sid)
        if sid in self.session:
            del self.session[sid]
        return True


    @synchronized
    def proc_buryall(self):
        for sid in self.session.keys():
            self.proc_bury(sid)


    @synchronized
    def proc_read(self, sid):
        """
        Read from process
        """
        if sid not in self.session:
            return False
        elif self.session[sid]['state'] != 'alive':
            return False
        try:
            fd = self.session[sid]['fd']
            d = os.read(fd, 65536)
            if not d:
                # Process finished, BSD
                self.proc_waitfordeath(sid)
                return False
        except (IOError, OSError):
            # Process finished, Linux
            self.proc_waitfordeath(sid)
            return False
        term = self.session[sid]['term']
        term.write(d)
        # Read terminal response
        d = term.read()
        if d:
            try:
                os.write(fd, d)
            except (IOError, OSError):
                return False
        return True


    @synchronized
    def proc_write(self, sid, d):
        """
        Write to process
        """
        if sid not in self.session:
            return False
        elif self.session[sid]['state'] != 'alive':
            return False
        try:
            term = self.session[sid]['term']
            d = term.pipe(d)
            fd = self.session[sid]['fd']
            os.write(fd, d)
        except (IOError, OSError):
            return False
        return True


    @synchronized
    def proc_dump(self, sid):
        """
        Dump terminal output
        """
        if sid not in self.session:
            return False
        return self.session[sid]['term'].dump()


    @synchronized
    def proc_getalive(self):
        """
        Get alive sessions, bury timed out ones
        """
        fds = []
        fd2sid = {}
        now = time.time()
        for sid in self.session.keys():
            then = self.session[sid]['time']
            if (now - then) > self.timeout:
                self.proc_bury(sid)
            else:
                if self.session[sid]['state'] == 'alive':
                    fds.append(self.session[sid]['fd'])
                    fd2sid[self.session[sid]['fd']] = sid
        return (fds, fd2sid)


    def proc_thread(self):
        """
        Supervisor thread
        """
        while not self.signal_stop:
            # Read fds
            (fds, fd2sid) = self.proc_getalive()
            try:
                i, o, e = select.select(fds, [], [], 1.0)
            except (IOError, OSError):
                i = []
            for fd in i:
                sid = fd2sid[fd]
                self.proc_read(sid)
                self.session[sid]["changed"] = time.time()
                self.queue.put(sid)
            if len(i):
                time.sleep(0.002)
        self.proc_buryall()

    def is_session_alive(self, sid):
        return self.session.get(sid, {}).get('state') == 'alive'
        
    def session_pid(self, sid):
        return self.session.get(sid, {}).get("pid", None)
        
    def last_session_change(self, sid):
        return self.session.get(sid, {}).get("changed", None)

