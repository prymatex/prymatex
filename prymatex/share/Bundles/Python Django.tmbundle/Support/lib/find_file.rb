class FindModel
  def self.find(project, appname, model, attribute=nil)
    filename = "#{project}/#{appname}/models"
    if File.exists? "#{filename}.py"
      filename = "#{filename}.py"
    elsif File.exists? "#{filename}/#{model}.py"
      filename = "#{filename}/#{model}.py"
    else
      return [nil, 0, 0]
    end
    
    if attribute
      File.open(filename) do |f|
        line_number = 0
        f.readlines.each do |line|
          line_number += 1
          if line =~ /^\s+#{attribute}\s*=/
            return [filename, line_number, (line =~ /#{attribute}/).to_i + 1]
          end
        end
      end
    end
    
    [filename, 0, 0]
  end
end