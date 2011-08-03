#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from xmlrpclib import ServerProxy
import sys, tempfile
from optparse import OptionParser
# sum(map(lambda c: ord(c), 'Prymatex is an open source textmate replacement'))

PORT = 4612

'''

*******************************************************************************
- help 
*******************************************************************************
8 commands registered:
	nib: Displays custom dialogs from NIBs.
	tooltip: Shows a tooltip at the caret with the provided content, optionally rendered as HTML.
	menu: Presents a menu using the given structure and returns the option chosen by the user
	popup: Presents the user with a list of items which can be filtered down by typing to select the item they want.
	defaults: Register default values for user settings.
	help: Gives a brief list of available commands, or usage details for a specific command.
	images: Add image files as named images for use by other commands/nibs.
	alert: Show an alert box.
Use `"$DIALOG" help command` for detailed help

*******************************************************************************
- nib 
*******************************************************************************
Displays custom dialogs from NIBs.

nib usage:
"$DIALOG" nib --load �nib file� [�options�]
"$DIALOG" nib --update �token� [�options�]
"$DIALOG" nib --wait �token�
"$DIALOG" nib --dispose �token�
"$DIALOG" nib --list

Options:
	--center
	--model �plist�
	--prototypes �plist�

*******************************************************************************
- tooltip 
*******************************************************************************
Shows a tooltip at the caret with the provided content, optionally rendered as HTML.

tooltip usage:
	"$DIALOG" tooltip --text 'regular text'
	"$DIALOG" tooltip --html '<some>html</some>'
Use --transparent to give the tooltip window a transparent background (10.5+ only)

*******************************************************************************
- menu 
*******************************************************************************
Presents a menu using the given structure and returns the option chosen by the user

menu usage:
	"$DIALOG" menu --items '({title = foo;}, {separator = 1;}, {header=1; title = bar;}, {title = baz;})'

*******************************************************************************
- popup 
*******************************************************************************
Presents the user with a list of items which can be filtered down by typing to select the item they want.

popup usage:
	"$DIALOG" popup --suggestions '( { display = law; }, { display = laws; insert = "(${1:hello}, ${2:again})"; } )'

*******************************************************************************
- defaults 
*******************************************************************************
Register default values for user settings.

defaults usage:
	"$DIALOG" defaults --register '{ webOutputTheme = night; }'

*******************************************************************************
- images 
*******************************************************************************
Add image files as named images for use by other commands/nibs.

images usage:
	"$DIALOG" images --register  "{ macro = '$(find_app com.macromates.textmate)/Contents/Resources/Bundle Item Icons/Macros.png'; }"

*******************************************************************************
- alert 
*******************************************************************************
Show an alert box.

alert usage:
	"$DIALOG" alert --alertStyle warning --title 'Delete File?' --body 'You cannot undo this action.' --button1 Delete --button2 Cancel

*******************************************************************************
- args 
*******************************************************************************
tm_dialog r9151 (Apr 12 2008)
Usage (dialog): tm_dialog [-cdnmqp] nib_file
Usage (window): tm_dialog [-cdnpaxts] nib_file
Usage (alert): tm_dialog [-p] -e [-i|-c|-w]
Usage (menu): tm_dialog [-p] -u

Dialog Options:
 -c, --center                 Center the window on screen.
 -d, --defaults <plist>       Register initial values for user defaults.
 -n, --new-items <plist>      A key/value list of classes (the key) which should dynamically be created at run-time for use as the NSArrayController�s object class. The value (a dictionary) is how instances of this class should be initialized (the actual instance will be an NSMutableDictionary with these values).
 -m, --modal                  Show window as modal (other windows will be inaccessible).
 -p, --parameters <plist>     Provide parameters as a plist.
 -q, --quiet                  Do not write result to stdout.

Alert Options:
 -e, --alert                  Show alert. Parameters: 'title', 'message', 'buttons'
                              'alertStyle' -- can be 'warning,' 'informational',
                              'critical'.  Returns the button index.
Menu Options:
 -u, --menu                   Treat parameters as a menu structure.

Async Window Options:
 -a, --async-window           Displays the window and returns a reference token for it
                              in the output property list.
 -l, --list-windows           List async window tokens.
 -t, --update-window <token>  Update an async window with new parameter values.
                              Use the --parameters argument (or stdin) to specify the
                              updated parameters.
 -x, --close-window <token>   Close and release an async window.
 -w, --wait-for-input <token> Wait for user input from the given async window.

Note:
If you DO NOT use the -m/--modal option,
OR you create an async window and then use the wait-for-input subcommand,
you must run tm_dialog in a detached/backgrounded process (`mycommand 2&>1 &` in bash).
Otherwise, TextMate's UI thread will hang, waiting for your command to complete.
You can recover from such a hang by killing the tm_dialog process in Terminal.

# create and show the dialog
sorcerer% $tm_dialog -a --parameters '{title = "Game Progress"; summary = "Playing the game..."; progressValue = 10;}' $HOME/Library/ Application\ Support/TextMate/Support/nibs/ProgressDialog.nib

# ... which returns the usual plist ...
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd ">
<plist version="1.0">
<dict>
        <key>returnCode</key>
        <integer>0</integer>
        <key>token</key>
        <integer>7</integer>
</dict>
</plist>

# ... fill the progress bar to completion ...
sorcerer% $tm_dialog -t 7 --parameters '{progressValue = 40;}'
sorcerer% $tm_dialog -t 7 --parameters '{progressValue = 80;}'
sorcerer% $tm_dialog -t 7 --parameters '{progressValue = 100;}'

# ...close the progress dialog.
sorcerer% $tm_dialog -x 7
'''

def new_dialgo_parser(args):
    parser = OptionParser()
    #Dialog Options
    parser.add_option('-c', '--center', action = 'store_true', default = False,
                          help = 'Center the window on screen.')
    parser.add_option('-d', '--defaults', action = 'store', dest="plist",
                          help = 'Register initial values for user defaults.')
    parser.add_option('-n', '--new-items', action = 'store', dest="plist",
                          help = 'A key/value list of classes (the key) which should dynamically be created at run-time for use as the NSArrayControllers object class. The value (a dictionary) is how instances of this class should be initialized (the actual instance will be an NSMutableDictionary with these values).')
    parser.add_option('-m', '--modal', action = 'store_true', default = False,
                          help = 'Show window as modal.')
    parser.add_option('-p', '--parameters', action = 'store', dest="plist",
                          help = 'Provide parameters as a plist.')
    parser.add_option('-q', '--quiet', action = 'store_true', default = False,
                          help = 'Do not write result to stdout.')
    #Alert Options            
    parser.add_option('-e', '--alert', action = 'store_true', default = False,
                          help = "Show alert. Parameters: 'title', 'message', 'buttons', 'alertStyle' -- can be 'warning,' 'informational', 'critical'.  Returns the button index.")
    #Menu Options
    parser.add_option('-u', '--menu', action = 'store_true', default = False,
                          help = 'Treat parameters as a menu structure.')
    
    #Async Window Options
    parser.add_option('-a', '--async-window', action = 'store_true', default = False,
                          help = 'Displays the window and returns a reference token for it in the output property list.')
    parser.add_option('-l', '--list-windows', action = 'store_true', default = False,
                          help = 'List async window tokens.')
    parser.add_option('-t', '--update-window', action = 'store', dest="token",
                          help = 'Update an async window with new parameter values. Use the --parameters argument (or stdin) to specify the updated parameters.')
    parser.add_option('-x', '--close-window', action = 'store', dest="token",
                          help = 'Close and release an async window.')
    parser.add_option('-w', '--wait-for-input', action = 'store', dest="token",
                          help = 'Wait for user input from the given async window.')
    return parser.parse_args(args)

def main(args):
    if len(args) > 1 and args[0] in ['nib', 'tooltip', 'menu', 'popup', 'images', 'alert']:
        server = ServerProxy('http://localhost:%d' % PORT)
        getattr(server, args[0])(" ".join(args[1:]))
    elif len(args) > 1 and args[0] == 'defaults':
        #TODO: Ejecutar el commando defaults con los argumentos
        pass
    else:
        # new version tm_dialog r9151 (Apr 12 2008)
        options, args = new_dialgo_parser(args)
        server = ServerProxy('http://localhost:%d' % PORT)
        server.debug(str(options), str(args))
        
if __name__ == '__main__':
    main(sys.argv[1:])
