import numpy as np
from numpy import array as nparray
from numpy import exp, pi
from scipy.signal import fftconvolve
from root_raised_cosine_filter_generator import root_raised_cosine_filter_generator

def generate_write_signal(ofile: str,
                          sample_type: str="32f",
                          endian: str="b",
                          data_type: str="c",
                          con_size: int=4,
                          num_syms: int=10000,
                          samples_per_sym: int=2,
                          beta: float=0.25) -> nparray:
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

    savesig(ofile,signal,sample_type,endian,data_type,'w',0,1)

def savesig(ofile, sig, sample_type, endian='b', data_type='r', mode='w', trunc=0, verbose=0):
    """
    Function to use numpy package to write PCM data.
    Writable data types are 8t, 16t, 32f
    Endian options: l=little, b=big
    Data type options: r=real, c=complex
    Mode: w=write, a=append
    Trunc: 0=True Zero, 1=True One (symmetric)
    Returns number of samples written if successful
    Returns -1 is unsuccessful
    """
    # Set the data type to numpy recognizable strings
    if sample_type == '8t':
        dtype = 'u1'
        mult = 2**7
    elif sample_type == '16t':
        dtype = 'u2'
        mult = 2**15
    elif sample_type == '32t':
        dtype = 'u4'
        mult = 2**31
    elif sample_type == '64t':
        dtype = 'u8'
        mult = 2**63
    elif sample_type == '32f':
        dtype = 'f4'
        mult = 1
    elif sample_type == '64f':
        dtype = 'f8'
        mult = 1
    else:
        print("Function savesig: Unrecognized data type: {}".format(sample_type))
        return -1

    # Set endian-ness in numpy recognizable way
    if endian == 'b':
        dtype = ">" + dtype
    elif endian == 'l':
        dtype = "<" + dtype
    else:
        print("Function savesig: Unrecognized endian type: {}".format(endian))
        return -1
    # Set multiplicative factor to double the number of samples for complex data
    if data_type == 'r':
        m_fact = 1
    elif data_type == 'c':
        m_fact = 2
    else:
        print("Function savesig: Unrecognized data type: {}".format(data_type))
        return -1
    # Check mode
    if mode not in ("a","w"):
        print("Function savesig: Unrecognized mode: {}".format(mode))
        return -1

    # Touch output file
    if len(sig) == 0:
        fid = open(ofile, mode)
        fid.close()
        return 0

    # Two's complement sample types
    if sample_type in ("8t","16t","32t","64t"):
        # Complex
        if data_type == 'c':
            # Turn list of complex numbers to list of floats
            sigflat = np.array([mult*sig.real,mult*sig.imag]).flatten("F")
        else:
            sigflat = np.copy(mult*sig)

        # Count how many will be clipped below
        clip = len(np.argwhere(sigflat<-1*mult).flatten())
        # Clipping values that are too low
        sigflat = np.where(sigflat < -1*mult, -1*mult, sigflat)

        # Count how many will be clipped above
        clip += len(np.argwhere(sigflat>=mult).flatten())
        # Clipping values that are too high
        sigflat = np.where(sigflat >= mult, mult-1, sigflat)

        # Map floats to ints according to truncating method
        if trunc == 0:
            # Round to nearest integer
            sigint = np.array(np.round(sigflat),"int")
        elif trunc == 1:
            sigint = np.array(sigflat,"int")

        # Modulo 2^8 or 2^16 to create two's complement
        sigint = np.remainder(sigint,2*mult)
        # Cast as unsigned integer
        sigint = np.array(sigint,dtype)
        #print(sigint.dtype)

        # Open file handle
        mode = mode + "b"
        fid = open(ofile, mode)
        # Write samples
        sigint.tofile(fid,"",dtype)
        # Close file handle
        fid.close()
        numwritten = len(sigint)//m_fact

    if sample_type in ("32f","64f"):
        # Open file handle
        fid = open(ofile, mode)
        if data_type == 'c':
            # Cast sample as the desired data type
            sig2 = np.array([sig.real,sig.imag],dtype).flatten("F")
        else:
            sig2 = np.array(sig,dtype)
        # Write samples
        sig2.tofile(fid,"",dtype)
        fid.close()
        numwritten = len(sig2)//m_fact
        clip = 0

    # Verbose output
    if verbose >= 1:
        if data_type == 'c':
            print(numwritten,"complex samples written,",clip,"floats were clipped")
        else:
            print(numwritten,"real samples written,",clip,"floats were clipped")

    return numwritten
