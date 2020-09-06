# DSPFTW

Starting points for learning digital signal processing.

## Setup

If you haven't already, install Python 3.5 or greater, and the `dspftw` package.

```sh
python3 -m pip install dspftw --user
```

## Sinusoids
Prefer to use the complex exponential form instead of real, as it's a more natural fit for fourier analysis and synthesis.

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
times = np.linspace(0, 10, num=10)  # 10 evenly spaced values between 0 and 10
my_signal = my_sinusoid(times)  # returns an array of complex values representing the signal
```

Now plot it out with `dspftw.plot_signal`, which uses matplotlib.

```python
import matplotlib.pyplot as plt
dspftw.plot_signal(my_signal, times)
plt.show()
```

[Complex Exponential Signals](https://www.cs.ccu.edu.tw/~wtchu/courses/2012s_DSP/Lectures/Lecture%203%20Complex%20Exponential%20Signals.pdf)

## Roots of Unity
![Roots of Unity Animation](https://mathworld.wolfram.com/images/gifs/rootsu.gif)

[Wolfram Mathworld](https://mathworld.wolfram.com/RootofUnity.html)

## Sample Signals
* [SigIDWiki sample signals](https://www.sigidwiki.com/)
