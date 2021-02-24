# vim: expandtab tabstop=4 shiftwidth=4

import unittest

import dspftw

class FullSignalTypeTests(unittest.TestCase):
    def test_create(self):
        dspftw.FullSignalType('8t', 'cplx', 'l')
        dspftw.FullSignalType('64f', 'r', 'b')

    def test_exceptions(self):
        with self.assertRaises(dspftw.SignalTypeException):
            dspftw.FullSignalType('4t', 'cplx', 'little')

        with self.assertRaises(dspftw.EndiannessException):
            dspftw.FullSignalType('8t', 'cplx', 'h')

        with self.assertRaises(dspftw.NumberSpaceException):
            dspftw.FullSignalType('8t', 'potato', 'big')
