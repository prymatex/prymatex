#!/usr/bin/env python

from glob import glob

BUILD_RULES = [
    { "attribute": 'attr.project.make',  "glob": 'Makefile',    "group": 'build', },
    { "attribute": 'attr.project.rake',  "glob": 'Rakefile',    "group": 'build', },
    { "attribute": 'attr.project.xcode', "glob": '*.xcodeproj', "group": 'build', },
    { "attribute": 'attr.project.ninja', "glob": '*.ninja',     "group": 'build', },
    { "attribute": 'attr.project.lein',  "glob": '*.lein',      "group": 'build', },
]

def attributes(filePath, projectDirectory = None):
    directories = osextra.path.fullsplit(projectDirectory or os.path.dirname(filePath))
    for rule in BUILD_RULES:
        testPath = os.sep + os.path.join(*(directories + [ rule["glob"] ]))
        if os.path.exists(testPath):
            return [ rule["attribute"] ]
    return [ ]
    
def attributes(filePath, projectDirectory = None):
    return []