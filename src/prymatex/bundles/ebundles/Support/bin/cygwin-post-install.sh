#!/bin/sh

# Link to equivalents of mac commands
ln -sf /bin/getclip.exe /bin/pbpaste.exe
ln -sf /bin/putclip.exe /bin/pbcopy.exe
ln -sf /bin/tac.exe /bin/rev.exe
ln -sf /bin/python.exe /bin/pythonw.exe
ln -sf /bin/cygstart.exe /bin/open.exe

# Some bundles refer to CocoaDialog via it's full mac path
mkdir -p "$TM_SUPPORT_PATH/bin/CocoaDialog.app/Contents/MacOS"
ln -sf "$TM_SUPPORT_PATH/bin/CocoaDialog.exe" "$TM_SUPPORT_PATH/bin/CocoaDialog.app/Contents/MacOS/CocoaDialog.exe"

# Ruby is sensitive to permissions for dirs in PATH
chmod o-w /usr/local/bin
chmod o-w /usr/local
chmod o-w /usr
chmod o-w /etc
chmod o-w /usr/sbin
chmod o-w /usr/bin
chmod o-w /usr/X11R6/bin
chmod o-w /usr/X11R6
chmod o-w `cygpath $HOMEDRIVE`
