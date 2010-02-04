
from prymatex.lib.exceptions import UnsupportedPlatformError

import sys
if sys.platform.count('linux'):
    from linux import *
elif sys.platform.count('win'):
    raise UnsupportedPlatformError("Windows :'(")
else:
    raise UnsupportedPlatformError("%s is not supported in %s. Please contact developers." %
                                    (__name__, sys.platform))