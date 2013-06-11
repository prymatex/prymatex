#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.core.exceptions import UnsupportedPlatformError

import sys
from prymatex.utils.osextra import path

if sys.platform.count('linux') or sys.platform.count('darwin'):
    from .linux import *
elif sys.platform.count('win'):
    from .win32 import *
else:
    raise UnsupportedPlatformError("%s is not supported in %s. Please contact developers." %
                                    (__name__, sys.platform))