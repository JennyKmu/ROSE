import numpy as np
try:
    # When it is imported as a module
    from .fstreamutils import *
    from .GVASErrors import *
except ImportError:
    # When running unit tests
    from fstreamutils import *
    from GVASErrors import *

class GVAS(object):
    def __init__(self, filename = None):
        self._sourcefilename = filename
        self._data = GVASData()
        self._header = GVASHeader()
        if self._sourcefilename is not None:
            self.read(self._sourcefilename)

    def read(self, filename):
        self._sourcefilename = filename
        with open(filename, 'rb') as fstream:
            self._header.readfrom(fstream)
            self._data.readfrom(fstream)

    def write(self, filename):
        with open(filename, 'wb') as fstream:
            self._header.writeto(fstream)
            self._data.writeto(fstream)

    @property
    def data(self):
        return self._data

    @property
    def header(self):
        return self._header

class GVASData(object):
    def __init__(self):
        self._properties = []

    def readfrom(self, fstream):
        while True:
            prop = self._readProperty(fstream)
            if prop is None:
                print("WARNING: None Property encountered !")
            else:
                self._properties.append(prop)
            # print(prop.name) # DEBUG
            if prop.name == "None": break
            # if prop._dtype == "TextProperty": # DEBUG
            #     print(prop)
        return self

    def find(self, property_name):
        for p in self._properties:
            if p.name == property_name:
                return p
        return None

    def _readProperty(self, fstream):
        c = peekInt8(fstream)
        if c == 0:
            print("None property found at ", end = '')
            print(hex(fstream.tell()))
            return None
        pname = readUEString(fstream)
        # print(pname) #DEBUG
        if pname == "" or pname is None:
            print("None property found at ", end = '')
            print(hex(fstream.tell()))
            return None
        prop = UEProperty()
        prop._name = pname
        if pname == "None":
            return prop

        ptype = readUEString(fstream)
        prop._ptype = ptype

        if ptype != "ArrayProperty":
            prop._isarray = False
            if ptype == "StrProperty":
                self._readStrProperty(fstream, prop)
            else:
                raise GVASParserNotImplemented(f"property type for '{pname}' is not implemented ('{ptype}')")
            return prop

        prop._isarray = True
        plen = readInt64(fstream)
        dtype = readUEString(fstream)
        prop._dtype = dtype

        if dtype == "StructProperty":
            self._readStructPropertyArray(fstream, prop, plen)

        elif dtype == "BoolProperty":
            self._readBoolPropertyArray(fstream, prop, plen)

        elif dtype == "IntProperty":
            self._readIntPropertyArray(fstream, prop, plen)

        elif dtype == "FloatProperty":
            self._readFloatPropertyArray(fstream, prop, plen)

        elif dtype == "StrProperty":
            self._readStrPropertyArray(fstream, prop, plen)

        elif dtype == "TextProperty":
            self._readTextPropertyArray(fstream, prop, plen)

        else:
            raise GVASParserNotImplemented(f"{dtype} data type for '{pname}' is not implemented")

        return prop

    def _readStructPropertyArray(self, fstream, prop, plen):
        # print(prop.name, plen)
        check_bool = readInt8(fstream)
        if check_bool != 0:
            raise GVASParserNotImplemented(f"check boolean is not 0 for '{pname}'")
        struct_size = readInt32(fstream)
        pname = readUEString(fstream)
        if pname != prop.name:
            raise GVASParserNotImplemented(f"field name in struct is different from property name for '{pname}'")
        if readUEString(fstream) != "StructProperty":
            raise GVASParserNotImplemented(f"Expected 'StructProperty' for '{pname}'")
        field_size = readInt64(fstream)
        field_name = readUEString(fstream)
        if not field_name in ["Vector", "Rotator"]:
            raise GVASParserNotImplemented(f"Expected a Vector or a Rotator for '{pname}'")
        buf = fstream.read(17) # unknown ? maybe index of field for the struct ?
        assert buf == b'\x00'*17
        data = np.frombuffer(fstream.read(field_size), dtype=np.float32).reshape(int(field_size/4/3),3).copy()
        prop._data = data
        prop._ftype = field_name

    def _readStrProperty(self, fstream, prop):
        sz = readInt64(fstream)
        # print(sz)
        check_bool = readInt8(fstream)
        if check_bool != 0:
            raise GVASParserNotImplemented(f"check boolean is not 0 for '{pname}'")
        prop._data = readUEString(fstream)
        # print(prop.data)

    def _readBoolPropertyArray(self, fstream, prop, plen):
        # print(prop.name, plen)
        check_bool = readInt8(fstream)
        if check_bool != 0:
            raise GVASParserNotImplemented(f"check boolean is not 0 for '{prop.name}'")
        nbool = readInt32(fstream)
        buffer = fstream.read(nbool)
        # print(repr(buffer))
        data = np.frombuffer(buffer, dtype=np.bool).copy()
        prop._data = data

    def _readIntPropertyArray(self, fstream, prop, plen):
        # print(prop.name, plen)
        check_bool = readInt8(fstream)
        if check_bool != 0:
            raise GVASParserNotImplemented(f"check boolean is not 0 for '{prop.name}'")
        nint = readInt32(fstream)
        buffer = fstream.read(nint*4)
        # print(repr(buffer))
        data = np.frombuffer(buffer, dtype=np.int32).copy()
        prop._data = data

    def _readFloatPropertyArray(self, fstream, prop, plen):
        check_bool = readInt8(fstream)
        if check_bool != 0:
            raise GVASParserNotImplemented(f"check boolean is not 0 for '{prop.name}'")
        nfloat = readInt32(fstream)
        data = np.frombuffer(fstream.read(nfloat*4), dtype=np.float32).copy()
        prop._data = data

    def _readStrPropertyArray(self, fstream, prop, plen):
        # print(prop.name, plen)
        check_bool = readInt8(fstream)
        if check_bool != 0:
            raise GVASParserNotImplemented(f"check boolean is not 0 for '{prop.name}'")
        nstr = readInt32(fstream)
        data = []
        for i in range(nstr):
            data.append(readUEString(fstream))
        prop._data = data

    def _readTextPropertyArray(self, fstream, prop, plen):
        # print(prop.name, plen)
        check_bool = readInt8(fstream)
        if check_bool != 0:
            raise GVASParserNotImplemented(f"check boolean is not 0 for '{prop.name}'")
        ntext = readInt32(fstream)
        # print('n = ' + str(ntext))
        data = []

        for i in range(ntext):
            data.append(UETextProperty(fstream).value)
            # print(i, '-', repr(data[-1]), '-', hex(fstream.tell()))

        prop._data = data

    def writeto(self, fstream):
        for prop in self._properties:
            self._writeProperty(fstream, prop)

    def _writeProperty(self, fstream, prop):
        writeUEString(fstream, prop.name)
        if prop.name == "None":
            writeInt32(fstream, 0)
            # writeInt8(fstream, 0)
            return

        writeUEString(fstream, prop.ptype)
        if prop.ptype == "StrProperty":
            if isUTF16(prop.data):
                sz = 2*len(prop.data) + 4 + 2
            else:
                sz = len(prop.data) + 4 + 1
            writeInt64(fstream, sz)
            writeInt8(fstream, 0)
            writeUEString(fstream, prop.data)
            return

        if prop.ptype == "ArrayProperty":
            sz_offset = fstream.tell()
            writeInt64(fstream, 0) # Size of property, come back later with correct value!!!
            sz = 0
            writeUEString(fstream, prop.dtype)

            if prop.dtype == "BoolProperty":
                sz = self._writeBoolPropertyArray(fstream, prop)
                end_offset = fstream.tell()
                fstream.seek(sz_offset)
                writeInt64(fstream, sz)
                fstream.seek(end_offset)
                return

            if prop.dtype == "IntProperty":
                sz = self._writeIntPropertyArray(fstream, prop)
                end_offset = fstream.tell()
                fstream.seek(sz_offset)
                writeInt64(fstream, sz)
                fstream.seek(end_offset)
                return

            if prop.dtype == "FloatProperty":
                sz = self._writeFloatPropertyArray(fstream, prop)
                end_offset = fstream.tell()
                fstream.seek(sz_offset)
                writeInt64(fstream, sz)
                fstream.seek(end_offset)
                return

            if prop.dtype == "StrProperty":
                sz = self._writeStrPropertyArray(fstream, prop)
                end_offset = fstream.tell()
                fstream.seek(sz_offset)
                writeInt64(fstream, sz)
                fstream.seek(end_offset)
                return

            if prop.dtype == "TextProperty":
                sz = self._writeTextPropertyArray(fstream, prop)
                end_offset = fstream.tell()
                fstream.seek(sz_offset)
                writeInt64(fstream, sz)
                fstream.seek(end_offset)
                return

            if prop.dtype == "StructProperty":
                sz = self._writeStructPropertyArray(fstream, prop)
                end_offset = fstream.tell()
                fstream.seek(sz_offset)
                writeInt64(fstream, sz)
                fstream.seek(end_offset)
                return

    def _writeBoolPropertyArray(self, fstream, prop):
        writeInt8(fstream, 0) # check bool
        writeInt32(fstream, prop.data.size)
        buffer = prop.data.tobytes()
        # print(len(buffer))
        # print(repr(buffer))
        fstream.write(buffer)
        return 4+len(buffer)

    def _writeIntPropertyArray(self, fstream, prop):
        writeInt8(fstream, 0) # check bool
        writeInt32(fstream, prop.data.size)
        buffer = prop.data.tobytes()
        # print(len(buffer))
        # print(repr(buffer))
        fstream.write(buffer)
        return 4+len(buffer)

    def _writeFloatPropertyArray(self, fstream, prop):
        writeInt8(fstream, 0) # check bool
        writeInt32(fstream, prop.data.size)
        buffer = prop.data.tobytes()
        # print(len(buffer))
        # print(repr(buffer))
        fstream.write(buffer)
        return 4+len(buffer)

    def _writeStrPropertyArray(self, fstream, prop):
        writeInt8(fstream, 0) # check bool
        writeInt32(fstream, len(prop.data))
        sz = 0
        for w in prop.data:
            # print(repr(w))
            if w is None or w == '':
                sz += 4
            elif isUTF8(w) :
                sz += 4 + len(w) + 1
            else:
                sz += 4 + 2*len(w) + 2
            writeUEString(fstream, w)
        sz += 4
        # print(prop.name, sz)
        return sz

    def _writeTextPropertyArray(self, fstream, prop):
        writeInt8(fstream, 0) # check bool
        writeInt32(fstream, len(prop.data))
        sz = 4
        for txt in prop.data:
            if txt is None:
                # if prev_is_formatted:
                #     writeInt32(fstream, 2)
                # else:
                writeInt32(fstream,0)
                writeInt8(fstream,-1)
                writeInt32(fstream,0)
                # prev_is_formatted=False
                sz += 9
                continue

            if not '<br>' in txt:
                writeInt32(fstream,2)
                writeInt8(fstream,-1)
                writeInt32(fstream,1)
                sz += 9
                writeUEString(fstream, txt)
                if isUTF8(txt):
                    sz += 4+len(txt)+1
                else:
                    sz += 4+2*len(txt)+2
                continue

            if '<br>' in txt:
                txt_parts = txt.split('<br>')
                writeInt32(fstream,1)
                writeInt8(fstream,3)
                writeInt64(fstream,8)
                writeInt8(fstream,0)
                sz += 14
                magic = "56F8D27149CC5E2D12103BBEBFCA9097"
                writeUEString(fstream, magic)
                sz += 4+len(magic)+1
                writeUEString(fstream, "{0}<br>{1}")
                sz += 4+10+1
                writeInt32(fstream, 2)
                sz += 4
                writeUEString(fstream, '0')
                sz += 4+1+1
                writeInt8(fstream, 4)
                sz += 1
                writeInt32(fstream,2)
                writeInt8(fstream,-1)
                sz += 5
                if txt_parts[0] != '':
                    writeInt32(fstream,1)
                    sz += 4
                    writeUEString(fstream, txt_parts[0])
                    if isUTF8(txt_parts[0]):
                        sz += 4+len(txt_parts[0])+1
                    else:
                        sz += 4+2*len(txt_parts[0])+2
                else:
                    writeInt32(fstream, 0)
                    sz += 4
                writeUEString(fstream, '1')
                sz += 6
                writeInt8(fstream,4)
                sz += 1
                if txt_parts[1] != '':
                    writeInt32(fstream, 2)
                    writeInt8(fstream,-1)
                    writeInt32(fstream,1)
                    sz += 9
                    writeUEString(fstream, txt_parts[1])
                    if isUTF8(txt_parts[1]):
                        sz += 4+len(txt_parts[1])+1
                    else:
                        sz += 4+2*len(txt_parts[1])+2
                else:
                    writeInt32(fstream,2)
                    writeInt8(fstream,-1)
                    writeInt32(fstream,0)
                    sz += 9
        # print(prop.name, sz)
        return sz

    def _writeStructPropertyArray(self, fstream, prop):
        writeInt8(fstream, 0) # check bool
        writeInt32(fstream, int(prop.data.size/3))

        writeUEString(fstream, prop.name)
        writeUEString(fstream, prop.dtype)
        writeInt64(fstream, prop.data.size*4)

        writeUEString(fstream, prop.ftype)
        fstream.write(b'\x00'*17)
        buffer = prop.data.flatten().tobytes()
        sz = (len(buffer)+17
            +len(prop.ftype)+1+4
            +len(prop.dtype)+1+4
            +len(prop.name) +1+4
            +4 + 8)
        # print(repr(buffer))
        fstream.write(buffer)
        return sz






class UEType(object):
    pass

class UETextProperty(UEType):
    count = 0
    def __init__(self, fstream):
        # UETextProperty.count += 1
        # print('count =' + str(UETextProperty.count))
        self.value = None

        before_sep = readInt32(fstream)

        if before_sep == 1:
            # UETextProperty.count += 1
            # print("counter:", UETextProperty.count)
            assert readInt8(fstream) == 3
            assert readInt64(fstream) == 8 # 8
            assert readInt8(fstream) == 0
            assert readUEString(fstream) == "56F8D27149CC5E2D12103BBEBFCA9097"
            format_str = readUEString(fstream)
            assert format_str == "{0}<br>{1}"
            assert readInt32(fstream) == 2
            assert readUEString(fstream) ==  "0"
            assert readInt8(fstream) == 4
            assert readInt32(fstream) == 2
            assert readInt8(fstream) == -1
            opt = readInt32(fstream)
            if opt == 1:
                first_line = readUEString(fstream)
            else:
                first_line = ''
            readUEString(fstream) # always "1"

            assert readInt8(fstream) == 4
            assert readInt32(fstream) == 2
            assert readInt8(fstream) == -1
            opt = readInt32(fstream)
            if opt == 1:
                second_line = readUEString(fstream)
            else:
                second_line = ""
            self.value = format_str.format(first_line, second_line)
        else:
            assert readInt8(fstream) == -1
            opt = readInt32(fstream)
            if opt == 1:
                self.value = readUEString(fstream)
            else:
                self.value = None
        # print(self.value)

class GVASHeader(dict):

    def __init__(self):
        pass

    def readfrom(self, fstream):
        self["Magic"] = fstream.read(4).decode()
        if self["Magic"] != "GVAS":
            raise GVASFileFormatError("Error reading file: Format doesn't start with GVAS.")
        self["SaveVersion"] = readInt32(fstream)
        self["StructureVersion"] = readInt32(fstream)
        self["EngineVersion"] = {}
        self["EngineVersion"]["Major"] = readInt16(fstream)
        self["EngineVersion"]["Minor"] = readInt16(fstream)
        self["EngineVersion"]["Patch"] = readInt16(fstream)
        self["EngineVersion"]["Build"] = readInt32(fstream)
        self["EngineVersion"]["BuildID"] = readUEString(fstream)
        self["CustomFormatVersion"] = readInt32(fstream)
        self["NCustomData"] = readInt32(fstream)
        self._readGUID(fstream)
        self["SaveType"] = readUEString(fstream)
        return self

    def _readGUID(self, fstream):
        self["CustomData"] = []
        for i in range(self["NCustomData"]):
            self["CustomData"].append((fstream.read(16), readInt32(fstream)))

    def _writeGUID(self, fstream):
        for i in range(self["NCustomData"]):
            fstream.write(self["CustomData"][i][0])
            writeInt32(fstream, self["CustomData"][i][1])

    def writeto(self, fstream):
        fstream.write(self["Magic"].encode())
        writeInt32(fstream, self["SaveVersion"])
        writeInt32(fstream, self["StructureVersion"])
        writeInt16(fstream, self["EngineVersion"]["Major"])
        writeInt16(fstream, self["EngineVersion"]["Minor"])
        writeInt16(fstream, self["EngineVersion"]["Patch"])
        writeInt32(fstream, self["EngineVersion"]["Build"])
        writeUEString(fstream, self["EngineVersion"]["BuildID"])
        writeInt32(fstream, self["CustomFormatVersion"])
        writeInt32(fstream, self["NCustomData"])
        self._writeGUID(fstream)
        writeUEString(fstream, self["SaveType"])


class UEProperty(UEType):
    def __init__(self, name = "", type = ""):
        self._name = ""
        self._ptype = ""
        self._data = None
        self._dtype = None
        self._ftype = None

    def __str__(self):
        s = self.name + '\n'
        s += "> property type: " + str(self.ptype) + '\n'
        if self.dtype is not None:
            s += "> data type: " + str(self.dtype) + '\n'
        if self.ftype is not None:
            s += "> field type: " + str(self.ftype) + '\n'
        s += "> data: " + str(self.data)
        return s

    @property
    def name(self):
        return self._name

    @property
    def ptype(self):
        return self._ptype

    @property
    def data(self):
        return self._data

    @property
    def dtype(self):
        return self._dtype

    @property
    def ftype(self):
        return self._ftype

#### UE specific data types ####
def readUEString(fstream):
    sz = readInt32(fstream)
    if sz == 0:
        return None
    if sz == 1 or sz == -1 :
        return ""
    if sz > 0 :
        buffer = fstream.read(sz)[:-1]
        return buffer.decode('utf8') # skipping last \x00
    elif sz < 0:
        buffer = fstream.read(-sz*2)[:-2]
        return buffer.decode('utf16')

def writeUEString(fstream, s):
    if s is None:
        writeInt32(fstream, 0)
        return
    if s == '':
        writeInt32(fstream, 1)
        return
    buffer = s.encode('utf8')
    if len(buffer) > len(s):
        buffer = s.encode('utf16')[2:]
        writeInt32(fstream, -len(s)-1)
        writeStr(fstream, buffer, end=b'\x00\x00')
    else:
        writeInt32(fstream, len(buffer)+1)
        writeStr(fstream, buffer)

def isUTF8(s):
    buffer = s.encode('utf8')
    if len(buffer) != len(s):
        return False
    else:
        return True

def isUTF16(s):
    return not isUTF8(s)



if __name__ == "__main__":
    print("{:-^72s}".format(" Running unit tests for file `GVAS.py` "))
    test_files = ["../../slot{}.sav".format(i) for i in range(1,11)]
    # test_files = ["../../slot7.sav"]
    total_passed_count = 0
    total_failed_count = 0
    import os.path
    for i, test_file in enumerate(test_files):
        if not os.path.isfile(test_file):
            continue
        print(f'> Test file is {test_file}')
        passed_count = 0
        failed_count = 0
        print("{:-^72s}".format('-'))
        print("- GVASHeader read and write...", end=' ')
        with open(test_file, 'rb') as fstream:
            header = GVASHeader().readfrom(fstream)

        with open('./testheader.sav', 'wb') as fstream:
            header.writeto(fstream)

        with open(test_file, 'rb') as fstream:
            b1 = fstream.read(1081)

        with open('./testheader.sav', 'rb') as fstream:
            b2 = fstream.read(1081)

        if b1==b2 :
            print("\033[1;32mPASSED\033[0m")
            passed_count += 1
        else:
            print("\033[1;31mFAILED\033[0m")
            failed_count += 1

        print("- GVAS read...", end=' ')
        try:
            gvas = GVAS(test_file)
            # print(gvas.data.find("FrameNameArray").data)
            print("\033[1;32mPASSED\033[0m")
            passed_count += 1

        except Exception as e:
            print("\033[1;31mFAILED\033[0m")
            print("> Details:")
            import sys
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            failed_count += 1

        print("- GVAS write...", end=' ')

        try:
            gvas.write(f"./testgvaswrite{i+1}.sav")
            print("\033[1;32mPASSED\033[0m")
            passed_count += 1

        except Exception as e:
            print("\033[1;31mFAILED\033[0m")
            print("> Details:")
            import sys
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            failed_count += 1

        print("- GVAS read vs write...", end=' ')
        with open(test_file, 'rb') as f:
            rdata = f.read()
        with open(f"./testgvaswrite{i+1}.sav", 'rb') as f:
            wdata = f.read()
        if rdata == wdata:
            print("\033[1;32mPASSED\033[0m")
            passed_count += 1
        else:
            print("\033[1;31mFAILED\033[0m")
            failed_count += 1
            for i in range(len(rdata)):
                if rdata[i] != wdata[i]:
                    print("First diff occuring at address {}".format(hex(i)))
                    break




        print("{:-^72s}".format('-'))
        print("> PASSED tests: \033[1;32m{}\033[0m".format(passed_count))
        if failed_count > 0:
            print("> FAILED tests: \033[1;31m{}\033[0m".format(failed_count))
        else :
            print("> FAILED tests: \033[1;32m0\033[0m")

        total_passed_count += passed_count
        total_failed_count += failed_count
        print("{:-^72s}".format('-'))



    print("> TOTAL PASSED tests: \033[1;32m{}\033[0m".format(total_passed_count))
    if total_failed_count > 0:
        print("> TOTAL FAILED tests: \033[1;31m{}\033[0m".format(total_failed_count))
    else :
        print("> TOTAL FAILED tests: \033[1;32m0\033[0m")


    print("{:-^72s}".format(' End of unit tests for file GVAS.py` '))

    # for p in gvas.data._properties:
    #     print(p)
