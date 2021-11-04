﻿# RRO_savefile_editor_v0.3.4

This program is intended to be used as an external tool to Railroads Online server hosts. It will read save files, allow to modify entries within it, and then save the file (creating a backup file in the process).

There are two ways to use the program. You can either:
* Have a python installation, with required modules, and use the released .pyz files.
  * Advantages: you only have to download the .pyz file to update the program, which is quite light, and you'll be able to use other python programs from other sources.
  * Disadvantages: you need to properly setup your python environment the first time, though once it's done it will be straightforward to add the newly required modules with each update.
* Use the standalone .exe files.
  * Advantages: only one file to download and execute, theoretically no need to install python or anything else.
  * Disadvantages: the executable is heavier, you'll have to fully download it with each update, it can only run on Windows, and might not run at all depending on your configuration.

Below is the detailed guide for using the .pyz files.

Using the .exe is straightforward: download the .exe file, place it in the same folder as your saves, and execute it.

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
* Reset trees (**EXPERIMENTAL**) back to the state they are in when starting a new game.

## In the work

* Editing rolling stock contents
* Plotting a map of the network
* Build new tracks
* Better tree reset feature (avoid existing tracks)
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
  * Install the python module that was not found using pip. Check below for detailed instruction.
* The UI is not yet functionnal with Unix sytems, and hasn't been tested with Mac (probably not working either).
* If you can't find a solution to your issue, the preferred way is to open an new issue on GitHub, and if necessary join your savefile there: https://github.com/JennyKmu/RRO_savefile_editor/issues

## Setting up the environment

* First go to the official https://www.python.org/downloads/, download Python 3 (latest release recommended), and install it. When asked so, **add pip to Path**.
* Open a command prompt (cmd or powershell) as administrator, and type in:
  * ``pip install numpy``

If you already had installed Python, but the pip command doesn't work, then you'll need to add pip to Path yourself (you probably didn't check the option originally). To do so:
* In the Windows search bar, look for "Environment Variables", and open the tool that shows up.
* In that tool, click "Environment Variables"
* Select the "Path" variable, and click "Modify"
* **Do not delete anything there**. Add a new line, in which you will put the Path/To/Python/Install/Scripts (Usually C:\\Users\\Username\\AppData\\Local\\Programs\\Python\\Python38-32\\Scripts)
* Apply your changes and exit the tool. Now pip should work well.
