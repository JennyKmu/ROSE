# RRO_savefile_editor_v0.3.4

This program is intended to be used as an external tool to Railroads Online server hosts. It will read save files, allow to modify entries within it, and then save the file (creating a backup file in the process).

## Requirements

* Having a working Python 3 install. Development was made using Python 3.8, so the program will warn you if you try using an older version, but allow you to continue if it's a Python 3 version.
* Having necessary python modules installed:
  * numpy (see https://pypi.org/project/numpy/ )

Setting up pip so that you can easily install python modules is recommended. More requirements will be added in the future.

## Installation and Use

1. Save your game.
2. Download the last .pyz file from the **release** list (https://github.com/JennyKmu/RRO_savefile_editor/releases) and place it inside your save folder (should be located somewhere around ``C:\Users\Username\AppData\Local\arr\Saved\SaveGames`` ). **No need to decompress the file**, if your python install was properly made, windows will correctly detect it as a python program.
3. Even though the program will create backups of your saves, **it is still recommended to create your own backups.**
4. Double-click on the .pyz file, and follow instructions. At any point, you can exit the program by pressing ``Ctrl+D`` (or less cleanly by pressing ``Ctrl+C``)
5. Likewise, you can always go back to previous menu by pressing ``Escape`` (escaping from the savefile selection menu will exit the program).
5. Exit the current session in-game or start the game, and load the file you edited.

## Functionalities

Currently, functionnalities are limited to:
* Editing xp value for each player;
* Editing money value for each player;
* Editing rolling stock names and numbers;
  * Editing is limited to what can be displayed on each rolling stock. Override by starting with \i when entering a new value.
* Rolling stock clean-up (**EXPERIMENTAL**):
  * Attempts to detect rolling stock which fell through the map, and moves them high up in the air, for you to recover them and rerail them. Watch out for your head!

## In the work

* Editing rolling stock contents
* Plotting a map of the network
* Exporting SVG files of the network
* Editing industries contents
* Editing water, sand and firewood places contents
* Teleportation of rolling stock and players, as well as rerailing
* Deletion of rolling stock, tracks, or players
* A "No cheat" mode, which will allow to take loans, sell unused rolling stock (at a lower price), order refills for water, sand or firewood...
* Improvements of the UI
* GUI

## Q&A

* **The program starts, but doesn't find any savefile**
  * Check that the program is placed in the right folder, next to your saves
  * If it is, then it's most likely an issue with your python installation. Reinstall it from the official https://www.python.org/downloads/. Also check you're using a version 3.x. **Installation from Windows Store will not work !**
* **The program starts, but tells me a module is not found**
  * Install the python module that was not found using pip.
* The UI is not yet functionnal with Unix sytems, and hasn't been tested with Mac (probably not working either).
* If you can't find a solution to your issue, the preferred way is to open an new issue on GitHub, and if necessary join your savefile there: https://github.com/JennyKmu/RRO_savefile_editor/issues
