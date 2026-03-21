"""Project package compatibility helpers.

The repository uses a nested ``Letti_dreads_Backend`` package layout. Django's
test discovery may try to import apps as ``Letti_dreads_Backend.cart`` even
though the app packages live one level higher. Re-export them here so discovery
works without changing the existing app/module structure.
"""

from importlib import import_module
import sys


for _app in ("cart", "products", "users"):
    sys.modules.setdefault(f"{__name__}.{_app}", import_module(_app))
