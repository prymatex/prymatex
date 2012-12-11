#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os, shutil

ICON_NAMES = ['view-fullscreen', 'application-x-executable-script',
    'edit-delete', 'edit-clear', 'go-up', 'document-save-all', 'edit-cut',
    'go-down-search', 'go-previus', 'project-development', 'go-previous-view',
    'document-save-as', 'project-open', 'applications-system', 'code-class',
    'edit-undo', 'code-variable', 'tab-cose-other', 'go-next', 'view-list-tree',
    'view-filter', 'bookmarks-organize', 'fill-color', 'go-next-view', 'tab-new',
    'document-save', 'tab-close', 'edit-reame', 'ksnapshot', 'help-about',
    'document-open-recent', 'edit-find-project', 'preferences-other', 'folder-sync',
    'applications-utilities', 'go-first-view', 'preferences-plugin-script',
    'emblem-important', 'view-refresh', 'edit-find', 'dialog-close', 'list-add',
    'list-remove', 'accessories-text-editor', 'system-swtch-user', 'go-up-search',
    'document-new', 'folder-new', 'utilities-terminal', 'edit-paste', 'preferences-plugin',
    'application-exit', 'configure', 'project-evelopment-new-template','document-open',
    'edit-copy', 'edit-redo', 'internet-web-browser', 'system-file-manager']

SOURCE = "/%s" % os.path.join('usr', 'share', 'icons', 'oxygen', '32x32')
DESTINITY = os.path.abspath(os.path.join(__file__, '..', '..', 'prymatex', 'share', 'Icons'))

if __name__ == '__main__':
    copyNames = set(ICON_NAMES)
    for dirpath, _, filenames in os.walk(SOURCE):
        sourceNames = set(map(lambda f: os.path.splitext(f)[0], filenames))
        names = sourceNames.intersection(copyNames)
        if names:
            destpath = os.path.join(DESTINITY, dirpath[len(SOURCE) + 1:])
            try:
                os.makedirs(destpath)
            except:
                pass
        for name in names:
            name = filter(lambda f: f.startswith("%s." % name), filenames)[0]
            src = os.path.join(dirpath, name)
            dst = os.path.join(destpath, name)
            shutil.copy(src, dst)
