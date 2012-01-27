#! /usr/bin/env ruby
bundle			= ENV['TM_BUNDLE_SUPPORT']
support			= ENV['TM_SUPPORT_PATH']
require support + "/lib/shelltokenize.rb"
require support + "/lib/Builder.rb"

puts TextMate::selected_paths_for_shell
STDOUT.sync = true
TEST_CLASS = /^class (.*)\(.*TestCase\):/

require ENV["TM_BUNDLE_SUPPORT"] + "/lib/markup"

command = [ENV["TM_PYTHON"] || "python", "-u", 
  "#{ENV['TM_PROJECT_DIRECTORY']}/manage.py", "test", "--noinput",
]

tests = []


def get_tests
  
  def get_app_name(filepath)
    # Technically, a django app does not need a tests module, but since we
    # only care about those that do, we can use this test to see if it is.
    # We could see if there is a model module there, and look for any
    # tests inside that (doctests)
    if filepath =~ /tests/
      return File.basename(filepath.split('/tests')[0])
    else
      if File.directory?(filepath)
        dirname = filepath
      else
        dirname = File.dirname(filepath)
      end
      while dirname != ENV["TM_PROJECT_DIRECTORY"] and dirname != "/"
        if contains_tests_module(dirname)
          return File.basename(dirname)
        end
        dirname = File.dirname(dirname)
      end
    end
    nil
  end
  
  def contains_tests_module(dirname)
    Dir.entries(dirname).member?('tests') or Dir.entries(dirname).member?('tests.py')
  end
  
  
  def test_cases_in_file(file)
    tests = []
    File.open(file) do |f|
      f.readlines.each do |line|
        if line =~ TEST_CLASS
          tests << "#{get_app_name(file)}.#{$1}"
        end
      end
    end
    tests
  end
  
  # If TM_SELECTED_TEXT contains any TestCase classes, then run these test cases.
  if ENV['TM_SELECTED_TEXT'] =~ TEST_CLASS
    test_case = $1
    # Currently assume there is a file or dir called tests[.py]
    app_name = get_app_name(ENV['TM_FILEPATH'])
    return ["#{app_name}.#{test_case}"]
  end
  
  # - If TM_CURRENT_WORD is a TestCase class, just run this test case.
  # - If TM_CURRENT_LINE is in a TestCase, just run this test case.
  
  # If TM_SELECTED_FILES contain any TestCase classes, then run each of these.
  # This is disabled until I can tell if the project drawer is active or not.
  # if ENV['TM_SELECTED_FILES']
  #   tests = []
  #   ENV['TM_SELECTED_FILES'].split(" ").each do |name|
  #     tests << test_cases_in_file(eval(name))
  #   end
  #   return tests unless tests.empty?
  # end
  
  # If TM_FILEPATH is a file with one or more TestCase classes, 
  # run each of these.
  if ENV['TM_FILEPATH']
    tests = test_cases_in_file(ENV['TM_FILEPATH'])
    return tests unless tests.empty?
  end

  # If TM_DIRECTORY contains a tests.py or tests/, then consider this an app, 
  # and run its tests
  app_name = get_app_name(ENV['TM_DIRECTORY'])
  return [app_name] if app_name
  
  # If TM_DIRECTORY has a parent directory that is tests/ then run all of 
  # the tests we can find in all of our child directories and files within.
  # This should have been caught by the previous part.
  # if ENV['TM_DIRECTORY'] =~ /tests/
  #   return [get_app_name(ENV['TM_DIRECTORY'])]
  # end
  
  # If TM_DIRECTORY's parent directories have a child called tests.py or 
  # tests, then consider that directory an app, and run the tests for that app.
  # Ditto
  
  # Else run the full suite.
  return []
end

tests = get_tests()

if tests == []
  ENV['TM_DISPLAYNAME'] = ENV['TM_PROJECT_DIRECTORY'].split('/')[-1] 
else
  ENV['TM_DISPLAYNAME'] = tests.join ", " 
  command << tests
end

require ENV["TM_SUPPORT_PATH"] + "/lib/tm/executor"

ENV["PYTHONPATH"] = ENV["TM_BUNDLE_SUPPORT"] + (ENV.has_key?("PYTHONPATH") ? ":" + ENV["PYTHONPATH"] : "")

Dir.chdir ENV['TM_PROJECT_DIRECTORY']

TextMate::Executor.run(command, :verb => "Testing") do |str, type|
  DjangoParser.parse(str,type)
end