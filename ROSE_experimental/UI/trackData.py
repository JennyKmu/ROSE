import numpy as np

spawnPositions = np.asarray([
    [720.,  -2503., 10160.],
    [720.,  -461.,  10160.],
    [1260., -2503., 10160.],
    [1260., -461.,  10160.],
    [1800., -2503., 10160.],
    [1800., -461.,  10160.],
])

spawnOrientations = np.asarray([
    [0., 90., 0.],
    [0., 90., 0.],
    [0., 90., 0.],
    [0., 90., 0.],
    [0., 90., 0.],
    [0., 90., 0.],
])

spawnZOffset = {
    "heisler": 10233.,
    "cooke260": 10239.,
    "class70": 10194.,
    "eureka": 10194.
}

def nextAvailableSpawn(gvas, pos):
    framelocs = gvas.data.find("FrameLocationArray").data
    for i, spawnPos in enumerate(spawnPositions):
        for frameloc in framelocs:
            checks = []
            checks.append(
                frameloc[0] > spawnPos[0]-270 and
                frameloc[0] < spawnPos[0]+270)
            checks.append(
                frameloc[1] > spawnPos[1]-1021 and
                frameloc[1] < spawnPos[1]+1021
            )
            if all(checks):
                break
        if all(checks):
            continue
        else:
            return i
    return None
