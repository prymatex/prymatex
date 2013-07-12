#!/usr/bin/env python

import os

from prymatex.utils import osextra

SCM_RULES = [
    { "attribute": 'attr.scm.svn',       "glob": '.svn',        "group": 'scm',   },
    { "attribute": 'attr.scm.hg',        "glob": '.hg',         "group": 'scm',   },
    { "attribute": 'attr.scm.git',       "glob": '.git',        "group": 'scm',   },
    { "attribute": 'attr.scm.p4',        "glob": '.p4config',   "group": 'scm',   },
]

def attributes(filePath, projectDirectory = None):
    directories = osextra.path.fullsplit(projectDirectory or os.path.dirname(filePath))
    for rule in SCM_RULES:
        testPath = os.sep + os.path.join(*(directories + [ rule["glob"] ]))
        if os.path.exists(testPath):
            return [ rule["attribute"] ]
    return [ ]