#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is based on the source of pyqterm from Henning Schroeder (henning.schroeder@gmail.com)
# License: GPL2

import sys
import os
import threading
import time
import signal
import struct
import select
import subprocess
import array

from win32file import ReadFile, WriteFile
from win32pipe import PeekNamedPipe
import msvcrt

from vt100 import Terminal

class Popen(subprocess.Popen):
    def recv(self, maxsize=None):
        return self._recv('stdout', maxsize)
    
    def recv_err(self, maxsize=None):
        return self._recv('stderr', maxsize)

    def send_recv(self, input='', maxsize=None):
        return self.send(input), self.recv(maxsize), self.recv_err(maxsize)

    def get_conn_maxsize(self, which, maxsize):
        if maxsize is None:
            maxsize = 1024
        elif maxsize < 1:
            maxsize = 1
        return getattr(self, which), maxsize
    
    def _close(self, which):
        getattr(self, which).close()
        setattr(self, which, None)
    
    def send(self, input):
        if not self.stdin:
            return None

        try:
            x = msvcrt.get_osfhandle(self.stdin.fileno())
            (errCode, written) = WriteFile(x, input)
        except ValueError:
            return self._close('stdin')
        except (subprocess.pywintypes.error, Exception), why:
            if why[0] in (109, errno.ESHUTDOWN):
                return self._close('stdin')
            raise

        return written

    def _recv(self, which, maxsize):
        conn, maxsize = self.get_conn_maxsize(which, maxsize)
        if conn is None:
            return None
        
        try:
            x = msvcrt.get_osfhandle(conn.fileno())
            (read, nAvail, nMessage) = PeekNamedPipe(x, 0)
            if maxsize < nAvail:
                nAvail = maxsize
            if nAvail > 0:
                (errCode, read) = ReadFile(x, nAvail, None)
        except ValueError:
            return self._close(which)
        except (subprocess.pywintypes.error, Exception), why:
            if why[0] in (109, errno.ESHUTDOWN):
                return self._close(which)
            raise
        
        if self.universal_newlines:
            read = self._translate_newlines(read)
        return read
    
class Multiplexer(object):
    def __init__(self, queue, timeout = 60*60*24):
        # Session
        self.session = {}
        self.queue = queue
        self.timeout = timeout
        self.signal_stop = 0
        
    def stop(self):
        # Stop supervisor thread
        self.signal_stop = 1
        #self.thread.join()

    def proc_resize(self, sid, w, h):
        self.session[sid]['term'].set_size(w, h)
        self.session[sid]['w'] = w
        self.session[sid]['h'] = h

    def proc_keepalive(self, sid, w, h, command = None):
        if not sid in self.session:
            print "creando", sid, self.session
            # Start a new session
            self.session[sid] = {
                'state':'unborn',
                'term':	Terminal(w, h),
                'time':	time.time(),
                'w':	w,
                'h':	h}
            return self.__proc_spawn(sid, command)
        elif self.session[sid]['state'] == 'alive':
            self.session[sid]['time'] = time.time()
            # Update terminal size
            if self.session[sid]['w'] != w or self.session[sid]['h'] != h:
                self.proc_resize(sid, w, h)
            return True
        else:
            return False

    def __proc_spawn(self, sid, command):
        # Session
        self.session[sid]['state'] = 'alive'
        w, h = self.session[sid]['w'], self.session[sid]['h']
        self.session[sid]['process'] = Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        self.session[sid]['pid'] = self.session[sid]['process'].pid
        
        self.session[sid]['thread'] = threading.Thread(target=self.proc_read, args=(sid, ))
        self.session[sid]['thread'].daemon = True
        self.session[sid]['thread'].start()
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

    def proc_read(self, sid):
        """
        Read from process
        """
        session = self.session[sid]
        while not self.signal_stop:
            if session['state'] != 'alive':
                break
            data = self.session[sid]['process'].recv()
            if data:
                session['term'].write(data)
                session["changed"] = time.time()
                self.queue.put([sid, str(session['term'].dump())])
            time.sleep(0.002)
        self.proc_bury(sid)

    def proc_write(self, sid, d):
        """
        Write to process
        """
        if sid not in self.session:
            return False
        elif self.session[sid]['state'] != 'alive':
            return False
        try:
            for c in d:
                if ord(c) == 13:
                    self.session[sid]['process'].send('\r\n')
                else:
                    self.session[sid]['process'].send(c)
        except (IOError, OSError):
            return False
        return True

    def proc_dump(self, sid):
        """
        Dump terminal output
        """
        if sid not in self.session:
            return False
        return self.session[sid]['term'].dump()

    def is_session_alive(self, sid):
        return self.session.get(sid, {}).get('state') == 'alive'
        
    def last_session_change(self, sid):
        return self.session.get(sid, {}).get("changed", None)

    def session_pid(self, sid):
        return self.session.get(sid, {}).get("pid", None)

    def session_info(self, sid):
        pid = self.session_pid(sid)
        return {}