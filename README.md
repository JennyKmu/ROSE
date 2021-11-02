# RRO_savefile_editor_v0.3.3

This program is intended to be used as an external tool to Railroads Online server hosts. It will read save files, allow to modify entries within it, and then save the file (creating a backup file in the process).

## Requirements

* Having a working Python 3 install. Development was made using Python 3.8, so the program will warn you if you try using an older version, but allow you to continue if it's a Python 3 version.
* Having necessary python modules installed:
  * numpy (see https://pypi.org/project/numpy/ )

Setting up pip so that you can easily install python modules is recommended. More requirements will be added in the future.

## Installation and Use

1. Save your game.
2. Dowload the last .pyz file and place it inside your save folder (should be located somewhere around ``C:\Users\Username\AppData\Local\arr\Saved\SaveGames`` )
3. Even though the program will create backups of your saves, **it is still recommended to create your own backups.**
4. Double-click on the file, and follow instructions. At any point, you can exit the program by pressing ``Ctrl+D``.
5. Exit the current session in-game or start the game, and load the file you edited.

## Functionalities

Currently, functionnalities are limited to:
* Editing xp value for each player;
* Editing money value for each player;
* Editing rolling stock names and numbers

## In the work

* Editing rolling stock contents
* Plotting a map of the network
* Exporting SVG files of the network
* Editing industries contents
* Editing water, sand and firewood places contents
* Teleportation of rolling stock and players
* Deletion of rolling stock, tracks, or players
* A "No cheat" mode, which will allow to take loans, sell unused rolling stock (at a lower price), order refills for water, sand or firewood...
* Improvements of the UI
* GUI

## Q&A

* **The program starts, but doesn't find any savefile**
  * Check that the program is placed in the right folder, next to your saves
  * If it is, then it's most likely an issue with your python installation. Reinstall it from the official https://www.python.org/downloads/. Also check you're using a version 3.x. **Installation from Windows Store will not work !**
* **The program starts, but tells me a module is not found**
  * Install the python module that was not found.
* The UI is not yet functionnal with Unix sytems, and hasn't been tested with Mac (probably not working either).
