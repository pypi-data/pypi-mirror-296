def _add_dll_directory():
    import os
    import sys

    if sys.platform.startswith('win'):
        # Get the directory of this __init__.py file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        if os.path.exists(current_dir):
            # Add the current directory to the DLL search path
            os.add_dll_directory(current_dir)
        else:
            print(f"Warning: {current_dir} does not exist.")


# Call this function when the package is imported
_add_dll_directory()

# Import all the functions from your C++ extension module
from pyix import *
