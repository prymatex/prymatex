import os
import sys
import subprocess
from prymatex.utils import six
from prymatex.core.exceptions import UnsupportedPlatformError


LINUX_PS_COMMAND = six.text_type('ps -eo pid,cmd')


def check_output_safe(*popenargs, **kwargs):
    '''Wrapper for bug http://bugs.python.org/issue6135'''
    if sys.version_info.major < 3:
        my_env = os.environ
        my_env['PYTHONIOENCODING'] = 'utf-8'
        kwargs.update(env=my_env)
        return subprocess.check_output(*popenargs, **kwargs).decode('utf-8', 'ignore')
    return subprocess.check_output(*popenargs, **kwargs)


def get_process_map():
    platform = sys.platform
    if 'linux' in platform:
        output = six.text_type(check_output_safe(LINUX_PS_COMMAND.split()))
        # Remove first line since it has the titles
        # and the last one which holds a null string
        lines = output.split('\\n')[1:-1]
        lines = map(lambda x: x.strip(), lines)
        processes = {}
        for line in lines:
            pid, cmd = line.split(' ', 1)  # Do not need regex since we used -o pid,cmd
            processes[int(pid)] = cmd
        return processes
    else:
        raise UnsupportedPlatformError("{} does not implement get_process_map".format(
            platform
        ))
