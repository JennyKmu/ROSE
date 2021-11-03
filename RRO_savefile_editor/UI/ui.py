import glob, os, shutil
from pathlib import Path

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
                print(" - "+selectfmt+"{}\033[0m".format(f))
            else:
                print(" - {}".format(f))
        k = getKey()
        if k == b'KEY_UP':
            current = max(0, current-1)
        if k == b'KEY_DOWN':
            current = min(len(filelist)-1, current+1)
        print("\033[{}A\033[J".format(len(filelist)+1), end='')
        if k == b'RETURN':
            return filelist[current]
        if k == b'ESCAPE':
            return -1

def mainMenu(gvas):
    options = [
        ("Players", playerMenu),
        ("Rolling stock", mainStockMenu),
        ("Environment", mainEnvMenu),
        ("Save & Exit", saveAndExit),
        ("Exit", noSaveAndExit)
    ]
    current = 0
    while True:
        print("Select the submenu (press ENTER to confirm):")
        for i, f in enumerate(options):
            if i == current:
                print(" - "+selectfmt+"{}\033[0m".format(f[0]))
            else:
                print(" - {}".format(f[0]))
        k = getKey()
        if k == b'KEY_UP':
            current = max(0, current-1)
        if k == b'KEY_DOWN':
            current = min(len(options)-1, current+1)
        print("\033[{}A\033[J".format(len(options)+1), end='')
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
    fbackup = Path("./backups") / Path("backup_"+gvas._sourcefilename)
    print("> Saving backup file as {}".format(fbackup))
    if not os.path.exists('backups'):
        os.makedirs('backups')
    shutil.copy(filename, fbackup)

    print("> Overwriting file {}".format(filename))
    # gvas.write("dev_"+filepath.name)
    gvas.write(filename)
    print("Press any key to close.")
    print("------------------")
    getKey()
    exit()

def noSaveAndExit(gvas):
    # gvas arg for compatibility with other ui functions
    print("Press any key to close.")
    print("------------------")
    getKey()
    exit()

def mainEnvMenu(gvas):
    pass

#
# class SubMenu(object):
#     def __init__(self,
#                         formatter,
#                         header,
#                         col_names,
#                         sep_size,
#                         properties,
#                         editable=True,
#                         editable_range=[1,2],
#                         special_format=None):
#         self.max_lines = 10
#         self.cur_col = 0
#         self.cur_lin = 0
#         self.cur_range = 0
#         self.header = header
#         self.col_names = col_names
#         self.formatter = formatter
#         self.properties = properties
#         self.sep_size = sep_size
#         self.editable = editable
#         self.editable_range = editable_range
#         if special_format is None:
#             self.special_format = [None]*len(self.properties)
#         else:
#             self.special_format = special_format
#
#     def __call__(self, gvas):
#         props = [gvas.find(prop).data for prop in self.properties]
#         while True:
#             print(self.header)
#             print(' | '.join(self.formatter).format(self.col_names))
#             print('-'*self.sep_size)
#             if len(props[0]) <= self.max_lines:
#                 for i in range(len(props[0]):
#                     if i == self.cur_lin and self.editable:
#                         k = 0
#                         line_format = []
#                         for j in range(len(props)):
#                             if j in self.editable_range and self.editable_range[k] == j and k == self.cur_col:
#                                 line_format.append(selectfmt + self.formatter[j] + "\033[0m")
#                             else:
#                                 line_format.append(self.formatter[j])
#                                 k += 1
#                         line_format = " | ".join(line_format)
#                     else :
#                         line_format = " | ".join(self.formatter)
#
#                     values = []
#                     for p in range(len(props)):
#                         if self.special_format[p] is not None:
#                             values.append(self.special_format[p](props[p][i]))
#                         else:
#                             values.append(props[p][i])
#                     print(line_format.format(*tuple(values)))
#
#             else:
#                 raise NotImplementedError("Under Construction")
#
#
#             k = getKey()
#
#             if k == b'KEY_RIGHT':
#                 cur_col = min(1,cur_col+1)
#             if k == b'KEY_LEFT':
#                 cur_col = max(0, cur_col-1)
#             if k == b'KEY_UP':
#                 cur_line = max(0, cur_line-1)
#             if k == b'KEY_DOWN':
#                 cur_line = min(len(player_names_prop.data)-1, cur_line+1)
#             if k == b'RETURN':
#                 self.edit()
#
#             if len(props[0]) <= self.max_lines:
#                 print("\033[{}A\033[J".format(len(props[0])+3), end='')
#             else:
#                 raise NotImplementedError()
#
#             if k == b'ESCAPE':
#                 return None
#
#
#
#     def edit(self, props):
#         prompt_text = "> Enter new value: "
#         while True:
#             n_line = 0
#             val = input(prompt_text)
#             n_line +=1
#             try:
#                 if self.special_input[self.cur_col] is not None:
#                     val = self.special_input[self.cur_col](val)
#             except ValueError:
#                 print("\033{}A\033[J".format(n_line), end='')
#                 prompt_text = "> Invalid input! Enter new value: "
#                 continue
#             except Exception as e:
#                 print("\033{}A\033[J".format(n_line), end='')
#                 prompt_text = "> {} Enter new value: ".format(e.message)
#                 continue
#
#             data = [props[k] for k in self.editable_range]
#             data[cur_col][cur_line] = val
#             print("\033[{}A\033[J".format(n_line), end='')
#             break
#
#
#         raise NotImplementedError("You need to implement that")
#
#
# def newPlayerMenu(gvas):
#     menu = SubMenu(
#         )
#     menu(gvas)

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
        n_page = int(ltot/10)+1*(not ltot%10 == 0)
    else: split_data = False
    while True:
        print("Select a field to edit (ESCAPE to quit, ENTER to valid selection)")
        cur_page = int(offset/10)
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page+1, n_page))
        print("{:<65s} | {:>9s} | {:>9s}".format(
            "Player name",
            "XP",
            "Money"
        ))
        print("-"*(65+3+9+3+9))
        formatters = [
            "{:<64s}",
            "{:>9d}",
            "{:>9.0f}",
        ]
        n_line = 0
        for i in range(len(player_names_prop.data)):
            if i not in range(offset, offset+10) and split_data:
                continue
            n_line+=1
            line_format = "{:<64s} "
            if i == cur_line:
                for j in range(2):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j+1] + "\033[0m"
                    else:
                        line_format += formatters[j+1]
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
            cur_col = min(1,cur_col+1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col-1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line-1)
            if cur_line < offset:
                k = b'PAGE_UP'
        if k == b'KEY_DOWN':
            cur_line = min(ltot-1, cur_line+1)
            if cur_line >= offset + 10:
                k = b'PAGE_DOWN'
        if k == b'PAGE_UP':
            offset = max(0, offset - 10)
            if cur_line not in range(offset, offset+10):
                cur_line = offset+10-1
        if k == b'PAGE_DOWN':
            max_offset = ltot-ltot%10
            offset = min(offset + 10, max_offset)
            if cur_line not in range(offset, offset+10):
                cur_line = offset
        if k == b'RETURN':
            prompt_text = "> Enter new value: "
            while True:
                n_rline = 0
                val = input(prompt_text)
                n_rline +=1
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

        if len(player_names_prop.data)<=10:
            print("\033[{}A\033[J".format(len(player_names_prop.data)+3), end='')
        else:
            print("\033[{}A\033[J".format(n_line+4), end='')


        if k == b'ESCAPE':
            return None

frametypeTranslator = {
    "flatcar_logs":"Flatcar Tier I",
    "flatcar_stakes":"Flatcar Tier II",
    "flatcar_cordwood":"Flatcar Tier III",
    "flatcar_hopper":"Hopper",
    "flatcar_tanker":"Tanker",
    "boxcar":"Boxcar",
    "porter_040":"Porter 0-4-0",
    "porter_042":"Porter 0-4-2",
    "climax":"Climax",
    "heisler":"Heisler",
    "cooke260":"Cooke Mogul",
    "cooke260_tender":"Cooke Mogul Tender",
    "class70":"D&RG Class 70",
    "class70_tender":"D&RG Class 70 Tender",
    "eureka":"Eureka",
    "eureka_tender":"Eureka Tender",
    "handcar":"Handcar",
}

frametypeNamingLimiter = {
    "default":{"numlen":4, "numlines":1, "namelen":10, "namelines":2},
    "flatcar_logs":{"numlen":12, "numlines":1, "namelen":7, "namelines":1},
    "flatcar_stakes":{"numlen":8, "numlines":1, "namelen":8, "namelines":1},
    "flatcar_cordwood":{"numlen":8, "numlines":1, "namelen":8, "namelines":1},
    "flatcar_hopper":{"numlen":4, "numlines":1, "namelen":7, "namelines":1},
    "flatcar_tanker":{"numlen":12, "numlines":1, "namelen":19, "namelines":1},
    "boxcar":{"numlen":7, "numlines":4, "namelen":13, "namelines":4},
    "porter_040":{"numlen":2, "numlines":1, "namelen":12, "namelines":1},
    "porter_042":{"numlen":2, "numlines":1, "namelen":12, "namelines":1},
    "climax":{"numlen":2, "numlines":1, "namelen":11, "namelines":7},
    "heisler":{"numlen":2, "numlines":1, "namelen":11, "namelines":6},
    "cooke260":{"numlen":3, "numlines":1, "namelen":12, "namelines":1},
    "cooke260_tender":{"numlen":6, "numlines":1, "namelen":11, "namelines":1},
    "class70":{"numlen":3, "numlines":1, "namelen":14, "namelines":1},
    "class70_tender":{"numlen":0, "numlines":0, "namelen":22, "namelines":3},
    "eureka":{"numlen":2, "numlines":1, "namelen":8, "namelines":1},
    "eureka_tender":{"numlen":0, "numlines":0, "namelen":18, "namelines":1},
    "handcar":{"numlen":5, "numlines":1, "namelen":18, "namelines":1},
}

def getNamingLimits(frametype, field):
    if not frametype in frametypeNamingLimiter:
        frametype = "default"

    if field == 0:
        maxlen = frametypeNamingLimiter[frametype]["numlen"]
        maxlines = frametypeNamingLimiter[frametype]["numlines"]
    else:
        maxlen = frametypeNamingLimiter[frametype]["namelen"]
        maxlines = frametypeNamingLimiter[frametype]["namelines"]

    return maxlen, maxlines

def namingSanityCheck(frametype, field, input):
    if not input.startswith("\i"):
        if input.isspace() or input == '': # if there is no text to work with, return nothing
            return ''

        lines = input.split("<br>") # split into separate lines first

        maxlen, maxlines = getNamingLimits(frametype,field)

        if maxlen == 0 or maxlines == 0: # of it's not to be named at all
            return "\Error: This field isn't displayed at all. Enter to leave"

        if len(lines) > maxlines: # check if line count is good
            return "\Error: Too many lines. Max is {}. Try again:".format(maxlines)

        sanelines = []
        linesHaveContent = False

        for line in lines:
            if len(line) > maxlen: # check if length for every line is good
                return "\Error: Line(s) too long. Max is {} per line. Try again:".format(maxlen)

            if line.isspace() or line == '':  # see if the line has content at all: all spaces or nothing
                line = ' '                       #if that's the case, make it one space
            else:
                linesHaveContent = True

            sanelines.append(line)

        #if we made it this far, reassemble the string
        if linesHaveContent: # if there is no content over multiple lines, return nothing instead
            saneinput = "<br>".join(sanelines)

            return saneinput
        else:
            return ''

    else:
        return input[2:]


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
        n_page = int(ltot/10)+1*(not ltot%10 == 0)
    else: split_data = False
    while True:
        print("Select field to edit (ESCAPE to quit, ENTER to valid selection)")
        print("Use <br> to create multiple line values where applicable. Override sanity checks with \i")
        #print("Sanity checks are enabled. To ignore limits start your input with \i")
        cur_page = int(offset/10)
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page+1, n_page))
        print(" | ".join(formatters).format(
            "Rolling stock type",
            "Number",
            "Name"
        ))
        print("-"*(32*3+3*2))
        n_line = 0
        for i in range(len(frametypes)):
            if i not in range(offset, offset+10) and split_data:
                continue
            n_line+=1
            if i == cur_line:
                line_format = formatters[0]
                for j in range(2):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j+1] + "\033[0m"
                    else:
                        line_format += formatters[j+1]
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
                frametypeTranslator[frametypes[i]],
                num,
                nam,
            ))
        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(1,cur_col+1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col-1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line-1)
            if cur_line < offset:
                k = b'PAGE_UP'
        if k == b'KEY_DOWN':
            cur_line = min(ltot-1, cur_line+1)
            if cur_line >= offset + 10:
                k = b'PAGE_DOWN'
        if k == b'PAGE_UP':
            offset = max(0, offset - 10)
            if cur_line not in range(offset, offset+10):
                cur_line = offset+10-1
        if k == b'PAGE_DOWN':
            max_offset = ltot-ltot%10
            offset = min(offset + 10, max_offset)
            if cur_line not in range(offset, offset+10):
                cur_line = offset
        if k == b'RETURN':
            maximums = getNamingLimits(frametypes[cur_line], cur_col)
            if maximums[0] == 0 or maximums[1] == 0:
                prompt_text = "> This field isn't displayed at all. Enter to leave "
            else:
                prompt_text = "> Max Length {0}, max lines {1}; Enter new value: ".format(maximums[0],maximums[1])
            while True:
                n_rline = 0
                val = input(prompt_text)
                n_rline +=1
                try:
                    val = str(val)
                    # if val.count('<br>') > 1 :
                        # print("\033[{}A\033[J".format(n_rline), end='')
                        # prompt_text = "> Can't handle more than two lines for now! Enter new value: "
                        # continue
                    val = namingSanityCheck(frametypes[cur_line],cur_col,val)   # new sanity check
                    if val.startswith("\Error: "):                               # filter Error returns
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

        if ltot<=10:
            print("\033[{}A\033[J".format(ltot+4), end='')
        else:
            print("\033[{}A\033[J".format(n_line+5), end='')

        if k == b'ESCAPE':
            return None


def moveStockMenu(gvas):
    n_line = 0
    min_height = 1000
    new_height = 20000
    print("This feature is \033[1;31mEXPERIMENTAL\033[0m. Use at your own risks.")
    frameloc = gvas.data.find("FrameLocationArray").data
    indexes = frameloc[:,2]<min_height
    submapframes = frameloc[indexes,:]
    nbelow = int(submapframes.size/3)
    if nbelow == 0:
        print(f"No car/loco was found below {min_height} game units in height.")
        print(f"Press any key to return to previous menu.")
        getKey()
        print("\033[{}A\033[J".format(3), end='')
        return

    print(f"\033[1;32m{nbelow}\033[0m cars/locos were found below {min_height} game units in height.")
    print(f"If you proceed, those cars will be repositionned at {new_height} game units in height.")
    cursor = 0
    choices = [ "Cancel", "Proceed at your own risks" ]
    while True:
        if cursor == 0:
            print(" "*5 + selectfmt + "{:^29s}".format(choices[0]) + "\033[0m"
                + " "*5 + "{:^29s}".format(choices[1]))
        else:
            print(" "*5 + "{:^29s}".format(choices[0])
                + " "*5 + selectfmt + "{:^29s}".format(choices[1]) + "\033[0m")
        k = getKey()

        if k == b'KEY_RIGHT':
            cursor = min(1, cursor+1)
        if k == b'KEY_LEFT':
            cursor = max(0, cursor-1)

        if k == b'RETURN':
            if cursor == 0:
                k = b'ESCAPE'
            elif cursor == 1:
                frameloc[indexes,2] = new_height
                print(f"{nbelow} cars/locos have been displaced. Watch out for your head !")
                print("(Press any key to go back to previous menu)")
                getKey()
                print("\033[{}A\033[J".format(6), end='')
                return None


        if k == b'ESCAPE':
            print("\033[{}A\033[J".format(4), end='')
            return None

        print("\033[{}A\033[J".format(1), end='')


def mainStockMenu(gvas):
    options = [
        ("Rename", renameStockMenu),
        ("Teleport", moveStockMenu),
    ]
    current = 0
    while True:
        print("Select the feature you want to run (press ENTER to confirm):")
        for i, f in enumerate(options):
            if i == current:
                print(" - "+selectfmt+"{}\033[0m".format(f[0]))
            else:
                print(" - {}".format(f[0]))
        k = getKey()
        if k == b'KEY_UP':
            current = max(0, current-1)
        if k == b'KEY_DOWN':
            current = min(len(options)-1, current+1)
        print("\033[{}A\033[J".format(len(options)+1), end='')
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
