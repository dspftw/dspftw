# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from dspftw import load_bits
from numpy import array as nparray

class LoadBitsTests(unittest.TestCase):
    def test_load_bits(self):
        with TemporaryDirectory() as tempdir:
            tempdir_path = Path(tempdir)
            tempfile = tempdir_path.joinpath('test.bits')
            tempfile.write_bytes(b'\x00\x01\x02\x03')

            bits = load_bits(str(tempfile.resolve()))
            expecting = nparray([False, False, False, False,
                                 False, False, False, False,

                                 False, False, False, False,
                                 False, False, False,  True,

                                 False, False, False, False,
                                 False, False,  True, False,

                                 False, False, False, False,
                                 False, False,  True,  True,],
                                dtype=bool)

            self.assertEqual(len(bits), len(expecting))

            for i in range(len(bits)):
                self.assertEqual(bits[i], expecting[i])

    def test_load_bits_with_offset_count(self):
        with TemporaryDirectory() as tempdir:
            tempdir_path = Path(tempdir)
            tempfile = tempdir_path.joinpath('test.bits')
            tempfile.write_bytes(b'\x00\x01\x02\x03')

            bits = load_bits(str(tempfile.resolve()), offset=19, count=4)
            expecting = nparray([False, False, False, True], dtype=bool)
            self.assertEqual(len(bits), len(expecting))

            for i in range(len(bits)):
                self.assertEqual(bits[i], expecting[i])
