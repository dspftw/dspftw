# vim: expandtab tabstop=4 shiftwidth=4

"""Regression tests for blocked signal correlation."""

import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

import dspftw
from dspftw.exceptions import DSPFTWException


class TestSignalCorrelationBlocked(unittest.TestCase):
    """Verify blocked correlation against legacy correlation."""

    BLOCK = 128
    PATTERN_LENGTH = 13

    @staticmethod
    def make_signals(length, pattern_length, dtype):
        """Generate repeatable complex-valued test signals."""
        rng = np.random.default_rng(12345)

        signal = (
            rng.standard_normal(length)
            + 1j * rng.standard_normal(length)
        ).astype(dtype)

        pattern = (
            rng.standard_normal(pattern_length)
            + 1j * rng.standard_normal(pattern_length)
        ).astype(dtype)

        return signal, pattern

    def compare_blocked(
        self,
        length,
        pattern_length,
        dtype,
        norm,
        mode,
    ):
        """Compare blocked output with the legacy implementation."""
        signal, pattern = self.make_signals(
            length,
            pattern_length,
            dtype,
        )

        expected = dspftw.signal_correlation(
            signal.astype(np.complex128),
            pattern.astype(np.complex128),
            norm=norm, mode=mode, method='fft', block=0)

        actual = dspftw.signal_correlation(
            signal,
            pattern,
            norm=norm,
            mode=mode,
            method='fft',
            block=self.BLOCK,
        )

        self.assertEqual(actual.shape, expected.shape)

        assert_allclose(
            actual,
            expected,
            rtol=1e-6,
            atol=1e-6,
        )

    def test_block_boundaries(self):
        """Verify output across overlap-save boundaries."""
        lengths = [
            self.BLOCK - 1,
            self.BLOCK,
            self.BLOCK + 1,
            2 * self.BLOCK - 1,
            2 * self.BLOCK,
            2 * self.BLOCK + 1,
            3 * self.BLOCK - 1,
            3 * self.BLOCK + 1,
        ]

        for length in lengths:
            for dtype in (np.complex64, np.complex128):
                for norm in (False, True):
                    for mode in ('full', 'same', 'valid'):
                        with self.subTest(
                            length=length,
                            dtype=dtype,
                            norm=norm,
                            mode=mode,
                        ):
                            self.compare_blocked(
                                length,
                                self.PATTERN_LENGTH,
                                dtype,
                                norm,
                                mode,
                            )

    def test_pattern_near_block_length(self):
        """Verify processing with a relatively long pattern."""
        for pattern_length in (63, 127, 128, 129):
            signal, pattern = self.make_signals(
                400,
                pattern_length,
                np.complex64,
            )

            expected = dspftw.signal_correlation(
                signal,
                pattern,
                norm=True,
                method='fft',
                block=0,
            )

            actual = dspftw.signal_correlation(
                signal,
                pattern,
                norm=True,
                method='fft',
                block=self.BLOCK,
            )

            assert_allclose(
                actual,
                expected,
                rtol=1e-6,
                atol=1e-6,
            )


    def test_zero_energy_across_boundary(self):
        """Verify normalization when zero-energy regions cross blocks."""
        signal = np.zeros(3 * self.BLOCK, dtype=np.complex64)
        pattern = np.ones(
            self.PATTERN_LENGTH,
            dtype=np.complex64,
        )

        signal[self.BLOCK - 5:self.BLOCK + 5] = 1 + 1j

        expected = dspftw.signal_correlation(
            signal.astype(np.complex128),
            pattern.astype(np.complex128),
            norm=True,
            method='fft',
            block=0,
        )

        actual = dspftw.signal_correlation(
            signal,
            pattern,
            norm=True,
            method='fft',
            block=self.BLOCK,
        )

        self.assertTrue(np.all(np.isfinite(actual)))

        # Count nonzero signal samples in each correlation window.
        active = np.convolve(
            (signal != 0).astype(np.int64),
            np.ones(len(pattern), dtype=np.int64),
            mode='full',
        ) > 0

        # Truly zero-energy windows must produce exactly zero.
        self.assertTrue(np.all(actual[~active] == 0))

        # Compare with legacy only where signal energy exists.
        assert_allclose(
            actual[active],
            expected[active],
            rtol=1e-6,
            atol=1e-6,
        )

    def test_unnormalized_matches_scipy(self):
        """Verify correlation convention and complex conjugation."""
        from scipy.signal import correlate

        signal, pattern = self.make_signals(
            2 * self.BLOCK + 1,
            self.PATTERN_LENGTH,
            np.complex64,
        )

        expected = correlate(
            signal.astype(np.complex128),
            pattern.astype(np.complex128),
            mode='full',
            method='fft',
        )

        actual = dspftw.signal_correlation(
            signal,
            pattern,
            norm=False,
            mode='full',
            method='fft',
            block=self.BLOCK,
        )

        assert_allclose(
            actual,
            expected,
            rtol=1e-6,
            atol=1e-6,
        )

    def test_automatic_block_selection(self):
        """Verify default processing agrees with legacy processing."""
        signal, pattern = self.make_signals(
            3 * self.BLOCK,
            self.PATTERN_LENGTH,
            np.complex64,
        )

        expected = dspftw.signal_correlation(
            signal,
            pattern,
            norm=True,
            block=0,
        )

        actual = dspftw.signal_correlation(
            signal,
            pattern,
            norm=True,
        )

        assert_allclose(
            actual,
            expected,
            rtol=1e-6,
            atol=1e-6,
        )

    def test_invalid_block_values(self):
        """Reject invalid block specifications."""
        signal = np.ones(100)
        pattern = np.ones(10)

        for block in (-1, 1.5, '128', True):
            with self.subTest(block=block):
                with self.assertRaises(DSPFTWException):
                    dspftw.signal_correlation(
                        signal,
                        pattern,
                        block=block,
                    )

    def test_short_signal_rejected(self):
        """Preserve existing signal-length validation."""
        signal = np.ones(5)
        pattern = np.ones(10)

        for block in (0, self.BLOCK):
            with self.subTest(block=block):
                with self.assertRaises(DSPFTWException):
                    dspftw.signal_correlation(
                        signal,
                        pattern,
                        block=block,
                    )



    def test_normalized_full_small(self):
        """Verify normalized blocked correlation against legacy."""
        signal, pattern = self.make_signals(
            257, 13, np.complex128
        )

        expected = dspftw.signal_correlation(
            signal, pattern,
            norm=True, mode='full',
            method='fft', block=0
        )

        actual = dspftw.signal_correlation(
            signal, pattern,
            norm=True, mode='full',
            method='fft', block=128
        )

        assert_allclose(
            actual, expected,
            rtol=1e-6, atol=1e-6
        )

    def test_automatic_large_signal_selection(self):
        """Verify automatic selection uses blocked processing."""
        from unittest.mock import patch
        from importlib import import_module
        correlation_module = import_module('dspftw.signal_correlation')

        rng = np.random.default_rng(12345)
        signal = (
            rng.standard_normal(300)
            + 1j * rng.standard_normal(300)
        ).astype(np.complex64)

        pattern = (
            rng.standard_normal(13)
            + 1j * rng.standard_normal(13)
        ).astype(np.complex64)

        with patch.object(correlation_module, 'BLOCK_DEFAULT', 128):
            actual = dspftw.signal_correlation(
                signal,
                pattern,
                norm=True,
                block=None,
            )

            expected = dspftw.signal_correlation(
                signal,
                pattern,
                norm=True,
                block=correlation_module.BLOCK_SIZE_DEFAULT,
            )

        assert_allclose(
            actual,
            expected,
            rtol=1e-6,
            atol=1e-6,
        )

if __name__ == '__main__':
    unittest.main()
