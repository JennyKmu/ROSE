from typing import Any

import glob
import os
import shutil
import sys
import numpy as np
from pathlib import Path
from .industryPlacables import *
from .rollingStock import *
from .trackData import *
from .playerTeleportReferences import *
dev_version = False

try:
    from uiutils import getKey
except:
    from .uiutils import getKey

selectfmt = "\033[1;32;42m"


def selectSaveFile(loc):
    excludedfiles = [
        "Options.sav",
        "GraphicsOptions.sav",
    ]
    # filelist = glob.glob(loc + '/' + "slot*.sav")
    filelist = glob.glob(loc + '/' + "*.sav")
    current = 0
    if len(filelist) == 0:
        return None
    for file in filelist:
        if file.split("\\")[-1] in excludedfiles:
            filelist.remove(file)
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


def mainMenu(gvas, dev_version_i=False):
    global dev_version
    dev_version = dev_version_i
    options = [
        ("Players", playerXpMoney),
        ("Teleport", playerteleport),
        ("Rolling stock", mainStockMenu),
        ("Environment", mainEnvMenu),
        ("Save & Exit", saveAndExit),
        ("Exit", noSaveAndExit)
    ]
    if dev_version:
        from .uidev import devslotA, devslotB, devslotC, devslotD, devslotE
        dev_options = [
            ("DEV A: move Industries", devslotA),
            ("DEV B: show removed Trees", devslotB),
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


def failedtofind(string):
    print("Couldn't find {} on your save.\nPress any key to return".format(string))
    getKey()
    print("\033[2A\033[J", end='')


def mainEnvMenu(gvas):
    options = [
        ("Edit Industry Contents", editindustries),
        ("Edit Utility Contents", editplacables),
        ("Smart tree replant", resetTreesSmart),
        ("Repaint Sheds", exchangesheds),
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
    print(" * Or worse, through the ground. But for that you can use the respawn tool.")

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


def resetTreesSmart(gvas):
    # NOTE:
    # - 500. for safe dist with norm1 gives a not to bad result, could be used
    #   to make a "network for rehab after long time unused"
    from .defaultRemovedTrees import default_removed_trees
    from .betterDefaultRemovedTrees import better_default_removed_trees
    print("This is an \033[1;31mEXPERIMENTAL\033[0m feature. Use at your own risks.")
    print("Risks include in particular:")
    print(" * Trees in the middle of the track (obviously)")
    print(" * Rolling stock being yeeted through the air at hypersonic speeds...")
    print(" * Or worse, through the ground. But for that you can use the respawn tool.")
    print("This tool will attempt to replant trees avoiding tracks and other assets.")
    print("Expect some computing time after launching the tool.")


    # Distance from placed elements where trees aren't respawned
    safeDistSplines= 800.
    safeDistWater= 700.
    safeDistFirewood = 1500.
    safeDistSand = 1200.
    # TODO: Add actual shapes (rectangles) for the facilities to be able to replant very close to them
    # Shed for example has the origin placed at the front wall, it would not allow replanting in a very large
    # area in front of it when using just a radius.

    removedTreesProp = gvas.data.find("RemovedVegetationAssetsArray")
    splinepoints = gvas.data.find("SplineControlPointsArray")
    waterpos = gvas.data.find("WatertowerLocationArray")
    industrytype = gvas.data.find("IndustryTypeArray")
    industrypos = gvas.data.find("IndustryLocationArray")
    firewoodpos = industrypos.data[industrytype.data == firewoodDepot["type"], :]
    shedpos = industrypos.data[industrytype in shed.keys(), :]
    sandpos = gvas.data.find("SandhouseLocationArray")
    switchpos = gvas.data.find("SwitchLocationArray")
    # switchtype = gvas.data.find("SwitchTypeArray")

    if firewoodpos.size == 0:
        firewoodpos = None
    if shedpos.size == 0:
        shedpos = None
    if switchpos is not None:
        if switchpos.data.size == 0:
            switchpos = None
    # others are returned as None if not found in the savefile


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
                print("\033[{}A\033[J".format(1), end='')
                print("Please Wait...")
                import time
                import struct
                t0 = time.perf_counter()

                A = removedTreesProp.data
                B = splinepoints.data if splinepoints is not None else None
                C = waterpos.data if waterpos is not None else None
                D = firewoodpos
                E = sandpos.data if sandpos is not None else None
                F = shedpos

                # print(f"Before reset: {A.shape}")
                # print(repr(A))
                # print([struct.pack('<f', v) for v in A[0]])
                T = np.asarray(default_removed_trees, dtype=np.float32)
                R = np.asarray(better_default_removed_trees, dtype=np.float32)
                # Remove originnally cut trees from the list
                A = A[~((A[:,None,:] == T).all(-1)).any(1)]
                A = A[~((A[:,None,:] == R).all(-1)).any(1)]

                # print(f"After removing origin: {A.shape}")
                check_comp_data = (
                    B is not None or
                    C is not None or
                    D is not None or
                    E is not None or
                    F is not None
                    )
                # Check if there's enough data for comparison else give rose default trees
                if A.size == 0 or not check_comp_data:
                    A = np.vstack([T, R])
                    removedTreesProp._data = A.astype(np.float32)
                    t1 = time.perf_counter()
                    print(f"There is no tree to replant. Computation took {t1-t0:f} s.")
                    print("(Press any key to go back to previous menu)")
                    getKey()
                    print("\033[{}A\033[J".format(10), end='')
                    return None
                A_size_before = A.shape[0]

                #--- Remove hidden control points from B ---
                start = gvas.data.find("SplineControlPointsIndexStartArray").data
                end = gvas.data.find("SplineControlPointsIndexEndArray").data
                ctrl = gvas.data.find("SplineControlPointsArray").data
                def mkslice(row):
                    s = slice(row[0], row[1]+1) # end index is included
                    return np.arange(s.stop)[s]
                indexes = [mkslice(r) for r in np.vstack([start, end]).T]
                splines = [ctrl[i,:] for i in indexes]

                vstart = gvas.data.find("SplineVisibilityStartArray").data
                vend = gvas.data.find("SplineVisibilityEndArray").data
                vis = gvas.data.find("SplineSegmentsVisibilityArray").data

                vindexes = [mkslice(r) for r in np.vstack([vstart, vend]).T]
                vsplines = [vis[i] for i in vindexes]
                cleanedsplines = []
                for i, spline in enumerate(splines):
                    vspline = vsplines[i]
                    # remove control points which are not visible
                    # non visible control points appear in those cases:
                    #   - first segment non visible -> first ctrl not visible
                    #   - last segment non visible -> last ctrl not visible
                    #   - two successive non visible segments -> ctrl between them not visible
                    cleanspline = []
                    if vspline[0] :
                        cleanspline.append(spline[0])
                    if vspline[-1]:
                        cleanspline.append(spline[-1])
                    for j in range(1,spline.shape[0]-1):
                        if vspline[j-1] or vspline[j]:
                            cleanspline.append(spline[j])
                    cleanspline = np.asarray(cleanspline)
                    cleanedsplines.append(cleanspline)
                cleanedsplines = np.vstack(cleanedsplines)
                B = cleanedsplines
                #--- End of spline cleanup ---

                # Adding switch locations
                if switchpos is not None:
                    B = np.vstack([B, switchpos.data])

                #--- Spline distance check ---
                # Build buckets to reduce computation load if necessary/avoid empty buckets
                # Might need tuning
                setting_bucket_size_limit = 100 # number of ctrl pts over which we make buckets
                if B.size > setting_bucket_size_limit*3:
                    # Generate buckets
                    avx = np.mean(A[:,0])
                    avy = np.mean(A[:,1])
                    # avx = 0.  # worse load balance
                    # avy = 0.
                    nbuckets = 4
                    Distbuckets = [None]*nbuckets
                    Abuckets = [
                        A[np.logical_and(A[:,0]<avx  , A[:,1]<avy), :],
                        A[np.logical_and(A[:,0]<avx  , A[:,1]>=avy), :],
                        A[np.logical_and(A[:,0]>=avx , A[:,1]<avy),  :],
                        A[np.logical_and(A[:,0]>=avx , A[:,1]>=avy), :]
                    ]
                    ds=safeDistSplines
                    Bbuckets = [
                        B[np.logical_and(B[:,0]<ds+avx   , B[:,1]<ds+avy  ), :].T,
                        B[np.logical_and(B[:,0]<ds+avx   , B[:,1]>=-ds+avy), :].T,
                        B[np.logical_and(B[:,0]>=-ds+avx , B[:,1]<ds+avy  ), :].T,
                        B[np.logical_and(B[:,0]>=-ds+avx , B[:,1]>=-ds+avy), :].T
                    ]
                    # utilities might not need buckets
                    # if C is not None:
                    #     ds=safeDistWater
                    #     Cbuckets = [
                    #         C[np.logical_and(C[:,0]<ds+avx   , C[:,1]<ds+avy  ), :].T,
                    #         C[np.logical_and(C[:,0]<ds+avx   , C[:,1]>=-ds+avy), :].T,
                    #         C[np.logical_and(C[:,0]>=-ds+avx , C[:,1]<ds+avy  ), :].T,
                    #         C[np.logical_and(C[:,0]>=-ds+avx , C[:,1]>=-ds+avy), :].T
                    #     ]
                    # if D is not None:
                    #     ds = safeDistFirewood
                    #     Dbuckets = [
                    #         D[np.logical_and(D[:,0]<ds+avx   , D[:,1]<ds+avy  ), :].T,
                    #         D[np.logical_and(D[:,0]<ds+avx   , D[:,1]>=-ds+avy), :].T,
                    #         D[np.logical_and(D[:,0]>=-ds+avx , D[:,1]<ds+avy  ), :].T,
                    #         D[np.logical_and(D[:,0]>=-ds+avx , D[:,1]>=-ds+avy), :].T
                    #     ]
                    # if E is not None:
                    #     ds = safeDistSand
                    #     Ebuckets = [
                    #         E[np.logical_and(E[:,0]<ds+avx   , E[:,1]<ds+avy  ), :].T,
                    #         E[np.logical_and(E[:,0]<ds+avx   , E[:,1]>=-ds+avy), :].T,
                    #         E[np.logical_and(E[:,0]>=-ds+avx , E[:,1]<ds+avy  ), :].T,
                    #         E[np.logical_and(E[:,0]>=-ds+avx , E[:,1]>=-ds+avy), :].T
                    #     ]
                    # TODO: add safe distance to buildings
                    # Performance indicators
                    # stat_A = [a.shape[0] for a in Abuckets]
                    # stat_B = [b.shape[1] for b in Bbuckets]
                    # print(f"A balance: {stat_A} over {A.shape[0]} - indicator = {(np.max(stat_A)-np.min(stat_A))/np.mean(stat_A)}")
                    # print(f"B balance: {stat_B} over {B.shape[0]} - indicator = {(np.max(stat_B)-np.min(stat_B))/np.mean(stat_B)}")
                    for i in range(nbuckets):
                        a = Abuckets[i]
                        b = Bbuckets[i]
                        if a.size == 0:
                            Distbuckets[i] = np.zeros(0, dtype=bool)
                            continue
                        if b.size == 0:
                            Distbuckets[i] = np.zeros(a.shape[0], dtype=bool)
                            continue
                        # buckets might not be needed for utilities
                        # c = Cbuckets[i]
                        # d = Dbuckets[i]
                        # e = Ebuckets[i]
                        # Compute distance mask
                        # norm2
                        bdistmask = safeDistSplines  > np.min(np.sqrt(np.sum((a[:,:2,None]-b[None,:2,:])**2, axis=1)), axis=1)
                        # buckets might not be needed for utilites
                        # cdistmask = safeDistWater    > np.min(np.sqrt(np.sum((a[:,:2,None]-c[None,:2,:])**2, axis=1)), axis=1)
                        # ddistmask = safeDistFirewood > np.min(np.sqrt(np.sum((a[:,:2,None]-d[None,:2,:])**2, axis=1)), axis=1)
                        # edistmask = safeDistFirewood > np.min(np.sqrt(np.sum((a[:,:2,None]-e[None,:2,:])**2, axis=1)), axis=1)
                        # norm1 (slightly faster but maybe lower quality)
                        # bdistmask = safeDistSplines  > np.min(np.sum(np.abs(a[:,:2,None]-b[None,:2,:]), axis=1), axis=1)
                        # cdistmask = safeDistWater    > np.min(np.sum(np.abs(a[:,:2,None]-c[None,:2,:]), axis=1), axis=1)
                        # ddistmask = safeDistFirewood > np.min(np.sum(np.abs(a[:,:2,None]-d[None,:2,:]), axis=1), axis=1)
                        # edistmask = safeDistSand     > np.min(np.sum(np.abs(a[:,:2,None]-e[None,:2,:]), axis=1), axis=1)

                        # merge masks
                        Distbuckets[i] = bdistmask
                        # Distbuckets[i] = np.any(
                        #         np.vstack([bdistmask, cdistmask, ddistmask, edistmask]),
                        #         axis = 1)

                        # Keep only cut trees that are close to the tracks
                        # Abuckets[i] = a[distmask,:]
                    A = np.vstack(Abuckets) # vstack since 2D (and want to keep axis 1 size)
                    distmask = np.hstack(Distbuckets) # hstack since 1D (and want to concatenate the arrays)
                elif B.size > 0:
                    distmask = safeDistSplines  > np.min(np.sqrt(np.sum((A[:,:2,None]-B[None,:2,:])**2, axis=1)), axis=1)
                    # no buckets
                else:
                    # unlikely case where there is no ctrl pts at all
                    distmask = np.zeros(A.shape[0], dtype=bool)
                #--- End of spline dist check ---

                #--- Placeable dist checks ---
                if C is not None:
                    cdistmask = safeDistWater    > np.min(np.sqrt(np.sum((A[:,:2,None]-C[None,:2,:])**2, axis=1)), axis=1)
                    distmask = np.vstack([distmask, cdistmask])
                if D is not None:
                    ddistmask = safeDistFirewood > np.min(np.sqrt(np.sum((A[:,:2,None]-D[None,:2,:])**2, axis=1)), axis=1)
                    distmask = np.vstack([distmask, ddistmask])
                if E is not None:
                    edistmask = safeDistSand     > np.min(np.sqrt(np.sum((A[:,:2,None]-E[None,:2,:])**2, axis=1)), axis=1)
                    distmask = np.vstack([distmask, edistmask])
                if F is not None:
                    fdistmask = safeDistFirewood > np.min(np.sqrt(np.sum((A[:,:2,None]-F[None,:2,:])**2, axis=1)), axis=1)
                    distmask = np.vstack([distmask, fdistmask])
                #--- End of Placeable checks ---

                # Combine checks into one mask
                if distmask.ndim > 1:
                    distmask = distmask.any(0)

                A = A[distmask,:]

                A_size_after = A.shape[0]

                # Add originally cut trees back
                A = np.vstack([T, R, A]) # I, N, S


                # Save to gvas property
                removedTreesProp._data = A.astype(np.float32)

                t1 = time.perf_counter()
                print("\033[{}A\033[J".format(1), end='')
                print(f"{A_size_before-A_size_after} trees have been replanted. Computation took {t1-t0:f} s.")
                print("(Press any key to go back to previous menu)")
                getKey()
                print("\033[{}A\033[J".format(9), end='')
                return None

        if k == b'ESCAPE':
            print("\033[{}A\033[J".format(8), end='')
            return None

        print("\033[{}A\033[J".format(1), end='')


def editindustries(gvas):
    try:
        industrytypes = gvas.data.find("IndustryTypeArray").data
    except AttributeError:
        failedtofind("industries")
        return
    industryin1 = gvas.data.find("IndustryStorageEduct1Array").data
    industryin2 = gvas.data.find("IndustryStorageEduct2Array").data
    industryin3 = gvas.data.find("IndustryStorageEduct3Array").data
    industryin4 = gvas.data.find("IndustryStorageEduct4Array").data
    industryout1 = gvas.data.find("IndustryStorageProduct1Array").data
    industryout2 = gvas.data.find("IndustryStorageProduct2Array").data
    industryout3 = gvas.data.find("IndustryStorageProduct3Array").data
    industryout4 = gvas.data.find("IndustryStorageProduct4Array").data

    industryins = np.stack([industryin1, industryin2, industryin3, industryin4], axis=1)
    industryouts = np.stack([industryout1, industryout2, industryout3, industryout4], axis=1)

    ind = []
    for i in range(len(industrytypes)):
        if industrytypes[i] in industryInputs.keys() or industrytypes[i] in industryOutputs.keys():
            ind.append(i)
    if len(ind) == 0:
        failedtofind("industries")
        return

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:12s}",
        "{:22}",
        "{:22}",
        "{:22}",
        "{:22}",
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    n_page = len(ind)
    cur_page = 0
    while True:
        print("Select value to edit (ESCAPE to quit, ENTER to valid selection)")
        print("Use PAGE_UP and PAGE_DOWN to switch industries ({}/{})".format(cur_page + 1, n_page))
        print("")

        cur_ind = ind[cur_page]
        cur_indtype = industrytypes[cur_ind]
        print(" | ".join(formatters).format(
            industryNames[cur_indtype],
            "1",
            "2",
            "3",
            "4",
        ))
        print(dashline)

        inputstrs = []
        outputstrs = []

        for p in range(4):
            if cur_indtype in industryInputs.keys():
                ingood = industryInputs[cur_indtype][p]
                if ingood[0] is not None:
                    goodname = cargotypeTranslator[ingood[0]]
                    inputstrs.append("{:>11}: {:4}/{:4}".format(goodname, industryins[cur_ind][p], ingood[1]))
                else:
                    inputstrs.append("")
            else:
                inputstrs.append("")
            if cur_indtype in industryOutputs.keys():
                outgood = industryOutputs[cur_indtype][p]
                if outgood[0] is not None:
                    goodname = cargotypeTranslator[outgood[0]]
                    outputstrs.append("{:>11}: {:4}/{:4}".format(goodname, industryouts[cur_ind][p], outgood[1]))
                else:
                    outputstrs.append("")
            else:
                outputstrs.append("")

        if 0 == cur_line:
            line_format = formatters[0]
            for j in range(4):
                line_format += " | "
                if j == cur_col:
                    line_format += selectfmt + formatters[j+1] + "\033[0m"
                else:
                    line_format += formatters[j+1]
        else:
            line_format = " | ".join(formatters)
        print(line_format.format(
            "Inputs:",
            *inputstrs
        ))
        if 1 == cur_line:
            line_format = formatters[0]
            for j in range(4):
                line_format += " | "
                if j == cur_col:
                    line_format += selectfmt + formatters[j + 1] + "\033[0m"
                else:
                    line_format += formatters[j + 1]
        else:
            line_format = " | ".join(formatters)
        print(line_format.format(
            "Outputs:",
            *outputstrs
        ))

        k = getKey()
        if k == b'KEY_RIGHT':
            cur_col = min(3, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
        if k == b'KEY_DOWN':
            cur_line = min(1, cur_line + 1)
        if k == b'PAGE_UP':
            cur_page = max(0, cur_page - 1)
        if k == b'PAGE_DOWN':
            cur_page = min(n_page - 1, cur_page + 1)
        if k == b'RETURN':
            if cur_line == 0 and cur_indtype in industryInputs.keys():
                cur_good = industryInputs[cur_indtype][cur_col]
            elif cur_line == 1 and cur_indtype in industryOutputs.keys():
                cur_good = industryOutputs[cur_indtype][cur_col]
            else:
                cur_good = [None, 0]
            if cur_good[0] is not None:
                prompt_text = "> Enter new value or leave blank for max: "
                while True:
                    val = input(prompt_text)
                    try:
                        if val == '':
                            val = cur_good[1]
                        else:
                            val = int(val)
                    except ValueError:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid input! Enter new value: "
                        continue

                    if val < 0 or val > cur_good[1]:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid amount! Enter new value: "
                        continue

                    print("\033[{}A\033[J".format(1), end='')
                    break
                if cur_line == 0:
                    industryins[cur_ind][cur_col] = val
                else:
                    industryouts[cur_ind][cur_col] = val

        print("\033[{}A\033[J".format(7), end='')

        if k == b'ESCAPE':
            break

    for i in range(len(industryins)):
        industryin1[i] = industryins[i][0]
        industryin2[i] = industryins[i][1]
        industryin3[i] = industryins[i][2]
        industryin4[i] = industryins[i][3]
        industryout1[i] = industryouts[i][0]
        industryout2[i] = industryouts[i][1]
        industryout3[i] = industryouts[i][2]
        industryout4[i] = industryouts[i][3]
    return None


def editplacables(gvas):
    try:
        industrytypes = gvas.data.find("IndustryTypeArray").data
        industrylocations = gvas.data.find("IndustryLocationArray").data
        industryinputs1 = gvas.data.find("IndustryStorageEduct1Array").data
        industryoutputs1 = gvas.data.find("IndustryStorageProduct1Array").data
        industryoutputs2 = gvas.data.find("IndustryStorageProduct2Array").data
        industryoutputs3 = gvas.data.find("IndustryStorageProduct3Array").data
        industryoutputs4 = gvas.data.find("IndustryStorageProduct4Array").data
    except AttributeError:
        industrytypes = []
        industrylocations = []
        industryinputs1 = []
        industryoutputs1 = []
        industryoutputs2 = []
        industryoutputs3 = []
        industryoutputs4 = []
    try:
        watertowers = gvas.data.find("WatertowerTypeArray").data
        watertowerlocations = gvas.data.find("WatertowerLocationArray").data
        watertowerlevels = gvas.data.find("WatertowerWaterlevelArray").data
    except AttributeError:
        watertowers = []
        watertowerlocations = []
        watertowerlevels = []

    ind = []
    for i in range(len(industrytypes)):
        if industrytypes[i] == firewoodDepot["type"]:
            ind.append(i)

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:29}",
        "{:15}",
        "{:40}",
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    dashline = dashline[2:]
    ltot = len(ind) + len(watertowers)
    if ltot == 0:
        failedtofind("Depots or Water towers")
        return
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    while True:
        print("Select Utility to fill (ESCAPE to quit, ENTER to fill)")
        print("")
        cur_page = int(np.floor(cur_line / 10))
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Utility",
            "Input",
            "Output"
        ))
        print(dashline)
        n_line = 0
        for i in range(len(ind)):
            if np.floor(i / 10) != cur_page and split_data:
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

            namestr = industryNames[industrytypes[ind[i]]]
            curlocation = industrylocations[ind[i]]
            curx = round(curlocation[0] / 100)
            cury = round(curlocation[1] / 100)
            namestr += " {:.0f}/ {:.0f}".format(curx, cury)

            inputstr = "{:3} / {:3} Wood".format(industryinputs1[ind[i]], firewoodDepot["input"][0])
            outputstr = ''
            outputstr += "{:3} / {:3}".format(industryoutputs4[ind[i]], firewoodDepot["output"][3])
            outputstr += ", {:3} / {:3}".format(industryoutputs1[ind[i]], firewoodDepot["output"][0])
            outputstr += ", {:3} / {:3}".format(industryoutputs2[ind[i]], firewoodDepot["output"][1])
            outputstr += ", {:3} / {:3}".format(industryoutputs3[ind[i]], firewoodDepot["output"][2])

            print(line_format.format(
                namestr,
                inputstr,
                outputstr,
            ))
        for i in range(len(watertowers)):
            if np.floor((i+len(ind)) / 10) != cur_page and split_data:
                continue
            n_line += 1
            if i + len(ind) == cur_line:
                cur_col = 1
                line_format = formatters[0]
                for j in range(2):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j + 1] + "\033[0m"
                    else:
                        line_format += formatters[j + 1]
            else:
                line_format = " | ".join(formatters)

            namestr = "Watertower"
            curlocation = watertowerlocations[i]
            curx = round(curlocation[0] / 100)
            cury = round(curlocation[1] / 100)
            namestr += " @ {:.0f}/ {:.0f}".format(curx, cury)

            outputstr = "{:6.0f} / {:4}".format(watertowerlevels[i], waterTower["output"])

            print(line_format.format(
                namestr,
                "",
                outputstr,
            ))

        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(1, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1
        if k == b'RETURN':
            if cur_line in range(len(ind)):
                depotindex = ind[cur_line]
                if cur_col == 0:
                    industryinputs1[depotindex] = firewoodDepot["input"][0]
                elif cur_col == 1:
                    industryoutputs1[depotindex] = firewoodDepot["output"][0]
                    industryoutputs2[depotindex] = firewoodDepot["output"][1]
                    industryoutputs3[depotindex] = firewoodDepot["output"][2]
                    industryoutputs4[depotindex] = firewoodDepot["output"][3]
            elif cur_line in range(len(ind), len(watertowers)+len(ind)):
                towerindex = cur_line - len(ind)
                watertowerlevels[towerindex] = waterTower["output"]

        if ltot <= 10:
            print("\033[{}A\033[J".format(ltot + 4), end='')
        else:
            print("\033[{}A\033[J".format(n_line + 5), end='')

        if k == b'ESCAPE':
            return None


def exchangesheds(gvas):
    try:
        industrytypes = gvas.data.find("IndustryTypeArray").data
        industrylocations = gvas.data.find("IndustryLocationArray").data
    except AttributeError:
        failedtofind("sheds")
        return

    ind = []
    standardinds = []
    for i in range(len(industrytypes)):
        if industrytypes[i] in shed.keys():
            ind.append(i)
        if industrytypes[i] in mapIndustries:
            standardinds.append(i)
    standardindtypes = industrytypes[standardinds]
    standardlocations = industrylocations[standardinds]
    if len(ind) == 0:
        failedtofind("sheds")
        return

    cur_line = 0
    formatters = [
        "{:15}",
        "{:15}",
        "{:15}",
        "{:8}",
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    dashline = dashline[2:]
    ltot = len(ind)
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    while True:
        print("Select Shed to repaint (ESCAPE to quit, ENTER to select)")
        print("")
        cur_page = int(np.floor(cur_line / 10))
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Shed",
            "Location",
            "Near",
            "Distance",
        ))
        print(dashline)
        n_line = 0
        for i in range(len(ind)):
            if np.floor(i / 10) != cur_page and split_data:
                continue
            n_line += 1
            if i == cur_line:
                line_format = selectfmt + formatters[0] + "\033[0m | "
                line_format += " | ".join(formatters[1:])
            else:
                line_format = " | ".join(formatters)

            namestr = industryNames[industrytypes[ind[i]]]
            curlocation = industrylocations[ind[i]]
            curx = round(curlocation[0] / 100)
            cury = round(curlocation[1] / 100)
            locstr = "{:>6}/{:>6}".format(curx, cury)

            closest = getclosest(curlocation, standardlocations)
            closestname = industryNames[standardindtypes[closest[0]]]
            closestdist = "{:>6}m".format(int(closest[1]/100))

            print(line_format.format(
                namestr,
                locstr,
                closestname,
                closestdist
            ))

        k = getKey()
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1
        if k == b'RETURN':
            curshedtype = industrytypes[ind[cur_line]]
            choices = []
            for shedtype in shed.keys():
                choices.append(shedtype)
            cursor = choices.index(curshedtype)
            while True:
                typeselection = "> Choose new paint:"
                for option in range(len(choices)):
                    if option == cursor:
                        typeselection += "  " + selectfmt + shed[choices[option]] + "\033[0m"
                    else:
                        typeselection += "  " + shed[choices[option]]
                print(typeselection)

                k2 = getKey()
                print("\033[{}A\033[J".format(1), end='')

                if k2 == b'KEY_RIGHT':
                    cursor = min(len(choices) - 1, cursor + 1)
                if k2 == b'KEY_LEFT':
                    cursor = max(0, cursor - 1)

                if k2 == b'RETURN':
                    industrytypes[ind[cur_line]] = choices[cursor]
                    break

                if k2 == b'ESCAPE':
                    break

        if ltot <= 10:
            print("\033[{}A\033[J".format(ltot + 4), end='')
        else:
            print("\033[{}A\033[J".format(n_line + 5), end='')

        if k == b'ESCAPE':
            return None


def playerteleport(gvas):
    try:
        playernames = gvas.data.find("playernamearray").data
        playerlocs = gvas.data.find("playerlocationarray").data
    except AttributeError:
        failedtofind("players")
        return

    try:
        industrytypes = gvas.data.find("IndustryTypeArray").data
        industrylocs = gvas.data.find("IndustryLocationArray").data
        industryrots = gvas.data.find("IndustryRotationArray").data
    except AttributeError:
        industrytypes = []
        industrylocs = []
        industryrots = []

    if len(industrytypes) > 0:
        standardinds = []
        for i in range(len(industrytypes)):
            if industrytypes[i] in mapIndustries:
                standardinds.append(i)
        standardindtypes = industrytypes[standardinds]
        standardindlocs = industrylocs[standardinds]
    else:
        standardindtypes = []
        standardindlocs = []

    try:
        framenumbers = gvas.data.find("FrameNumberArray").data
        framenames = gvas.data.find("FrameNameArray").data
        frametypes = gvas.data.find("FrameTypeArray").data
        framelocs = gvas.data.find("FrameLocationArray").data
        framerots = gvas.data.find("FrameRotationArray").data
    except AttributeError:
        framenumbers = []
        framenames = []
        frametypes = []
        framelocs = []
        framerots = []

    cur_line = 0
    ltot = len(playernames)
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    formatters = [
        "{:35}",
        "{:18}",
        "{:15}",
        "{:>10}",
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    dashline = dashline[2:]

    while True:
        print("Select a player to teleport (ESCAPE to quit, ENTER to select)")
        cur_page = int(np.floor(cur_line / 10))
        n_line = 3
        if split_data:
            print("Use PAGE UP and PAGE DOWN to scroll pages ({}/{})".format(cur_page + 1, n_page))
            n_line += 1
        print(" | ".join(formatters).format(
            "Player",
            "Location in m",
            "Near",
            "Distance  ",
        ))
        print(dashline)

        for i in range(ltot):
            if np.floor(i / 10) == cur_page:
                if i == cur_line:
                    line_format = selectfmt + formatters[0] + "\033[0m"
                    for j in range(len(formatters) - 1):
                        line_format += " | " + formatters[j + 1]
                else:
                    line_format = " | ".join(formatters)
                cur_name = playernames[i]
                cur_loc = playerlocs[i]

                cur_x = int(round(cur_loc[0] / 100))
                cur_y = int(round(cur_loc[1] / 100))
                cur_z = int(round(cur_loc[2] / 100))
                locstr = "{:.0f}/{:.0f}/{:.0f}".format(cur_x, cur_y, cur_z)

                closest = getclosest(cur_loc, standardindlocs)
                clostr = industryNames[standardindtypes[closest[0]]]
                diststr = "{:.2f}m".format(closest[1]/100)

                if dev_version and cur_line == 0 and i == 0:  # DEV Tool to find relative positions
                    closest = getclosest(cur_loc, industrylocs)
                    clostr = industryNames[industrytypes[closest[0]]]
                    diststr = "{:.2f}m".format(closest[1]/100)
                    closestpos = industrylocs[closest[0]]
                    closestrot = industryrots[closest[0]]
                    print("Closest Ind: {} in {:.0f}cm".format(industrytypes[closest[0]], closest[1]))
                    print("Player vals: {}".format(cur_loc))
                    print("Target vals: {} {}".format(closestpos, closestrot))
                    print("Relative:    [Dir {:.1f}, Dist {:.1f}, Height {:.1f}], Rot {:.1f}".format(
                        *getrelative(cur_loc, 0, closestpos, closestrot)))
                    n_line += 4

                if dev_version and cur_line == 0 and i == 0:  # DEV Tool to find relative positions
                    closest = getclosest(cur_loc, framelocs)
                    clostr = gettypedescription(frametypes[closest[0]], 1)
                    diststr = "{:.2f}m".format(closest[1]/100)
                    closestpos = framelocs[closest[0]]
                    closestrot = framerots[closest[0]]
                    print("Closest car: {} in {:.0f}cm".format(frametypes[closest[0]], closest[1]))
                    print("Player vals: {}".format(cur_loc))
                    print("Target vals: {} {}".format(closestpos, closestrot))
                    print("Relative:    [Dir {:.1f}, Dist {:.1f}, Height {:.1f}], Rot {:.1f}".format(
                        *getrelative(cur_loc, 0, closestpos, closestrot)))
                    n_line += 4

                n_line += 1

                print(line_format.format(
                    cur_name,
                    locstr,
                    clostr,
                    diststr,
                ))

        k = getKey()
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1

        if k == b'RETURN':
            cursor = 0
            options = [
                "Spawn.",
                "Industry...",
                "Firewood Depot...",
                "Caboose...",
                "other Player..."
            ]
            while True:
                prompt_line = "Teleport to: "
                for c in range(len(options)):
                    if c == cursor:
                        prompt_line += selectfmt + " " + options[c]
                    else:
                        prompt_line += " \033[0m" + options[c]
                prompt_line += " \033[0m"
                print(prompt_line)

                k2 = getKey()
                print("\033[1A\033[J", end='')
                if k2 == b'KEY_RIGHT':
                    cursor = min(cursor + 1, len(options) - 1)
                if k2 == b'KEY_LEFT':
                    cursor = max(0, cursor - 1)
                if k2 == b'RETURN':
                    if cursor == 0:
                        playerlocs[cur_line] = getplayertppos(0)
                        break  # move player to start and exit destination type sel
                    else:
                        list = []
                        listloc = []
                        listrot = []
                        if cursor == 1:
                            listname = "Industry"
                            for i in range(len(industrytypes)):
                                if industrytypes[i] in mapIndustries:
                                    list.append(industrytypes[i])
                                    listloc.append(industrylocs[i])
                                    listrot.append(industryrots[i])
                        elif cursor == 2:
                            listname = "Firewood Depot"
                            for i in range(len(industrytypes)):
                                if industrytypes[i] == firewoodDepot["type"]:
                                    list.append(industrytypes[i])
                                    listloc.append(industrylocs[i])
                                    listrot.append(industryrots[i])
                        elif cursor == 3:
                            listname = "Caboose"
                            for i in range(len(frametypes)):
                                if frametypes[i] in player_teleport_pts.keys():
                                    cabooseid = getidentifier(frametypes[i], framenames[i], framenumbers[i],
                                                              framelocs[i], onlynear=True)
                                    if cabooseid[1] == "":
                                        list.append(cabooseid[0])
                                    else:
                                        list.append(cabooseid[1])
                                    listloc.append(framelocs[i])
                                    listrot.append(framerots[i])
                        elif cursor == 4:
                            listname = "Player"
                            for i in range(len(playernames)):
                                if playernames[i] != playernames[cur_line]:
                                    list.append(playernames[i])
                                    listloc.append(playerlocs[i])
                                    # not building listrot since 220121, player rotation isn't saved
                        else:
                            break  # to make the IDE happy and prevent anything weird
                        if len(list) == 0:  # if there is nothing to choose from, abort
                            failedtofind("teleport targets")
                            break

                        namelist = []
                        loclist = []
                        nearlist = []
                        distlist = []
                        for j in range(len(list)):
                            cur_x = int(round(listloc[j][0] / 100))
                            cur_y = int(round(listloc[j][1] / 100))
                            cur_z = int(round(listloc[j][2] / 100))
                            loclist.append("{:.0f}/{:.0f}/{:.0f}".format(cur_x, cur_y, cur_z))
                            if cursor == 1 or cursor == 2:  # Name is an Industry or Firewood Depot
                                namelist.append(industryNames[list[j]])
                            elif cursor == 3:               # Name is Caboose
                                namelist.append(list[j])
                            elif cursor == 4:               # Name is player
                                namelist.append(list[j])
                            if cursor == 1:  # Is industry, no need to find nearest
                                nearlist.append("")
                                distlist.append("")
                            else:            # Nearest Industry
                                closest = getclosest(listloc[j], standardindlocs)
                                nearlist.append(industryNames[standardindtypes[closest[0]]])
                                distlist.append("{:.2f}m".format(closest[1] / 100))

                        cur_line2 = 0
                        ltot2 = len(list)
                        if ltot2 > 10:
                            split_data2 = True
                            n_page2 = np.ceil(ltot2/10)
                        else:
                            split_data2 = False
                            n_page2 = 1
                        print("\033[{}A\033[J".format(n_line), end='')
                        formatters2 = [
                            "{:35}",
                            "{:18}",
                            "{:15}",
                            "{:>10}",
                        ]
                        dashline2 = ''
                        for i in formatters:
                            dashline2 += "---" + len(i.format('')) * "-"
                        dashline2 = dashline2[2:]
                        while True:
                            n_line = 4
                            print("Teleport " + selectfmt + playernames[cur_line] + "\033[0m to ...")
                            print("Select destination (ESCAPE to quit, ENTER to select)")
                            cur_page2 = np.floor(cur_line2/10)
                            if split_data2:
                                print("Use PAGE UP and PAGE DOWN to scroll pages ({}/{})".format(cur_page + 1, n_page))
                                n_line += 1
                            print(" | ".join(formatters2).format(
                                listname,
                                "Location",
                                "Near",
                                "Distance",
                            ))
                            print(dashline2)
                            for i in range(len(list)):
                                if np.floor(i/10) == cur_page2:
                                    if i == cur_line2:
                                        line_format = selectfmt + formatters2[0] + "\033[0m | "
                                        line_format += " | ".join(formatters2[1:])
                                    else:
                                        line_format = " | ".join(formatters2)
                                    print(line_format.format(
                                        namelist[i],
                                        loclist[i],
                                        nearlist[i],
                                        distlist[i],
                                    ))
                                    n_line += 1

                            k3 = getKey()
                            print("\033[{}A\033[J".format(n_line), end='')
                            n_line = 1
                            if k3 == b'KEY_UP':
                                cur_line2 = max(0, cur_line2 - 1)
                            if k3 == b'KEY_DOWN':
                                cur_line2 = min(cur_line2 + 1, ltot2 - 1)
                            if k3 == b'PAGE_UP':
                                if cur_page2 < n_page2 - 1 and split_data2:
                                    cur_page2 -= 1
                                    cur_line2 = cur_page2 * 10
                                else:
                                    cur_line2 = 0
                            if k3 == b'PAGE_DOWN':
                                if cur_page2 > 0 and split_data2:
                                    cur_page2 += 1
                                    cur_line2 = cur_page2 * 10
                                else:
                                    cur_line2 = ltot2 - 1
                            if k3 == b'ESCAPE':
                                break
                            if k3 == b'RETURN':
                                if cursor == 4:  # if it's a player, just copy values
                                    playerlocs[cur_line] = listloc[cur_line2]
                                else:            # else get the absolute position that's relative to the target
                                    if cursor == 3:  # for cabooses replace name with type
                                        tptype = "caboose"
                                    else:
                                        tptype = list[cur_line2]
                                    playerlocs[cur_line] = getplayertppos(tptype, listloc[cur_line2], listrot[cur_line2])
                                break  # exit destination sel
                        n_line -= 2
                        break  # exit destination type sel, always happens after leaving destination sel

                if k2 == b'ESCAPE':
                    break  # exit destination type sel

        print("\033[{}A\033[J".format(n_line), end='')
        if k == b'ESCAPE':
            break  # exit menu


def playerXpMoney(gvas):
    player_ids = gvas.data.find("playeridarray").data
    player_names = gvas.data.find("playernamearray").data
    player_money = gvas.data.find("playermoneyarray").data
    player_xp = gvas.data.find("playerxparray").data
    cur_col = 0
    cur_line = 0
    ltot = len(player_names)
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    formatters = [
        "{:<35}",
        "{:<20}",
        "{:>9}",
        "{:>9}",
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    dashline = dashline[2:]

    while True:
        print("Select a field to edit (ESCAPE to quit, ENTER to valid selection)")
        cur_page = int(np.floor(cur_line / 10))
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Player name",
            "Steam ID 64",
            "XP",
            "Money"
        ))
        print(dashline)

        n_line = 0
        for i in range(len(player_names)):
            if np.floor(i / 10) != cur_page and split_data:
                continue
            n_line += 1
            line_format = " | ".join([*formatters[:2], ""])
            if i == cur_line:
                if cur_col == 0:
                    line_format += selectfmt + formatters[2] + "\033[0m | " + formatters[3]
                else:
                    line_format += formatters[2] + " | " + selectfmt + formatters[3] + "\033[0m"
            else:
                line_format += " | ".join(formatters[2:])

            line = line_format.format(
                player_names[i],
                player_ids[i],
                player_xp[i],
                player_money[i],
            )
            print(line)
        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(1, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1

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

                data = [player_xp, player_money]
                data[cur_col][cur_line] = val
                print("\033[{}A\033[J".format(n_rline), end='')
                break

        if len(player_names) <= 10:
            print("\033[{}A\033[J".format(len(player_names) + 3), end='')
        else:
            print("\033[{}A\033[J".format(n_line + 4), end='')

        if k == b'ESCAPE':
            return None


def renameStockMenu(gvas):
    framenumbers = gvas.data.find("FrameNumberArray").data
    framenames = gvas.data.find("FrameNameArray").data
    frametypes = gvas.data.find("FrameTypeArray").data

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:<32s}",
        "{:<32s}",
        "{:<32s}",
    ]
    ltot = len(frametypes)
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    while True:
        print("Select field to edit (ESCAPE to quit, ENTER to valid selection)")
        print("Use <br> to create multiple line values where applicable.")
        print("Sanity checks are enabled. To ignore limitation start your input with \i")
        cur_page = int(np.floor(cur_line / 10))
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
            if np.floor(i / 10) != cur_page and split_data:
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

            print(line_format.format(
                gettypedescription(frametypes[i]),
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
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1

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

    indtypes = gvas.data.find("IndustryTypeArray").data
    indlocs = gvas.data.find("IndustryLocationArray").data

    standardtypes = []
    standardlocs = []
    for index in range(len(indtypes)):
        if indtypes[index] in mapIndustries:
            standardtypes.append(indtypes[index])
            standardlocs.append(indlocs[index])

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:^6s}",
        "{:<10s}",
        "{:<25s}",
        "{:^17s}",
        "{:>18s}",
        "{:^9s}",
        "{:^9s}"
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    dashline = dashline[2:]

    min_height = 1000.
    status_str = "⬤"

    ltot = len(frametypes)
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    while True:
        n_line = 0
        print("Select method (ESCAPE to quit, ENTER to valid selection)")
        n_line += 1
        cur_page = int(np.floor(cur_line / 10))

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
            "Number/Name",
            "Location",
            "Near",
            "Respawn",
            "Yeet it"
        ))
        print(dashline)
        n_line += 2

        for i in range(len(frametypes)):
            if np.floor(i / 10) != cur_page and split_data:
                continue

            if i == cur_line:
                line_format = " | ".join(formatters[:5])
                for j in range(2):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j + 5] + "\033[0m"
                    else:
                        line_format += formatters[j + 5]
            else:
                line_format = " | ".join(formatters)

            identifier = getidentifier(frametypes[i], framenames[i], framenumbers[i], framelocs[i], True, standardtypes,
                                       standardlocs)

            if framelocs[i, 2] < min_height:
                line_format = line_format.split(" | ")
                line_format[0] = "\033[1;41m" + line_format[0] + "\033[0m"
                line_format = " | ".join(line_format)

            print(line_format.format(
                status_str,
                *identifier,
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
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1

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
                        zoffset = spawnZOffset.get(
                            frametypes[cur_line],
                            spawnPositions[spawn_idx][2]
                        )
                        framelocs[cur_line][2] = zoffset
                        framerots[cur_line] = spawnOrientations[spawn_idx]
                        moved_something = True
            elif cur_col == 1:
                # YEET IT !
                print("The frame will be yeeted close to the spawn point.")
                ans = input("Type 'YES' to proceed (at your own risks): ")
                n_line += 2
                if ans == "YES":
                    global n_yeeted

                    framelocs[cur_line] = [
                        720.+(n_yeeted%3)*540.,
                        -2503-2100.-int(n_yeeted/3)*1500,
                        10300.
                        ]
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
    framesandamount = gvas.data.find("SanderAmountArray").data

    ind = []
    for i in range(len(frametypes)):
        if (frametypes[i] in waterBoiler.keys()) or (frametypes[i] in waterReserves.keys()) or \
                (frametypes[i] in firewoodReserves.keys() or frametypes[i] in sandLevel.keys()):
            ind.append(i)

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:<48s}",
        "{:>12}",
        "{:>11}",
        "{:>11}",
        "{:>4}"
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    dashline = dashline[2:]
    ltot = len(ind)
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    while True:
        print("Select value to edit (ESCAPE to quit, ENTER to valid selection)")
        print("Enter nothing to fill up, or type in an amount.")
        cur_page = int(np.floor(cur_line / 10))
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Engine / Tender",
            "Water Boiler",
            "Water Tank",
            "Firewood",
            "Sand",
        ))
        print(dashline)
        n_line = 0
        for i in range(len(ind)):
            if np.floor(i / 10) != cur_page and split_data:
                continue
            n_line += 1
            if i == cur_line:
                line_format = formatters[0]
                for j in range(4):
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

            namestr = "{:<10s}:".format(gettypedescription(frametype, 1))
            if not num == '':
                namestr += " {:>4}".format(num.split("<br>")[0].strip())
            if not nam == '':
                namestr += " " + nam.split("<br>")[0].strip()
            namestr = namestr[:48]

            if frametype in waterBoiler.keys():
                waterboilerstr = "{:.0f} / {:4}".format(frameboilerwater[ind[i]], waterBoiler[frametype])
            else:
                waterboilerstr = ''

            if frametype in waterReserves.keys():
                waterreservestr = "{:.0f} / {:4}".format(frametenderwater[ind[i]], waterReserves[frametype])
            else:
                waterreservestr = ''

            if frametype in firewoodReserves.keys():
                firewoodstr = "{:.0f} / {:4}".format(frametenderfuel[ind[i]], firewoodReserves[frametype])
            else:
                firewoodstr = ''

            if frametype in sandLevel.keys():
                sandstr = "{:.0f}%".format(framesandamount[ind[i]])
            else:
                sandstr = ''

            print(line_format.format(
                namestr,
                waterboilerstr,
                waterreservestr,
                firewoodstr,
                sandstr
            ))
        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(3, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1

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

            elif cur_col == 3 and curframetype in sandLevel.keys():
                prompt_text = "> Enter new value or leave blank for max: "
                while True:
                    val = input(prompt_text)
                    try:
                        if val == '':
                            val = sandLevel[curframetype]
                        else:
                            val = float(val)
                    except ValueError:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid input! Enter new value: "
                        continue

                    if val < 0 or val > sandLevel[curframetype]:
                        print("\033[{}A\033[J".format(1), end='')
                        prompt_text = "> Invalid amount! Enter new value: "
                        continue

                    framesandamount[ind[cur_line]] = val
                    print("\033[{}A\033[J".format(1), end='')
                    break

        if ltot <= 10:
            print("\033[{}A\033[J".format(ltot + 4), end='')
        else:
            print("\033[{}A\033[J".format(n_line + 5), end='')

        if k == b'ESCAPE':
            return None


def editattachmentmenu(gvas):
    framenumbers = gvas.data.find("FrameNumberArray").data
    framenames = gvas.data.find("FrameNameArray").data
    frametypes = gvas.data.find("FrameTypeArray").data
    framestacks = gvas.data.find("SmokestackTypeArray").data
    framelights = gvas.data.find("HeadlightTypeArray").data

    ind = []
    for i in range(len(frametypes)):
        if frametypes[i] in availableHeadlights.keys() or frametypes[i] in availableSmokestacks.keys():
            ind.append(i)

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:<50s}",
        "{:>10}",
        "{:>10}",
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    dashline = dashline[2:]
    ltot = len(ind)
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    while True:
        print("Select field to edit (ESCAPE to quit, ENTER to valid selection)")
        print("")
        cur_page = int(np.floor(cur_line / 10))
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Engine/Tender",
            "Smokestack",
            "Headlight"
        ))
        print(dashline)
        n_line = 0
        for i in range(len(ind)):
            if np.floor(i / 10) != cur_page and split_data:
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
            stack = framestacks[ind[i]]
            light = framelights[ind[i]]

            num = '' if num is None else num
            nam = '' if nam is None else nam

            namestr = "{:<10s}:".format(gettypedescription(frametype, 1))
            if not num == '':
                namestr += " " + num.split("<br>")[0].strip()
            if not nam == '':
                namestr += " " + nam.split("<br>")[0].strip()
            namestr = namestr[:48]

            if frametype in availableSmokestacks.keys():
                if availableSmokestacks[frametype] > 1:
                    stackstr = "{}  ( {} )".format(stack, availableSmokestacks[frametype])
                else:
                    stackstr = "{}  (fix)".format(stack)
            else:
                stackstr = ''

            if frametype in availableHeadlights.keys():
                if availableHeadlights[frametype] > 1:
                    lightstr = "{}  ( {} )".format(light, availableHeadlights[frametype])
                else:
                    lightstr = "{}  (fix)".format(light)
            else:
                lightstr = ''

            print(line_format.format(
                namestr,
                stackstr,
                lightstr
            ))
        k = getKey()

        if k == b'KEY_RIGHT':
            cur_col = min(1, cur_col + 1)
        if k == b'KEY_LEFT':
            cur_col = max(0, cur_col - 1)
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1

        if k == b'RETURN':
            curtype = frametypes[ind[cur_line]]
            if cur_col == 0 and curtype in availableSmokestacks.keys():
                choices = []
                for option in range(1, availableSmokestacks[curtype] + 1):
                    choices.append(option)
                curstack = framestacks[ind[cur_line]] - 1
                try:
                    cursor = choices.index(curstack) + 1
                except ValueError:
                    cursor = 0
                # cursor = curstack if curstack + 1 in choices else 0
                while True:
                    typeselection = "> Choose new Smokestack:"
                    for option in range(len(choices)):
                        if option == cursor:
                            typeselection += "  " + selectfmt + " {} \033[0m".format(choices[option])
                        else:
                            typeselection += "   {} ".format(choices[option])
                    print(typeselection)

                    k = getKey()
                    print("\033[{}A\033[J".format(1), end='')

                    if k == b'KEY_RIGHT':
                        cursor = min(len(choices) - 1, cursor + 1)
                    if k == b'KEY_LEFT':
                        cursor = max(0, cursor - 1)

                    if k == b'RETURN':
                        framestacks[ind[cur_line]] = choices[cursor]
                        break

                    if k == b'ESCAPE':
                        break

            elif cur_col == 1 and curtype in availableHeadlights.keys():
                choices = []
                for option in range(1, availableHeadlights[curtype] + 1):
                    choices.append(option)
                curlight = framelights[ind[cur_line]] - 1
                try:
                    cursor = choices.index(curlight) + 1
                except ValueError:
                    cursor = 0
                # cursor = curlight if curlight + 1 in choices else 0
                while True:
                    typeselection = "> Choose new Headlight:"
                    for option in range(len(choices)):
                        if option == cursor:
                            typeselection += "  " + selectfmt + " {} \033[0m".format(choices[option])
                        else:
                            typeselection += "   {} ".format(choices[option])
                    print(typeselection)

                    k = getKey()
                    print("\033[{}A\033[J".format(1), end='')

                    if k == b'KEY_RIGHT':
                        cursor = min(len(choices) - 1, cursor + 1)
                    if k == b'KEY_LEFT':
                        cursor = max(0, cursor - 1)

                    if k == b'RETURN':
                        framelights[ind[cur_line]] = choices[cursor]
                        break

                    if k == b'ESCAPE':
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
    framelocations = gvas.data.find("FrameLocationArray").data

    indtypes = gvas.data.find("IndustryTypeArray").data
    indlocs = gvas.data.find("IndustryLocationArray").data

    standardtypes = []
    standardlocs = []
    for index in range(len(indtypes)):
        if indtypes[index] in mapIndustries:
            standardtypes.append(indtypes[index])
            standardlocs.append(indlocs[index])

    ind = []
    for i in range(len(frametypes)):
        if frametypes[i] in frametypeCargoLimits.keys():
            ind.append(i)

    cur_col = 0
    cur_line = 0
    formatters = [
        "{:^8}",
        "{:<40}",
        "{:>18}",
        "{:<12}",
        "{:>6}",
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    dashline = dashline[2:]

    ltot = len(ind)
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    while True:
        print("Select value to edit (ESCAPE to quit, ENTER to valid selection)")
        print("Empty fields mean this wagon hasn't been used yet")
        cur_page = int(np.floor(cur_line / 10))
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
        print(" | ".join(formatters).format(
            "Type",
            "Number / Name",
            "Near",
            "Cargo",
            "Amount"
        ))
        print(dashline)
        n_line = 0
        for i in range(len(ind)):
            if np.floor(i / 10) != cur_page and split_data:
                continue
            n_line += 1
            if i == cur_line:
                line_format = " | ".join(formatters[:3])
                for j in range(2):
                    line_format += " | "
                    if j == cur_col:
                        line_format += selectfmt + formatters[j + 3] + "\033[0m"
                    else:
                        line_format += formatters[j + 3]
            else:
                line_format = " | ".join(formatters)

            j = ind[i]
            cargo = framecargotypes[j]

            identifier = getidentifier(frametypes[j], framenames[j], framenumbers[j], framelocations[j], True,
                                       standardtypes, standardlocs, True)

            if cargo in cargotypeTranslator.keys():
                cargostr = cargotypeTranslator[cargo]
            elif cargo is None:
                cargostr = cargotypeTranslator["empty"]
            else:
                cargostr = cargotypeTranslator["default"]

            if cargo is not None:
                amount = framecargoamounts[j]
                amountstr = "{}/{}".format(amount, frametypeCargoLimits[frametypes[j]][cargo])
            else:
                amountstr = ''

            print(line_format.format(
                *identifier,
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
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1

        if k == b'RETURN':
            curframetype = frametypes[ind[cur_line]]
            curframecargo = framecargotypes[ind[cur_line]]
            if cur_col == 0:
                choices = [None, ]
                for cargotype in frametypeCargoLimits[curframetype].keys():
                    choices.append(cargotype)
                cursor = choices.index(curframecargo)
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
                        cursor = min(len(choices)-1, cursor + 1)
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


def changestockmenu(gvas):
    framenumbers = gvas.data.find("FrameNumberArray").data
    framenames = gvas.data.find("FrameNameArray").data
    frametypes = gvas.data.find("FrameTypeArray").data
    framebrakes = gvas.data.find("BrakeValueArray").data
    framelocs = gvas.data.find("FrameLocationArray").data
    framecouplingfront = gvas.data.find("CouplerFrontStateArray").data
    framecouplingrear = gvas.data.find("CouplerRearStateArray").data
    framecargotypes = gvas.data.find("FreightTypeArray").data
    framecargoamounts = gvas.data.find("FreightAmountArray").data

    indtypes = gvas.data.find("IndustryTypeArray").data
    indlocs = gvas.data.find("IndustryLocationArray").data

    standardtypes = []
    standardlocs = []
    for index in range(len(indtypes)):
        if indtypes[index] in mapIndustries:
            standardtypes.append(indtypes[index])
            standardlocs.append(indlocs[index])

    cur_line = 0
    formatters = [
        "{:^10}",
        "{:<40}",
        "{:>18}",
        "{:<16}",
    ]
    dashline = ''
    for i in formatters:
        dashline += "---" + len(i.format('')) * "-"
    dashline = dashline[2:]

    ind = []
    for i in range(len(frametypes)):
        if frametypes[i] in frametypeExchangeable:
            ind.append(i)

    ltot = len(ind)
    if ltot > 10:
        split_data = True
        n_page = int(np.ceil(ltot / 10))
    else:
        split_data = False
        n_page = 1
    while True:
        print("Select flatcar (ESCAPE to quit, ENTER to valid selection)")
        supported_names = "Only supported types are: "
        for flatcar in frametypeExchangeable:
            supported_names += gettypedescription(flatcar, 1) + ", "
        print(supported_names[:-2])
        n_line = 2
        cur_page = int(np.floor(cur_line / 10))
        if split_data:
            print("Use PAGE_UP and PAGE_DOWN to switch page ({}/{})".format(cur_page + 1, n_page))
            n_line += 1
        print(" | ".join(formatters).format(
            "Type",
            "Number / Name",
            "Near",
            "Cargo"
        ))
        print(dashline)
        n_line += 2

        for i in range(ltot):
            if np.floor(i / 10) != cur_page and split_data:
                continue

            if i == cur_line:
                line_format = selectfmt + formatters[0] + "\033[0m | "
                line_format += " | ".join(formatters[1:])
            else:
                line_format = " | ".join(formatters)

            j = ind[i]
            frametype = frametypes[ind[i]]

            identifier = getidentifier(frametype, framenames[j], framenumbers[j], framelocs[j], False,
                                       standardtypes, standardlocs, True)

            curcargotype = framecargotypes[ind[i]]
            if curcargotype is None:
                cargostr = cargotypeTranslator[None]
            else:
                curcargoamount = framecargoamounts[ind[i]]
                if curcargoamount == 0:
                    cargostr = "Last: " + cargotypeTranslator[curcargotype]
                else:
                    cargostr = "{:2}/{:2} ".format(curcargoamount, frametypeCargoLimits[frametype][curcargotype]) + \
                        cargotypeTranslator[curcargotype]

            print(line_format.format(
                *identifier,
                cargostr
            ))
            n_line += 1
        k = getKey()
        if k == b'KEY_UP':
            cur_line = max(0, cur_line - 1)
        if k == b'KEY_DOWN':
            cur_line = min(cur_line + 1, ltot - 1)
        if k == b'PAGE_UP':
            if split_data and cur_page > 0:
                cur_page -= 1
                cur_line = cur_page * 10 + 9
            else:
                cur_line = 0
        if k == b'PAGE_DOWN':
            if split_data and cur_page < n_page - 1:
                cur_page += 1
                cur_line = cur_page * 10
            else:
                cur_line = ltot - 1

        if k == b'RETURN':
            curframetype = frametypes[ind[cur_line]]
            choices = []
            for frametype in frametypeExchangeable:
                choices.append(frametype)
            cursor = choices.index(curframetype)
            while True:
                typeselection = "> Choose new type:"
                for option in range(len(choices)):
                    if option == cursor:
                        typeselection += "  " + selectfmt + gettypedescription(choices[option], 1) + "\033[0m"
                    else:
                        typeselection += "  " + gettypedescription(choices[option], 1)
                print(typeselection)

                k = getKey()
                print("\033[{}A\033[J".format(1), end='')

                if k == b'KEY_RIGHT':
                    cursor = min(len(choices)-1, cursor + 1)
                if k == b'KEY_LEFT':
                    cursor = max(0, cursor - 1)

                if k == b'RETURN':
                    newtype = choices[cursor]
                    if not curframetype == newtype:
                        frametypes[ind[cur_line]] = newtype
                        framecargotypes[ind[cur_line]] = None
                        framecargoamounts[ind[cur_line]] = 0
                    break

                if k == b'ESCAPE':
                    break

        if ltot <= 10:
            print("\033[{}A\033[J".format(n_line), end='')
        else:
            print("\033[{}A\033[J".format(n_line), end='')

        if k == b'ESCAPE':
            return None


def mainStockMenu(gvas):
    options = [
        ("Rename", renameStockMenu),
        ("Respawn", teleportStockMenu),
        ("Cargo", cargoStockMenu),
        ("Locomotive Restock", engineStockMenu),
        ("Change Attachments", editattachmentmenu),
        ("Replace Flatcar Types", changestockmenu),
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
    filename = selectSaveFile('')
    print(filename)
    submenu = mainMenu()
    print(submenu)
    # playerMenu() # needs a gvas !
