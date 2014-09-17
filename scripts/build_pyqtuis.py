#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import utils

PROJECT_PATH = os.path.abspath(os.path.join(__file__, '..', '..'))

def has_been_updated(source, dest):
    ''' Chcecks weather a file needs to be updated'''
    source_mtime = os.path.getmtime(source)
    try:
        dest_mtime = os.path.getmtime(dest)
    except os.error:
        return True
    if source_mtime > dest_mtime:
        return True
    return False


class QtUiBuild(object):
    """Build PyQt (.ui) files and resources."""
 
    description = "Build PyQt GUIs (.ui) for prymatex directory schema"
    
    def __init__(self, verbose, force = False):
        self.verbose = verbose
        self.force = force
    
    def _ui2py(self, ui_file, py_file):
        try:
            os.system("pyuic5 -o %s %s" % (py_file, ui_file))
        except Exception as e:
            try:
                os.system("pyuic4 -o %s %s" % (py_file, ui_file))
            except Exception as e:
                self.warn('Unable to compile user interface %s: %s' % (py_file, e))
                if not os.path.exists(py_file) or not open(py_file).read():
                    raise SystemExit(1)

    def compile_ui(self, ui_file, py_file = None):
        """Compile the .ui files to python modules."""
        # Search for pyuic4 in python bin dir, then in the $Path.
        if py_file is None:
            projectIndex = len(utils.fullsplit(PROJECT_PATH))
            py_path = os.path.join(PROJECT_PATH, 'prymatex', *utils.fullsplit(ui_file)[projectIndex + 1:-1])
            py_file = os.path.split(ui_file)[1]
            py_file = os.path.splitext(py_file)[0] + '.py'
            py_file = os.path.join(py_path, py_file)
            
        
        if has_been_updated(ui_file, py_file) or self.force:
            if self.verbose:
                print(("Compiling %s -> %s" % (ui_file, py_file)))
            self._ui2py(ui_file, py_file)
        elif self.verbose > 1:
            print(("%s has not been modified" % ui_file)) 
    
    def _rc2py(self, rc_file, py_file):
        try:
            command = 'pyrcc4 %s -o %s'
            os.system(command % (rc_file, py_file))
        except Exception as e:
            self.warn('Unable to compile resources %s: %s', py_file, e)
            if not os.path.exists(py_file) or not open(py_file).read():
                raise SystemExit(1)
            return    
        
    def compile_rc(self, rc_file, py_file = None):
        if py_file is None:
            py_file = os.path.basename(rc_file)
            py_file = os.path.splitext(py_file)[0] + '_rc.py'
            py_file = os.path.join(PROJECT_PATH, 'prymatex', py_file)
            
        if has_been_updated(rc_file, py_file) or self.force:
            if self.verbose:
                print(("Building resource %s -> %s" % (rc_file,py_file)))
            self._rc2py(rc_file, py_file)
        elif self.verbose > 1:
            print(("%s has not been modified" % rc_file ))

    def create_package(self, dirpath):
        projectIndex = len(utils.fullsplit(PROJECT_PATH))
        pkgpath = os.path.join("prymatex", *utils.fullsplit(dirpath)[ projectIndex + 1: ])
        if not os.path.exists(pkgpath):
            os.makedirs(pkgpath)
        init = os.path.join(pkgpath, '__init__.py')
        if not os.path.isfile(init):
            f = open(init, 'w')
            f.flush()
            f.close()

    def run(self):
        """Execute the command."""
        self._wrapuic()
        basepath = os.path.join(PROJECT_PATH, 'resources', 'ui')
        for dirpath, _, filenames in os.walk(basepath):
            self.create_package(dirpath)
            for filename in filenames:
                if filename.endswith('.ui'):
                    
                    self.compile_ui(os.path.join(dirpath, filename))
        #self.compile_rc(os.path.join('resources', 'resources.qrc'))
    _wrappeduic = False
    
    def warn(self, message, *largs):
        print((message % largs))
    
    @classmethod
    def _wrapuic(cls):
        """Wrap uic to use gettext's _() in place of tr()"""
        if cls._wrappeduic:
            return
 
        from PyQt4.uic.Compiler import compiler, qtproxies, indenter
 
        class _UICompiler(compiler.UICompiler):
            """Speciallized compiler for qt .ui files."""
            def createToplevelWidget(self, classname, widgetname):
                output = indenter.getIndenter()
                output.level = 0
                output.write('from prymatex.utils.i18n import ugettext as _')
                return super(_UICompiler, self).createToplevelWidget(classname, widgetname)
                
            def compileUi(self, input_stream, output_stream, from_imports):
                indenter.createCodeIndenter(output_stream)
                w = self.parse(input_stream)

                output = indenter.getIndenter()
                output.write("")

                self.factory._cpolicy._writeOutImports()
                
                for res in self._resources:
                    output.write("from prymatex import %s" % res)
                    #write_import(res, from_imports)

                return {"widgetname": str(w),
                        "uiclass" : w.uiclass,
                        "baseclass" : w.baseclass}
        compiler.UICompiler = _UICompiler
 
        class _i18n_string(qtproxies.i18n_string):
            """Provide a translated text."""
            def __str__(self):
                return "_('%s')" % self.string.encode('string-escape')
        qtproxies.i18n_string = _i18n_string
 
        cls._wrappeduic = True

if __name__ == '__main__':
    verbose = 0
    if len(sys.argv) > 1:
        verbose = int(sys.argv[1])
    sys.exit(QtUiBuild(verbose, force = False).run())
    
