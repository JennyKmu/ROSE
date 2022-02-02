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


class BuildingsBaseClass:
    def __init__(self, btype, pos, rot, inputs=None, outputs=None):
        self._btype = btype
        self._pos = pos
        self._rot = rot
        self._inputs = inputs
        self._outputs = outputs

    @property
    def typenumerical(self) -> int:
        return self._btype

    @property
    def displayname(self) -> str:
        return "Building"

    @property
    def typename(self) -> str:
        return "Unknown"

    @property
    def location(self) -> np.ndarray:
        return np.asarray([*self._pos, self._rot[1]], dtype=np.float32)
        # program only needs position and rotation around height axis anyway

    @location.setter
    def location(self, newlocation):
        if np.shape(newlocation) != (4,):
            raise IndexError
        newlocation = np.asarray(newlocation, dtype=np.float32)
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
        self._pos = np.asarray(newlocation[:4], dtype=np.float32)
        self._rot = np.asarray([0, newlocation[4], 0], dtype=np.float32)
        # pos and rotation values stored in two separate arrays like in the savegame

    @property
    def inventory(self) -> list[int]:
        val = [0, 0, 0, 0] if self._inputs is None else self._inputs
        val.append([0, 0, 0, 0] if self._outputs is None else self._outputs)
        return val  # much effort, but in case industries get added, so we don't change values

    def dump(self) -> list:  # return all values so they can be stacked as arrays
        return [self._btype, self._pos, self._rot, *self.inventory]


class Industry(BuildingsBaseClass):
    Types = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    __Subtype_Industry = "Industry"
    __Subtype_Depot = "Depot"
    __Names = {  # these Arrays are sorted by industry chain order
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
    __invlimits = {
        1: [None, None, None, None, 100, 32, 32, 100],
        2: [100, None, None, None, 100, 100, None, None],
        8: [50, 30, None, None, 290, None, None, None],
        3: [100, 1000, None, None, 100, 100, None, None],
        7: [30, 60, None, None, 750, None, None, None],
        4: [100, 1000, 50, None, 100, 100, None, None],
        5: [30, 30, 100, None, 1000, None, None, None],
        6: [1000, 100, 50, None, 100, 100, None, None]
    }
    __invtypes = {
        1: [None, None, None, None, "log", "cordwood", "cordwood", "log"],
        2: ["log", None, None, None, "lumber", "beam", None, None],
        8: ["lumber", "beam", None, None, "ironore", None, None, None],
        3: ["cordwood", "ironore", None, None, "rawiron", "rail", None, None],
        7: ["beam", "rail", None, None, "coal", None, None, None],
        4: ["rawiron", "coal", "lumber", None, "steelpipe", "crate_tools", None, None],
        5: ["steelpipe", "beam", "crate_tools", None, "crudeoil", None, None, None],
        6: ["crudeoil", "steelpipe", "lumber", None, "oilbarrel", "oilbarrel", None, None]
    }
    __StandardLocations = {
        1: [122173.2, 39657.6, 10699.0, 90.8],
        2: [56895.5, 88823.6, 10250.2, -147.0],
        3: [-29255.8, 140891.5, 6873.4, 0.0],
        4: [80843.7, -113526.4, 9999.2, -90.0],
        5: [117671.6, -73781.4, 10000.0, 0.0],
        6: [14387.8, -122723.5, 10936.1, -171.5],
        7: [-107836.7, -133014.6, 16524.6, -64.1],
        8: [-81678.5, -41662.1, 13631.8, -132.6],
        9: [4659.6, 9236.2, 10000.0, 90.0],
    }

    def __init__(self, btype: int, pos, rot, inputs, outputs):
        # if btype not in self.Types:
        #    raise ValueError
        # TODO: FIX THIS
        # self.attribute isn't that of the child class if method is of parent class
        if btype not in self.__invlimits.keys():
            inputs = [0, 0, 0, 0]  # catching depot and make sure it's empty
            outputs = [0, 0, 0, 0]
            self._subtype = Industry.__Subtype_Depot
        else:
            self._subtype = self.__Subtype_Industry
        BuildingsBaseClass.__init__(self, btype, pos, rot, inputs, outputs)

    @property
    def displayname(self) -> str:
        return self.__Names[self._btype]

    @property
    def typename(self) -> str:
        return self._subtype

    @property
    def inventory(self) -> list:
        return [*self._inputs, *self._outputs]

    @inventory.setter
    def inventory(self, newinv: list[int]):
        # sets inventory via iterable input. 0-3 inputs, 4-7 outputs. Unchanged if "None" is transmitted
        if np.shape(newinv) != (8,):
            raise IndexError  # must be array of 8
        limits = self.__invlimits[self._btype]
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
    def inventorylimits(self) -> list[int]:
        return self.__invlimits[self._btype]

    @property
    def inventorytypes(self) -> list[str]:
        return self.__invtypes[self._btype]

    def __resetlocation(self):
        self.location = (Industry.__StandardLocations[self._btype])


class Shed(BuildingsBaseClass):
    Types = (11, 12, 13, 14,)
    _Name = "Shed"
    _NameFormat = "Shed {}"
    _Colours = {
        11: "Blue",
        12: "Gold",
        13: "Red",
        14: "Brown",
    }
    Colours = list(_Colours.values())

    def __init__(self, btype: int, pos, rot):
        if btype not in Shed.Types:
            raise ValueError
        BuildingsBaseClass.__init__(self, btype, pos, rot)

    @property
    def displayname(self) -> str:
        return Shed._NameFormat.format(Shed._Colours[self._btype])

    @property
    def typename(self) -> str:
        return Shed._Name

    def repaint(self, newcolour: str):
        if newcolour not in Shed._Colours.values():
            raise ValueError
        self._btype = next(num for num, colour in Shed._Colours.items() if colour == newcolour)
        # complicated method to use a dict backwards


class FirewoodDepot(Industry):
    Types = (10,)
    __Names = {10: "Firewood Depot"}
    __Subtype_Industry = "Utility"
    __invlimits = {10: [32, None, None, None, 100, 100, 100, 100]}
    __invtypes = {10: ["anywood", None, None, None, "firewood", "firewood", "firewood", "firewood"]}

    def __init__(self, btype, pos, rot, inputs, outputs):
        Industry.__init__(self, btype, pos, rot, inputs, outputs)

    def inventoryfill(self):
        self.inventory = self.__invlimits


class UtilityBaseClass(BuildingsBaseClass):
    __Type = "Test"

    def __init__(self, btype, pos, rot):
        BuildingsBaseClass.__init__(self, btype, pos, rot)
        del self._inputs  # do not keep inputs and outputs
        del self._outputs

    def inventory(self):
        pass  # not possible for this subclass

    def dump(self) -> list:
        return [self._btype, self._pos, self._rot]

    def typename(self) -> str:
        return "Utility"


class WaterTower(UtilityBaseClass):
    Types = (0,)
    typearray = "WatertowerTypeArray"
    locationarray = "WatertowerLocationArray"
    rotationarray = "WatertowerRotationArray"
    levelarray = "WatertowerWaterlevelArray"
    __Names = {0: "Watertower", }
    __limits = {0: 360, }

    def __init__(self, btype, pos, rot, level):
        self._level = level
        UtilityBaseClass.__init__(self, btype, pos, rot)

    @property
    def displayname(self) -> str:
        return self.__Names[self._btype]

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, newlevel):
        float(newlevel)  # dirty exception throw
        if newlevel < 0:
            raise ValueError
        self._level = min(self.__limits[self._btype], newlevel)

    def fill(self):
        self._level = self.__limits[self._btype]

    @property
    def limit(self):
        return self.__limits[self._btype]


class SandHouse(UtilityBaseClass):
    Types = (0,)
    typearray = "SandhouseTypeArray"
    locationarray = "SandhouseLocationArray"
    rotationarray = "SandhouseRotationArray"
    __Names = {0: "Sandhouse", }
    __limits = {0: 50, }

    @property
    def displayname(self) -> str:
        return self.__Names[self._btype]


# TODO: reader, handler, writer schreiben
class gedoehns:
    # --- CLASS ATTRIBUTES/METHODS BELOW FOR READING AND SAVING
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
    data = []

    @classmethod
    def makeindustrylist(cls):
        cls.data = []
        for i, indtype in enumerate(cls._types):
            if indtype in cls._StandardLocations.keys():
                cls.data.append(Industry(indtype, cls._locs[i], cls._rots[i],
                                         cls._inputs[i], cls._outputs[i]))
        # TODO: Add sheds and firewood depots here

    @classmethod
    def readfromsave(cls, gvas):
        cls._types = gvas.data.find(cls._typearray).data
        cls._locs = gvas.data.find(cls._locationarray).data
        cls._rots = gvas.data.find(cls._rotationarray).data
        inputs = []
        outputs = []
        for i in range(1, 4 + 1):
            inputs.append(gvas.data.find(cls._inputarrays.format(i)).data)
            outputs.append(gvas.data.find(cls._outputarrays.format(i)).data)
        cls._inputs = np.column_stack(inputs)
        cls._outputs = np.column_stack(outputs)
        cls.makeindustrylist()  # build industry list

    @classmethod
    def writetosave(cls, gvas):
        types = []
        locs = []
        rots = []
        inputs = []
        outputs = []
        for entry in cls.data:
            types.append(entry.numericaltype)
            locrot = entry.location
            locs.append(locrot[:4])
            rots.append([0, locrot[4], 0])
            inv = entry.inventory
            inputs.append(inv[:4])
            outputs.append([inv[4:]])
        # TODO: Add sheds and firewood depots here
        inputsarray = np.asarray(inputs)
        outputsarray = np.asarray(outputs)
        typesarray = np.asarray(types)
        locsarray = np.asarray(locs, dtype=np.float32)
        rotsarray = np.asarray(rots, dtype=np.float32)
        gvas.data.find(cls._typearray)._data = typesarray
        gvas.data.find(cls._locationarray)._data = locsarray
        gvas.data.find(cls._rotationarray)._data = rotsarray
        for i in range(1, 4 + 1):
            gvas.data.find(cls._inputarrays.format(i))._data = inputsarray[:, i - 1]
            gvas.data.find(cls._outputarrays.format(i))._data = outputsarray[:, i - 1]
