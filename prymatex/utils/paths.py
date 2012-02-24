import re, os
from functools import partial

shell_var = re.compile('(\$[\w\d]+)')

def callback(match, context = None, sensitive = True, default = ''):
    key = match.group().replace('$', '')
    if callable(context):
        context = context()
    if not sensitive:
        return context.get(key.lower(), context.get(key.upper(), default))
    else:
        return context.get(key, default)

environ_repl_callback = partial(callback, sensitive = False, context = os.environ)

#===============================================================================
# Expand $exp taking os.environ as context
#===============================================================================
expand_shell_var = lambda path: shell_var.sub(path, environ_repl_callback)


if __name__ == "__main__":
    print expand_shell_var('$home/alfa')