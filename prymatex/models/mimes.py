#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import pickle
import io

from prymatex.qt import QtCore

class PyMimeData(QtCore.QMimeData):
    """ 
    The PyMimeData wraps a Python instance as MIME data.
    """
    # The MIME type for instances.
    MIME_TYPE = 'application/x-ets-qt4-instance'

    def __init__(self, data = None):
        """ 
        Initialise the instance.
        """
        QtCore.QMimeData.__init__(self)

        # Keep a local reference to be returned if possible.
        self._local_instance = data

        if data is not None:
            # We may not be able to pickle the data.
            try:
                pdata = pickle.dumps(data)
            except Exception as e:
                pdata = ""
                #return
    
            # This format (as opposed to using a single sequence) allows the
            # type to be extracted without unpickling the data itself.
            self.setData(self.MIME_TYPE, pickle.dumps(data.__class__) + pdata)

    @classmethod
    def coerce(cls, md):
        """ 
        Coerce a QMimeData instance to a PyMimeData instance if possible.
        """
        # See if the data is already of the right type. If it is then we know
        # we are in the same process.
        if isinstance(md, cls):
            return md

        # See if the data type is supported.
        if not md.hasFormat(cls.MIME_TYPE):
            return None

        nmd = cls()
        nmd.setData(cls.MIME_TYPE, md.data())
        return nmd

    def instance(self):
        """ 
        Return the instance.
        """
        if self._local_instance is not None:
            return self._local_instance

        io = io.StringIO(str(self.data(self.MIME_TYPE)))

        try:
            # Skip the type.
            pickle.load(io)

            # Recreate the instance.
            return pickle.load(io)
        except:
            pass

        return None

    def instanceType(self):
        """ 
        Return the type of the instance.
        """
        if self._local_instance is not None:
            return self._local_instance.__class__

        try:
            return pickle.loads(str(self.data(self.MIME_TYPE)))
        except:
            pass
        return None