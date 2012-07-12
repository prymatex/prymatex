#!/bin/bash
#BASH_INIT=`echo $TM_SUPPORT_PATH | tr -d '"'`
# source "$BASH_INIT/lib/bash_init.sh"
source "$TM_SUPPORT_PATH/lib/bash_init.sh"
exec /usr/bin/env $@
