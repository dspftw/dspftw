# This will build a QPSK with and without Noise and save the file out

# Pick output file type for file <64|32f|16t|16o|8o|8t|8u>
output_file_name = argv(){1}
fT = argv(){2}
endianness = argv(){3}

printf("Output file: %s, fT: %s, endianness: %s\n", output_file_name, fT, endianness);

#data size
ds = 1000

b = randi(4, 1, ds);
filt = rrcfiltgen(31, 1, 10, 0.30);
const = [exp(j*2*pi*[1 3 7 5]/8)]
pt = kron(const(b), [1, zeros(1,9)]);

#Generates the signal without noise
sig = fconv(pt, filt, 'same');

# Adds noise to the signal
#sigN = sig+0.15*(randn(size(sig))+randn(size(sig)));

# Saves the signal as a little endian file and pick file type

if(endianness == "little")
  printf("Running savesig\n");
  savesig(output_file_name, sig, fT, 1);
else
  printf("Running savesigBigE\n");
  savesigBigE(output_file_name, sig, fT, 1);
endif
