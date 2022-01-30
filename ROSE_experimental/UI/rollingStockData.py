frametypeNamingLimiter = {
    "default": {"numlen": 4, "numlines": 1, "namelen": 10, "namelines": 2},
    "flatcar_logs": {"numlen": 12, "numlines": 1, "namelen": 7, "namelines": 1},
    "flatcar_stakes": {"numlen": 8, "numlines": 1, "namelen": 8, "namelines": 1},
    "flatcar_cordwood": {"numlen": 8, "numlines": 1, "namelen": 8, "namelines": 1},
    "flatcar_hopper": {"numlen": 4, "numlines": 1, "namelen": 7, "namelines": 1},
    "flatcar_tanker": {"numlen": 12, "numlines": 1, "namelen": 19, "namelines": 1},
    "boxcar": {"numlen": 7, "numlines": 4, "namelen": 13, "namelines": 4},
    "porter_040": {"numlen": 2, "numlines": 1, "namelen": 12, "namelines": 1},
    "porter_042": {"numlen": 2, "numlines": 1, "namelen": 12, "namelines": 1},
    "climax": {"numlen": 2, "numlines": 1, "namelen": 11, "namelines": 7},
    "heisler": {"numlen": 2, "numlines": 1, "namelen": 11, "namelines": 6},
    "cooke260": {"numlen": 3, "numlines": 1, "namelen": 12, "namelines": 1},
    "cooke260_tender": {"numlen": 6, "numlines": 1, "namelen": 11, "namelines": 1},
    "class70": {"numlen": 3, "numlines": 1, "namelen": 14, "namelines": 1},
    "class70_tender": {"numlen": 0, "numlines": 0, "namelen": 22, "namelines": 3},
    "eureka": {"numlen": 2, "numlines": 1, "namelen": 8, "namelines": 1},
    "eureka_tender": {"numlen": 0, "numlines": 0, "namelen": 18, "namelines": 1},
    "handcar": {"numlen": 5, "numlines": 1, "namelen": 18, "namelines": 1},
    "caboose": {"numlen": 12, "numlines": 1, "namelen": 20, "namelines": 1},
}


frametypeTranslatorLong = {
    "default": "Unknown",
    "flatcar_logs": "Flatcar T1: Logs",
    "flatcar_stakes": "Flatcar T2: Stakes",
    "flatcar_cordwood": "Flatcar T3: Bulkhead",
    "flatcar_hopper": "Hoppercar",
    "flatcar_tanker": "Tankercar",
    "boxcar": "Boxcar",
    "porter_040": "Porter 0-4-0",
    "porter_042": "Porter 0-4-2",
    "climax": "Climax",
    "heisler": "Heisler",
    "cooke260": "Cooke Mogul",
    "cooke260_tender": "Cooke Mogul Tender",
    "class70": "D&RG Class 70",
    "class70_tender": "D&RG Class 70 Tender",
    "eureka": "Eureka",
    "eureka_tender": "Eureka Tender",
    "handcar": "Handcar",
    "caboose": "Bobber Caboose",
}


frametypeTranslatorShort = {
    "default": "Unknown",
    "flatcar_logs": "Logcar",
    "flatcar_stakes": "Stakes",
    "flatcar_cordwood": "Bulkhead",
    "flatcar_hopper": "Hopper",
    "flatcar_tanker": "Tanker",
    "boxcar": "Boxcar",
    "porter_040": "Porter 1",
    "porter_042": "Porter 2",
    "climax": "Climax",
    "heisler": "Heisler",
    "cooke260": "Mogul",
    "cooke260_tender": "Mogul-T",
    "class70": "Class 70",
    "class70_tender": "Class 70-T",
    "eureka": "Eureka",
    "eureka_tender": "Eureka-T",
    "handcar": "Handcar",
    "caboose": "Caboose",
}


frametypeCargoLimits = {
    "flatcar_logs": {"log": 6, "steelpipe": 9},
    "flatcar_stakes": {"beam": 3, "lumber": 6, "rail": 10, "rawiron": 3},
    "flatcar_cordwood": {"cordwood": 8, "oilbarrel": 46},
    "flatcar_hopper": {"ironore": 10, "coal": 10},
    "flatcar_tanker": {"crudeoil": 12},
    "boxcar": {"crate_tools": 32},
}


cargotypeTranslator = {
    None: "Empty",
    "default": "Unknown",
    "log": "Logs",
    "cordwood": "Cordwood",
    "beam": "Beams",
    "lumber": "Lumber",
    "ironore": "Iron Ore",
    "rail": "Rails",
    "rawiron": "Raw Iron",
    "coal": "Coal",
    "steelpipe": "Steel Pipes",
    "crate_tools": "Tools",
    "crudeoil": "Crude Oil",
    "oilbarrel": "Oil Barrels",
}


frametypeExchangeable = [
    # Flatcars that have the exact same length
    "flatcar_logs",
    "flatcar_stakes",
    "flatcar_cordwood",
    "flatcar_hopper",
    "flatcar_tanker",
]


firewoodReserves = {
    "porter_040": 66,
    "porter_042": 164,
    "climax": 332,
    "heisler": 454,
    "cooke260_tender": 1460,
    "class70_tender": 1350,
    "eureka_tender": 499,
    "caboose": 15,
}


waterReserves = {
    # Amount of water that fits in the tank
    # For tank engines, it's with the engine
    # For tender engines, it's the tender
    "porter_040": 800,
    "porter_042": 800,
    "climax": 3000,
    "heisler": 3000,
    "cooke260_tender": 9500,
    "class70_tender": 9500,
    "eureka_tender": 3800,
}


waterBoiler = {
    # Amount of water that fits in the boiler
    "porter_040": 500,
    "porter_042": 500,
    "climax": 4000,
    "heisler": 5000,
    "cooke260": 5000,
    "class70": 6000,
    "eureka": 5000,
}


availableSmokestacks = {
    # Count of available smokestacks. Should be >=1
    "porter_040": 1,
    "porter_042": 1,
    "climax": 3,
    "heisler": 2,
    "cooke260": 3,
    "class70": 3,
    "eureka": 1,
}


availableHeadlights = {
    # Count of available headlights. Should be >=1
    "porter_040": 2,
    "porter_042": 2,
    "climax": 1,
    "heisler": 1,
    "cooke260": 2,
    "cooke260_tender": 2,
    "class70": 2,
    "eureka": 3,
}


sandLevel = {
    # Max amounts of sand
    "porter_040": 100,
    "porter_042": 100,
    "climax": 100,
    "heisler": 100,
    "cooke260": 100,
    "class70": 100,
    "eureka": 100,
}

spawnPositions = [
    [720.,  -2503., 10160.],
    [720.,  -461.,  10160.],
    [1260., -2503., 10160.],
    [1260., -461.,  10160.],
    [1800., -2503., 10160.],
    [1800., -461.,  10160.],
]

spawnOrientations = [
    [0., 90., 0.],
    [0., 90., 0.],
    [0., 90., 0.],
    [0., 90., 0.],
    [0., 90., 0.],
    [0., 90., 0.],
]

spawnZOffset = {
    "heisler": 10233.,
    "cooke260": 10239.,
    "class70": 10194.,
    "eureka": 10194.
}
