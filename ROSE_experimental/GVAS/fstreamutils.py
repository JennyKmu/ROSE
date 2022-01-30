import struct

#### Regular data types ####
#--- Int64 ---
def readInt64(fstream):
    buf = fstream.read(8)
    if len(buf) != 8 :
        fstream.seek(fstream.tell() - len(buf))
        return None
    return struct.unpack('<q', buf)[0]

def peekInt64(fstream):
    v = readInt64(fstream)
    if v is None: return None
    fstream.seek(fstream.tell()-8)
    return v

def writeInt64(fstream, v):
    fstream.write(struct.pack('<q', v))


#--- Int32 ---
def readInt32(fstream):
    buf = fstream.read(4)
    if len(buf) != 4 :
        fstream.seek(fstream.tell() - len(buf))
        return None
    return struct.unpack('<i', buf)[0]

def peekInt32(fstream):
    v = readInt32(fstream)
    if v is None: return None
    fstream.seek(fstream.tell()-4)
    return v

def writeInt32(fstream, v):
    fstream.write(struct.pack('<i', v))

#--- Int16 ---
def readInt16(fstream):
    buf = fstream.read(2)
    if len(buf) != 2 :
        fstream.seek(fstream.tell() - len(buf))
        return None
    return struct.unpack('<h', buf)[0]

def peekInt16(fstream):
    v = readInt16(fstream)
    if v is None: return None
    fstream.seek(fstream.tell()-2)
    return v

def writeInt16(fstream, v):
    fstream.write(struct.pack('<h', v))

#--- Int8 ---
def readInt8(fstream):
    buf = fstream.read(1)
    return struct.unpack('<b', buf)[0] if len(buf) == 1 else None

def peekInt8(fstream):
    v = readInt8(fstream)
    if v is None: return None
    fstream.seek(fstream.tell()-1)
    return v

def writeInt8(fstream, v):
    fstream.write(struct.pack('<b', v))

#--- Char ---
def readChar(fstream):
    buf = fstream.read(1)
    return struct.unpack('<c', buf)[0].decode() if len(buf) == 1 else None

def peekChar(fstream):
    v = readChar(fstream)
    if v is None: return None
    fstream.seek(fstream.tell()-1)
    return v

def writeChar(fstream, v):
    fstream.write(struct.pack("<c", v))

#--- Float32 ---
def readFloat32(fstream):
    buf = fstream.read(4)
    if len(buf) != 4 :
        fstream.seek(fstream.tell() - len(buf))
        return None
    return struct.unpack('<f', buf)[0]

def peekFloat32(fstream):
    v = readFloat32(fstream)
    if v is None: return None
    fstream.seek(fstream.tell()-4)
    return v

def writeFloat32(fstream, v):
    fstream.write(struct.pack('<f', v))

#--- Str ---
def readStr(fstream, end=b'\x00'):
    b = fstream.read(1)
    if b is None: return None
    buf = bytearray()
    while True:
        if b == end: break
        buf.append(b)
        b = fstream.read(1)
    return buf.decode()

def peekStr(fstream, end=b'\x00'):
    s = readStr(fstream, end=end)
    if s is None: return None
    fstream.seek(fstream.tell()-len(s))
    return s

def writeStr(fstream, s, end=b'\x00'):
    if isinstance(s, bytes) or isinstance(s, bytearray):
        fstream.write(s + end)
        return
    elif not isinstance(s, str):
        s = str(s)
    fstream.write(s.encode() + end)
