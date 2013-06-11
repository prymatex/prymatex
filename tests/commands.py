#!/usr/bin/env python

import sys
from subprocess import Popen, PIPE

p1 = Popen([ "find", "." ], stdout = PIPE)
p2 = Popen([ "grep", "model", "--colour=always" ], stdin = p1.stdout, stdout = PIPE)
output = p2.communicate()[0]
sys.stdout.write(output)
