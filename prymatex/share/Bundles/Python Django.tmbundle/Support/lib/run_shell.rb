#! /usr/bin/env ruby

Dir.chdir ENV['TM_PROJECT_DIRECTORY']

command = [ENV["TM_PYTHON"] || "python", "-u", "manage.py"] + ($* or "shell")

%x{terminal.py clear; cd \"${TM_PROJECT_DIRECTORY}\"; #{command.join(' ')}}