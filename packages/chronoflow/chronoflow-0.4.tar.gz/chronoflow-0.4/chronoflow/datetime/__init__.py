from .main import hello, ltz_here
import importlib

def imports():
    print("This will run when we import this")

    # Check if tzlocal is already installed
    try:
        importlib.import_module('tzlocal')
    except ImportError:
        raise ImportError(
            "The 'tzlocal' package is not installed. Please install it by running 'pip install tzlocal'."
        )

    # Import tzlocal and make sure to import `get_localzone`
    global get_localzone
    from tzlocal import get_localzone

imports()
