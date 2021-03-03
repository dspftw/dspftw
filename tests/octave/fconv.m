function outArr = fconv(a, b, shp = 'full')

# Usage: outA-rr = fconv(a, b, shape)
# a-inputvector
# b-inputvector
# shape -'full' or'same'
#
# This function will return the convolution of the
# two input arrays but will be calculated using the
# FFT.

  aRowFlg = 0;
  if(isrow(a) == 1)
   a = a.';
   aRowFlg = 1;
  end
  
  bRowFlg = 0;
  if(isrow(b) == 1)
    b = b.';
    bRowFlg = 1;
  end
  
  fftLen = 2^ceil(log2(length(a) + length(b) - 1));

  outArr = ifft(fft(a, fftLen).*fft(b, fftLen))(1:length(a)+length(b)-1, :);

  if ((isreal(a) == 1) && (isreal(b) == 1))
    outArr = real(outArr);
  endif

  if(shp == 'full')
    if((aRowFlg == 1)&&(bRowFlg == 1))
      outArr = outArr.';
    end
    return;
  else
     minLen = min(length(a), length(b));
    maxLen = max(length(a), length(b));
    if(mod(minLen, 2) == 0)
      strt = minLen/2 + 1;
      stop = strt + maxLen - 1;
    else
      strt = (minLen + 1)/2;
      stop = strt + maxLen -1;
    endif
    
    outArr = outArr(strt:stop, :);
  end
  
  if((aRowFlg == 1)&&(bRowFlg == 1))
    outArr = outArr.';
  end
end