#! /usr/bin/env ruby

require ENV["TM_BUNDLE_SUPPORT"] + "/markup"

Dir.chdir ENV['TM_PROJECT_DIRECTORY']

command = [ENV["TM_PYTHON"] || "python", "-u", "manage.py"] + ($* or "validate")

require ENV["TM_SUPPORT_PATH"] + "/lib/tm/executor"
require ENV["TM_BUNDLE_SUPPORT"] + "/find_file"

TextMate::Executor.run(command, :verb => "Validating") do |str, type|
  DjangoParser.parse(str,type)
end