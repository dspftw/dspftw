# vim: expandtab tabstop=4 shiftwidth=4

import matplotlib.pyplot as plt

def plot_signal(signal, times):
    figure = plt.figure()
    gridspec = figure.add_gridspec(2, 2)
    real_subplot = figure.add_subplot(gridspec[0, 0])
    imaginary_subplot = figure.add_subplot(gridspec[1, 0])
    constellation_subplot = figure.add_subplot(gridspec[0, 1])
    ortho_subplot = figure.add_subplot(gridspec[1, 1], projection='3d')

    real_data = [s.real for s in signal]
    imag_data = [s.imag for s in signal]

    real_subplot.plot(times, real_data)
    real_subplot.set_xlabel('time')
    real_subplot.set_ylabel('real')

    imaginary_subplot.plot(times, imag_data)
    imaginary_subplot.set_xlabel('time')
    imaginary_subplot.set_ylabel('imaginary')

    constellation_subplot.scatter(real_data, imag_data, color='red')
    constellation_subplot.set_xlabel('real')
    constellation_subplot.set_ylabel('imaginary')

    ortho_subplot.plot(times, real_data, imag_data)
    ortho_subplot.set_xlabel('time')
    ortho_subplot.set_ylabel('real')
    ortho_subplot.set_zlabel('imaginary')

    return figure
