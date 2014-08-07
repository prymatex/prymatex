#!/usr/bin/env python

import os
import platform
from glob import glob

# TODO Para los scm hay toda una bateria de alternativas
GLOB_RULES = [
    { "auxiliary": 'attr.project.make',  "glob": 'Makefile',    "group": 'build', },
    { "auxiliary": 'attr.project.rake',  "glob": 'Rakefile',    "group": 'build', },
    { "auxiliary": 'attr.project.xcode', "glob": '*.xcodeproj', "group": 'build', },
    { "auxiliary": 'attr.project.ninja', "glob": '*.ninja',     "group": 'build', },
    { "auxiliary": 'attr.project.lein',  "glob": '*.lein',      "group": 'build', },
    { "auxiliary": 'attr.scm.svn',       "glob": '.svn',        "group": 'scm',   },
    { "auxiliary": 'attr.scm.hg',        "glob": '.hg',         "group": 'scm',   },
    { "auxiliary": 'attr.scm.git',       "glob": '.git',        "group": 'scm',   },
    { "auxiliary": 'attr.scm.p4',        "glob": '.p4config',   "group": 'scm',   },
]

def _system(scope, file_path = None):
    return scope.push_scope("attr.os-version." + platform.release())

def _path(scope, file_path = None):
    if file_path:
        rev_path = file_path.replace(" ", "_").split(os.sep)
        if not rev_path[0]:
            rev_path.pop(0)
        rev_path = rev_path[:-1] + rev_path[-1].split(".") + ['rev-path', 'attr']
        scope.push_scope(".".join(rev_path[::-1]))
    else:
        scope.push_scope('attr.untitled')

def _glob(scope, file_path = None):
    if file_path is not None:
        source =  os.path.split(file_path)[0]
        groups = []
        while True:
            for rule in GLOB_RULES:
                pattern = os.path.join(source, rule["glob"])
                if glob(pattern) and rule["group"] not in groups:
                    scope.push_scope(rule["auxiliary"])
                    groups.append(rule["group"])
            source, tail = os.path.split(source)
            if not tail:
                break

def auxiliary(scope, file_path = None):
    for function in (_system, _path, _glob):
        function(scope, file_path)
    return scope