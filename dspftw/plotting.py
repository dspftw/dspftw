# vim: expandtab tabstop=4 shiftwidth=4

import matplotlib.pyplot as plt

def plot_signal(signal, times):
    rows = 2
    columns = 2
    figure, subplots = plt.subplots(rows, columns)
    real_subplot = subplots[0][0]
    constellation_subplot = subplots[0][1]
    imaginary_subplot = subplots[1][0]
    ortho_subplot = subplots[1][1]

    real_subplot.plot(times, [s.real for s in signal])
    real_subplot.set_xlabel('time')
    real_subplot.set_ylabel('real')

    imaginary_subplot.plot(times, [s.imag for s in signal])
    imaginary_subplot.set_xlabel('time')
    imaginary_subplot.set_ylabel('imaginary')

    constellation_subplot.scatter(
        [s.real for s in signal],
        [s.imag for s in signal],
        color='red')
    constellation_subplot.set_xlabel('real')
    constellation_subplot.set_ylabel('imaginary')

    return figure
