# vim: expandtab tabstop=4 shiftwidth=4

from numpy import exp, pi

def complex_sinusoid(A, f, t, phi):
    return A * exp(1j*(2*pi*f*t+phi))
