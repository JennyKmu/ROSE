industryNames = {
    1: "Logging Camp",
    2: "Sawmill",
    8: "Iron Mine",
    3: "Smelter",
    7: "Coal Mine",
    4: "Ironworks",
    5: "Oilfield",
    6: "Refinery",
    9: "Freight Depot",
    10: "Firewood Depot",
}


mapIndustries = range(10)


industryInputs = {
    1: [[None], [None], [None], [None]],
    2: [["log", 100], [None], [None], [None]],
    8: [["lumber", 24], ["beam", 20], [None], [None]],
    3: [["cordwood", 100], ["ironore", 1000], [None], [None]],
    7: [["beam", 20], ["rail", 50], [None], [None]],
    4: [["rawiron", 100], ["coal", 1000], [None], [None]],
    5: [["steelpipe", 18], ["beam", 20], ["crate_tools", 100], [None]],
    6: [["crudeoil", 1000], ["steelpipe", 100], ["lumber", 24], [None]],
}


industryOutputs = {
    1: [["log", 100], ["cordwood", 32], ["cordwood", 32], ["log", 100]],
    2: [["lumber", 100], ["beam", 100], [None], [None]],
    8: [["ironore", 290], [None], [None], [None]],
    3: [["rawiron", 100], ["rail", 100], [None], [None]],
    7: [["coal", 750], [None], [None], [None]],
    4: [["steelpipe", 100], ["crate_tools", 100], [None], [None]],
    5: [["crudeoil", 1000], [None], [None], [None]],
    6: [["oilbarrel", 100], ["oilbarrel", 100], [None], [None]],
}


industryStandardLocations = {
    1: [122173.2,   39657.6,    10699.0,    90.8],
    2: [56895.5,    88823.6,    10250.2,    -147.0],
    3: [-29255.8,   140891.5,   6873.4,     0.0],
    4: [80843.7,    -113526.4,  9999.2,     -90.0],
    5: [117671.6,   -73781.4,   10000.0,    0.0],
    6: [14387.8,    -122723.5,  10936.1,    -171.5],
    7: [-107836.7,  -133014.6,  16524.6,    -64.1],
    8: [-81678.5,   -41662.1,   13631.8,    -132.6],
    9: [4659.6,     9236.2,     10000.0,    90.0],
}


placingLimits = {
    "X": [-190000.0, 190000.0],
    "Y": [-190000.0, 190000.0],
    "Z": [5000.0, 20000.0],
    "R": [-180.0, 180.0],
}


firewoodDepot = {
    "type": 10,
    "input": [32],
    "output": [100, 100, 100, 100]
}

waterTower = {
    "type": 0,
    "output": 360,
}

sandHouse = {
    "type": 0,
    "output": 50,
}
