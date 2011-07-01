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
from distutils.core import setup

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
    }
)
