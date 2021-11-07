import glob
import os
import shutil
import sys
from pathlib import Path
from .rollingStock import *
from .trackData import *

try:
    from uiutils import getKey
except:
    from .uiutils import getKey

selectfmt = "\033[1;32;42m"


def selectSaveFile(loc):
    filelist = glob.glob(loc + '/' + "slot*.sav")
    current = 0
    if len(filelist) == 0:
        return None
    while True:
        print("Select a file to read (press ENTER to confirm):")
        for i, f in enumerate(filelist):
            if i == current:
                print(" - " + selectfmt + "{}\033[0m".format(f))
            else:
                print(" - {}".format(f))
        k = getKey()
        if k == b'KEY_UP':
            current = max(0, current - 1)
        if k == b'KEY_DOWN':
            current = min(len(filelist) - 1, current + 1)
        print("\033[{}A\033[J".format(len(filelist) + 1), end='')
        if k == b'RETURN':
            return filelist[current]
        if k == b'ESCAPE':
            return -1


def mainMenu(gvas, dev_version = False):
    options = [
        ("Players", playerMenu),
        ("Rolling stock", mainStockMenu),
        ("Environment", mainEnvMenu),
        ("Save & Exit", saveAndExit),
        ("Exit", noSaveAndExit)
    ]
    if dev_version:
        from .uidev import devslotA, devslotB, devslotC, devslotD, devslotE
        dev_options = [
            ("DEV A", devslotA),
            ("DEV B", devslotB),
            ("DEV C", devslotC),
            ("DEV D", devslotD),
            ("DEV E", devslotE)
        ]
        options = dev_options + options
    current = 0
    while True:
        print("Select the submenu (press ENTER to confirm):")
        for i, f in enumerate(options):
            if i == current:
                print(" - " + selectfmt + "{}\033[0m".format(f[0]))
            else:
                print(" - {}".format(f[0]))
        k = getKey()
        if k == b'KEY_UP':
            current = max(0, current - 1)
        if k == b'KEY_DOWN':
            current = min(len(options) - 1, current + 1)
        print("\033[{}A\033[J".format(len(options) + 1), end='')
        if k == b'RETURN':
            options[current][1](gvas)
        if k == b'ESCAPE':
            print("You're about to exit the program without saving potential changes.")
            print("Press Enter to confirm you want to exit, or any other key to go back.")
            k = getKey()
            print("\033[{}A\033[J".format(2), end='')
            if k == b'RETURN':
                noSaveAndExit(gvas)


def saveAndExit(gvas):
    fbackup = Path("./backups") / Path("backup_" + gvas._sourcefilename.name)
    print("> Saving backup file as {}".format(fbackup))
    if not os.path.exists('backups'):
        os.makedirs('backups')
    shutil.copy(gvas._sourcefilename, fbackup)

    print("> Overwriting file {}".format(gvas._sourcefilename))
    # gvas.write("dev_"+filepath.name)
    gvas.write(gvas._sourcefilename)
    print("Press any key to close.")
    print("------------------")
    getKey()
    sys.exit()


def noSaveAndExit(gvas):
    # gvas arg for compatibility with other ui functions
    print("Press any key to close.")
    print("------------------")
    getKey()
    sys.exit()


def mainEnvMenu(gvas):
    options = [
        ("Reset trees to new game state (EXPERIMENTAL)", resetTreesToNewGame),
    ]
    current = 0
    while True:
        print("Select the feature you want to run (press ENTER to confirm):")
        for i, f in enumerate(options):
            if i == current:
                print(" - " + selectfmt + "{}\033[0m".format(f[0]))
            else:
                print(" - {}".format(f[0]))
        k = getKey()
        if k == b'KEY_UP':
            current = max(0, current - 1)
        if k == b'KEY_DOWN':
            current = min(len(options) - 1, current + 1)
        print("\033[{}A\033[J".format(len(options) + 1), end='')
        if k == b'RETURN':
            options[current][1](gvas)
        if k == b'ESCAPE':
            return None


def resetTreesToNewGame(gvas):
    import numpy as np
    from .defaultRemovedTrees import default_removed_trees
    print("This is an \033[1;31mEXPERIMENTAL\033[0m feature. Use at your own risks.")
    print("Risks include in particular:")
    print(" * Trees in the middle of the track (obviously)")
    print(" * Rolling stock being yeeted through the air at hypersonic speeds...")
    print(" * Or worse, through the ground. But for that there's another experimental feature.")

    removedTreesProp = gvas.data.find("RemovedVegetationAssetsArray")

    cursor = 0
    choices = ["Cancel", "Proceed at your own risks"]
    while True:
        if cursor == 0:
            print(" " * 5 + selectfmt + "{:^29s}".format(choices[0]) + "\033[0m"
                  + " " * 5 + "{:^29s}".format(choices[1]))
        else:
            print(" " * 5 + "{:^29s}".format(choices[0])
                  + " " * 5 + selectfmt + "{:^29s}".format(choices[1]) + "\033[0m")
        k = getKey()

        if k == b'KEY_RIGHT':
            cursor = min(1, cursor + 1)
        if k == b'KEY_LEFT':
            cursor = max(0, cursor - 1)

        if k == b'RETURN':
            if cursor == 0:
                k = b'ESCAPE'
            elif cursor == 1:
                removedTreesProp._data = np.asarray(default_removed_trees)
                print(f"The trees have been reset.")
                print("(Press any key to go back to previous menu)")
                getKey()
                print("\033[{}A\033[J".format(8), end='')
                return None

        if k == b'ESCAPE':
            print("\033[{}A\033[J".format(6), end='')
            return None

        print("\033[{}A\033[J".format(1), end='')

def playerMenu(gvas):
    player_names_prop = gvas.data.find("PlayerNameArray")
    player_money_prop = gvas.data.find("PlayerMoneyArray")
    player_xp_prop = gvas.data.find("PlayerXPArray")
    cur_col = 0
    cur_line = 0
    offset = 0
    ltot = len(player_names_prop.data)
    if len(player_names_prop.data) > 10:
        split_data = True
        n_page = int(ltot / 10) + 1 * (not ltot % 10 == 0)
    else:
        split_data = False
    while True:
        print("Select a field to edit (ESCAPE to quit, ENTER to valid selection)")
        cur_page = int(offset / 10)
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print("{:<65s} | {:>9s} | {:>9s}".format(
            "Player name",
            "XP",
            "Money"
        ))
        print("-" * (65 + 3 + 9 + 3 + 9))
        formatters = [
            "{:<64s}",
            "{:>9d}",
            "{:>9.0f}",
        ]
        n_line = 0
        for i in range(len(player_names_prop.data)):
            if i not in range(offset, offset + 10) and split_data:
                continue
            n_line += 1
            line_format = "{:<64s} "
            if i == cur_line:
                for j in range(2):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j + 1] + "\033[0m"
                    else:
                        line_format += formatters[j + 1]
            else:
                line_format += "".join([" | " + f for f in formatters[1:]])

            line = line_format.format(
                player_names_prop.data[i],
                player_xp_prop.data[i],
                player_money_prop.data[i]
            )
            print(line)
        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(1, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
            if cur_line < offset:
                k = b'PAGE_UP'
        if k == b'KEY_DOWN':
            cur_line = min(ltot - 1, cur_line + 1)
            if cur_line >= offset + 10:
                k = b'PAGE_DOWN'
        if k == b'PAGE_UP':
            offset = max(0, offset - 10)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset + 10 - 1
        if k == b'PAGE_DOWN':
            max_offset = ltot - ltot % 10
            offset = min(offset + 10, max_offset)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset
        if k == b'RETURN':
            prompt_text = "> Enter new value: "
            while True:
                n_rline = 0
                val = input(prompt_text)
                n_rline += 1
                try:
                    val = int(val)
                except ValueError:
                    print("\033{}A\033[J".format(n_rline), end='')
                    prompt_text = "> Invalid input! Enter new value: "
                    continue

                data = [player_xp_prop.data, player_money_prop.data]
                data[cur_col][cur_line] = val
                print("\033[{}A\033[J".format(n_rline), end='')
                break

        if len(player_names_prop.data) <= 10:
            print("\033[{}A\033[J".format(len(player_names_prop.data) + 3), end='')
        else:
            print("\033[{}A\033[J".format(n_line + 4), end='')

        if k == b'ESCAPE':
            return None


def renameStockMenu(gvas):
    framenumbers = gvas.data.find("FrameNumberArray").data
    framenames = gvas.data.find("FrameNameArray").data
    frametypes = gvas.data.find("FrameTypeArray").data
    # print(framenumbers)
    # print(framenames)
    # print(frametypes)
    cur_col = 0
    cur_line = 0
    formatters = [
        "{:<32s}",
        "{:<32s}",
        "{:<32s}",
    ]
    offset = 0
    ltot = len(frametypes)
    if ltot > 10:
        split_data = True
        n_page = int(ltot / 10) + 1 * (not ltot % 10 == 0)
    else:
        split_data = False
    while True:
        print("Select field to edit (ESCAPE to quit, ENTER to valid selection)")
        print("Use <br> to create multiple line values where applicable.")
        print("Sanity checks are enabled. To ignore limitation start your input with \i")
        cur_page = int(offset / 10)
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Rolling stock type",
            "Number",
            "Name"
        ))
        print("-" * (32 * 3 + 3 * 2))
        n_line = 0
        for i in range(len(frametypes)):
            if i not in range(offset, offset + 10) and split_data:
                continue
            n_line += 1
            if i == cur_line:
                line_format = formatters[0]
                for j in range(2):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j + 1] + "\033[0m"
                    else:
                        line_format += formatters[j + 1]
            else:
                line_format = " | ".join(formatters)

            num = framenumbers[i]
            nam = framenames[i]

            num = '-' if num is None else num
            nam = '-' if nam is None else nam

            # not necessary anymore (new line stored as <br>)
            # num = num if '<br>' not in num else num.replace('\n', '<br>')
            # nam = nam if '<br>' not in nam else nam.replace('\n', '<br>')

            print(line_format.format(
                frametypeTranslatorLong[frametypes[i]],
                num,
                nam,
            ))
        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(1, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
            if cur_line < offset:
                k = b'PAGE_UP'
        if k == b'KEY_DOWN':
            cur_line = min(ltot - 1, cur_line + 1)
            if cur_line >= offset + 10:
                k = b'PAGE_DOWN'
        if k == b'PAGE_UP':
            offset = max(0, offset - 10)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset + 10 - 1
        if k == b'PAGE_DOWN':
            max_offset = ltot - ltot % 10
            offset = min(offset + 10, max_offset)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset
        if k == b'RETURN':
            maximums = getnaminglimits(frametypes[cur_line], cur_col)
            if maximums[0] == 0 or maximums[1] == 0:
                prompt_text = "> This field isn't displayed at all. Enter to leave "
            else:
                prompt_text = "> Max Length {0}, max lines {1}; Enter new value: ".format(maximums[0], maximums[1])
            while True:
                n_rline = 0
                val = input(prompt_text)
                n_rline += 1
                try:
                    val = str(val)
                    # if val.count('<br>') > 1 :
                    # print("\033[{}A\033[J".format(n_rline), end='')
                    # prompt_text = "> Can't handle more than two lines for now! Enter new value: "
                    # continue
                    val = namingsanitycheck(frametypes[cur_line], cur_col, val)  # new sanity check
                    if val.startswith("\Error: "):  # filter Error returns
                        print("\033[{}A\033[J".format(n_rline), end='')
                        prompt_text = "> {} ".format(val[1:])
                        continue

                    # val = val.replace('<br>', '\n')
                    if val == '':
                        val = None

                except ValueError:
                    print("\033[{}A\033[J".format(n_rline), end='')
                    prompt_text = "> Invalid input! Enter new value: "
                    continue

                data = [framenumbers, framenames]
                data[cur_col][cur_line] = val
                print("\033[{}A\033[J".format(n_rline), end='')
                break

        if ltot <= 10:
            print("\033[{}A\033[J".format(ltot + 5), end='')
        else:
            print("\033[{}A\033[J".format(n_line + 6), end='')

        if k == b'ESCAPE':
            return None


n_yeeted = 0

def teleportStockMenu(gvas):
    framenumbers = gvas.data.find("FrameNumberArray").data
    framenames = gvas.data.find("FrameNameArray").data
    frametypes = gvas.data.find("FrameTypeArray").data
    framelocs = gvas.data.find("FrameLocationArray").data
    framerots = gvas.data.find("FrameRotationArray").data
    framebrakes = gvas.data.find("BrakeValueArray").data
    framecouplingfront = gvas.data.find("CouplerFrontStateArray").data
    framecouplingrear = gvas.data.find("CouplerRearStateArray").data
    # print(framenumbers)
    # print(framenames)
    # print(frametypes)
    cur_col = 0
    cur_line = 0
    formatters = [
        "{:^7s}",
        "{:<12s}",
        "{:<16s}",
        "{:<32s}",
        "{:^11s}",
        "{:^11s}"
    ]

    min_height = 1000.
    indexes = framelocs[:, 2] < min_height
    submapframes = framelocs[indexes, :]


    status_str = "⬤"

    offset = 0
    ltot = len(frametypes)
    if ltot > 10:
        split_data = True
        n_page = int(ltot / 10) + 1 * (not ltot % 10 == 0)
    else:
        split_data = False
    while True:
        n_line = 0
        print("Select method (ESCAPE to quit, ENTER to valid selection)")
        n_line += 1
        cur_page = int(offset / 10)

        print("\033[1;41m" + "      " + "\033[0m marks frames which are below ground.")
        n_line += 1
        indexes = framelocs[:, 2] < min_height
        submapframes = framelocs[indexes, :]
        nbelow = int(submapframes.size / 3)
        if nbelow == 0:
            n_line += 1
            print(f"No frame was found below {int(min_height/100.):d} m in height.")
        else :
            n_line += 1
            print(f"\033[1;32m{nbelow}\033[0m frames were found below {int(min_height/100.):d} m in height.")




        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
            n_line += 1
        print(" | ".join(formatters).format(
            "Status",
            "Frame type",
            "Number",
            "Name",
            "Respawn",
            "Yeet it"
        ))
        print("-" * (32 * 3 + 3 * 2))
        n_line += 2


        for i in range(len(frametypes)):
            if i not in range(offset, offset + 10) and split_data:
                continue

            if i == cur_line:
                line_format = " | ".join(formatters[0:4])
                for j in range(2):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j + 4] + "\033[0m"
                    else:
                        line_format += formatters[j + 4]
            else:
                line_format = " | ".join(formatters)

            num = framenumbers[i]
            nam = framenames[i]

            num = '-' if num is None else num
            nam = '-' if nam is None else nam

            # not necessary anymore (new line stored as <br>)
            # num = num if '<br>' not in num else num.replace('\n', '<br>')
            # nam = nam if '<br>' not in nam else nam.replace('\n', '<br>')

            if framelocs[i,2] < min_height:
                line_format = line_format.split(" | ")
                line_format[0] = "\033[1;41m" + line_format[0] + "\033[0m"
                line_format = " | ".join(line_format)

            print(line_format.format(
                " ",
                frametypeTranslatorShort[frametypes[i]],
                num,
                nam,
                "[RESPAWN]",
                "[YEET IT]"
            ))
            n_line += 1
        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(1, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
            if cur_line < offset:
                k = b'PAGE_UP'
        if k == b'KEY_DOWN':
            cur_line = min(ltot - 1, cur_line + 1)
            if cur_line >= offset + 10:
                k = b'PAGE_DOWN'
        if k == b'PAGE_UP':
            offset = max(0, offset - 10)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset + 10 - 1
        if k == b'PAGE_DOWN':
            max_offset = ltot - ltot % 10
            offset = min(offset + 10, max_offset)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset
        if k == b'RETURN':
            moved_something = False
            if cur_col == 0:
                # RESPAWN
                # check if respawn possible
                spawn_idx = nextAvailableSpawn(gvas, framelocs[cur_line])
                if spawn_idx is None:
                    print("There is no spawn point available for respawn !")
                    print("You can try to 'Yeet it' next to the spawn.")
                    print("Press any key to continue.")
                    getKey()
                    n_line += 3
                else:
                    print(f"Spawn point number {spawn_idx+1} is available.")
                    ans = input("Type 'YES' to proceed: ")
                    n_line += 2
                    if ans == "YES":
                        framelocs[cur_line] = spawnPositions[spawn_idx]
                        framerots[cur_line] = spawnOrientations[spawn_idx]
                        moved_something = True
            elif cur_col == 1:
                # YEET IT !
                print("The frame will be yeeted close to the spawn point.")
                ans = input("Type 'YES' to proceed (at your own risks): ")
                n_line += 2
                if ans == "YES":
                    global n_yeeted

                    framelocs[cur_line] = [n_yeeted*2400., 0., 15000.]
                    framerots[cur_line] = [0., 90., 0.]

                    n_yeeted += 1
                    moved_something = True
            if moved_something:
                framebrakes[cur_line] = 1.0
                framecouplingrear[cur_line] = False
                framecouplingfront[cur_line] = False


        if ltot <= 10:
            print("\033[{}A\033[J".format(n_line), end='')
        else:
            print("\033[{}A\033[J".format(n_line), end='')

        if k == b'ESCAPE':
            return None


def moveStockMenu(gvas):
    n_line = 0
    min_height = 1000
    new_height = 20000
    print("This feature is \033[1;31mEXPERIMENTAL\033[0m. Use at your own risks.")
    frameloc = gvas.data.find("FrameLocationArray").data
    indexes = frameloc[:, 2] < min_height
    submapframes = frameloc[indexes, :]
    nbelow = int(submapframes.size / 3)
    if nbelow == 0:
        n_line += 1
        print(f"No car/loco was found below {int(min_height/100.):d} m in height.")
    else :
        n_line += 1
        print(f"\033[1;32m{nbelow}\033[0m cars/locos were found below {int(min_height/100.):d} m in height.")
    cursor = 0
    choices = ["Cancel", "Proceed at your own risks"]
    while True:
        if cursor == 0:
            print(" " * 5 + selectfmt + "{:^29s}".format(choices[0]) + "\033[0m"
                  + " " * 5 + "{:^29s}".format(choices[1]))
        else:
            print(" " * 5 + "{:^29s}".format(choices[0])
                  + " " * 5 + selectfmt + "{:^29s}".format(choices[1]) + "\033[0m")
        k = getKey()

        if k == b'KEY_RIGHT':
            cursor = min(1, cursor + 1)
        if k == b'KEY_LEFT':
            cursor = max(0, cursor - 1)

        if k == b'RETURN':
            if cursor == 0:
                k = b'ESCAPE'
            elif cursor == 1:
                frameloc[indexes, 2] = new_height
                print(f"{nbelow} cars/locos have been displaced. Watch out for your head !")
                print("(Press any key to go back to previous menu)")
                getKey()
                print("\033[{}A\033[J".format(6), end='')
                return None

        if k == b'ESCAPE':
            print("\033[{}A\033[J".format(4), end='')
            return None

        print("\033[{}A\033[J".format(1), end='')


def engineStockMenu(gvas):
    framenumbers = gvas.data.find("FrameNumberArray").data
    framenames = gvas.data.find("FrameNameArray").data
    frametypes = gvas.data.find("FrameTypeArray").data
    frameboilerwater = gvas.data.find("BoilerWaterLevelArray").data
    frametenderwater = gvas.data.find("TenderWaterAmountArray").data
    frametenderfuel = gvas.data.find("TenderFuelAmountArray").data

    ind = []
    for i in range(len(frametypes)):
        if (frametypes[i] in waterBoiler.keys()) or (frametypes[i] in waterReserves.keys()) or \
                (frametypes[i] in firewoodReserves.keys()):
            ind.append(i)

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:<48s}",
        "{:>14}",
        "{:>14}",
        "{:>12}",
    ]
    dashline =''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    offset = 0
    ltot = len(ind)
    if ltot > 10:
        split_data = True
        n_page = int(ltot / 10) + 1 * (not ltot % 10 == 0)
    else:
        split_data = False
    while True:
        print("Select value to edit (ESCAPE to quit, ENTER to valid selection)")
        print("Enter nothing to fill up, or type in an amount.")
        cur_page = int(offset / 10)
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Engine / Tender",
            "Water Boiler",
            "Water Tank",
            "Firewood",
        ))
        print(dashline)
        n_line = 0
        for i in range(len(ind)):
            if i not in range(offset, offset + 10) and split_data:
                continue
            n_line += 1
            if i == cur_line:
                line_format = formatters[0]
                for j in range(3):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j + 1] + "\033[0m"
                    else:
                        line_format += formatters[j + 1]
            else:
                line_format = " | ".join(formatters)

            frametype = frametypes[ind[i]]
            num = framenumbers[ind[i]]
            nam = framenames[ind[i]]

            num = '' if num is None else num
            nam = '' if nam is None else nam

            namestr = "{:<10s}:".format(frametypeTranslatorShort[frametype])
            if not num == '':
                namestr += " {:>4}".format(num.split("<br>")[0].strip())
            if not nam == '':
                namestr += " " + nam.split("<br>")[0].strip()
            namestr = namestr[:48]

            if frametype in waterBoiler.keys():
                waterboilerstr = "{.1f} / {:4}".format(frameboilerwater[ind[i]], waterBoiler[frametype])
            else:
                waterboilerstr = ''

            if frametype in waterReserves.keys():
                waterreservestr = "{.1f} / {:4}".format(frametenderwater[ind[i]], waterReserves[frametype])
            else:
                waterreservestr = ''

            if frametype in firewoodReserves.keys():
                firewoodstr = "{:.0f} / {:4}".format(frametenderfuel[ind[i]], firewoodReserves[frametype])
            else:
                firewoodstr = ''

            print(line_format.format(
                namestr,
                waterboilerstr,
                waterreservestr,
                firewoodstr,
            ))
        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(2, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
            if cur_line < offset:
                k = b'PAGE_UP'
        if k == b'KEY_DOWN':
            cur_line = min(ltot - 1, cur_line + 1)
            if cur_line >= offset + 10:
                k = b'PAGE_DOWN'
        if k == b'PAGE_UP':
            offset = max(0, offset - 10)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset + 10 - 1
        if k == b'PAGE_DOWN':
            max_offset = ltot - ltot % 10
            offset = min(offset + 10, max_offset)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset
        if k == b'RETURN':
            curframetype = frametypes[ind[cur_line]]
            if cur_col == 0 and curframetype in waterBoiler.keys():
                prompt_text = "> Enter new value or leave blank for max: "
                while True:
                    val = input(prompt_text)
                    try:
                        if val == '':
                            val = waterBoiler[curframetype]
                        else:
                            val = float(val)
                    except ValueError:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid input! Enter new value: "
                        continue

                    if val < 0 or val > waterBoiler[curframetype]:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid amount! Enter new value: "
                        continue

                    frameboilerwater[ind[cur_line]] = val
                    print("\033[{}A\033[J".format(1), end='')
                    break

            elif cur_col == 1 and curframetype in waterReserves.keys():
                prompt_text = "> Enter new value or leave blank for max: "
                while True:
                    val = input(prompt_text)
                    try:
                        if val == '':
                            val = waterReserves[curframetype]
                        else:
                            val = int(val)
                    except ValueError:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid input! Enter new value: "
                        continue

                    if val < 0 or val > waterReserves[curframetype]:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid amount! Enter new value: "
                        continue

                    frametenderwater[ind[cur_line]] = val
                    print("\033[{}A\033[J".format(1), end='')
                    break

            elif cur_col == 2 and curframetype in firewoodReserves.keys():
                prompt_text = "> Enter new value or leave blank for max: "
                while True:
                    val = input(prompt_text)
                    try:
                        if val == '':
                            val = firewoodReserves[curframetype]
                        else:
                            val = int(val)
                    except ValueError:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid input! Enter new value: "
                        continue

                    if val < 0 or val > firewoodReserves[curframetype]:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid amount! Enter new value: "
                        continue

                    frametenderfuel[ind[cur_line]] = val
                    print("\033[{}A\033[J".format(1), end='')
                    break

        if ltot <= 10:
            print("\033[{}A\033[J".format(ltot + 4), end='')
        else:
            print("\033[{}A\033[J".format(n_line + 5), end='')

        if k == b'ESCAPE':
            return None


def cargoStockMenu(gvas):
    framenumbers = gvas.data.find("FrameNumberArray").data
    framenames = gvas.data.find("FrameNameArray").data
    frametypes = gvas.data.find("FrameTypeArray").data
    framecargotypes = gvas.data.find("FreightTypeArray").data
    framecargoamounts = gvas.data.find("FreightAmountArray").data

    ind = []
    for i in range(len(frametypes)):
        if frametypes[i] in frametypeCargoLimits.keys():
            ind.append(i)

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:<48s}",
        "{:<12}",
        "{:>6}",
    ]
    offset = 0
    ltot = len(ind)
    if ltot > 10:
        split_data = True
        n_page = int(ltot / 10) + 1 * (not ltot % 10 == 0)
    else:
        split_data = False
    while True:
        print("Select value to edit (ESCAPE to quit, ENTER to valid selection)")
        print("Empty fields mean this wagon hasn't been used yet")
        cur_page = int(offset / 10)
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Cargo Wagon",
            "Type",
            "Amount"
        ))
        print("-" * (48 + 12 + 6 + 3 * 2))
        n_line = 0
        for i in range(len(ind)):
            if i not in range(offset, offset + 10) and split_data:
                continue
            n_line += 1
            if i == cur_line:
                line_format = formatters[0]
                for j in range(2):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j + 1] + "\033[0m"
                    else:
                        line_format += formatters[j + 1]
            else:
                line_format = " | ".join(formatters)

            frametype = frametypes[ind[i]]
            num = framenumbers[ind[i]]
            nam = framenames[ind[i]]
            cargo = framecargotypes[ind[i]]

            num = '' if num is None else num
            nam = '' if nam is None else nam

            namestr = "{:<10s}:".format(frametypeTranslatorShort[frametype])
            if not num == '':
                namestr += " " + num.split("<br>")[0].strip()
            if not nam == '':
                namestr += " " + nam.split("<br>")[0].strip()
            namestr = namestr[:48]

            if cargo in cargotypeTranslator.keys():
                cargostr = cargotypeTranslator[cargo]
            elif cargo is None:
                cargostr = cargotypeTranslator["empty"]
            else:
                cargostr = cargotypeTranslator["default"]

            if cargo is not None:
                amount = framecargoamounts[ind[i]]
                amountstr = "{}/{}".format(amount, frametypeCargoLimits[frametype][cargo])
            else:
                amountstr = ''

            print(line_format.format(
                namestr,
                cargostr,
                amountstr
            ))
        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(1, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
            if cur_line < offset:
                k = b'PAGE_UP'
        if k == b'KEY_DOWN':
            cur_line = min(ltot - 1, cur_line + 1)
            if cur_line >= offset + 10:
                k = b'PAGE_DOWN'
        if k == b'PAGE_UP':
            offset = max(0, offset - 10)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset + 10 - 1
        if k == b'PAGE_DOWN':
            max_offset = ltot - ltot % 10
            offset = min(offset + 10, max_offset)
            if cur_line not in range(offset, offset + 10):
                cur_line = offset
        if k == b'RETURN':
            curframetype = frametypes[ind[cur_line]]
            curframecargo = framecargotypes[ind[cur_line]]
            if cur_col == 0:
                cursor = 0
                choices = [None, ]
                for cargotype in frametypeCargoLimits[curframetype].keys():
                    choices.append(cargotype)
                while True:
                    typeselection = "> Choose new cargo:"
                    for option in range(len(choices)):
                        if option == cursor:
                            typeselection += "  " + selectfmt + cargotypeTranslator[choices[option]] + "\033[0m"
                        else:
                            typeselection += "  " + cargotypeTranslator[choices[option]]
                    print(typeselection)

                    k = getKey()
                    print("\033[{}A\033[J".format(1), end='')

                    if k == b'KEY_RIGHT':
                        cursor = min(len(choices), cursor + 1)
                    if k == b'KEY_LEFT':
                        cursor = max(0, cursor - 1)

                    if k == b'RETURN':
                        newcargo = choices[cursor]
                        if not curframecargo == newcargo:
                            framecargotypes[ind[cur_line]] = newcargo
                            if choices[cursor] is None:
                                framecargoamounts[ind[cur_line]] = 0
                            else:
                                framecargoamounts[ind[cur_line]] = frametypeCargoLimits[curframetype][newcargo]
                        break

                    if k == b'ESCAPE':
                        break

            elif cur_col == 1:
                if curframecargo is not None:
                    prompt_text = "> Enter new value: "
                    while True:
                        val = input(prompt_text)
                        try:
                            if val == '':
                                val = 0
                            else:
                                val = int(val)
                        except ValueError:
                            print("\033[{}A\033[J".format(1), end='')
                            prompt_text = "> Invalid input! Enter new value: "
                            continue

                        if val < 0 or val > frametypeCargoLimits[curframetype][curframecargo]:
                            print("\033[{}A\033[J".format(1), end='')
                            prompt_text = "> Invalid amount! Enter new value: "
                            continue

                        framecargoamounts[ind[cur_line]] = val
                        print("\033[{}A\033[J".format(1), end='')
                        break

        if ltot <= 10:
            print("\033[{}A\033[J".format(ltot + 4), end='')
        else:
            print("\033[{}A\033[J".format(n_line + 5), end='')

        if k == b'ESCAPE':
            return None


def mainStockMenu(gvas):
    options = [
        ("Rename", renameStockMenu),
        ("Respawn", teleportStockMenu),
        ("Cargo", cargoStockMenu),
        ("Locomotive Restock", engineStockMenu),
    ]
    current = 0
    while True:
        print("Select the feature you want to run (press ENTER to confirm):")
        for i, f in enumerate(options):
            if i == current:
                print(" - " + selectfmt + "{}\033[0m".format(f[0]))
            else:
                print(" - {}".format(f[0]))
        k = getKey()
        if k == b'KEY_UP':
            current = max(0, current - 1)
        if k == b'KEY_DOWN':
            current = min(len(options) - 1, current + 1)
        print("\033[{}A\033[J".format(len(options) + 1), end='')
        if k == b'RETURN':
            options[current][1](gvas)
        if k == b'ESCAPE':
            return None


if __name__ == "__main__":
    filename = selectSaveFile()
    print(filename)
    submenu = mainMenu()
    print(submenu)
    # playerMenu() # needs a gvas !
