import numpy as np


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
    "porter_0402": "Porter 0-4-0",
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
    "porter_0402": "Porter 1",
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


def getnaminglimits(frametype, field) -> tuple[int, int]:
    # Returns the limits of that field. 0 = Number, 1 = Name
    if frametype not in frametypeNamingLimiter:
        frametype = "default"

    if field == 0:
        maxlen = frametypeNamingLimiter[frametype]["numlen"]
        maxlines = frametypeNamingLimiter[frametype]["numlines"]
    else:
        maxlen = frametypeNamingLimiter[frametype]["namelen"]
        maxlines = frametypeNamingLimiter[frametype]["namelines"]

    return maxlen, maxlines


def namingsanitycheck(frametype, field, newname) -> str:
    # Limits the input to the field to change. 0 = Number, 1 = Name
    if not newname.startswith("\i"):
        if newname.isspace() or newname == '':  # if there is no text to work with, return nothing
            return ''

        lines = newname.split("<br>")  # split into separate lines first

        maxlen, maxlines = getnaminglimits(frametype, field)

        if maxlen == 0 or maxlines == 0:  # of it's not to be named at all
            return "\Error: This field isn't displayed at all. Enter to leave"

        if len(lines) > maxlines:  # check if line count is good
            return "\Error: Too many lines. Max is {}. Try again:".format(maxlines)

        sanelines = []
        lines_have_content = False

        for line in lines:
            if len(line) > maxlen:  # check if length for every line is good
                return "\Error: Line(s) too long. Max is {} per line. Try again:".format(maxlen)

            if line.isspace() or line == '':  # see if the line has content at all: all spaces or nothing
                line = ' '  # if that's the case, make it one space
            else:
                lines_have_content = True

            sanelines.append(line)

        # if we made it this far, reassemble the string
        if lines_have_content:  # if there is no content over multiple lines, return nothing instead
            saneinput = "<br>".join(sanelines)

            return saneinput
        else:
            return ''

    else:
        return newname[2:]


def gettypedescription(frametype, short=0) -> str:
    # Lookup for rolling stock type name; if not in list, use descriptor
    if short == 1:
        if frametype in frametypeTranslatorShort.keys():
            return frametypeTranslatorShort[frametype]
        else:
            return frametype
    else:
        if frametype in frametypeTranslatorLong.keys():
            return frametypeTranslatorLong[frametype]
        else:
            return frametype


def getidentifier(stocktype, name, number, loc, includey=False, indtypes=None, indlocs=None, onlynear=False):
    # Get a set of formatted info as string: Type, Name and Number, Location, nearest industry and distance to it
    typestr = gettypedescription(stocktype, 1)

    idstr = ""
    if number is not None:
        number = number.split("<br>")[0].strip()
        if not number == "":
            idstr += "{:>4} ".format(number)
    if name is not None:
        name = name.split("<br>")[0].strip()
        if not name == "":
            idstr += name
    idstr = idstr[:40]

    returnpackage = [typestr, idstr]

    if not onlynear:
        locm = np.round_(loc / 100)
        if includey:
            locstr = "{:5.0f}|{:5.0f}|{:5.0f}".format(*locm)
        else:
            locstr = "{:5.0f}|{:5.0f}".format(locm[0], locm[2])
        returnpackage.append(locstr)

    if indtypes is not None and indlocs is not None:
        from .playerTeleportReferences import getclosest
        from .industryPlacables import industryNames
        nearest, distance = getclosest(loc, indlocs)
        nearstr = industryNames[indtypes[nearest]] + " {:3.0f}m".format(distance/100)
        returnpackage.append(nearstr)

    return returnpackage
