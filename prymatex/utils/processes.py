import sys
from subprocess import check_output
import six
from prymatex.core.exceptions import UnsupportedPlatformError


LINUX_PS_COMMAND = 'ps -eo pid,cmd'.split()


def get_process_map():
    platform = sys.platform
    if 'linux' in platform:
        output = six.text_type(check_output(LINUX_PS_COMMAND))
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
