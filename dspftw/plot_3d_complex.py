# vim: expandtab tabstop=4 shiftwidth=4

from numpy import ndarray
from .exceptions import DSPFTWException

import matplotlib.pyplot as plt

def plot_3d_complex(*args, **kwargs):
    '''
    Plots complex data in a 3D space (time vs complex plane).
    
    Parameters
    ----------
    args: complex ndarray(s) and possibly str(s)
        The complex data along with possibly time as well as formatting string(s)
        You may pair a real array with a complex one if you would like the real
        values to be displayed on the "time" axis.  The strings are for plotting
        parameters such as "r*-" which means plot it with a red line, marking the
        points with stars and connecting the stars.
    kwargs: dict
        Parameters passed through to plt.axes.plot3D()
    '''
    # Check the input parameters in args to make sure that they're valid
    num_strs = 0
    num_reals = 0
    num_cplxs = 0
    for arg in args:
        if type(arg) is str:
            num_strs += 1
        elif np.isrealobj(arg):
            num_reals += 1
        elif np.iscomplexobj(arg):
            num_complex += 1
        else:
            raise DSPFTWException("Input number {} (argument {}) is not a valid input argument".format(args.index(arg), arg))
    if num_reals > num_cplxs:
        raise DSPFTWException("Too many real arguments were given.  You must have 1 complex argument for each real argument")
    if num_strs > num_cplxs:
        raise DSPFTWException("Too many formatting arguments were given.  You must have 1 complex argument for each formatting argument")

    # Check the order of the arguments to make sure they're valid
    for k in range(len(args)):
        if type(args[k]) is str:
            if k == 0:
                raise DSPFTWException("A complex argument must precede the formatting argument {}".format(args[k]))
            elif not np.iscomplexobj(args[k-1]):
                raise DSPFTWException("A complex argument must precede the formatting argument {}".format(args[k]))
        if np.isrealobj(args[k]):
            if k == len(args)-1:
                raise DSPFTWException("A complex argument must follow the real argument {}".format(args[k]))
            elif not np.iscomplexobj(args[k+1]):
                raise DSPFTWException("A complex argument must follow the real argument {}".format(args[k+1]))

    # Work through the input argument list, separating it into chunks that go together
    plotargs = []
    t_args = []
    for k in range(len(args)):
        if np.isrealobj(args[k]):
            t_args.append(args[k])
        if np.iscomplexobj(args[k]):
            t_args.append(args[k].real)
            t_args.append(args[k].imag)
            if k+1 < len(args) and type(args[k+1]) is str:
                t_args.append(args[k+1])
            else:
                t_args.append("-")
            plotargs.append(t_args)
            t_args = []
        


    # x = time
    # y = real part
    # z = imag part
    ax = plt.axes(projection='3d')
    


def plot3c(*args, **kwargs) -> plt.Figure:
    '''
    An alias of plot_complex().
    '''
    return plot_3d_complex(*args, **kwargs)
