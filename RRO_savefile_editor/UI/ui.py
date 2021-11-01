import glob

try:
    from uiutils import getKey
except:
    from .uiutils import getKey

selectfmt = "\033[1;32m"

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

def mainMenu():
    options = [
        "Players",
        # "Locos and Cars",
        "Save & Exit",
        "Exit",
    ]
    current = 0
    while True:
        print("Select the submenu (press ENTER to confirm):")
        for i, f in enumerate(options):
            if i == current:
                print(" - "+selectfmt+"{}\033[0m".format(f))
            else:
                print(" - {}".format(f))
        k = getKey()
        if k == b'KEY_UP':
            current = max(0, current-1)
        if k == b'KEY_DOWN':
            current = min(len(options)-1, current+1)
        print("\033[{}A\033[J".format(len(options)+1), end='')
        if k == b'RETURN':
            return options[current]
        if k == b'ESCAPE':
            return None

def playerMenu(gvas):
    player_names_prop = gvas.data.find("PlayerNameArray")
    player_money_prop = gvas.data.find("PlayerMoneyArray")
    player_xp_prop = gvas.data.find("PlayerXPArray")
    cur_col = 0
    cur_line = 0
    while True:
        print("Select a field to edit (ESCAPE to quit, ENTER to valid selection):")
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
        for i in range(len(player_names_prop.data)):
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
        if k == b'KEY_DOWN':
            cur_line = min(len(player_names_prop.data)-1, cur_line+1)
        if k == b'RETURN':
            prompt_text = "> Enter new value: "
            while True:
                n_line = 0
                val = input(prompt_text)
                n_line +=1
                try:
                    val = int(val)
                except ValueError:
                    print("\033{}A\033[J".format(n_line), end='')
                    prompt_text = "> Invalid input! Enter new value: "
                    continue

                data = [player_xp_prop.data, player_money_prop.data]
                data[cur_col][cur_line] = val
                print("\033[{}A\033[J".format(n_line), end='')
                break

        print("\033[{}A\033[J".format(len(player_names_prop.data)+3), end='')

        if k == b'ESCAPE':
            return None


if __name__ == "__main__":
    filename = selectSaveFile()
    print(filename)
    submenu = mainMenu()
    print(submenu)
    # playerMenu() # needs a gvas !
