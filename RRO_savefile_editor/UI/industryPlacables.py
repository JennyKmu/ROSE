industryNames = {
    1: "Logging Camp",
    2: "Sawmill",
    8: "Iron Mine",
    3: "Smelter",
    7: "Coal Mine",
    4: "Ironworks",
    5: "Oilfield",
    6: "Refinery",
}


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


firewoodDepot = {
    "type": 10,
    "input": [32],
    "output": [100, 100, 100, 100]
}

waterTower = {
    "type": 0,
    "output": 360
}

sandHouse = {
    "type": 0
}
