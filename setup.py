#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://launchpad.net/encuentro

"""Build tar.gz for prymatex.

Needed packages to run (using Debian/Ubuntu package names):
"""

import os

from distutils.command.install import install
from distutils.command.build import build
from distutils.core import setup

class QtBuild(build):
    """Build PyQt (.ui) files and resources."""
 
    description = "build PyQt GUIs (.ui)."
 
    def compile_ui(self, ui_file, py_file=None):
        """Compile the .ui files to python modules."""
        # Search for pyuic4 in python bin dir, then in the $Path.
        if py_file is None:
            # go from the ui_file in the data folder to the
            # python file in the qt moodule
            py_file = os.path.split(ui_file)[1]
            py_file = os.path.splitext(py_file)[0] + '_ui.py'
            py_file = os.path.join('package', 'qt', py_file)
        # we indeed want to catch Exception, is ugle but w need it
        # pylint: disable=W0703
        try:
            # import the uic compiler from pyqt and generate the 
            # .py files something similar could be done with pyside
            # but that is left as an exercise for the reader.
            from PyQt4 import uic
            fp = open(py_file, 'w')
            uic.compileUi(ui_file, fp)
            fp.close()
            log.info('Compiled %s into %s', ui_file, py_file)
        except Exception, e:
            self.warn('Unable to compile user interface %s: %s',
                           py_file, e)
            if not os.path.exists(py_file) or\
                                            not file(py_file).read():
                raise SystemExit(1)
            return
        # pylint: enable=W0703
 
    def run(self):
        """Execute the command."""
        self._wrapuic()
        basepath = os.path.join('prymatex',  'gui')
        for dirpath, _, filenames in os.walk(basepath):
            for filename in filenames:
                if filename.endswith('.ui'):
                    self.compile_ui(os.path.join(dirpath, filename))
 
    # pylint: disable=E1002
    _wrappeduic = False
    @classmethod
    def _wrapuic(cls):
        """Wrap uic to use gettext's _() in place of tr()"""
        if cls._wrappeduic:
            return
 
        from PyQt4.uic.Compiler import compiler, qtproxies, indenter
 
        # pylint: disable=C0103
        class _UICompiler(compiler.UICompiler):
            """Speciallized compiler for qt .ui files."""
            def createToplevelWidget(self, classname, widgetname):
                o = indenter.getIndenter()
                o.level = 0
                o.write('from module.with.gettext.setup import _')
                return super(_UICompiler, self).createToplevelWidget(
                                   classname, widgetname)
        compiler.UICompiler = _UICompiler
 
        class _i18n_string(qtproxies.i18n_string):
            """Provide a translated text."""
 
            def __str__(self):
                return "_('%s')" % self.string.encode(
                                                'string-escape')
 
        qtproxies.i18n_string = _i18n_string
 
        cls._wrappeduic = True
        # pylint: enable=C0103
    # pylint: enable=E1002

class CustomInstall(install):
    """Custom installation class on package files.

    It copies all the files into the "PREFIX/PROJECTNAME" dir.
    """
    def run(self):
        """Run parent install, and then save the install dir in the script."""
        install.run(self)

        for script in self.distribution.scripts:
            script_path = os.path.join(self.install_scripts, os.path.basename(script))
            with open(script_path, 'rb') as fh:
                content = fh.read()
            content = content.replace('@ INSTALLED_BASE_DIR @', self._custom_data_dir)
            with open(script_path, 'wb') as fh:
                fh.write(content)

    def finalize_options(self):
        """Alter the installation path."""
        install.finalize_options(self)

        # the data path is under 'prefix'
        data_dir = os.path.join(self.prefix, self.distribution.get_name())

        # if we have 'root', put the building path also under it (used normally
        # by pbuilder)
        if self.root is None:
            build_dir = data_dir
        else:
            build_dir = os.path.join(self.root, data_dir[1:])

        # change the lib install directory so all package files go inside here
        self.install_lib = build_dir

        # save this custom data dir to later change the scripts
        self._custom_data_dir = data_dir

# Dynamically calculate the version based on prymatex.VERSION.
vmodule = __import__('prymatex.version', fromlist=['prymatex'])
version = vmodule.get_version()
if u'GIT' in version:
    version = ' '.join(version.split(' ')[:-1])

setup(
    name = 'prymatex',
    version = version,
    license = 'GPL-3',
    author = vmodule.AUTHOR,
    author_email = vmodule.AUTHOR_EMAIL,
    description = vmodule.DESCRIPTION,
    long_description = vmodule.LONG_DESCRIPTION,
    url = vmodule.URL,

    packages = ["prymatex"],
    package_data = {"prymatex": ["resources/*", "share/*"]},
    scripts = ["prymatex/bin/pmx"],

    cmdclass = {
        'install': CustomInstall,
        'build_ui': QtBuild 
    }
)
