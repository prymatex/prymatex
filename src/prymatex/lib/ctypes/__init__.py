#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 09/02/2010 by defo

import sys
from prymatex.lib import exceptions

if sys.platform.count('linux'):
    try:
        import onig_linux2 as oniguruma
    except Exception, e:
        print "Se neceista tener /usr/lib/libonig.so"
        print "Busque el paquete en su distribución"
        sys.exit()
else:
    raise exceptions.UnsupportedPlatformError(sys.platform)  