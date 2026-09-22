# vim: expandtab tabstop=4 shiftwidth=4

import unittest

from numpy import array
from numpy.testing import assert_array_equal

import dspftw
from dspftw.exceptions import DSPFTWException


class TestBaseConvertToDecimal(unittest.TestCase):

    def test_single_binary_number(self):
        base_array = array([1, 0, 1])

        result = dspftw.base_convert_to_decimal(base_array, 2)

        assert_array_equal(result, array([5]))

    def test_multiple_base4_numbers(self):
        base_array = array([
            [1, 2, 3],
            [0, 1, 2],
            [1, 0, 1],
        ])

        result = dspftw.base_convert_to_decimal(base_array, 4)

        assert_array_equal(result, array([17, 36, 57]))

    def test_base2num_alias(self):
        base_array = array([1, 0, 1])

        result = dspftw.base2num(base_array, 2)

        assert_array_equal(result, array([5]))

    def test_invalid_digit(self):
        base_array = array([1, 4, 2])

        with self.assertRaises(DSPFTWException):
            dspftw.base_convert_to_decimal(base_array, 4)

    def test_negative_digit(self):
        base_array = array([1, -1, 2])

        with self.assertRaises(DSPFTWException):
            dspftw.base_convert_to_decimal(base_array, 4)

    def test_noninteger_digit(self):
        base_array = array([1, 1.5, 2])

        with self.assertRaises(DSPFTWException):
            dspftw.base_convert_to_decimal(base_array, 4)

    def test_invalid_base(self):
        base_array = array([1, 0, 1])

        with self.assertRaises(DSPFTWException):
            dspftw.base_convert_to_decimal(base_array, 1)

    def test_noninteger_base(self):
        base_array = array([1, 0, 1])

        with self.assertRaises(DSPFTWException):
            dspftw.base_convert_to_decimal(base_array, 2.5)

    def test_too_many_dimensions(self):
        base_array = array([[[1, 0], [0, 1]]])

        with self.assertRaises(DSPFTWException):
            dspftw.base_convert_to_decimal(base_array, 2)

    def test_zero_dimensions(self):
        base_array = array(1)

        with self.assertRaises(DSPFTWException):
            dspftw.base_convert_to_decimal(base_array, 2)

if __name__ == '__main__':
    unittest.main()
