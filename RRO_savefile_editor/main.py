#!/usr/bin/env python3

# built-in imports
import sys, glob, os, shutil
try:
    from GVAS import *
except ModuleNotFoundError:
    from .GVAS import *

try:
    from UI import *
except ModuleNotFoundError:
    from .UI import *

def main():
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
                exit()
            else:
                print("------------------")
        else:
            print("------------------")
            exit()


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
    ]

    version = (0,3,2)

    def header():
        print("="*72)
        print("| {:^68s} |".format("~~~ RAILROADS Online savefile editor ~~~"))
        print("| {:^68s} |".format("v{}.{}.{}".format(*version)))
        print("| {:^68s} |".format("Created by Jenny."))
        print("| {:^68s} |".format(""))
        print("| {:<68s} |".format("Feel free to use or modify the script."))
        print("| {:<68s} |".format("Just add your name to the list of contributors and change version."))
        print("| {:^68s} |".format(""))
        print("| {:<68s} |".format("Contributors :"))
        for contributor in contributors:
            print("| * {:<66s} |".format(contributor))
        print("="*72)
        print()
        print("--- How to use ---")
        print("> \033[1mBACK-UP YOUR SAVEFILES\033[0m before using this program, even though it should create backups !")
        print("> Have a working Python installation (the program should work with any Python 3 version)")
        print("> Install required python modules (numpy)")
        print("> Have the script file inside the folder containing saved games")
        print("  (Should be located in C:\\Users\\Username\\AppData\\Local\\arr\\Saved\\SaveGames)")
        print("> \033[1mBACK-UP YOUR SAVEFILES\033[0m before using this program !")
        print("> At any point during execution you can stop execution by pressing Ctrl-D.")
        print("> And finally, \033[1mBACK-UP YOUR SAVEFILES\033[0m before using this program !")
        print("------------------")

    header()

    # Checking requirements (pip modules)
    try:
        import numpy
    except ImportError:
        print("> \033[1;31mERROR: Impossible to import numpy module.\033[0m")
        print("> Please install numpy to use this program.")
        print("------------------")
        exit()




    # Importing custom modules
    # try:
    #     from GVAS.GVAS import GVAS
    # except ModuleNotFoundError:
    #     from .GVAS.GVAS import GVAS
    # try:
    #     from UI import getKey
    # except ModuleNotFoundError:
    #     from .UI import getKey
    # try:
    #     from UI import selectSaveFile, mainMenu, playerMenu
    # except ModuleNotFoundError:
    #     from .UI import selectSaveFile, mainMenu, playerMenu


    def loop(loc = "."):
        if __name__ == "__main__":
            loc = ".."
        from pathlib import Path
        filename = selectSaveFile(loc)
        if filename is None:
            print("No save file detected ! Please check program location.")
            print("Press any key to exit.")
            print("------------------")
            getKey()
            exit()
        if filename == -1:
            print("No save file selected.")
            print("Press any key to exit.")
            print("------------------")
            getKey()
            exit()
        filepath = Path(filename)

        gvas = GVAS.GVAS(filename)
        print("Currently loaded file is '\033[1m{}\033[0m'".format(filename))
        print("------------------")
        while True:
            choice = mainMenu()
            if choice == "Players":
                playerMenu(gvas)
            elif choice == "Rolling stock":
                rstockMenu(gvas)
            elif choice == "Save & Exit":
                fbackup = Path("./backups") / Path("backup_"+filepath.name)
                print("> Saving backup file as {}".format(fbackup))
                if not os.path.exists('backups'):
                    os.makedirs('backups')
                shutil.copy(filename, fbackup)

                print("> Overwriting file {}".format(filename))
                # gvas.write("dev_"+filepath.name)
                gvas.write(filename)
                print("Press any key to exit.")
                print("------------------")
                getKey()
                exit()
            elif choice == "Exit":
                exit()
                pass

    try:
        loop()
    except Exception as e:
        print(e)
        print("Please send the above error to the dev team. Press any key to leave.")
        getKey()




if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(e)
        print("Please send the above error to the dev team. Press any key to leave.")
        getKey()
