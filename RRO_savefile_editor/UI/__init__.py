__all__ = [
    "selectSaveFile",
    "mainMenu",
    "playerMenu",
    "getKey",
]

try:
    from ui import selectSaveFile, mainMenu, playerMenu
except ModuleNotFoundError:
    from .ui import selectSaveFile, mainMenu, playerMenu

try:
    from uiutils import getKey
except ModuleNotFoundError:
    from .uiutils import getKey
