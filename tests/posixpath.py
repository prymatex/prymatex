#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from glob import glob
os.chdir("..")
prymatex_dir = 'prymatex'

replaces = [('…', '...'), ('—', '-'), ('‘', "'"), ('’', "'"), ("“", '"'), ("”", '"')]

def main():
    for dirpath, dirnames, filenames in os.walk(prymatex_dir):
        for file in filenames:
            nfile = file
            for replace in replaces:
                index = nfile.find(replace[0])
                if index != -1:
                    nfile = nfile.replace(replace[0], replace[1])
            if file != nfile:
                old = os.path.join(dirpath, file.replace('"', '\"').replace("?", "\?").replace(">", "\>").replace("<", "\<").replace("$", "\$"))
                new = os.path.join(dirpath, nfile.replace('"', '\"').replace("?", "\?").replace(">", "\>").replace("<", "\<").replace("$", "\$"))
                print(old, new)
                os.system('git mv "%s" "%s"' % (old, new))
    
if __name__ == "__main__":
    main()