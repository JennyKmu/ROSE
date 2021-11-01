__all__ = [
    "selectSaveFile",
    "mainMenu",
    "playerMenu",
    "rstockMenu",
    "getKey",
]

try:
    from ui import selectSaveFile, mainMenu, playerMenu, rstockMenu
except ModuleNotFoundError:
    from .ui import selectSaveFile, mainMenu, playerMenu, rstockMenu

try:
    from uiutils import getKey
except ModuleNotFoundError:
    from .uiutils import getKey
