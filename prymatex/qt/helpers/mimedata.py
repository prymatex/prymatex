#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path as osp

from prymatex.qt import QtGui

def _process_mime_path(path, extlist):
    if path.startswith(r"file://"):
        if os.name == 'nt':
            # On Windows platforms, a local path reads: file:///c:/...
            # and a UNC based path reads like: file://server/share
            if path.startswith(r"file:///"): # this is a local path
                path=path[8:]
            else: # this is a unc path
                path = path[5:]
        else:
            path = path[7:]
    if osp.exists(path):
        if extlist is None or osp.splitext(path)[1] in extlist:
            return path


def mimedata2url(source, extlist=None):
    """
    Extract url list from MIME data extlist: for example ('.py', '.pyw')
    """
    pathlist = []
    if source.hasUrls():
        for url in source.urls():
            path = _process_mime_path(url, extlist)
            if path is not None:
                pathlist.append(path)
    elif source.hasText():
        for rawpath in source.text().splitlines():
            path = _process_mime_path(rawpath, extlist)
            if path is not None:
                pathlist.append(path)
    if pathlist:
        return pathlist