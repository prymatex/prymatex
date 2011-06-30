#!/usr/bin/env python
# coding: utf-8
import sys
from optparse import OptionParser
import xml.etree.ElementTree as ET

def main(argv = sys.argv):
    parser = OptionParser()
    parser.add_option('-r', '--resource', type=str,
                      help = "Resource file",
                      default = "res.qrc"
                     )
    opts, files = parser.parse_args(argv[1:])

    resource_xml = ET.parse(opts.resource)
    print (resource_xml)
    from ipdb import set_trace; set_trace()
    

if __name__ == "__main__":
    sys.exit(main())
