function outArr = fsigcorr(a, b, opt=1)
  
# Usage: outArr = fsigcon(a, b, opt)
# a - input vector
# b - input vector
# opt - if 1 then normalize, otherwise leave raw. Default is 1
#
# This functiom will return the cross correlation of the
# two input arrays. This is the same as xcorr but does it
# directly versus using an FFT. This function will only
# compute the fuII cross correlation. If you just want the
# valid portion then you must drop the beginning and ending
# portions.

  if length(a(:).') > length(b(:).')
    arrL = a(:).';
    arrS = b(:).';
  else
    arrL = b(:).';
    arrS = a(:).';
  endif
  
  lenL = length(arrL);
  lenS = length(arrS);
  
  outArr = fconv(arrL, fliplr(conj(arrS)), "full");
  
  if opt == 1
    sPow = sqrt(arrS*arrS');
    lPow = sqrt(fconv(arrL.*conj(arrL), ones(1, lenS), "full"))*sPow;
    outArr = outArr./lPow;
  endif
endfunction