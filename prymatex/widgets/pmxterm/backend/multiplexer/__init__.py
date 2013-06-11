import sys

if sys.platform.startswith("linux"):
    from .linux import Multiplexer
elif sys.platform == "win32":
    from .windows import Multiplexer