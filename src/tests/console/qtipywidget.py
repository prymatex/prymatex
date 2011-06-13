import sys,re, os,  locale,  textwrap
import time
import cgi

from PyQt4.QtGui import QWidget,  QApplication,  QKeyEvent
from PyQt4 import QtGui
from PyQt4.QtCore import QObject,  pyqtRemoveInputHook,  QEvent,  Qt
from PyQt4 import Qsci
from qt_ipython import Ui_IPyForm
from StringIO import StringIO
import IPython.Shell
import IPython
from PyQt4.Qsci import *
  
ANSI_STYLES = {'0;30': [0, 'BLACK'],            '0;31': [1, 'RED'],
                     '0;32': [2, 'GREEN'],            '0;33': [3, 'BROWN'],
                     '0;34': [4, 'BLUE'],             '0;35': [5, 'PURPLE'],
                     '0;36': [6, 'CYAN'],             '0;37': [7, 'LIGHTGREY'],
                     '1;30': [8, 'DARKGREY'],        '1;31': [9, 'RED'],
                     '1;32': [10, 'SEAGREEN'],       '1;33': [11, 'YELLOW'],
                     '1;34': [12, 'LIGHTBLUE'],      '1;35':
                                                       [13, 'MEDIUMVIOLET RED'],
                     '1;36': [14, 'LIGHTSTEELBLUE'], '1;37': [15, 'YELLOW']}


# Xterm escape sequences
color_pat = re.compile('\x01?\x1b\[(.*?)m\x02?')
title_pat = re.compile('\x1b]0;(.*?)\x07')

__orig_out = sys.stdout
def pr(s):
    print >> __orig_out, s
    __orig_out.flush()

def ansi_escapes_to_html(text):
    # XXX: do not put print statements to sys.stdout/sys.stderr in 
    # this method, the print statements will call this method, as 
    # you will end up with an infinit loop
    #title = self.title_pat.split(text)
    #if len(title)>1:
    #    self.title = title[-2]
    text = cgi.escape(text)
    #text=text.replace('\n', '<br/>')
    pr(`text`)
    out = []
    text = title_pat.sub('', text)
    segments = color_pat.split(text)
    segment = segments.pop(0)
    out.append(segment)
    pr("segs=" + `segments`)
    #self.GotoPos(self.GetLength())
    #s#elf.StartStyling(self.GetLength(), 0xFF)
    #try:
    #    self.AppendText(segment)
    #except UnicodeDecodeError:
    #    # XXX: Do I really want to skip the exception?
    #    pass
   
    if segments:
        for ansi_tag, text in zip(segments[::2], segments[1::2]):
            pr("At %s t %s" % (ansi_tag, text))
            if ansi_tag not in ANSI_STYLES:
                #pr('add t' + text)
                out.append(text)
            else:
                #pr("add font")
                style = ANSI_STYLES[ansi_tag][1]
                out.append('<font color="%s">%s</font>' % (style, text))
    pr("Out = " + `out`)
    return ''.join(out)




class IPythonWidget(QWidget, Ui_IPyForm):
    def __init__(self, parent = None):
        self.orig_stdout = sys.stdout
        self.orig_stderr = sys.stderr
        QWidget.__init__(self, parent)
        self.setupUi(self)
        #self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.command_entered)
        self.setup_editor()
        self.setup_stdio()
        self.ev_filt = IpyEventFilter()
        #self.ev_filt.bindings['Ctrl+H'] = self.edit_current_headline
        self.ev_filt.bindings['Ctrl+Return'] = self.editor_exec
        self.ev_filt.bindings['Ctrl+PageUp'] = self.editor_hist_up
        self.ev_filt.bindings['Ctrl+PageDown'] = self.editor_hist_down
        self.ev_filt.bindings['Tab'] = self.editor_complete
        self.ev_filt.bindings['Return'] = self.editor_return_pressed
        self.editor.installEventFilter(self.ev_filt)
        
        self.hist_pos = 0
        self.history = ['']
        
        self._complete_sep =  re.compile('[\s\{\}\[\]\(\)\=]')
        self.welcome()


    def editor_hist_up(self):
        if self.hist_pos < 1:
            self.hist_pos = len(self.history)
            
        self.hist_pos-=1
        
        t = self.history[self.hist_pos]
        self.editor.setText(t)
    def editor_hist_down(self):
        self.hist_pos+=1
        if self.hist_pos >= len(self.history):
            self.hist_pos = 0
            return
        
        t = self.history[self.hist_pos]
        self.editor.setText(t)

    def welcome(self):
        banner = textwrap.dedent("""\
        <h1>IPython Qt ui</h1>
        
        <p>Welcome to the qt ui!</p>
        
        <p><b>Ctrl+Enter</b> executes multiline blocks. <b>Ctrl+PgUp/PgDn</b> navigates history.
        </p>        
        """)
        
        self.textEdit.append(banner)

    def editor_complete(self):
        line, index = self.editor.getCursorPosition()
        text = unicode(self.editor.text(line))
        # indent if no text
        if not text.strip():
            raise IPython.ipapi.TryNext
        ctext = text[:index]
        
        print "Complete!", line, index,  text,  ctext
        newtext,  possibilities = self.complete(ctext)
        print newtext,":", possibilities
        if len(newtext) > len(ctext):
            addtext = newtext[len(ctext):]
            self.editor.insertAt(addtext,  line,  index)
            self.editor.setCursorPosition(line,  index + len(newtext))
        if len(possibilities) > 1:  
            poss_html = "<ul>" + "".join(['<li>%s<li>' % it for it in possibilities  ]) + "</ul>"
            self.textEdit.append(poss_html)
    
    def editor_clear(self):
        self.editor.setText("")
    def editor_return_pressed(self):
        t = unicode(self.editor.text())
        rs = t.rstrip()
        # more than one line
        if rs.endswith(':'):
            raise IPython.ipapi.TryNext

        if rs.count('\n') > 0:
            raise IPython.ipapi.TryNext
        
        # execute simple statements directly
        
        self.exec_code(rs)
        self.editor_clear()
        
        
    def editor_exec(self):
        text = unicode(self.editor.text())
        self.history.append(text)
        self.exec_code(text)
        self.editor_clear()
        

        print "exec"
    def setup_editor(self):
        #self.editor = QsciScintilla()
        lexer = QsciLexerPython()
        #lexer.setDefaultFont(font)
        self.editor.setLexer(lexer)
        self.editor.setAutoIndent(True)
        self.editor.show()

    def startup_ops(self):
        #embed_ipython()
        pass

    def setup_stdio(self):
        # for debuggin
        self.cin = StringIO()
        self.cout = StringIO()
        self.cerr = StringIO()
        #self.cout.write = self.write
        #self.cerr.write = self.write
        IPython.Shell.Term.cin = self.cin
        IPython.Shell.Term.cout = self.cout
        IPython.Shell.Term.cerr = self.cout



    def embed_ipython(self):
        import IPython.ipapi
        sys.argv = ['ipython', '-p' , 'sh']
        ses = IPython.ipapi.make_session()

        self.ip = ses.IP.getapi()
        self.ip.set_hook('shell_hook', self._shell)

    def exec_code(self, t):
        self.textEdit.append('<pre><i>' + cgi.escape(t) + '</i></pre>')
        sys.stdout = self.cout
        sys.stderr = self.cout
        self.cout.seek(0)
        self.cout.truncate(0)
        self.ip.runlines(t)
        #self.ip.IP.interact_handle_input(t)
        out = self.cout.getvalue()
        html = ansi_escapes_to_html(out)
        pr("Output :" + html)
        self.textEdit.append('<pre>' + html + '</pre>')
        #self.lineEdit.clear()
        self.cout.seek(0)
        self.cout.truncate(0)
        self.ip.IP.interact_prompt()
        out = self.cout.getvalue()
        html = ansi_escapes_to_html(out)
        self.textEdit.append(html)
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        sys.stdout = self.orig_stdout
        sys.stderr = self.orig_stderr

        #print "command",t
    def command_entered(self):
        #t = unicode(self.lineEdit.text())
        #self.exec_code(t)
        pass

    def write(self,text):
        pass

    def complete(self, line):
        '''
        Returns an auto completed line and/or posibilities for completion.

        Origin: Laurent's wx gui
        
        @param line: Given line so far.
        @type line: string

        @return: Line completed as for as possible,
        and possible further completions.
        @rtype: tuple
        
        
        '''
        split_line = self._complete_sep.split(line)
        possibilities = self.ip.IP.complete(split_line[-1])
        if possibilities:

            def _commonPrefix(str1, str2):
                '''
                Reduction function. returns common prefix of two given strings.

                @param str1: First string.
                @type str1: string
                @param str2: Second string
                @type str2: string

                @return: Common prefix to both strings.
                @rtype: string
                '''
                for i in range(len(str1)):
                    if not str2.startswith(str1[:i+1]):
                        return str1[:i]
                return str1
            common_prefix = reduce(_commonPrefix, possibilities)
            completed = line[:-len(split_line[-1])]+common_prefix
        else:
            completed = line
        return completed, possibilities

    def _shell(self, ip, cmd):
        '''
        Replacement method to allow shell commands without them blocking.

        @param ip: Ipython instance, same as self._IP
        @type cmd: Ipython instance
        @param cmd: Shell command to execute.
        @type cmd: string
        '''
        stdin, stdout = os.popen4(cmd)
        result = stdout.read().decode('cp437').encode(locale.getpreferredencoding())
        #we use print command because the shell command is called
        #inside IPython instance and thus is redirected to thread cout
        #"\x01\x1b[1;36m\x02" <-- add colour to the text...
        print "\x01\x1b[1;36m\x02"+result
        stdout.close()
        stdin.close()



class IpyEventFilter(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.bindings = {}
    def eventFilter(self, obj, event):

        # print "ev",obj, event
        if event.type() == QEvent.KeyPress:
            return self.key_pressed(obj, event)
        return False
    def key_pressed(self, obj, event):
        """ Handle key presses (on any window) """

        keynum = int(event.key())
        keys = {
                Qt.Key_Enter : "Enter",
                Qt.Key_Return : "Return",
                Qt.Key_PageUp: "PageUp",
                Qt.Key_PageDown: "PageDown", 
                Qt.Key_Tab : "Tab", 


                }

        try:
            char = chr(keynum)
        except ValueError:
            print keys,keynum
            char = keys.get(keynum, '<unknown>')
     
        mods = []
        if event.modifiers() & Qt.AltModifier:
            mods.append("Alt")
        if event.modifiers() & Qt.ControlModifier:
            mods.append("Ctrl")
        if event.modifiers() & Qt.ShiftModifier:
            mods.append("Shift")
 
        txt = "+".join(mods) + (mods and "+" or "") + char
        #print "Keypress: [",txt,"]", event.text(), obj, hex(keynum)
        # key was not consumed

        
        cmd = self.bindings.get(txt, None)
        if cmd:
            try:
                cmd()
                return True
            except IPython.ipapi.TryNext:
                return False
            
        
        return False

def create_widget():
    argv = sys.argv
    
    pyqtRemoveInputHook()
    window = IPythonWidget()
    window.embed_ipython()
    
    window.show()
    return window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = create_widget()
    sys.exit(app.exec_())
