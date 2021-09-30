# vim: expandtab tabstop=4 shiftwidth=4

from math import ceil
from pathlib import Path
from random import choice
from tempfile import TemporaryDirectory

import unittest

import dspftw

class SaveLoadBitsTests(unittest.TestCase):
    def test_save_to_load_packed(self):
        with TemporaryDirectory() as tempdir:
            temp_path = Path(tempdir)
            temp_file = temp_path.joinpath('bits_file')

            bits1 = [choice((True, False)) for i in range(128)]  # length a multiple of 8
            bits2 = [choice((True, False)) for i in range(128)]  # length a multiple of 8

            # write bits1
            with temp_file.open('wb') as outfile:
                num_bytes_written = dspftw.save_bits_to(outfile, bits1)
                self.assertEqual(num_bytes_written, len(bits1) / 8.0)

            # append bits2
            with temp_file.open('ab') as outfile:
                num_bytes_written = dspftw.save_bits_to(outfile, bits2)
                self.assertEqual(num_bytes_written, len(bits2) / 8.0)

            loaded_bits = dspftw.load_bits(str(temp_file))
            all_bits = bits1 + bits2

            self.assertEqual(len(all_bits), len(loaded_bits))

            for i in range(len(all_bits)):
                self.assertEqual(all_bits[i], loaded_bits[i])

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
