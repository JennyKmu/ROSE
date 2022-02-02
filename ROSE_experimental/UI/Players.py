import numpy as np


class Player:
    def __init__(self, name, money, xp, loc, steamid=None):
        self._name = name
        self._money = money
        self._xp = xp
        self._loc = loc
        self._steamid = steamid

    def getall(self):
        return self._name, self._money, self._xp, self._loc, self._steamid

    def getname(self):
        return self._name

    def getid(self):
        return self._steamid

    def editmoney(self, newamount, add=False):
        if add:
            newamount += self._money
        newamount = min(newamount, (2**31)-1)   # Maximum amount, or the game puts you in debt.
        newamount = max(newamount, -(2**31))    # I don't know why one would like to go lower, but nah.
        self._money = newamount

    def getmoney(self):
        return self._money

    def editxp(self, newamount, add=False):
        if add:
            newamount += self._xp
        newamount = min(newamount, (2**31)-1)
        newamount = max(newamount, 0)
        self._xp = newamount

    def getxp(self):
        return self._xp

    def editloc(self, newloc):
        # Newlocation should be an array of [X, Y, Z] in float32
        if not np.ma.isarray(newloc):       # Check for data integrity: Array of size 3
            raise ValueError
        if not len(newloc) == 3:
            raise ValueError
        if not (-19000 < newloc[0] < 19000 and -19000 < newloc[1] < 19000 and 5000 < newloc[2] < 15000):
            raise OverflowError             # Check that the new location is still within bounds
        self._loc = newloc

    def getloc(self):
        return self._loc


class PlayerArrays:
    _namearray = "playernamearray"
    _xparray = "playerxparray"
    _moneyarray = "playermoneyarray"
    _idarray = "playeridarray"
    _locationarray = "playerlocationarray"

    def __init__(self):
        self._names = []
        self._xp = []
        self._money = []
        self._ids = []
        self._locs = []
        self.players = []

    # Keeping list of names and IDs accessible
    @property
    def names(self):
        return self._names

    @property
    def ids(self):
        return self._ids

    def makeplayerarray(self):
        self.players = []
        for i, name in enumerate(self._names):
            if i < len(self._ids):
                cur_id = self._ids[i]
            else:
                cur_id = None
            self.players.append(Player(name, self._money[i], self._xp[i], self._locs[i], cur_id))

    def readfromsave(self, gvas):
        self._names = gvas.data.find(PlayerArrays._namearray).data
        self._xp = gvas.data.find(PlayerArrays._xparray).data
        self._money = gvas.data.find(PlayerArrays._moneyarray).data
        self._ids = gvas.data.find(PlayerArrays._idarray).data
        self._locs = gvas.data.find(PlayerArrays._locationarray).data
        self.makeplayerarray()  # update player class array

    def makedataarrays(self):
        names = []
        xp = []
        money = []
        ids = []
        locs = []
        for player in self.players:
            names.append(player.getname())
            money.append(player.getmoney())
            xp.append(player.getxp())
            locs.append(player.getloc())
            if player.getid() is not None:  # Only add SteamID64 if it is specified.
                ids.append(player.getid())
        self._names = np.asarray(names)
        self._xp = np.asarray(xp)
        self._money = np.asarray(money)
        self._ids = np.asarray(ids)
        self._locs = np.asarray(locs, dtype=np.float32)

    def writetosave(self, gvas):
        self.makedataarrays()   # update data arrays
        gvas.data.find(PlayerArrays._namearray)._data = self._names
        gvas.data.find(PlayerArrays._moneyarray)._data = self._money
        gvas.data.find(PlayerArrays._xparray)._data = self._xp
        gvas.data.find(PlayerArrays._locationarray)._data = self._locs
        gvas.data.find(PlayerArrays._idarray)._data = self._ids

    # Utility methods
    def removeduplicates(self):
        self.makedataarrays()   # update data arrays
        namelist = list(self._names)
        idlist = list(self._ids)
        duplicates = []
        for name in namelist:                                   # find duplicate names and mark those
            if namelist.count(name) > 1:                        # are there multiple?
                nameduplicates = [i for i in range(len(namelist)) if namelist[i] == name]  # entries with the same name
                if nameduplicates[0] < len(idlist):             # does this player have an ID yet?
                    cur_id = idlist[nameduplicates[0]]
                    for i in nameduplicates[1:]:                # all but the first
                        if i < len(idlist):                     # if there's multiple with the same ID
                            if idlist[i] == cur_id:
                                duplicates.append(i)
                        else:                                   # if other entries have no ID,
                            duplicates.append(i)                # assume it's the same player and delete
        for cur_id in idlist:
            if cur_id in namelist:                              # artifact of save data versions 220120
                duplicates.append(namelist.index(cur_id))       # where ID replaced names

        duplicates.sort(reverse=True)
        duplicates = list(dict.fromkeys(duplicates))            # remove duplicate duplicates
        for duplicate in duplicates:
            self.players.pop(duplicate)
        self.makedataarrays()   # update data arrays
