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
# For further info, check http://www.prymatex.org/

"""Build tar.gz for prymatex.

Needed packages to run (using Debian/Ubuntu package names):
"""

import os

from distutils.command.install import install
from distutils.command.build import build
from distutils.command.install_data import install_data
from distutils.core import setup


class CustomInstall(install):
    """Custom installation class on package files.
    It copies all the files into the "PREFIX/share/PROJECTNAME" dir.
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
        data_dir = os.path.join(self.prefix, "share", self.distribution.get_name())

        # if we have 'root', put the building path also under it (used normally by pbuilder)
        if self.root is None:
            build_dir = data_dir
        else:
            build_dir = os.path.join(self.root, data_dir[1:])

        # change the lib install directory so all package files go inside here
        self.install_lib = build_dir

        # save this custom data dir to later change the scripts
        self._custom_data_dir = data_dir

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't have an easy way to do this.
packages, package_data = [], {}
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
prymatex_dir = 'prymatex'

for dirpath, dirnames, filenames in os.walk(prymatex_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        package = '.'.join(fullsplit(dirpath))
        packages.append(package)
        package_data.setdefault(package, [])
    elif filenames:
        #Find package
        parts = fullsplit(dirpath)
        while '.'.join(parts) not in packages:
            parts = parts[:-1]
        #Build patterns
        patterns = []
        for file in filenames:
            name, ext = os.path.splitext(file)
            pattern = '*%s' % ext
            if not ext:
                patterns.append(name)
            elif pattern not in patterns:
                patterns.append(pattern)
        #Build basename
        basename = os.path.join(*fullsplit(dirpath)[1:])
        package_data['.'.join(parts)].extend([os.path.join(basename, p) for p in patterns])

import prymatex

setup(
    name = prymatex.__name__,
    version = str(prymatex.__version__.replace(' ', '-')),
    license = prymatex.__license__,
    author = prymatex.__author__,
    author_email = prymatex.__mail__,
    description = prymatex.__doc__,
    url = prymatex.__url__,

    packages = packages,
    package_data = package_data,
    scripts = ["prymatex/bin/pmx.py"],

    cmdclass = {
        'install': CustomInstall
    }
)
