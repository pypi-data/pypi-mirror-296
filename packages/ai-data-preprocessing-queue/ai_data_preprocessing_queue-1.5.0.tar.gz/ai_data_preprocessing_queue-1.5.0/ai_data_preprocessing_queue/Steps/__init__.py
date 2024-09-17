from glob import glob
from os.path import basename, dirname, isfile

# Loads all modules that are inside this directory
modules = glob(f"{dirname(__file__)}/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")]
