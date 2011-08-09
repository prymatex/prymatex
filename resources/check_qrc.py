#!/usr/bin/env python
# coding: utf-8

'''
Checks if all the QRC files are available
'''

import sys
from xml.etree.ElementTree import ElementTree as ET
from os.path import join, normpath, dirname, exists
from optparse import OptionParser

DEFAULT_RESOURCE_FILE = 'resources.qrc'

class FileDoesNotExists(Exception):
    pass

def get_missing_files(qrc_filename, base_path = None):
    ''' Generates a list of missing files 
    @param qrc_filename: QRC File
    @param base_path: Base path, if not given takes dirname(__file__)
    '''
    tree = ET()
    tree.parse(qrc_filename)
    if not base_path:
        base_path = __file__
    base_path = dirname(base_path)
    for file_node in tree.findall('*/file'):
        file_path = file_node.text
        path = normpath(join(base_path, file_path))
        if not exists(path):
            yield file_path

parser = OptionParser()
parser.add_option('-c', '--check', action = 'store_true', default = False,
                  help = 'Check files, does not terminate upon first'
                  'missing file found')
parser.add_option('-b', '--base', default = None,
                  help = 'Base path for resources, default is current dir')

def main(argv = sys.argv):
    
    options, files = parser.parse_args(argv)
    if not files:
        files = [DEFAULT_RESOURCE_FILE, ]
    
    missing_count = 0
    for file in files:
        for missing in get_missing_files(file, options.base):
            sys.stderr.write("File missing: %s" % missing)
            missing_count += 1
            if not options.check:
                return missing_count
    return missing_count


if __name__ == "__main__":
    sys.exit(main())
