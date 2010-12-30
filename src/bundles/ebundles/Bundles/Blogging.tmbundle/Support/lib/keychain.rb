# Simple interface for reading and writing Internet passwords to
# the KeyChain.

# We don't have the KeyChain app on Windows!
module KeyChain
  class << self
    require 'yaml'
    PREFS_DIR = ENV['HOME'] + "/Library/Preferences"
    PASS_FILE = PREFS_DIR + "/com.macromates.textmate.blogging_pass.yaml"
    
    def add_internet_password(user, proto, host, path, pass)
      FileUtils.mkdir_p(PREFS_DIR) unless File.directory?(PREFS_DIR)
      site_passwords = []
      site_passwords = open(PASS_FILE) {|f| YAML.load(f) } if File.exists?(PASS_FILE)
      site_passwords.each_with_index do |arr, index|
        if (arr[:host] == host && arr[:user] == user && arr[:path] == path && arr[:proto] == proto) then
          site_passwords[index] = {:user => user, :host => host, :proto => proto, :path => path, :pass => pass}
          open(PASS_FILE, 'w') {|f| YAML.dump(site_passwords, f)}
          return
        end
      end
      site_passwords.push( {:user => user, :host => host, :proto => proto, :path => path, :pass => pass} )
      open(PASS_FILE, 'w') {|f| YAML.dump(site_passwords, f)}
    end
    
    def find_internet_password(user, proto, host, path)
      if File.exists?(PASS_FILE)
        site_passwords = open(PASS_FILE) {|f| YAML.load(f) }
        site_passwords.each { |arr| return arr[:pass] if (arr[:host] == host && 
                                           arr[:user] == user && 
                                           arr[:path] == path && 
                                           arr[:proto] == proto) }
      end
      return nil
    end
    
  end
end
