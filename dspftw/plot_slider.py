# vim: expandtab tabstop=4 shiftwidth=4

from .exceptions import DSPFTWException

import matplotlib.pyplot as plt
from ipywidgets import interact
import ipywidgets as widgets

def plot_slider(*args, **kwargs) -> plt.Figure:
    '''
    Plot the input, displaying one plot per column and giving a slider to change
    which column is being displayed.
    
    Parameters
    ----------
    args: real ndarray(s) and possibly a str
        The real data with multiple columns as well as possibly a formatting string
        The string is for plotting parameters such as "r*-" which means
        plot it with a red line, marking the points with stars and connecting
        the stars.
        This plot will handle only a single set of inputs such as:
        Y
        X,Y
        Y,"<format>"
        X,Y,"<format>"
        where X and Y have the same size
    kwargs: dict
        Parameters passed through to plt.Figure.plot()
    '''

    # Check to make sure the inputs have the same number of columns
    num_cols = []
    data_idx = []
    str_idx = []
    frmt_str = "-"
    for k in range(len(args)):
        arg = args[k]
        if type(arg) is not str:
            if len(arg.shape) != 2:
                raise DSPFTWException("Input array {} (argument {}) is not a 2D input array".format(k, arg))
            num_cols.append(arg.shape[1])
            data_idx.append(k)
        else:
            frmt_str = arg
            str_idx.append(k)
    
    # Check that all the number of columns are the same
    if len(set(num_cols)) > 1:
        raise DSPFTWException("Not all the input arrays have the same number of columns")
    
    # Figure out the number of input arrays
    num_inputs = len(data_idx)

    # Plot the columns using the ipywidget
    def plot_funct(col_num):
        fig = plt.gcf()
        if num_inputs == 1:
            x = np.arange(args[0].shape[0])
            y = args[0][:, col_num]
        else:
            x = args[0][:, col_num]
            y = args[1][:, col_num]
        if len(fig.get_axes()) == 0:
            ax, = plt.plot(x,y,frmt_str, **kwargs)
        else:
            ax = fig.gca()
            ln = ax.get_lines()
            ln[0].set_data(x, y)
            ax.relim()
            ax.autoscale_view(True, True, True)
        fig.canvas.draw()
        
    interact(plot_funct, col_num = widgets.IntSlider(value=0, min=0, max=num_cols[0]-1, step=1))
            


def plots(*args, **kwargs) -> plt.Figure:
    '''
    An alias of plot_slider().
    '''
    return plot_slider(*args, **kwargs)
