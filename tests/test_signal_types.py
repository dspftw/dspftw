# vim: expandtab tabstop=4 shiftwidth=4

import unittest

import dspftw

class FullSignalTypeTests(unittest.TestCase):
    def test_create(self):
        dspftw.FullSignalType('8t', 'l', 'cplx')
        dspftw.FullSignalType('64f', 'b', 'r')

    def test_exceptions(self):
        with self.assertRaises(dspftw.SignalTypeException):
            dspftw.FullSignalType('4t', 'l', 'cplx')

        with self.assertRaises(dspftw.EndiannessException):
            dspftw.FullSignalType('8t', 'h', 'cplx')

        with self.assertRaises(dspftw.SignalTypeException):
            dspftw.FullSignalType('8t', 'l', 'potato')
