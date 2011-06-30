VERSION = (0, 9, 6, 'alpha', 0)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    from prymatex.utils.version import get_git_revision
    svn_rev = get_git_revision()
    if svn_rev != u'GIT-unknown':
        version = "%s %s" % (version, svn_rev)
    return version
