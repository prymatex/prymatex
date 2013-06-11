#!/usr/bin/env python

import os, sys
sys.path.append(os.path.abspath('..'))

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, package_data = [], {}
os.chdir("..")
prymatex_dir = 'prymatex'

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

if __name__ == "__main__":
    print(packages, package_data)