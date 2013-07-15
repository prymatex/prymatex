#!/usr/bin/env python

import os
from glob import glob

from prymatex.utils import osextra

BUILD_RULES = [
    { "attribute": 'attr.project.make',  "glob": 'Makefile',    "group": 'build', },
    { "attribute": 'attr.project.rake',  "glob": 'Rakefile',    "group": 'build', },
    { "attribute": 'attr.project.xcode', "glob": '*.xcodeproj', "group": 'build', },
    { "attribute": 'attr.project.ninja', "glob": '*.ninja',     "group": 'build', },
    { "attribute": 'attr.project.lein',  "glob": '*.lein',      "group": 'build', },
]

def attributes(filePath, projectDirectory = None):
    if filePath:
        directories = osextra.path.fullsplit(projectDirectory or os.path.dirname(filePath))
        for rule in BUILD_RULES:
            # TODO Iterative search until root
            directory = directories + [ rule["glob"] ]
            while len(directory) > 1:
                testPath = os.sep + os.path.join(*directory)
                if glob(testPath):
                    return [ rule["attribute"] ]
                directory.pop(-2)
    return [ ]
