rollingStockData = {}


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
}


frametypeTranslatorLong = {
    "flatcar_logs": "Flatcar T1: Logs",
    "flatcar_stakes": "Flatcar T2: Stakes",
    "flatcar_cordwood": "Flatcar T3: Bulkhead",
    "flatcar_hopper": "Hopper",
    "flatcar_tanker": "Tanker",
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
}


frametypeTranslatorShort = {
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
    "cooke260_tender": "Mogul Tender",
    "class70": "Class 70",
    "class70_tender": "Class 70 Tender",
    "eureka": "Eureka",
    "eureka_tender": "Eureka Tender",
    "handcar": "Handcar",
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


def getnaminglimits(frametype, field):
    if frametype not in frametypeNamingLimiter:
        frametype = "default"

    if field == 0:
        maxlen = frametypeNamingLimiter[frametype]["numlen"]
        maxlines = frametypeNamingLimiter[frametype]["numlines"]
    else:
        maxlen = frametypeNamingLimiter[frametype]["namelen"]
        maxlines = frametypeNamingLimiter[frametype]["namelines"]

    return maxlen, maxlines


def namingsanitycheck(frametype, field, newname):
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

