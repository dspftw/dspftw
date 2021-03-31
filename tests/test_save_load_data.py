# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from tempfile import TemporaryDirectory

import unittest

from numpy import array as nparray

import dspftw

class SaveLoadDataTests(unittest.TestCase):
    def try_save_load(self, data, data_type, endianness):
        with TemporaryDirectory() as tempdir:
            temp_path = Path(tempdir)
            file_path = temp_path.joinpath('data_file')

            num_written = dspftw.save_data(str(file_path), data, data_type, endianness)
            self.assertEqual(num_written, len(data))

            loaded_data = dspftw.load_data(str(file_path), data_type, endianness)

            for i in range(len(loaded_data)):
                self.assertEqual(loaded_data[i], data[i])

    def test_save_load(self):
        data = nparray(range(127))  # wrap-around causes values above 127 to fail for int8
        data_types = ('uint8', 'uint16', 'uint32', 'uint64',
                      'int8', 'int16', 'int32', 'int64',
                      'float32', 'float64', 'float128')
        endiannesses = ('little', 'big')

        for data_type in data_types:
            for endianness in endiannesses:
                self.try_save_load(data, data_type, endianness)
