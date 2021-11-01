import io

class GVASError(Exception):
    def __init__(self,  msg):
        Exception.__init__(self, "GVAS | " + msg)

class GVASFileFormatError(GVASError):
    def __init__(self, file, msg):
        if isinstance(file, io.IOBase):
            fname = file.name
        else:
            fname = file
        GVASError.__init__(self, "GVASFileFormatError with file {}: ".format(fname)+msg)

class GVASNotImplemented(GVASError):
    def __init__(self, msg):
        GVASError.__init__(self, "GVASNotImplemented: " + msg)

class GVASParserNotImplemented(GVASNotImplemented):
    def __init__(self, msg):
        GVASNotImplemented.__init__(self, "Parser: " + msg)

class GVASSerializerNotImplemented(GVASNotImplemented):
    def __init__(self, msg):
        GVASNotImplemented.__init__(self, "Serializer: " + msg)
