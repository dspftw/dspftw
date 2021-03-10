# vim: expandtab tabstop=4 shiftwidth=4

class DSPFTWException(Exception):
    pass

class DataTypeException(DSPFTWException):
    pass

class EndiannessException(DSPFTWException):
    pass

class FileNameException(DSPFTWException):
    pass

class NumberSpaceException(DSPFTWException):
    pass

class SignalTypeException(DSPFTWException):
    pass

class WriteModeException(DSPFTWException):
    pass
