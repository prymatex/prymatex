#!/usr/bin/env python

BUILD_ATTRIBUTES = {
    "rules": [
        { "attribute": 'attr.project.make',  "glob": 'Makefile',    "group": 'build', },
        { "attribute": 'attr.project.rake',  "glob": 'Rakefile',    "group": 'build', },
        { "attribute": 'attr.project.xcode', "glob": '*.xcodeproj', "group": 'build', },
        { "attribute": 'attr.project.ninja', "glob": '*.ninja',     "group": 'build', },
        { "attribute": 'attr.project.lein',  "glob": '*.lein',      "group": 'build', },
    ],
}

def attributes(filePath, projectDirectory = None):
    return []