import os
import sys

from src.Environment import Environment
from src.External import External
from src.builtin import *

if __package__ is None and not hasattr(sys, "frozen"):
    import os.path

    path = os.path.realpath(os.path.abspath(__file__))
    root_path = os.path.dirname(os.path.dirname(path))
    sys.path.append(root_path)

from src.App import App

if __name__ == "__main__":
    executables = {
        "echo": Echo(),
        "exit": Exit(),
        "pwd": Pwd(),
        "cat": Cat(),
        "wc": Wc(),
        "cd": Cd(),
        "ls": Ls(),
        "ebash": External(sys.executable, Environment.path_to("__main__.py"))
    }

    app = App(dict(os.environ), executables)
    if len(sys.argv) > 1:
        app.execute_args(sys.argv[1:])
    else:
        app.run()
