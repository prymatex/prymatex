def get_project
  # Returns the django project that is in this TextMate project.
  
  # Find the directory inside ENV['TM_PROJECT_DIRECTORY'] that contains
  # settings.py
  
  return ENV['TM_PROJECT_DIRECTORY']
end
