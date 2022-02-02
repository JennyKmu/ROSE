import numpy as np


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
    11: "Shed Alp. Blue",
    12: "Shed AspenGold",
    13: "Shed Barn Red",
    14: "Shed Min.Brown",
}

placingLimits = {
    "X": [-190000.0, 190000.0],
    "Y": [-190000.0, 190000.0],
    "Z": [5000.0, 20000.0],
    "R": [-180.0, 180.0],
}


class Industry:
    _Names = {  # these Arrays sorted by industry chain order
        1: "Logging Camp",
        2: "Sawmill",
        8: "Iron Mine",
        3: "Smelter",
        7: "Coal Mine",
        4: "Ironworks",
        5: "Oilfield",
        6: "Refinery",
        9: "Freight Depot"
    }

    _invlimits = {
        1: [None, None, None, None, 100, 32, 32, 100],
        2: [100, None, None, None, 100, 100, None, None],
        8: [50, 30, None, None, 290, None, None, None],
        3: [100, 1000, None, None, 100, 100, None, None],
        7: [30, 60, None, None, 750, None, None, None],
        4: [100, 1000, 50, None, 100, 100, None, None],
        5: [30, 30, 100, None, 1000, None, None, None],
        6: [1000, 100, 50, None, 100, 100, None, None]
    }

    _invtypes = {
        1: [None, None, None, None, "log", "cordwood", "cordwood", "log"],
        2: ["log", None, None, None, "lumber", "beam", None, None],
        8: ["lumber", "beam", None, None, "ironore", None, None, None],
        3: ["cordwood", "ironore", None, None, "rawiron", "rail", None, None],
        7: ["beam", "rail", None, None, "coal", None, None, None],
        4: ["rawiron", "coal", "lumber", None, "steelpipe", "crate_tools", None, None],
        5: ["steelpipe", "beam", "crate_tools", None, "crudeoil", None, None, None],
        6: ["crudeoil", "steelpipe", "lumber", None, "oilbarrel", "oilbarrel", None, None]
    }

    _StandardLocations = {
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

    def __init__(self, itype: int, pos, rot, inputs, outputs):
        if itype not in Industry._StandardLocations.keys():
            raise ValueError
        self._itype = itype
        if self._itype in Industry._invlimits.keys():
            self._subtype = "Industry"
            self._inputs = inputs
            self._outputs = outputs
        else:
            self._subtype = "Depot"
            self._inputs = [0, 0, 0, 0]
            self._outputs = [0, 0, 0, 0]
        self._pos = pos
        self._rot = rot

    @property
    def displayname(self) -> str:
        return Industry._Names[self._itype]

    @property
    def numericaltype(self) -> int:
        return self._itype

    @property
    def subtype(self) -> str:
        return self._subtype

    @property
    def inventory(self) -> list:
        return [*self._inputs, *self._outputs]

    @inventory.setter
    def inventory(self, newinv: list):
        # sets inventory via iterable input. 0-3 inputs, 4-7 outputs. Unchanged if "None" is transmitted
        if len(newinv) != 8:
            raise IndexError    # must be array of 8
        limits = Industry._invlimits[self._itype]
        for i in range(8):
            if limits[i] is not None:
                if newinv[i] is None:
                    newinv[i] = [*self._inputs, *self._outputs][i]
                elif newinv[i] < 0:
                    raise ValueError
                else:
                    newinv[i] = min(limits[i], newinv[i])
            else:
                newinv[i] = 0
        self._inputs = newinv[:4]
        self._outputs = newinv[4:]

    @property
    def inventorylimits(self) -> list:
        return Industry._invlimits[self._itype]

    @property
    def location(self) -> list:
        return [*self._pos, self._rot[1]]

    @location.setter
    def location(self, newlocation: list):
        if len(newlocation) != 4:
            raise IndexError
        for i, axis in placingLimits.keys():
            limitlower = min(placingLimits[axis])
            limitupper = max(placingLimits[axis])
            if not limitlower <= newlocation[i] <= limitupper:
                if axis == "R":
                    while newlocation[i] > limitupper:
                        newlocation[i] -= 360
                    while newlocation[i] < limitlower:
                        newlocation[i] += 360
                else:
                    raise ValueError
        self._pos = newlocation[:4]
        self._rot = [0, newlocation[4], 0]

    def resetlocation(self):
        self.location = (Industry._StandardLocations[self._itype])

    # --- CLASS METHODS BELOW FOR READING AND SAVING
    _typearray = "IndustryTypeArray"
    _locationarray = "IndustryLocationArray"
    _rotationarray = "IndustryRotationArray"
    _inputarrays = "IndustryStorageEduct{}Array"
    _outputarrays = "IndustryStorageProduct{}Array"

    _types = []
    _locs = []
    _rots = []
    _inputs = []
    _outputs = []

    @staticmethod
    def makeindustrylist():
        data = []
        for i, indtype in enumerate(Industry._types):
            if indtype in Industry._StandardLocations.keys():
                data.append(Industry(indtype, Industry._locs[i], Industry._rots[i],
                                     Industry._inputs[i], Industry._outputs[i]))

    @staticmethod
    def readfromsave(gvas):
        Industry._types = gvas.data.find(Industry._typearray).data
        Industry._locs = gvas.data.find(Industry._locationarray).data
        Industry._rots = gvas.data.find(Industry._rotationarray).data
        inputs = []
        outputs = []
        for i in range(1, 4+1):
            inputs.append(gvas.data.find(Industry._inputarrays.format(i)).data)
            outputs.append(gvas.data.find(Industry._outputarrays.format(i)).data)
        Industry._inputs = np.vstack(inputs)
        Industry._outputs = np.vstack(outputs)
        Industry.makeindustrylist()  # build industry list


# TODO: Add sheds and firewood depots, since they're in the same arrays
# And while we're at it, we could also add watertowers and sandhouses.
