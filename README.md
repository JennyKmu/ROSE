# RROSE - v0.3.7

This program is intended to be used as an external tool to Railroads Online server hosts. It will read save files, allow to modify entries within it, and then save the file (creating a backup file in the process).

There are two ways to use the program. You can either:
* Have a python installation, with required modules, and use the released .pyz files.
  * Advantages: you only have to download the .pyz file to update the program, which is quite light, and you'll be able to use other python programs from other sources.
  * Disadvantages: you need to properly setup your python environment the first time, though once it's done it will be straightforward to add the newly required modules with each update.
* Use the standalone .exe files.
  * Advantages: only one file to download and execute, theoretically no need to install python or anything else.
  * Disadvantages: the executable is heavier, you'll have to fully download it with each update, it can only run on Windows, and might not run at all depending on your configuration. **Windows defender will flag the .exe as containing a virus, while it is not the case**. You can reassure yourself by checking the SHA256 hash of the file you downloaded (see below).

Below is the detailed guide for using the .pyz files.

Using the .exe is straightforward: download the .exe file, place it in the same folder as your saves, and execute it.

## Checksums

With each release will be included the SHA-256 hash of the .pyz and .exe files. This made to check that the files haven't been tempered with since they were prepared for release (meaning that no one modified them). To check that the hash is correct, open a command prompt (powershell) at the location of the downloaded file, and type: ``Get-FileHash  <filename> -Algorithm SHA256 | Format-List``. Compare the result to the hash given with the release notice.

## Requirements

* Having a working Python 3 install. Development was made using Python 3.8, so the program will warn you if you try using an older version, but allow you to continue if it's a Python 3 version.
* Having necessary python modules installed:
  * numpy (see https://pypi.org/project/numpy/ )

Setting up pip so that you can easily install python modules is recommended. More requirements will be added in the future.

## Installation and Use -- Python

1. Save your game.
2. Download the latest .pyz file from the **release** list (https://github.com/JennyKmu/RRO_savefile_editor/releases) and place it inside your save folder (should be located somewhere around ``C:\Users\Username\AppData\Local\arr\Saved\SaveGames`` ). **No need to decompress the file**, if your python install was properly made, windows will correctly detect it as a python program.
3. Even though the program will create backups of your saves, **it is still recommended to create your own backups.**
4. Double-click on the .pyz file, and follow instructions. At any point, you can exit the program by pressing ``Ctrl+D`` (or less cleanly by pressing ``Ctrl+C``)
5. Likewise, you can always go back to previous menu by pressing ``Escape`` (escaping from the savefile selection menu will exit the program).
6. Exit the current session in-game or start the game, and load the file you edited.

## Installation and Use -- Standalone Executable

1. Save your game.
2. Download the latest .exe file from the **release** list (https://github.com/JennyKmu/RRO_savefile_editor/releases) and place it inside your save folder (should be located somewhere around ``C:\Users\Username\AppData\Local\arr\Saved\SaveGames`` ).
3. Even though the program will create backups of your saves, **it is still recommended to create your own backups.**
4. Double-click on the .exe file, and follow instructions. At any point, you can exit the program by pressing ``Ctrl+D`` (or less cleanly by pressing ``Ctrl+C``)
5. Likewise, you can always go back to previous menu by pressing ``Escape`` (escaping from the savefile selection menu will exit the program).
6. Exit the current session in-game or start the game, and load the file you edited.

## Functionalities

Currently, functionnalities are limited to:
* Editing xp value for each player;
* Editing money value for each player;
* Editing rolling stock names and numbers;
  * Editing is limited to what can be displayed on each rolling stock. Override by starting with  `\i` when entering a new value.
* Editing cargo on wagons:
  * Changing cargo type (within allowed types and empty)
    * Upon switching to 'Empty', the wagon is emptied. If switching to any cargo, the wagon is filled.
  * Changing cargo amount
* Editing Engine and Tender contents:
  * Refill firewood, water, sand.
* Editing Utility contents:
  * Can refill water towers
  * Can refill sand towers
  * Can refill firewood depots
* Rolling stock respawn :
  * Allows to respawn rolling stock at one of the six spawn points. The rolling stock should be re-railed when respawning at one of the spawn points.
  * If all the points are occupied, an option is available to teleport rolling stock close to the spawn points (behind the deck at the end of the tracks).
  * Detects most cars that fell through the ground and indicates them in the menu.
* Reset trees (**EXPERIMENTAL**) back to the state they are in when starting a new game.

## In the work

* Plotting a map of the network
* Build new tracks
* Better tree reset feature (avoid existing tracks)
* Exporting SVG files of the network
* Editing industries contents
* Teleportation of players
* Better teleportation of rolling stock, as well as rerailing
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
* **Windows tell me there's a virus in the released .exe file**
  * There's no virus.
  * You can check the SHA256 hash to check that the file you downloaded isn't corrupted.
  * Making it so Windows doesn't see a virus in the file would be too much of a hassle at this stage of development.
  * If you really don't want to use the .exe file because of that, you can always use the .pyz version which won't trigger Windows.
* The UI is not yet functional with Unix systems, and hasn't been tested with Mac (probably not working either).
* If you can't find a solution to your issue, the preferred way is to open an new issue on GitHub (if necessary joining your savefile) there: https://github.com/JennyKmu/RRO_savefile_editor/issues

## Setting up the environment

* First go to the official https://www.python.org/downloads/, download Python 3 (latest release recommended), and install it. When asked so, **add pip to Path**.
* Open a command prompt (cmd or powershell) as administrator, and type in either:
  * ``pip install numpy``
  * ``python -m pip install numpy``

If you already had installed Python, but the pip command doesn't work, then you'll need to add pip to Path yourself (you probably didn't check the option to do so when installing Python originally). To do so:
* In the Windows search bar, look for "Environment Variables", and open the tool that shows up.
* In that tool, click "Environment Variables"
* Select the "Path" variable, and click "Modify"
* **Do not delete anything there**. Add a new line, in which you will put the Path/To/Python/Install/Scripts (Usually C:\\Users\\Username\\AppData\\Local\\Programs\\Python\\Python38-32\\Scripts)
* Apply your changes and exit the tool. Now pip should work well, go back to first step.
