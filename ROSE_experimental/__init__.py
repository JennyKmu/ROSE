__all__ = [
    "main",
]

try:
    from main import main
except ModuleNotFoundError:
    from .main import main

main()
