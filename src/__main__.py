import os
import sys

if __package__ is None and not hasattr(sys, 'frozen'):
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    root_path = os.path.dirname(os.path.dirname(path))
    sys.path.append(root_path)

from src.App import App

if __name__ == "__main__":
    App(dict(os.environ)).run()
