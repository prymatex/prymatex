require "#{ENV['TM_SUPPORT_PATH']}/lib/ui"

class TextMateSTDIN < IO
  def gets(*args)
    return super if IO.select([self],[],[],0.1)
    TextMate::UI.request_string( :prompt  => "Script is Requesting Input:",
                                 :button1 => "Send" ) + "\n"
  end
end

$TM_STDIN = TextMateSTDIN.new(STDIN.fileno)
STDIN.reopen($TM_STDIN)
def gets(*args)
  $TM_STDIN.gets(*args)
end
