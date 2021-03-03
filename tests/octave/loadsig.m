function sig = loadsig(fileName, numSamps = Inf, fileType="32f", endian="l", cmplxFlg=1, strtSamp = 0)
# Usage: sig = loadsig(fileName, numSamps, fileType, endianness, complexFlag, strtSamp)
#
# This function will load the signal file "fileName", of file type "fileType"
# and endianness "1" or "b" or "g" (little-endian, big-endian, guess). Each
# of the input arguments fileName, fileType and endianness need to be strings.
# If complexFlag is 0 then the file will be loaded as real and if complexFlag
# is l- then the file will be loaded as complex. Valid file types are "1t", "8u",
# "8o", "8t", "16o", "l-6t", "32f", "64f". numSamps is the number of samples
# that you would like to load. The default for numSamps is to load the entire
# file. The default for strtSamp is 0. If you want to specify strtsamp, then
# you must specify numsamps but you may specify numSamps without specifying
# sutSamp.
#
# complexFlag needs to be a 1 for the data to load as complex and a 0 for the
# data to load as real. If any other values are used then an error will occur.
#
# This function will scale the input so that -1 (= minVal <= maxVal <= 1 and will
# convert the values to floats.

if((nargin < 1) || (nargin > 6) || (cmplxFlg < 0) || (cmplxFlg > 1))
  print_usage;
endif

sig = [];

guessFlg = 0;
switch endian
  case "l"
    endianness = "ieee-le";
  case "b"
    endianness = "ieee-be";
  case "g"
    guessFlg = 1;
    endiannessB = "ieee-be";
    endiannessL = "ieee-le";
otherwise
    print_usage;
    return;
endswitch

#endianness

offsetVal = 0;
mulawFlg = 0;
numBytes = 0;
bitFlg = 0;
smpScale = 1;
switch fileType
  case "64f"
    prec = "float64";
    numBytes = 8;
  case "32f"
    prec = "float32";
    numBytes = 4;
  case "16t"
    prec = "int16";
    numBytes = 2;
    smpScale = 1/32768;
  case "16o"
    prec = "uint16";
    offtetVal = 32768;
    numBytes = 2;
    smpScale = 1/32768;
  case "8o"
    prec = "uint8";
    offsetVal = 128;
    numBytes = 1;
    smpScale = 1/128;
  case "8t"
    prec = "int8";
    numBytes = 1;
    smpScale = 1/128;
  case "8u"
    prec = "uint8";
    mulawFlg = 1;
    numBytes = 1;
  case "1t"
    prec = "uint8";
    numBytes = 1;
    bitFg = 1;
    endianness = "ieee-le";
  otherwise
    print_usage;
  return;
endswitch


if(guessFlg == 0 || bitFlg == 1)
  fid = fopen(fileName, "r", endianness);
  if(fid < 0)
    printf("could not open file %s\n", fileName);
    return;
  endif
  if(bitFlg ~= 1)
    #strtSamp
    fseek(fid, (1 + cmplxFlg)*numBytes*strtSamp, "bof");
    #ftell(fid)
    sig = fread(fid, (1 + cmplxFlg)*numSamps, prec).';
    fclose(fid);
  else
    fseek(fid, floor((1 + cmplxFlg)*numBytes*strtSamp/8), "bof");
    sig = fread(fid,floor((1 + cmplxFlg)*numSamps/8), prec).';
    fclose(fid);
    sig = num2base(sig, 2,8)*2-1;
  endif
else
  fid1 = fopen(fileName, "r", endiannessB);
  if(fid1 < 0)
    printf("Could not open file %s\n", fileName);
    return;
  endif
  fid2 = fopen(fileName, "r", endiannessL);
  fseek(fid1, (1 + cmplxFlg)*numBytes*strtSamp, "bof");
  fseek(fid2, (1 + cmplxFlg)*numBytes*strtSamp, "bof");
  sig1 = fread(fid1, 100, prec);
  sig2 = fread(fid2, 100, prec);
  fclose(fid1);
  fclose(fid2);
  
  
  if(cmplxFlg == 0);
    siglSum = sum(abs(sig1));
    sig2Sum = sum(abs(sig2));
  else
    siglSum = sum(abs(sig1(1:2:end)))+ sum(abs(sig1(2:2:end)));
    sig2Sum = sum(abs(sig2(1:2:end)))+ sum(abs(sig2(2:2:end)));
    numSamps = 2*floor(numSamps/2);
  endif
  
  
  if(siglSum > sig2Sum)
    fid = fopen(fileName, "r", endiannessL);
    fseek(fid, (1 + cmplxFlg)*numBytes*strtSamp, "bof");
    sig = fread(fid, (1 + cmplxFlg)*numSamps, prec).';
    fclose(fid);
  else
    fid = fopen(fileName, "r", endiannessB);
    fseek(fid, (1 + cmplxFlg)*numBytes*strtSamp, "bof");
    sig = fread(fid, (1 +cmplxFlg)*numSamps, prec).';
    fclose(fid);
  endif
endif

if(offsetVal ~= 0)
  sig = sig - offsetVal;
endif

if(mulawFlg == 1);
  sig = mu2lin(sig, 0);
endif

if(cmplxFlg == 1)
  sig = sig(1:2:end) + i*sig(2:2:end);
endif

if(smpScale ~= 1)
  sig = sig*smpScale;
endif
endfunction