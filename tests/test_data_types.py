# vim: expandtab tabstop=4 shiftwidth=4

import unittest

import dspftw

class FullDataTypeTests(unittest.TestCase):
    def test_create(self):
        dspftw.FullDataType('uint8', 'l')
        dspftw.FullDataType('f64', 'b')

    def test_exceptions(self):
        with self.assertRaises(dspftw.DataTypeException):
            dspftw.FullDataType('f8', 'l')

        with self.assertRaises(dspftw.EndiannessException):
            dspftw.FullDataType('f32', 'h')

        with self.assertRaises(dspftw.DataTypeException):
            dspftw.FullDataType('u4', 'big')
