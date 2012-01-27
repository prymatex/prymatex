#! /usr/bin/env ruby

FIXTURES = ['json', 'yaml']

def fixture? filename
  FIXTURES.member? filename.split('.')[-1].downcase
end

require ENV["TM_BUNDLE_SUPPORT"] + "/lib/markup"

Dir.chdir ENV['TM_PROJECT_DIRECTORY']

command = ["python", "-u", "manage.py", "loaddata"]

require ENV["TM_SUPPORT_PATH"] + "/lib/tm/executor"

files = []

if fixture? ENV["TM_FILEPATH"]
  files << ENV["TM_FILEPATH"] unless ENV["TM_SELECTED_FILES"]
end

ENV["TM_SELECTED_FILES"].split(' ').each do |file|
  file = file.gsub("'", "")
  if File.directory? file
    Dir.glob(file + '/*').each do |f|
      (files << f unless File.directory? f) if fixture? f
    end
  else
    files << file if fixture? file
  end
end

if files == []
  print "No fixtures found."
else
  TextMate::Executor.run(command + files) do |str, type|
    DjangoParser.parse(str,type)
  end
  exit 205
end