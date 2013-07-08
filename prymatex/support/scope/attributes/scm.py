#!/usr/bin/env python

SCM_ATTRIBUTES = {
    "rules": [
        { "attribute": 'attr.scm.svn',       "glob": '.svn',        "group": 'scm',   },
        { "attribute": 'attr.scm.hg',        "glob": '.hg',         "group": 'scm',   },
        { "attribute": 'attr.scm.git',       "glob": '.git',        "group": 'scm',   },
        { "attribute": 'attr.scm.p4',        "glob": '.p4config',   "group": 'scm',   },
    ],
}

def attributes(filePath, projectDirectory = None):
    return [ ]