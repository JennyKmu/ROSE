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
    0: {[False, np.array(0, 0, 0), [0, 0, 0]]},  # Spawn point, absolute position
    1: {[True, [0, 0, 0], [0, 0, 0]]},  # Logging Camp
    2: {[True, [0, 0, 0], [0, 0, 0]]},  # Sawmill
    3: {[True, [0, 0, 0], [0, 0, 0]]},  # Smelter
    4: {[True, [0, 0, 0], [0, 0, 0]]},  # Ironworks
    5: {[True, [0, 0, 0], [0, 0, 0]]},  # Oilfield
    6: {[True, [0, 0, 0], [0, 0, 0]]},  # Refinery
    7: {[True, [0, 0, 0], [0, 0, 0]]},  # Coal mine
    8: {[True, [0, 0, 0], [0, 0, 0]]},  # Iron mine
    9: {[True, [0, 0, 0], [0, 0, 0]]},  # Freight Depot
    10: {[True, [0, 0, 0], [0, 0, 0]]},  # Firewood Depot
}

def getplayertppos(indtype, indpos, indrot):
    tpdata = player_teleport_pts[indtype]

    if tpdata[0]:
        newpos = indpos + np.array(tpdata[1])
        newrot = indrot + np.array(tpdata[2])
        if newrot[1] > 180:
            newrot[1] -= 360
        if newrot[1] < -180:
            newrot[1] += 360
    else:
        newpos = tpdata[1]
        newrot = tpdata[2]
    return newpos, newrot


def getdistance(pos1, pos2):
    pass

