#!/usr/bin/env python3

# built-in imports
import sys, glob, os, shutil

def inner_main():
    # Check if python3
    if not sys.version_info > (3,8):
        print("------------------")
        print("> \033[1;31mERROR: Python version not officialy supported.\033[0m")
        print("> Please use/install Python version 3.8 or above.")
        if sys.version_info > (3,):
            print("> You can input 'continue' if you're sure your python install meets requirements.")
            c = input("> ")
            if not c == "continue":
                print("------------------")
                sys.exit()
            else:
                print("------------------")
        else:
            print("------------------")
            sys.exit()

    # To enable ANSI control sequences on Windows
    os.system('color')
    # if os.name == 'nt':
    #     from ctypes import windll
    #     k = windll.kernel32
    #     k.SetConsoleMode(k.GetStdHandle(-11), 7)

    # import colorama
    # colorama.init()


    # Contributors list:

    contributors = [
        "Jenny",
        "Leif_The_Head",
    ]

    version = (0,3,5)
    dev_version = False

    def header():
        print("="*72)
        print("| {:^68s} |".format("~~~ RAILROADS Online savefile editor ~~~"))
        if not dev_version:
            print("| {:^68s} |".format("v{}.{}.{}".format(*version)))
        else:
            print("| {:^68s} |".format("v{}.{}.{} - UNDER DEV".format(*version)))
        print("| {:^68s} |".format("Created by Jenny."))
        print("| {:^68s} |".format(""))
        print("| {:^68s} |".format("See repo on GitHub for sources and documentation:"))
        print("| {:^68s} |".format("https://github.com/JennyKmu/RRO_savefile_editor"))
        print("| {:^68s} |".format(""))
        print("| {:<68s} |".format("Contributors :"))
        for contributor in contributors:
            print("| * {:<66s} |".format(contributor))
        print("="*72)
        print()
        print("--- How to use ---")
        print("> \033[1mBACK-UP YOUR SAVEFILES\033[0m before using this program, even though it should create a backup!")
        print("> Have a working Python installation (the program should work with any Python 3 version)")
        print("> Install required python modules (numpy)")
        print("> Have the program inside the folder containing saved games")
        print("  (Should be located in C:\\Users\\Username\\AppData\\Local\\arr\\Saved\\SaveGames)")
        print("> \033[1mBACK-UP YOUR SAVEFILES\033[0m before using this program !")
        print("> At any point during execution you can stop execution by pressing Ctrl-D (or Ctrl-C)")
        print("> Likewise, you can always go back to previous menu by pressing Escape.")
        print("> And finally, \033[1mBACK-UP YOUR SAVEFILES\033[0m before using this program!")
        print("------------------")

    header()

    # Checking requirements (pip modules)
    try:
        import numpy
    except ImportError:
        print("!> \033[1;31mERROR: Impossible to import numpy module.\033[0m")
        print("!> Please install numpy to use this program.")
        print("!> Press Enter to exit.")
        print("------------------")
        input()
        sys.exit()

    # Importing inner modules
    try:
        from GVAS.GVAS import GVAS
    except ModuleNotFoundError:
        from .GVAS import GVAS

    try:
        from UI import playerMenu, mainMenu, mainStockMenu, selectSaveFile, getKey
    except ModuleNotFoundError:
        from .UI import playerMenu, mainMenu, mainStockMenu, selectSaveFile, getKey

    def loop(loc = "."):
        from pathlib import Path
        if __name__ == "__main__":
            loc = ".."
        filename = selectSaveFile(loc)
        if filename is None:
            print("No save file detected ! Please check program location.")
            print("Press any key to exit.")
            print("------------------")
            getKey()
            sys.exit()
        if filename == -1:
            print("No save file selected.")
            print("Press any key to exit.")
            print("------------------")
            getKey()
            sys.exit()
        filepath = Path(filename)

        gvas = GVAS(filepath)
        print("Currently loaded file is '\033[1m{}\033[0m'".format(filename))
        print("------------------")

        mainMenu(gvas)

    try:
        loop()
    except Exception as e:
        print(e)
        print("Please send the above error to the dev team. Press any key to leave.")
        getKey()

def main():
    try:
        inner_main()
    except ImportError as e:
        print(e)
        print("Please install missing python packages. Press Enter to leave.")
        input()
    except Exception as e:
        print(e)
        print("Please send the above error(s) to the dev team. Press Enter to leave.")
        input()

if __name__=="__main__":
        main()
