import numpy as np

player_teleport_ref = {
    'shop_east': ([
                      [372.28885, -2242.27, 10182.059],
                      [372.29062, -3640.885, 10182.301]
                  ], 10, 0.00085449),
    'shop_west': ([
                      [2163.643, -3640.9148, 10182.186],
                      [2160.5266, -1800.1119, 10182.296]
                  ], 10),
    'freight_east': ([
                         [3714.635, 7211.3237, 10206.743],
                         [3714.853, 10954.901, 10206.743]
                     ], 10, 179.98926),
    'freight_north': ([
                          [3789.4954, 11303.7, 10206.743],
                          [5520.617, 11300.044, 10206.496]
                      ], 10, 89.88441),
    'freight_west': ([
                         [5601.0693, 10933.228, 10206.496],
                         [5601.2134, 6224.057, 10206.743]
                     ], 15, 0.01278686),
    'freight_south': ([
                          [5234.722, 7173.5503, 10206.713],
                          [4093.9934, 7179.2866, 10206.743]
                      ], 5, -90.284325),
}

location_names = {
    ''
}

player_teleport_pts = {  # keys referring to industry types
    # Absolute positions: [False, [x, y, z], r]
    # Relative positions: [True, [rel dir, rel dist, rel z], rel r]
    0: [False, [338.8, -3430.9, 10182.3], 0.0],  # Spawn point
    1: [True, [68.5, 4385.4, 196.7], -90.0],  # Logging Camp
    2: [True, [228.2, 5497.6, -11.2], 45.0],  # Sawmill
    3: [True, [8.8, 3622.8, 191.9], -145.0],  # Smelter
    4: [True, [296.4, 3312.7, 220.2], 155.0],  # Ironworks
    5: [True, [226.1, 893.9, 340.2], 120.0],  # Oilfield
    6: [True, [309.9, 2969.6, 272.7], 135.0],  # Refinery
    7: [True, [267.7, 2931.5, -233.6], 135.0],  # Coal mine
    8: [True, [92.5, 1885.9, 220.2], 255.0],  # Iron mine
    9: [True, [-163.2, 3160.8, 206.7], 30.0],  # Freight Depot
    10: [True, [-62.3, 531.1, 178.9], 56.0],  # Firewood Depot
}


def getplayertppos(indtype, indpos=None, indrot=None):
    tpdata = player_teleport_pts[indtype]

    if tpdata[0]:
        reldir, reldist, relz = tpdata[1]
        newpos = [0, 0, 0]
        alpha = reldir + indrot[1]
        deltax = np.cos(np.radians(alpha)) * reldist
        deltay = np.sin(np.radians(alpha)) * reldist
        newpos[0] = indpos[0] + deltax
        newpos[1] = indpos[1] + deltay
        newpos[2] = indpos[2] + relz + 1.0  # just add a cm to avoid rdg errors sticking you into ground
        newrot = indrot[1] + tpdata[2]
        while newrot > 180:
            newrot -= 360
        while newrot < -180:
            newrot += 360
    else:
        newpos = tpdata[1]
        newrot = tpdata[2]
    return newpos, newrot


def getdistfast(pos1, pos2):
    dist = np.sum((pos2-pos1)**2)
    return dist


def getdistance(pos1, pos2):
    dist = np.linalg.norm(pos2 - pos1)
    return dist


def getclosest(pos, poslist):
    # Compares a point to a list of points and returns index and distance of closest
    dist = []
    for target in poslist:
        dist.append(getdistance(pos, target))
    closestind = np.argmin(dist)
    closestdist = np.min(dist)

    return closestind, closestdist


def getrelative(pos, rot, compos, comrot):
    relpos = pos - compos
    reldist = getdistance(pos[:-1], compos[:-1])
    if relpos[0] > 0:
        alpha = np.degrees(np.arctan(relpos[1]/relpos[0]))
    elif relpos[0] == 0:
        if relpos[1] > 0:
            alpha = 90
        else:
            alpha = -90
    else:
        alpha = np.degrees(np.arctan(relpos[1]/relpos[0])) + 180
    reldir = alpha - comrot[1]
    relrot = rot - comrot[1]  # viewing angle

    return reldir, reldist, relpos[2], relrot
