# tnsa_standard/import_all.py

import pkgutil
import importlib
import sys

# Get the current package
package = sys.modules[__name__]

# Iterate through the modules in the package
for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    module = importlib.import_module(f'.{module_name}', package=__package__)
    # Import all classes and functions from the module
    for name in dir(module):
        if not name.startswith('_'):
            setattr(package, name, getattr(module, name))
