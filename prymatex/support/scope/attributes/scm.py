#!/usr/bin/env python

import os
from glob import glob

from prymatex.utils import osextra

SCM_RULES = [
    { "attribute": 'attr.scm.svn',       "glob": '.svn',        "group": 'scm',   },
    { "attribute": 'attr.scm.hg',        "glob": '.hg',         "group": 'scm',   },
    { "attribute": 'attr.scm.git',       "glob": '.git',        "group": 'scm',   },
    { "attribute": 'attr.scm.p4',        "glob": '.p4config',   "group": 'scm',   },
]

def attributes(filePath, projectDirectory = None):
    if filePath:
        directories = osextra.path.fullsplit(projectDirectory or os.path.dirname(filePath))
        for rule in SCM_RULES:
            # TODO Iterative search until root
            directory = directories + [ rule["glob"] ]
            while len(directory) > 1:
                testPath = os.sep + os.path.join(*directory)
                if glob(testPath):
                    return [ rule["attribute"] ]
                directory.pop(-2)
    return [ ]