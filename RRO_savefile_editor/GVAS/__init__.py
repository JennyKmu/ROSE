__all__ = [
    "GVAS",
]

try:
    from GVAS import GVAS
except ModuleNotFoundError:
    from .GVAS import GVAS
