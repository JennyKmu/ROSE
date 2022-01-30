import numpy as np
from .rollingStockData import *


class RollingStock:
    def __init__(self, ftype, pos, rot, brakes, name, number, couplerfront, couplerrear):
        self.type = ftype
        self.pos = pos
        self.rot = rot
        self.brakes = brakes
        self.name = name
        self.number = number
        self.couplerfront = couplerfront
        self.couplerrear = couplerrear


class Engine(RollingStock):
    def __init__(self, ftype, pos, rot, brakes, name, number, couplerfront, couplerrear, reg, rev, boilerwater,
                 boilerfuel, boilerpressure, tempwater, tempfire, smokestack, headlight, compressorpressure,
                 headlightstate, markerlightstate, generatorvalve, compressorvalve, sanderamount):
        RollingStock.__init__(self, ftype, pos, rot, brakes, name, number, couplerfront, couplerrear)
        self.reg = reg
        self.rev = rev
        self.boilerwater = boilerwater
        self.boilerfuel = boilerfuel
        self.boilerpressure = boilerpressure
        self.tempwater = tempwater
        self.tempfire = tempfire
        self.smokestack = smokestack
        self.headlight = headlight
        self.compressorpressure = compressorpressure
        self.headlightstate = headlightstate
        self.markerlightstate = markerlightstate
        self.generatorvalve = generatorvalve
        self.compressorvalve = compressorvalve
        self.sanderamount = sanderamount


class Tender(RollingStock):
    def __init__(self, ftype, pos, rot, brakes, name, number, couplerfront, couplerrear, tenderfuel, tenderwater):
        RollingStock.__init__(self, ftype, pos, rot, brakes, name, number, couplerfront, couplerrear)
        self.tenderfuel = tenderfuel
        self.tenderwater = tenderwater


class TankEngine(Engine):
    def __init__(self, ftype, pos, rot, brakes, name, number, couplerfront, couplerrear, reg, rev, boilerwater,
                 boilerfuel, boilerpressure, tempwater, tempfire, smokestack, headlight, compressorpressure,
                 headlightstate, markerlightstate, generatorvalve, compressorvalve, sanderamount,
                 tenderfuel, tenderwater):
        Engine.__init__(self, ftype, pos, rot, brakes, name, number, couplerfront, couplerrear, reg, rev, boilerwater,
                        boilerfuel, boilerpressure, tempwater, tempfire, smokestack, headlight, compressorpressure,
                        headlightstate, markerlightstate, generatorvalve, compressorvalve, sanderamount)
        self.tenderfuel = tenderfuel
        self.tenderwater = tenderwater


class FreightCar(RollingStock):
    def __init__(self, ftype, pos, rot, brakes, name, number, couplerfront, couplerrear, freighttype, freightamount):
        RollingStock.__init__(self, ftype, pos, rot, brakes, name, number, couplerfront, couplerrear)
        self.freighttype = freighttype
        self.freightamount = freightamount


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
