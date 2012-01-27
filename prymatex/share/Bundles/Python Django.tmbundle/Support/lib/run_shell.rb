#! /usr/bin/env ruby

#---NOT IN USE.  This script is not used.

require 'osx/cocoa'
include OSX

Dir.chdir ENV['TM_PROJECT_DIRECTORY']

command = [ENV["TM_PYTHON"] || "python", "-u", "manage.py"] + ($* or "shell")

src = "tell app \"Terminal\"
  launch
	activate
  do script \"clear; cd \"${TM_PROJECT_DIRECTORY}\"; #{command.join(' ')}\"
  set position of first window to { 100, 100 }
end tell"

p NSAppleScript.alloc.initWithSource(src).executeAndReturnError(nil)