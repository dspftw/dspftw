# vim: expandtab tabstop=4 shiftwidth=4

import unittest

import dspftw

class FullDataTypeTests(unittest.TestCase):
    def test_create(self):
        dspftw.FullDataType('8t', 'l', 'cplx')
        dspftw.FullDataType('64f', 'b', 'r')

    def test_exceptions(self):
        with self.assertRaises(dspftw.DataTypeException):
            dspftw.FullDataType('4t', 'l', 'cplx')

        with self.assertRaises(dspftw.DataTypeException):
            dspftw.FullDataType('8t', 'h', 'cplx')

        with self.assertRaises(dspftw.DataTypeException):
            dspftw.FullDataType('8t', 'l', 'potato')
