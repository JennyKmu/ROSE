industryNames = {
    2: "Logging Camp",
    3: "Sawmill",
    4: "Iron Mine",
    5: "Smelter",
    6: "Coal Mine",
    7: "Ironworks",
    8: "Oilfield",
    9: "Refinery",
}


industryInputs = {
    3: {"log": 100},
    4: {"beam": 20, "lumber": 24},
    5: {"cordwood": 100, "ironore": 1000},
    6: {"beam": 20, "rail": 100},
    7: {"coal": 1000, "rawiron": 100},
    8: {"beam": 20, "steelpipe": 100, "crate_tools": 100},
    9: {"lumber": 20, "steelpipe": 100, "crudeoil": 1000},
}


industryOutputs = {
    2: {"log": 100, "cordwood": 100},
    3: {"beam": 100, "lumber": 100},
    4: {"ironore": 290},
    5: {"rail": 100, "rawiron": 100},
    6: {"coal": 750},
    7: {"steelpipe": 100, "crate_tools": 100},
    8: {"crudeoil": 1000},
    9: {"oilbarrel": 100, "oilbarrel2": 100},
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
