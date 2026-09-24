# vim: expandtab tabstop=4 shiftwidth=4

import unittest

from numpy import abs, array, ones, sqrt, zeros
from numpy.testing import assert_allclose, assert_array_equal
from scipy.signal import convolve, correlate

import dspftw
from dspftw.exceptions import DSPFTWException


class TestSignalCorrelation(unittest.TestCase):
    def test_empty_in1(self):
        with self.assertRaises(DSPFTWException):
            dspftw.signal_correlation(array([]), array([1, 2]))

    def test_empty_in2(self):
        with self.assertRaises(DSPFTWException):
            dspftw.signal_correlation(array([1, 2]), array([]))

    def test_in2_longer_than_in1(self):
        with self.assertRaises(DSPFTWException):
            dspftw.signal_correlation(
                array([1, 2]),
                array([1, 2, 3]),
            )

    def test_multidimensional_in1(self):
        with self.assertRaises(DSPFTWException):
            dspftw.signal_correlation(
                array([[1, 2], [3, 4]]),
                array([1, 2]),
            )

    def test_multidimensional_in2(self):
        with self.assertRaises(DSPFTWException):
            dspftw.signal_correlation(
                array([1, 2, 3, 4]),
                array([[1, 2]]),
            )

    def test_invalid_norm(self):
        with self.assertRaises(DSPFTWException):
            dspftw.signal_correlation(
                array([1, 2, 3]),
                array([1, 2]),
                norm='yes',
            )

    def test_invalid_mode(self):
        with self.assertRaises(DSPFTWException):
            dspftw.signal_correlation(
                array([1, 2, 3]),
                array([1, 2]),
                mode='invalid',
            )

    def test_invalid_method(self):
        with self.assertRaises(DSPFTWException):
            dspftw.signal_correlation(
                array([1, 2, 3]),
                array([1, 2]),
                method='invalid',
            )

    def test_partial_match_is_penalized(self):
        reference = ones(4)
        signal = ones(4)

        result = dspftw.signal_correlation(signal, reference)

        self.assertAlmostEqual(result[0], 0.5)
        self.assertAlmostEqual(result[3], 1.0)
        self.assertAlmostEqual(result[-1], 0.5)

    def test_zero_energy(self):
        signal = zeros(4)
        reference = ones(2)

        result = dspftw.signal_correlation(signal, reference)

        self.assertTrue((result == zeros(5)).all())

    def test_zero_reference_energy(self):
        signal = ones(4)
        reference = zeros(2)

        result = dspftw.signal_correlation(signal, reference)

        self.assertTrue((result == zeros(5)).all())

    def test_complex_reference(self):
        reference = array([1+1j, 2-1j, -1+2j])
        signal = array([0, 0, 1+1j, 2-1j, -1+2j, 0])

        result = dspftw.signal_correlation(signal, reference)

        self.assertAlmostEqual(abs(result).max(), 1.0)
        self.assertEqual(abs(result).argmax(), 4)

    def test_no_normalization(self):
        signal = array([1, 2, 3, 4])
        reference = array([1, 2])

        result = dspftw.signal_correlation(signal, reference, norm=False)
        expected = correlate(signal, reference)

        assert_array_equal(result, expected)

    def test_modes(self):
        signal = ones(6)
        reference = ones(3)

        result_full = dspftw.signal_correlation(signal, reference, mode='full')
        result_same = dspftw.signal_correlation(signal, reference, mode='same')
        result_valid = dspftw.signal_correlation(signal, reference, mode='valid')

        self.assertEqual(len(result_full), 8)
        self.assertEqual(len(result_same), 6)
        self.assertEqual(len(result_valid), 4)

    def test_direct_and_fft(self):
        signal = array([1.0, 2.0, -1.0, 3.0, 2.0, -2.0])
        reference = array([1.0, -1.0, 2.0])

        result_direct = dspftw.signal_correlation(
            signal,
            reference,
            method='direct',
        )
        result_fft = dspftw.signal_correlation(
            signal,
            reference,
            method='fft',
        )

        assert_allclose(
            result_direct,
            result_fft,
            rtol=1e-12,
            atol=1e-12,
        )


    def test_valid_normalization(self):
        signal = array([1.0, 2.0, 3.0, 4.0])
        reference = array([1.0, 2.0])

        result = dspftw.signal_correlation(
            signal,
            reference,
            mode='valid',
        )

        expected = array([
            5.0 / (sqrt(5.0) * sqrt(5.0)),
            8.0 / (sqrt(13.0) * sqrt(5.0)),
            11.0 / (5.0 * sqrt(5.0)),
        ])

        assert_allclose(result, expected)


    def test_same_normalization_odd_reference(self):
        signal = array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        reference = ones(3)

        result = dspftw.signal_correlation(
            signal,
            reference,
            mode='same',
        )

        expected_energy = convolve(
            signal**2,
            ones(3),
            mode='same',
        )

        expected = correlate(
            signal,
            reference,
            mode='same',
        ) / sqrt(expected_energy * 3.0)

        assert_allclose(result, expected)


    def test_same_normalization_even_reference(self):
        signal = array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        reference = ones(4)

        result = dspftw.signal_correlation(
            signal,
            reference,
            mode='same',
        )

        expected_energy = convolve(
            signal**2,
            ones(4),
            mode='same',
        )

        expected = correlate(
            signal,
            reference,
            mode='same',
        ) / sqrt(expected_energy * 4.0)

        assert_allclose(result, expected)


    def test_large_dynamic_range(self):
        signal = array([
            1e8, 1.0, 1.0, 1.0, 1.0,
            1e8, 1.0, 1.0, 1.0, 1.0,
        ])
        reference = array([1.0, 2.0, 3.0, 4.0])

        result = dspftw.signal_correlation(
            signal,
            reference,
            mode='full',
            method='direct',
        )

        numerator = correlate(
            signal,
            reference,
            mode='full',
            method='direct',
        )

        signal_energy = convolve(
            abs(signal)**2,
            ones(len(reference)),
            mode='full',
            method='direct',
        )

        reference_energy = (abs(reference)**2).sum()

        denominator = sqrt(signal_energy * reference_energy)

        expected = zeros(len(numerator))
        nonzero = denominator != 0
        expected[nonzero] = numerator[nonzero] / denominator[nonzero]

        assert_allclose(
            result,
            expected,
            rtol=1e-12,
            atol=1e-12,
        )


if __name__ == '__main__':
    unittest.main()
