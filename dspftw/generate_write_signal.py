from numpy import exp, pi
from scipy.signal import fftconvolve

import numpy as np

from .root_raised_cosine_filter_generator import root_raised_cosine_filter_generator
from .save_signal import savesig

def generate_write_signal(ofile: str,
                          sample_type: str="32f",
                          endian: str="b",
                          data_type: str="c",
                          con_size: int=4,
                          num_syms: int=10000,
                          samples_per_sym: int=2,
                          beta: float=0.25) -> np.array:
    '''
    Generate a QAM signal and write to file

    Parameters
    ----------
    ofile: str
        Output file name. (Default: sig<con_name>.<data_type>.<samples_per_sym>.<sample_type>)
    sample_type: str
        Sample type. Options 8t, 16t, 32t, 64t, 32f, 64f (Default: 32f)
    endian: str
        Endianness. Options are b and l (Default: b)
    data_type: str
        Data Type.  Options are r (real) and c (complex) (Default: c)
    con_size: int
        Constellation size.  Options are 4 (QPSK) and 8 (8PSK) (Default: 4)
    num_syms: int
        Number of symbols generated. (Default: 10000)
    samples_per_sym: int
        Number of samples per symbol. (Default: 2)
    beta: float
        Roll off factor. (Default: 0.25)
    Remarks:
        To prevent aliasing for complex signals we must have (1+beta) < samples_per_sym
        To prevent aliasing for real signals we must have 2*(1+beta) < samples_per_sym
        Complex signals will be centered at 0
        Real signals will be centered at samples_per_sym/4
    '''
    if con_size == 4:
        con_name = "QPSK"
        con = exp(2j*pi*np.arange(1,8,2)/8.0)
        max_mag = 1.0
    elif con_size == 8:
        con_name = "8PSK"
        con = exp(2j*pi*np.arange(1,16,2)/16.0)
        max_mag = 1.0

    if ofile == "":
        field = "cplx"
        if data_type == "r":
            field = "real"
        stype = sample_type
        if endian == "l" and sample_type != "8t":
            stype = "{0}l".format(sample_type)
        ofile = "sig{0}.{1}.{2}.{3}".format(con_name,field,samples_per_sym,stype)

    print("ofile:",ofile)

    # Hard coded parameters
    # Baud width of root raised cosine filter
    baud_width = 21

    # constellation size
    con_size = len(con)

    # Generate random symbols
    symidx = np.random.randint(0,con_size,num_syms)

    # Convert symbol indices to complex number symbols
    symbol = con[symidx]

    # Create pulse train by inserting sps-1 zeros between each symbol
    pulse_train = np.kron(symbol,np.append([1],np.zeros(samples_per_sym-1)))

    # Create pulse shaping filter
    pulse_shape = root_raised_cosine_filter_generator(baud_width,1,samples_per_sym,beta)

    # Convolve to create QAM signal
    signal = fftconvolve(pulse_train,pulse_shape,mode="same")

    # Scale if using twos-complement
    if sample_type in ("8t","16t","32t","64t"):
        signal /= (2.0*max_mag)

    # Convert to real if necessary
    if data_type == "r":
        signal = signal * exp(2j*samples_per_sym/4*np.arange(0,len(signal)))
        signal = signal.real

    savesig(ofile, signal, sample_type, data_type, endian)
