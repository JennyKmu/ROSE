def devslotA(gvas):
    print("> Running DEV SLOT A")
    from .industryPlacables import industryNames, industryStandardLocations, placingLimits, mapIndustries
    from .ui import selectfmt
    from .uiutils import getKey

    industrytypes = gvas.data.find("IndustryTypeArray").data
    industrylocations = gvas.data.find("IndustryLocationArray").data
    industryrotations = gvas.data.find("IndustryRotationArray").data

    ind = []
    for i in range(len(industrytypes)):
        if industrytypes[i] in industryNames.keys():
            ind.append(i)

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:15}",
        "{:>10}",
        "{:>10}",
        "{:>10}",
        "{:>10}",
        "{:7}",
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    offset = 0
    ltot = len(ind)
    if ltot > 10:
        split_data = True
        n_page = int(ltot / 10) + 1 * (not ltot % 10 == 0)
    else:
        split_data = False
        n_page = 1
    while True:
        print("Select Industry to move (ESCAPE to quit, ENTER to select)")
        print("West +X .. -X East | North +Y .. -Y South | High +Z .. +z Low")
        cur_page = int(offset / 10)
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Industry",
            "X",
            "Y",
            "Z",
            "Rot",
            ""
        ))
        print(dashline)
        n_line = 0
        for i in range(len(ind)):
            if i not in range(offset, offset + 10) and split_data:
                continue
            n_line += 1
            if i == cur_line:
                line_format = formatters[0]
                for j in range(5):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j + 1] + "\033[0m"
                    else:
                        line_format += formatters[j + 1]
            else:
                line_format = " | ".join(formatters)

            namestr = industryNames[industrytypes[ind[i]]]
            curlocation = industrylocations[ind[i]]
            curx = curlocation[0]
            cury = curlocation[1]
            curz = curlocation[2]
            curr = industryrotations[ind[i]][1]
            if industrytypes[ind[i]] in mapIndustries:
                reset_str = "[RESET]"
            else:
                reset_str = ""

            print(line_format.format(
                namestr,
                "{:.1f}".format(curx),
                "{:.1f}".format(cury),
                "{:.1f}".format(curz),
                "{:.1f}".format(curr),
                reset_str,
            ))

        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(4, cur_col + 1)
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
            if cur_col == 4:
                if industrytypes[ind[cur_line]] in mapIndustries:
                    industrylocations[ind[cur_line]][0] = industryStandardLocations[industrytypes[ind[cur_line]]][0]
                    industrylocations[ind[cur_line]][1] = industryStandardLocations[industrytypes[ind[cur_line]]][1]
                    industrylocations[ind[cur_line]][2] = industryStandardLocations[industrytypes[ind[cur_line]]][2]
                    industryrotations[ind[cur_line]][1] = industryStandardLocations[industrytypes[ind[cur_line]]][3]
            else:
                switcher = {0: "X", 1: "Y", 2: "Z", 3: "R"}[cur_col]
                limitlower = placingLimits[switcher][0]
                limitupper = placingLimits[switcher][1]
                if limitlower > limitupper:
                    limitlower, limitupper = limitupper, limitlower

                prompt_text = "> Enter new value: "
                while True:
                    n_rline = 0
                    val = input(prompt_text)
                    n_rline += 1
                    print("\033[{}A\033[J".format(n_rline), end='')
                    try:
                        val = float(val)

                        if cur_col == 3:
                            while val > limitupper:
                                val -= 360
                            while val < limitlower:
                                val += 360
                        else:
                            if not limitlower <= val <= limitupper:
                                prompt_text = "> Out of placement limits! Enter value: "
                                continue
                    except ValueError:
                        prompt_text = "> Invalid input! Enter new value: "
                        continue

                    if cur_col == 3:
                        industryrotations[ind[cur_line]][1] = val
                    else:
                        industrylocations[ind[cur_line]][cur_col] = val
                    break

        if ltot <= 10:
            print("\033[{}A\033[J".format(ltot + 4), end='')
        else:
            print("\033[{}A\033[J".format(n_line + 5), end='')

        if k == b'ESCAPE':
            print("\033[1A\033[J", end='')
            return None

def devslotB(gvas):
    import math
    import numpy as np
    from .uiutils import getKey
    from .defaultRemovedTrees import default_removed_trees
    print("> Running DEV SLOT B")
    print("> Fetching removed trees...")
    removedtrees = gvas.data.find("RemovedVegetationAssetsArray").data
    defaulttrees = np.asarray(default_removed_trees, dtype=np.float32)
    tformat = "[{:<17}, {:<17}, {:<17}],"
    print("(A)ll Trees or just additional (R)emoved ones?")
    while True:
        k = getKey()
        if k == b'r' or k == b'R':
            print("Limiting to player-removed trees...")
            removedtrees = removedtrees[~((removedtrees[:, None, :] == defaulttrees).all(-1)).any(1)]
            break
        elif k == b'ESCAPE':
            return
        elif k == b'a' or k == b'A':
            break
    if len(removedtrees) > 1000:
        print("> These are many trees, displaying in parts of 1000, ENTER to continue")
        for thousands in range(int(math.ceil(len(removedtrees)/1000.0))):
            print("{},000s of trees ({} TOTAL) ".format(thousands, len(removedtrees)) + "-" * 60)
            k = None
            while k != b'RETURN':
                k = getKey()
                if k == b'ESCAPE':
                    return
            for t in range(1000):
                if (t + thousands * 1000) >= len(removedtrees):
                    break
                else:
                    print(tformat.format(*removedtrees[t + thousands * 1000]))
    elif len(removedtrees) > 0:
        for tree in removedtrees:
            print(tformat.format(*tree))
    print("> End of trees. {} in Total".format(len(removedtrees)))
    print("Any key to return")
    getKey()
    print("-" * 80 + "\n")

def devslotC(gvas):
    print("> Running DEV SLOT C")
    pass

def devslotD(gvas):
    print("> Running DEV SLOT D")
    pass

def devslotE(gvas):
    print("> Running DEV SLOT E")
    pass
