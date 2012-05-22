# Contains all of the markup that takes output from the various
# django manage.py options, and turns them into links if
# applicable.

require ENV["TM_BUNDLE_SUPPORT"] + "/lib/find_file"

class DjangoParser
  
  def self.parse str, type
    case str
    when /^(.*)\.(.*):\s\"(.*)\":(.*)/
      # Validate Models
      appname, model_name, attribute, message = $1, $2, $3, $4
      filename, line_number, column = FindModel.find(ENV['TM_PROJECT_DIRECTORY'], appname, model_name, attribute)
      file_link = "<a class=\"near\" href=\"txmt://open?line=#{line_number}&column=#{column}&url=file://#{filename}\">#{appname}.#{model_name}</a>"
      str = "#{file_link}: \"#{attribute}\": #{message}"
    when /\[.*\]\s\".*\"\s(\d+)\s\d+/
      # Run Server - interpret HTTP Result Code
      code = $1
      type = (code.to_i >= 400 ? "err" : "ok")
    when /^Installing (.*) fixture \'(.*)\' from \'(.*)\'\./
      method, path = $1, $2
      path = "#{path}.#{method}"
      filename = path.split('/')[-1]
      file_url = "txmt://open?line=0&url=file://#{path}"
      file_link = "<a class=\"near\" href=\"#{file_url}\">#{filename}</a>"
      str = "Installing #{method} fixtures from #{file_link}."
      return ""
    when /^Installing index for (.+)\.(.+) model/
      return ""
    when /^Creating table (.+)$/
      return ""
    when /\A[\.EF]*\Z/
      str.gsub!(/(\.)/, "<span class=\"test ok\">\\1</span>")
      str.gsub!(/(E|F)/, "<span class=\"test fail\">\\1</span>")
      str + "<br/>\n"
    when /\A(FAILED.*)\Z/
      type = "test fail"
      str = htmlize str
    when /\A(OK.*)\Z/
      type = "test ok"
      str = htmlize str
    when /^(\s+)File "(.+)", line (\d+), in (.*)/
      indent, file, line, method = $1, $2, $3, $4
      indent += " " if file.sub!(/^\"(.*)\"/,"\1")
      url = "&url=file://" + e_url(file)
      display_name = file.split('/').last 
      str = "#{htmlize(indent)}<a class=\"near\" href=\"txmt://open?line=#{line + url}\">" +
        (method ? "method #{method}" : "<em>at top level</em>") +
        "</a> in <strong>#{display_name}</strong> at line #{line}<br/>\n"
    when /^Ran (\d+) tests in (\d+\.\d+)s$/
      type = ""
    else
      type = ""
      str = htmlize str
    end
    "<div class=\"#{type}\">#{str}</div>"
  end
  
end