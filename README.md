# DSPFTW

Starting points and helper functions for learning digital signal processing.

## Versioning

DSPFTW maintains two independent version identifiers:

- **Release version:** A calendar-based version in the format
  `YEAR.DAY_OF_YEAR.MINUTE_OF_DAY`, used for PyPI releases.
- **Maturity version:** A semantic version indicating the
  library's development maturity.

**Current maturity version: 0.2.0**

The library is functional and tested across supported Python
versions, but its public API may change as development continues.
A maturity version of 1.0.0 will indicate a stable public API.

## Setup

Requires Python 3.10 or newer (Python 3.10 through 3.14 supported).

```sh
python3 -m pip install dspftw --user
```

## Intro

### Decomposition

[Superposition: The foundation of DSP](http://www.dspguide.com/ch5/6.htm)

### Sinusoids
Prefer to use the complex exponential form instead of real, as it's a more natural fit for fourier analysis and synthesis.

The following functions represent a complex sinusoid.  They are equivalent, and take the same parameters:

* A = Amplitude (y axis is amplitude).
* f = Frequency (cycles per second) in Hertz.  It is multiplied by 2π to get radians per second.
* t = Time in seconds.  These functions work in the time domain (x axis is time).
* ϕ = Phase offset at t=0, in radians.

```
z(t) = A*exp(j*(2π*f*t+ϕ))

z(t) = A*cos(2π*f*t+ϕ)+j*A*sin(2π*f*t+ϕ)
```

We can define this in Python with the following.

```python
import numpy as np

# Here we use the name "complex_sinusoid" instead of just "z".
def complex_sinusoid(A, f, t, phi): return A * np.exp(1j*(2*np.pi*f*t+phi))
```

In fact, this is defined in the `dspftw` package, so let's import that.

```python
import dspftw
```

We can create our own sinusoid by defining everything except `t`.

```python
def my_sinusoid(t): return dspftw.complex_sinusoid(A=5, f=5, t=t, phi=0)
```

We can get the signal at a bunch of times thanks to numpy arrays.  We use `numpy.linspace` to generate the evenly spaced times.

```python
import numpy as np
times = np.linspace(0, 1, num=25)  # 25 evenly spaced values between 0 and 1
my_signal = my_sinusoid(times)  # returns an array of complex values representing the signal
```

Now plot the real and imaginary components of the complex sinusoid using Matplotlib.

```python
import matplotlib.pyplot as plt

plt.plot(times, my_signal.real, label='Real')
plt.plot(times, my_signal.imag, label='Imaginary')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()
```

[Complex Exponential Signals](https://www.cs.ccu.edu.tw/~wtchu/courses/2012s_DSP/Lectures/Lecture%203%20Complex%20Exponential%20Signals.pdf)

### Roots of Unity
![Roots of Unity Animation](https://mathworld.wolfram.com/images/gifs/rootsu.gif)

[Wolfram Mathworld](https://mathworld.wolfram.com/RootofUnity.html)

### Delta Function

### Conjugate

[Complex Conjugate](https://en.wikipedia.org/wiki/Complex_conjugate)

### Convolution

[Convolution](https://www.dspguide.com/ch6/2.htm)

### Correlation

[numpy.correlate](https://numpy.org/doc/stable/reference/generated/numpy.correlate.html)


#### Signal Correlation

`dspftw.signal_correlation()` computes the cross-correlation of two
one-dimensional signals, with optional normalization.

The function supports `full`, `same`, and `valid` output modes.

For large signals, it uses overlap-save FFT processing to reduce
peak memory usage.

The `block` parameter controls processing:

- `block=None` (default): Automatically selects the implementation.
  Signals containing at most 2**22 samples use the original SciPy
  implementation. Larger signals use overlap-save processing with
  a default block size of 2**16 samples.
- `block=0`: Forces the original SciPy implementation.
- `block=N` (positive integer): Uses overlap-save processing with
  N new samples per block.

Example:

```python
from dspftw import signal_correlation

# Automatic processing
result = signal_correlation(signal, reference, norm=True)

# Explicit overlap-save processing
result = signal_correlation(signal, reference, norm=True,
                            block=65536)
```

For a one-million-sample complex64 signal and a 1024-sample reference,
benchmarking showed approximately 66% less additional peak memory
with blocked processing compared with the original implementation.

### Kronecker Product

[numpy.kron](https://numpy.org/doc/stable/reference/generated/numpy.kron.html)

### Sample Signals

[SigIDWiki sample signals](https://www.sigidwiki.com/)

### Loading Signals

#### Complex 8 bit

```python
import numpy as np
signal = np.fromfile('filename', dtype='b')  # load the whole file
signal = np.fromfile('filename', dtype='b', count=1024)  # only load the first 1024 bytes of the file
signal = np.fromfile('filename', dtype='b', offset=1024)  # skip the first 1024 bytes of the file
signal = np.fromfile('filename', dtype='b', offset=1024, count=1024)  # skip 1024, then load 1024
```

This just loads the values as an array of real numbers, but we want it as complex.  We have to interpret every other value as the imaginary component.

```python
signal = signal[0::2] + signal[1::2]*1j
```

#### Complex 32 bit float, little-endian (x86)

```python
signal = np.fromfile('filename', dtype='<f')
```

`count` and `offset` work as above, but note that `offset` is in bytes, so you must multiple by 4 since there are 4 bytes in 32 bits.


#### Complex 32 bit float, big-endian

```python
signal = np.fromfile('filename', dtype='>f')
```

`count` and `offset` work as above, but note that `offset` is in bytes, so you must multiple by 4 since there are 4 bytes in 32 bits.

#### Loading Signals with DSPFTW

The `dspftw.load_signal()` function supports real and complex binary recordings in five formats: `8t`, `16t`, `32t` (signed two's-complement integers), and `32f`, `64f` (floating-point).

By default, integer recordings are normalized to floating-point values, and complex recordings are returned as NumPy complex arrays.

For large recordings, `memory_map=True` allows NumPy to access samples directly through a memory-mapped file without first loading the entire recording into a separate array.

##### Memory-Mapped Floating-Point Signals

```python
from dspftw import load_signal

signal = load_signal(
    "recording.bin",
    "32f",
    "complex",
    endianness="big",
    memory_map=True,
)
```

Both little-endian and big-endian `32f` and `64f` recordings retain their original byte order and remain memory-mapped without an initial byte-swapping operation.

Real signals return one-dimensional floating-point arrays. Complex signals return one-dimensional NumPy complex arrays.

##### Memory-Mapped Two's-Complement Integer Signals

For `8t`, `16t`, and `32t` recordings, use `normalize=False` to preserve the original integer samples and avoid converting the entire recording into floating-point values.

```python
signal = load_signal(
    "recording.bin",
    "16t",
    "complex",
    memory_map=True,
    normalize=False,
)
```

Complex integer recordings return a two-dimensional array with shape `(N, 2)`:

```python
i_samples = signal[:, 0]
q_samples = signal[:, 1]
```

Column 0 contains the in-phase (I) samples, and column 1 contains the quadrature (Q) samples. Both columns remain backed by the memory-mapped file.

Real integer recordings return a one-dimensional integer array.

The original signed integer dtype and byte order are preserved. Neither normalization nor byte swapping is performed. The `rounding` argument has no effect in this mode.

`normalize=False` requires `memory_map=True` and is supported only for two's-complement integer recordings.

##### Normalized Integer Signals

The default is `normalize=True`, preserving the library's existing behavior.

When integer samples are normalized, the result is a new floating-point array, even if `memory_map=True`. Therefore, normalized integer recordings do not retain the zero-copy advantage of raw memory-mapped loading.

##### Memory-Mapping Considerations

Memory maps use copy-on-write mode (`mode='c'`). Changes to the returned array do not modify the original recording file.

Memory mapping avoids an initial full-array copy, but accessing samples still consumes physical memory through operating-system memory management. Mathematical operations that create new arrays can also allocate additional memory.

For empty selections, the function returns an ordinary empty NumPy array because an empty file region cannot be memory-mapped.
