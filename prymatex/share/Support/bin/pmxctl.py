#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import sys, tempfile

try:
    import zmq
except ImportError, reason:
    raise Exception("In order to use pmxctl you must install zmq in your python path\nor if you are runining inside virtualenv please activate the global site-package with toggleglobalsitepackages")
    #raise reason

from optparse import OptionParser, OptionGroup

if 'PMX_SERVER_PORT' in os.environ:
    PMX_SERVER_PORT = os.environ['PMX_SERVER_PORT']
else:
    raise Exception("PMX_SERVER_PORT is not in environ")

'''
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

# ##############################################################################
# nib 
# ##############################################################################
def nib_parse_args(args):
    '''
    Displays custom dialogs from NIBs.

    nib usage:
    "$DIALOG" nib --load <nib file> [<options>]
    "$DIALOG" nib --update <token> [<options>]
    "$DIALOG" nib --wait <token>
    "$DIALOG" nib --dispose <token>
    "$DIALOG" nib --list

    Options:
        --center
        --model <plist>
        --prototypes <plist>
    '''
    parser = OptionParser()
    parser.add_option('--load', action = 'store', metavar="file",
                        help = 'Load nib file [options].')
    parser.add_option('--update', action = 'store', metavar="token",
                        help = 'Update dialog [options].')
    parser.add_option('--wait', action = 'store', metavar="token")
    parser.add_option('--dispose', action = 'store', metavar="token")
    parser.add_option('--list', action = 'store_true', default = False)
    
    #Options
    group = OptionGroup(parser, "Options")
    group.add_option('--center', action = 'store_true', default = False,
                          help = 'Center the window on screen.')
    group.add_option('--model', action = 'store', dest="plist")
    group.add_option('--prototypes', action = 'store', dest="plist")
    parser.add_option_group(group)
    
    options, args = parser.parse_args(args)
    return options, args

# ##############################################################################
# tooltip 
# ##############################################################################
def tooltip_parse_args(args):
    '''
    Shows a tooltip at the caret with the provided content, optionally rendered as HTML.

    tooltip usage:
        "$DIALOG" tooltip --text 'regular text'
        "$DIALOG" tooltip --html '<some>html</some>'
    Use --transparent to give the tooltip window a transparent background (10.5+ only)
    '''
    parser = OptionParser()
    parser.add_option('--text', action = 'store_true', default = False)
    parser.add_option('--html', action = 'store_true', default = False)
    parser.add_option('--transparent', action = 'store_true', default = False)
    options, args = parser.parse_args(args)
    if options.text and options.html:
        parser.error("options --text and --html are mutually exclusive")
    return options, args

# ##############################################################################
# menu
# ##############################################################################
def menu_parse_args(args):
    '''
    Presents a menu using the given structure and returns the option chosen by the user

    menu usage:
        "$DIALOG" menu --items '({title = foo;}, {separator = 1;}, {header=1; title = bar;}, {title = baz;})'
    '''
    parser = OptionParser()
    parser.add_option('--items', action = 'store', dest="parameters")
    
    options, args = parser.parse_args(args)
    return options, args

# ##############################################################################
# popup 
# ##############################################################################
def popup_parse_args(args):
    '''
    Presents the user with a list of items which can be filtered down by typing to select the item they want.

    popup usage:
        "$DIALOG" popup --suggestions '( { display = law; }, { display = laws; insert = "(${1:hello}, ${2:again})"; } )'
        --returnChoice
        --alreadyTyped
        --staticPrefix
        --additionalWordCharacters
        --caseInsensitive
    '''
    parser = OptionParser()
    parser.add_option('--suggestions', action = 'store', dest="suggestions")
    parser.add_option('--returnChoice', action = 'store_true')
    parser.add_option('--alreadyTyped', action = 'store')
    parser.add_option('--staticPrefix', action = 'store')
    parser.add_option('--additionalWordCharacters', action = 'store')
    parser.add_option('--caseInsensitive', action = 'store_true')
    
    options, args = parser.parse_args(args)
    return options, args
    
# ##############################################################################
# defaults 
# ##############################################################################
def defaults_parse_args(args):
    '''
    Register default values for user settings.

    defaults usage:
        "$DIALOG" defaults --register '{ webOutputTheme = night; }'
    ''' 
    parser = OptionParser()
    parser.add_option('--items', action = 'store', dest="plist")
    
    options, args = parser.parse_args(args)
    return options, args

# ##############################################################################
# images 
# ##############################################################################
def images_parse_args(args):
    """
    Add image files as named images for use by other commands/nibs.

    images usage:
        "$DIALOG" images --register  "{ macro = '$(find_app com.macromates.textmate)/Contents/Resources/Bundle Item Icons/Macros.png'; }"
    """ 
    parser = OptionParser()
    parser.add_option('--register', action = 'store', dest="plist")
    
    options, args = parser.parse_args(args)
    return options, args



# ##############################################################################
# alert 
# ##############################################################################
def alert_parse_args(args):
    '''
    Show an alert box.

    alert usage:
        "$DIALOG" alert --alertStyle warning --title 'Delete File?' --body 'You cannot undo this action.' --button1 Delete --button2 Cancel
    ''' 
    parser = OptionParser()
    parser.add_option('--alertStyle', action = 'store')
    parser.add_option('--title', action = 'store')
    parser.add_option('--body', action = 'store')
    parser.add_option('--button1', action = 'store', default="Ok")
    parser.add_option('--button2', action = 'store', default="Cancel")

    options, args = parser.parse_args(args)
    return options, args

# ##############################################################################
# open 
# ##############################################################################
def open_parse_args(args):
    """
    Add image files as named images for use by other commands/nibs.

    images usage:
        "$DIALOG" open url
    """ 
    return None, args

   
def new_dialgo_parse_args(args):
    '''
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
    '''
    usage = """
    %prog command\n
        Commands registered:
        nib: Displays custom dialogs from NIBs.
        tooltip: Shows a tooltip at the caret with the provided content, optionally rendered as HTML.
        menu: Presents a menu using the given structure and returns the option chosen by the user
        popup: Presents the user with a list of items which can be filtered down by typing to select the item they want.
        defaults: Register default values for user settings.
        images: Add image files as named images for use by other commands/nibs.
        alert: Show an alert box.
        Use '%prog command --help' for detailed help
    
    %prog [options] r9151 (Apr 12 2008) <--- :P Full Support \n
        Usage (dialog): %prog [-cdnmqp] nib_file
        Usage (window): %prog [-cdnpaxts] nib_file
        Usage (alert): %prog [-p] -e [-i|-c|-w]
        Usage (menu): %prog [-p] -u
    """
    note = """
Note:
    If you DO NOT use the -m/--modal option,
    OR you create an async window and then use the wait-for-input subcommand,
    you must run tm_dialog.py in a detached/backgrounded process (`mycommand 2&>1 &` in bash).
    Otherwise, Prymatex's UI thread will hang, waiting for your command to complete.
    You can recover from such a hang by killing the tm_dialog process in Terminal.
    """
    
    parser = OptionParser(usage=usage, version="%prog 1.0")
    #Dialog Options
    group = OptionGroup(parser, "Dialog Options")
    group.add_option('-c', '--center', action = 'store_true', default = False,
                          help = 'Center the window on screen.')
    group.add_option('-d', '--defaults', action = 'store', dest="plist",
                          help = 'Register initial values for user defaults.')
    group.add_option('-n', '--new-items', action = 'store', dest="plist",
                          help = 'A key/value list of classes (the key) which should dynamically be created at run-time for use as the NSArrayControllers object class. The value (a dictionary) is how instances of this class should be initialized (the actual instance will be an NSMutableDictionary with these values).')
    group.add_option('-m', '--modal', action = 'store_true', default = False,
                          help = 'Show window as modal.')
    group.add_option('-p', '--parameters', action = 'store',
                          help = 'Provide parameters as a plist.')
    group.add_option('-q', '--quiet', action = 'store_true', default = False,
                          help = 'Do not write result to stdout.')
    parser.add_option_group(group)
    
    #Alert Options            
    group = OptionGroup(parser, "Alert Options")
    group.add_option('-e', '--alert', action = 'store_true', default = False,
                          help = "Show alert. Parameters: 'title', 'message', 'buttons', 'alertStyle' -- can be 'warning,' 'informational', 'critical'.  Returns the button index.")
    parser.add_option_group(group)
    
    #Menu Options
    group = OptionGroup(parser, "Menu Options")
    group.add_option('-u', '--menu', action = 'store_true', default = False,
                          help = 'Treat parameters as a menu structure.')
    parser.add_option_group(group)
    
    #Async Window Options
    group = OptionGroup(parser, "Async Window Options")
    group.add_option('-a', '--async_window', action = 'store_true', default = False,
                          help = 'Displays the window and returns a reference token for it in the output property list.')
    group.add_option('-l', '--list_windows', action = 'store_true', default = False,
                          help = 'List async window tokens.')
    group.add_option('-t', '--update_window', action = 'store', dest="token",
                          help = 'Update an async window with new parameter values. Use the --parameters argument (or stdin) to specify the updated parameters.')
    group.add_option('-x', '--close_window', action = 'store', dest="token",
                          help = 'Close and release an async window.')
    group.add_option('-w', '--wait_for_input', action = 'store', dest="token",
                          help = 'Wait for user input from the given async window.')
    parser.add_option_group(group)
    
    options, args = parser.parse_args(args)
    if options.alert and options.menu:
        parser.error("options --alert and --menu are mutually exclusive")

    return options, args
    

PARSERS = {
           'nib': nib_parse_args,
           'tooltip': tooltip_parse_args,
           'menu': menu_parse_args,
           'popup': popup_parse_args,
           'defaults': defaults_parse_args,
           'images': images_parse_args,
           'alert': alert_parse_args,
           'open': open_parse_args
           }

class CommandHandler(object):
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://127.0.0.1:%s' % PMX_SERVER_PORT)
        
    def async_window(self, options, args):
        if options.parameters is None:
            parameters = sys.stdin.readlines()
            args.append( "".join(parameters))
        else:
            args.append(options.parameters)
        command = {"name": "async_window", "args": args, "kwargs": {}}
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value)
        
    def update_window(self, options, args):
        """docstring for update_window"""
        args.append(options.token)    
        if options.parameters is None:
            parameters = sys.stdin.readlines()
            args.append( "".join(parameters))
        else:
            args.append(options.parameters)

        command = {"name": "update_window", "args": args, "kwargs": {}}
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value["result"])
    
    def modal_window(self, options, args):
        """docstring for modal_window"""
        if options.parameters is None:
            parameters = sys.stdin.readlines()
            args.append( "".join(parameters))
        else:
            args.append(options.parameters)
            
        kwargs = {
            "center": options.center
        }
        command = {"name": "modal_window", "args": args, "kwargs": kwargs}
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value)

    def close_window(self, options, args):
        pass
        
    def tooltip(self, options, args):
        if not args:
            args = [ "".join(sys.stdin.readlines()) ]

        kwargs = {
            "format": options.html and "html" or "text",
            "transparent": options.transparent
        }
        
        command = {"name": "tooltip", "args": args, "kwargs": kwargs}
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value)

    def menu(self, options, args):
        if options.parameters == None:
            parameters = sys.stdin.readlines()
            args.append("".join(parameters))
        else:
            args.append(options.parameters)
        command = {"name": "menu", "args": args, "kwargs": {}}
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value)
        
    def popup(self, options, args):
        if options.suggestions is None:
            parameters = sys.stdin.readlines()
            args.append("".join(parameters))
        else:
            args.append(options.suggestions)
        
        kwargs = {
            "returnChoice": options.returnChoice,
            "alreadyTyped": options.alreadyTyped,
            "staticPrefix": options.staticPrefix,
            "additionalWordCharacters": options.additionalWordCharacters,
            "caseInsensitive": options.caseInsensitive
        }
        
        command = {"name": "popup", "args": args, "kwargs": kwargs}
        
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value)
        
    def defaults(self, options, args):
        command = {"name": "defaults", "args": args, "kwargs": {}}
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value)

    def images(self, options, args):
        if options.plist is None:
            parameters = sys.stdin.readlines()
            args.append("".join(parameters))
        else:
            args.append(options.plist)
        
        command = {"name": "images", "args": args, "kwargs": {}}
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value)
        
    def alert(self, options, args):
        command = {"name": "alert", "args": args, "kwargs": {}}
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value)

    def open(self, options, urls):
        for url in urls:
            if url.startswith("txmt"):
                command = {"name": "open", "args": [ url ], "kwargs": {}}
                self.socket.send_pyobj(command)
                value = self.socket.recv()
                sys.stdout.write(value)
            else:
                os.popen("xdg-open %s" % url)
                
    def debug(self, options, args):
        if options.parameters == None:
            parameters = sys.stdin.readlines()
            args.append( "".join(parameters))
        command = {"name": "debug", "args": args, "kwargs": {}}
        self.socket.send_pyobj(command)
        value = self.socket.recv()
        sys.stdout.write(value)
    
def main(args):
    handler = CommandHandler()
    if len(args) >= 1 and args[0] in PARSERS:
        #Old dialog
        commandName = args[0]
        parser = PARSERS[commandName]
        options, args = parser(args[1:])
        getattr(handler, commandName)(options, args)
    else:
        #New dialog
        options, args = new_dialgo_parse_args(args)
        if options.menu:
            handler.menu(options, args)
        elif options.async_window:
            handler.async_window(options, args)
        elif options.update_window:
            handler.update_window(options, args)
        elif options.modal:
            handler.modal_window(options, args)
        elif options.close_window:
            handler.close_window(options, args)
        else:
            handler.debug(options, args)

if __name__ == '__main__':
    main(sys.argv[1:])