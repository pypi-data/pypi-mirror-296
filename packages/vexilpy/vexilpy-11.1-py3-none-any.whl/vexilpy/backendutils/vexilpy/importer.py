from importlib import import_module
from typing import Any

from ..safety.handler import handle

@handle
def stock_import(sector: str, name: str, material: str) -> Any:
    root: Any = import_module(f"..stock.{sector}.{name}", __package__)

    return getattr(root, material)

@handle
def batch_import(sector: str, name: str, material: str) -> Any:
    root: Any = import_module(f"..stock.{sector}.{name}", __package__)

    return root