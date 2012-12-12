#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os, shutil

ICON_NAMES = ['tab-close-other', 'edit-rename', 'view-split-left-right',
    'list-add-user', 'system-run', 'project-development-new-template', 'user-properties',
    'bulletblue', 'go-previous', 'view-split-top-bottom', 'user-identity',
    'system-switch-user', 'list-remove-user']

SOURCE = "/%s" % os.path.join('usr', 'share', 'icons', 'oxygen', '32x32')
DESTINITY = os.path.abspath(os.path.join(__file__, '..', '..', 'prymatex', 'share', 'Icons'))

if __name__ == '__main__':
    copyNames = set(ICON_NAMES)
    for dirpath, _, filenames in os.walk(SOURCE):
        sourceNames = set(map(lambda f: os.path.splitext(f)[0], filenames))
        names = sourceNames.intersection(copyNames)
        if names:
            destpath = os.path.join(DESTINITY, dirpath[len(SOURCE) + 1:])
            if not os.path.exists(destpath):
                os.makedirs(destpath)
        for name in names:
            name = filter(lambda f: f.startswith("%s." % name), filenames)[0]
            src = os.path.join(dirpath, name)
            dst = os.path.join(destpath, name)
            shutil.copy(src, dst)
