# vim: expandtab tabstop=4 shiftwidth=4

class DSPFTWException(Exception):
    pass

class SignalTypeException(DSPFTWException):
    pass

class DataTypeException(DSPFTWException):
    pass

class EndiannessException(DSPFTWException):
    pass
