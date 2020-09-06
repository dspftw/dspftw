# DSPFTW

Starting points for learning digital signal processing.

## Sinusoids
Prefer to use the complex exponential form instead of real, as it's a more natural fit for fourier analysis and synthesis.

```
z(t) = A*exp(j*(2π*f*t+ϕ))

z(t) = A*cos(2π*f*t+ϕ)+j*A*sin(2π*f*t+ϕ)
```

But we're going to do it in Python...

```python
import numpy as np

# Here we use the name "complex_sinusoid" instead of just "z".
def complex_sinusoid(A, f, t, phi): return A * np.exp(1j*(2*np.pi*f*t+phi))
```

Now we create a new function just for our sinusoid by defining everything except t.  This is called partial function application.

```python
def my_sinusoid(t): return complex_sinusoid(A=5, f=5, t=t, phi=0)
```

We can get the signal at a bunch of times thanks to numpy arrays.

```python
times = np.linspace(0, 10, num=10)  # 10 evenly spaced values between 0 and 10
my_signal = my_sinusoid(times)
```

And plot it out with matplotlib.

```python
import matplotlib.pyplot as plt

X = [x.real for x in my_signal]
Y = [x.imag for x in my_signal]
plt.scatter(X,Y, color='red')
plt.show()
```

[Complex Exponential Signals](https://www.cs.ccu.edu.tw/~wtchu/courses/2012s_DSP/Lectures/Lecture%203%20Complex%20Exponential%20Signals.pdf)

## Roots of Unity
![Roots of Unity Animation](https://mathworld.wolfram.com/images/gifs/rootsu.gif)

[Wolfram Mathworld](https://mathworld.wolfram.com/RootofUnity.html)

## Sample Signals
* [SigIDWiki sample signals](https://www.sigidwiki.com/)
