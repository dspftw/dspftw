# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from tempfile import TemporaryDirectory

import unittest

from numpy import array
from numpy.testing import assert_allclose

import dspftw


class LoadSignalTests(unittest.TestCase):
    def test_real_16t(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [-32768, -16384, 0, 16384, 32767],
                dtype='<i2',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '16t',
                'real',
                'little',
            )

            expected = array([
                -1.0,
                -0.5,
                0.0,
                0.5,
                32767 / 32768,
            ])

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'float64')

    def test_complex_16t(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            # Interleaved I, Q samples
            data = array(
                [16384, -16384, 8192, 24576],
                dtype='<i2',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '16t',
                'complex',
                'little',
            )

            expected = array([
                0.5 - 0.5j,
                0.25 + 0.75j,
            ])

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'complex128')

    def test_real_32f(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [-1.0, -0.5, 0.0, 0.5, 1.0],
                dtype='<f4',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '32f',
                'real',
                'little',
            )

            assert_allclose(result, data)
            self.assertEqual(result.dtype.name, 'float32')

    def test_complex_32f(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [0.5, -0.5, 0.25, 0.75],
                dtype='<f4',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '32f',
                'complex',
                'little',
            )

            expected = array(
                [0.5 - 0.5j, 0.25 + 0.75j],
                dtype='complex64',
            )

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'complex64')

    def test_start_sample_and_num_samples(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
                dtype='<f4',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '32f',
                'real',
                'little',
                num_samples=3,
                start_sample=2,
            )

            expected = array(
                [2.0, 3.0, 4.0],
                dtype='float32',
            )

            assert_allclose(result, expected)

    def test_big_endian(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [16384, -16384, 8192],
                dtype='>i2',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '16t',
                'real',
                'big',
            )

            expected = array([
                0.5,
                -0.5,
                0.25,
            ])

            assert_allclose(result, expected)


    def test_true_one_rounding(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [-32768, -16384, 0, 16384, 32767],
                dtype='<i2',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '16t',
                'real',
                'little',
                rounding=1,
            )

            scale = 32768
            expected = data / scale + 1 / (2 * scale)

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'float64')

    def test_complex_start_sample_and_num_samples(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            # Four complex samples stored as interleaved I, Q values:
            # (1+2j), (3+4j), (5+6j), (7+8j)
            data = array(
                [
                    1.0, 2.0,
                    3.0, 4.0,
                    5.0, 6.0,
                    7.0, 8.0,
                ],
                dtype='<f4',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '32f',
                'complex',
                'little',
                num_samples=2,
                start_sample=1,
            )

            expected = array(
                [
                    3.0 + 4.0j,
                    5.0 + 6.0j,
                ],
                dtype='complex64',
            )

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'complex64')


    def test_memory_map_complex_float(self):
        """Memory-mapped complex floats should share mapped storage."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        expected = np.array(
            [1 + 2j, 3 + 4j, 5 + 6j],
            dtype=np.complex64
        )

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "complex32f.bin")
            expected.view(np.float32).tofile(filename)

            actual = load_signal(
                filename,
                "32f",
                "complex",
                memory_map=True
            )

            np.testing.assert_array_equal(actual, expected)
            self.assertEqual(actual.dtype, np.dtype("complex64"))

            # The returned array must share storage with a memory map.
            base = actual

            while isinstance(base, np.ndarray):
                if isinstance(base, np.memmap):
                    break
                base = base.base

            self.assertIsInstance(base, np.memmap)


    def test_memory_map_big_endian_preserves_file(self):
        """Big-endian memory mapping must not modify the source file."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        expected = np.array(
            [1 + 2j, 3 + 4j, 5 + 6j],
            dtype=np.complex64
        )

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "big_endian.bin")

            # Write interleaved I/Q samples in big-endian format.
            expected.view(np.float32).astype(">f4").tofile(filename)

            with open(filename, "rb") as file:
                original_bytes = file.read()

            actual = load_signal(
                filename,
                "32f",
                "complex",
                endianness="big",
                memory_map=True
            )

            np.testing.assert_array_equal(actual, expected)
            self.assertEqual(actual.dtype, np.dtype(">c8"))

            # Verify the source file remains byte-for-byte unchanged.
            with open(filename, "rb") as file:
                final_bytes = file.read()

            self.assertEqual(original_bytes, final_bytes)


    def test_memory_map_count_beyond_eof(self):
        """Memory mapping should return available samples beyond EOF."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        expected = np.arange(10, dtype=np.float32)

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "short_signal.bin")
            expected.tofile(filename)

            actual = load_signal(
                filename,
                "32f",
                "real",
                num_samples=20,
                memory_map=True,
            )

            np.testing.assert_array_equal(actual, expected)


    def test_memory_map_empty_file(self):
        """Memory-mapped loading should handle an empty file."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "empty.bin")

            # Create an empty binary file.
            open(filename, "wb").close()

            for number_space in ("real", "complex"):
                with self.subTest(number_space=number_space):
                    expected = load_signal(
                        filename,
                        "32f",
                        number_space,
                    )

                    actual = load_signal(
                        filename,
                        "32f",
                        number_space,
                        memory_map=True,
                    )

                    np.testing.assert_array_equal(actual, expected)
                    self.assertEqual(actual.dtype, expected.dtype)


    def test_memory_map_offset_beyond_eof(self):
        """Loading beyond EOF should return an empty array."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "short_signal.bin")
            np.arange(10, dtype=np.float32).tofile(filename)

            for number_space in ("real", "complex"):
                for memory_map in (False, True):
                    with self.subTest(
                        number_space=number_space,
                        memory_map=memory_map,
                    ):
                        actual = load_signal(
                            filename,
                            "32f",
                            number_space,
                            start_sample=20,
                            memory_map=memory_map,
                        )

                        self.assertEqual(actual.size, 0)
                        self.assertEqual(
                            actual.dtype,
                            np.dtype(
                                "complex64"
                                if number_space == "complex"
                                else "float32"
                            ),
                        )


    def test_memory_map_incomplete_complex_sample(self):
        """Compare loading behavior for an incomplete I/Q pair."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "incomplete_complex.bin")

            # Two complete complex samples plus an unmatched I value.
            np.array(
                [1, 2, 3, 4, 5],
                dtype=np.float32
            ).tofile(filename)

            for memory_map in (False, True):
                with self.subTest(memory_map=memory_map):
                    with self.assertRaises(ValueError):
                        load_signal(
                            filename,
                            "32f",
                            "complex",
                            memory_map=memory_map,
                        )


    def test_memory_map_integer_signal(self):
        """Memory-mapped integer loading should match normal loading."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "integer_signal.bin")

            np.array(
                [-32768, -16384, 0, 16384, 32767],
                dtype=">i2",
            ).tofile(filename)

            for rounding in (0, 1):
                with self.subTest(rounding=rounding):
                    expected = load_signal(
                        filename,
                        "16t",
                        "real",
                        endianness="big",
                        rounding=rounding,
                    )

                    actual = load_signal(
                        filename,
                        "16t",
                        "real",
                        endianness="big",
                        rounding=rounding,
                        memory_map=True,
                    )

                    np.testing.assert_array_equal(actual, expected)
                    self.assertEqual(actual.dtype, expected.dtype)


    def test_memory_map_raw_complex_16t(self):
        """Raw complex 16t data should remain file-backed integers."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        expected = np.array(
            [
                [1000, -2000],
                [3000, -4000],
                [5000, -6000],
            ],
            dtype=np.int16,
        )

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "complex16t.bin")

            # Store I/Q components as interleaved 16-bit integers.
            expected.reshape(-1).tofile(filename)

            with open(filename, "rb") as file:
                original_bytes = file.read()

            actual = load_signal(
                filename,
                "16t",
                "complex",
                memory_map=True,
                normalize=False,
            )

            # Verify the returned values, shape, and integer dtype.
            np.testing.assert_array_equal(actual, expected)
            self.assertEqual(actual.shape, (3, 2))
            self.assertEqual(actual.dtype, np.dtype("int16"))

            # Verify the result is backed by memory-mapped storage.
            base = actual
            while isinstance(base, np.ndarray):
                if isinstance(base, np.memmap):
                    break
                base = base.base

            self.assertIsInstance(base, np.memmap)

            # Verify the source file has not changed.
            with open(filename, "rb") as file:
                self.assertEqual(file.read(), original_bytes)


    def test_memory_map_raw_integer_formats(self):
        """Raw integer memory maps preserve dtype, shape, and values."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        formats = (
            ("8t", "i1"),
            ("16t", "i2"),
            ("32t", "i4"),
        )

        with tempfile.TemporaryDirectory() as directory:
            for signal_type, dtype_code in formats:
                for endianness in ("little", "big"):
                    for number_space in ("real", "complex"):
                        with self.subTest(
                            signal_type=signal_type,
                            endianness=endianness,
                            number_space=number_space,
                        ):
                            file_dtype = np.dtype(
                                ("<" if endianness == "little" else ">")
                                + dtype_code
                            )

                            values = np.array(
                                [10, -20, 30, -40, 50, -60],
                                dtype=file_dtype,
                            )

                            filename = os.path.join(
                                directory,
                                "raw_integer.bin",
                            )
                            values.tofile(filename)

                            actual = load_signal(
                                filename,
                                signal_type,
                                number_space,
                                endianness=endianness,
                                memory_map=True,
                                normalize=False,
                            )

                            if number_space == "complex":
                                expected = values.reshape(-1, 2)
                            else:
                                expected = values

                            np.testing.assert_array_equal(
                                actual, expected
                            )
                            self.assertEqual(
                                actual.shape, expected.shape
                            )
                            self.assertEqual(
                                actual.dtype, file_dtype
                            )

                            # Verify that mapped storage is retained.
                            base = actual
                            while isinstance(base, np.ndarray):
                                if isinstance(base, np.memmap):
                                    break
                                base = base.base

                            self.assertIsInstance(base, np.memmap)


    def test_raw_integer_requires_memory_map(self):
        """Raw integer loading requires memory_map=True."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "signal.bin")
            np.array([100, -200], dtype=np.int16).tofile(filename)

            with self.assertRaisesRegex(
                ValueError,
                "normalize=False requires memory_map=True",
            ):
                load_signal(
                    filename,
                    "16t",
                    "real",
                    memory_map=False,
                    normalize=False,
                )

            # Default non-mapped loading still returns normalized floats.
            actual = load_signal(
                filename,
                "16t",
                "real",
            )

            expected = np.array([100, -200], dtype=np.float64) / 32768
            np.testing.assert_array_equal(actual, expected)
            self.assertEqual(actual.dtype, np.dtype("float64"))


    def test_memory_map_non_native_float_zero_copy(self):
        """Non-native-endian floats must remain file-backed without swapping."""
        import os
        import sys
        import tempfile
        import numpy as np
        from dspftw import load_signal

        endianness = "big" if sys.byteorder == "little" else "little"
        prefix = ">" if endianness == "big" else "<"

        with tempfile.TemporaryDirectory() as directory:
            for signal_type, float_code, complex_code in (
                ("32f", "f4", "c8"),
                ("64f", "f8", "c16"),
            ):
                for number_space in ("real", "complex"):
                    with self.subTest(
                        signal_type=signal_type,
                        number_space=number_space,
                    ):
                        dtype = np.dtype(prefix + float_code)
                        values = np.array(
                            [1.25, -2.5, 3.75, -4.125],
                            dtype=dtype,
                        )

                        filename = os.path.join(directory, "signal.bin")
                        values.tofile(filename)

                        with open(filename, "rb") as file:
                            original_bytes = file.read()

                        actual = load_signal(
                            filename,
                            signal_type,
                            number_space,
                            endianness=endianness,
                            memory_map=True,
                        )

                        if number_space == "complex":
                            expected = np.array(
                                [1.25 - 2.5j, 3.75 - 4.125j]
                            )
                            expected_dtype = np.dtype(
                                prefix + complex_code
                            )
                        else:
                            expected = values
                            expected_dtype = dtype

                        np.testing.assert_array_equal(actual, expected)

                        # Preserve the file's original byte order.
                        self.assertEqual(actual.dtype, expected_dtype)

                        # Confirm that the result remains memory-mapped.
                        base = actual
                        while isinstance(base, np.ndarray):
                            if isinstance(base, np.memmap):
                                break
                            base = base.base

                        self.assertIsInstance(base, np.memmap)

                        # The underlying mapped bytes must be unchanged.
                        # This catches eager copy-on-write byte swapping.
                        self.assertEqual(
                            base.tobytes(),
                            original_bytes,
                        )

                        # The original file must remain unchanged.
                        with open(filename, "rb") as file:
                            self.assertEqual(file.read(), original_bytes)


    def test_memory_map_float_abbreviated_endianness(self):
        """Memory-mapped floats support abbreviated byte-order arguments."""
        import os
        import tempfile
        import numpy as np
        from dspftw import load_signal

        with tempfile.TemporaryDirectory() as directory:
            for signal_type, float_code, complex_code in (
                ("32f", "f4", "c8"),
                ("64f", "f8", "c16"),
            ):
                for endianness, prefix in (("b", ">"), ("l", "<")):
                    for number_space in ("real", "complex"):
                        with self.subTest(
                            signal_type=signal_type,
                            endianness=endianness,
                            number_space=number_space,
                        ):
                            values = np.array(
                                [1.25, -2.5, 3.75, -4.125],
                                dtype=np.dtype(prefix + float_code),
                            )

                            filename = os.path.join(
                                directory, "signal.bin"
                            )
                            values.tofile(filename)

                            actual = load_signal(
                                filename,
                                signal_type,
                                number_space,
                                endianness=endianness,
                                memory_map=True,
                            )

                            if number_space == "complex":
                                expected = np.array(
                                    [1.25 - 2.5j, 3.75 - 4.125j]
                                )
                                expected_dtype = np.dtype(
                                    prefix + complex_code
                                )
                            else:
                                expected = values
                                expected_dtype = values.dtype

                            np.testing.assert_array_equal(
                                actual, expected
                            )
                            self.assertEqual(
                                actual.dtype, expected_dtype
                            )

                            # Confirm that the result is file-backed.
                            base = actual
                            while isinstance(base, np.ndarray):
                                if isinstance(base, np.memmap):
                                    break
                                base = base.base

                            self.assertIsInstance(base, np.memmap)

if __name__ == '__main__':
    unittest.main()
