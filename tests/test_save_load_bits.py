# vim: expandtab tabstop=4 shiftwidth=4

from math import ceil
from pathlib import Path
from random import choice
from tempfile import TemporaryDirectory

import unittest

import dspftw

class SaveLoadBitsTests(unittest.TestCase):
    def test_save_load_packed(self):
        with TemporaryDirectory() as tempdir:
            temp_path = Path(tempdir)
            temp_file = temp_path.joinpath('bits_file')

            bits = [choice((True, False)) for i in range(987)]  # length not a multiple of 8

            num_bytes_written = dspftw.save_bits(str(temp_file), bits)
            self.assertEqual(num_bytes_written, ceil(len(bits) / 8.0))

            loaded_bits = dspftw.load_bits(str(temp_file))

            for i in range(len(bits)):
                self.assertEqual(bits[i], loaded_bits[i])

    def test_save_load_unpacked(self):
        with TemporaryDirectory() as tempdir:
            temp_path = Path(tempdir)
            temp_file = temp_path.joinpath('bits_file')

            bits = [choice((True, False)) for i in range(987)]  # length not a multiple of 8

            num_bytes_written = dspftw.save_bits(str(temp_file), bits, packed=False)
            self.assertEqual(num_bytes_written, len(bits))

            loaded_bits = dspftw.load_bits(str(temp_file), packed=False)

            for i in range(len(loaded_bits)):
                self.assertEqual(bits[i], loaded_bits[i])
