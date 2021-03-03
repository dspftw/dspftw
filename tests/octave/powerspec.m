function [pwrSpec, frqs] = powerspec(inSig, fftLen = 2^13, stepSize = fftLen/2, dspFlg = 1, sr = 1,
winType ='rectangle')


# Usage: pwrSpec = powerspec(inSig, fftLen, stpSize, dspFlg, sr, winType)
#
# inSig - the input signal
# fftLen - the length of the fft
# stpSize - the size of the step between fft calculations. l/2 of the fft
# length is optimal
# dspFlg - flag to set in order to display
# sr - the input sample rate
# winType - windowing type
# Valid options:
# 'rectangle'(default)
# 'hamming'
# 'hanning'
# 'blackman'
# 'bartlett'


   # Set indices for signal
   indices = [1:stepSize:length(inSig(:).')]+[0:fftLen-1]';
   # Set window
   switch winType
     case'rectangle'
        sigWin = 0;
      case'hamming'
        sigWin = window(@hamming, fftLen);
      case'hanning'
        sigWin = window(@hanning, fftLen);
      case'blackman'
       sigWin = window(@blackman, fftLen);
      case 'bartlett'
        sigWin = window(@bartlett, fftLen);
      otherwise
       sigWin = 0;
  endswitch

  paddedSig = [inSig(:).', zeros(1, fftLen)];

  # Create power spectrum
  if(sigWin == 0)
   if(columns(indices) == 1);
     pwrSpec = fftshift(abs(fft(paddedSig(indices))));
    else
     pwrSpec = mean(fftshift(abs(fft(paddedSig(indices))), 1).');
    endif
  else
    if(columns(indices) == 1)
     pwrSpec = fftshift(abs(fft(paddedSig(indices).*sigwin)));
    else
      pwrSpec = mean(fftshift(abs(fft(paddedSig(indices).*sigWin)), 1).');
   endif
  endif

  pwrSpec = 20*log10(pwrSpec);

  xVals = linspace(-sr/2, sr/2, fftLen+1)(1:end-1);
  frqs = xVals;

  if(dspFlg == 1)
   # yVals = 20*log10(pwrSpec);
   plot(xVals, pwrSpec);
   axis([xVals(1), xVals(end), min(pwrSpec), max(pwrSpec)+0.1*(max(pwrSpec)-min(pwrSpec))]);
  endif
endfunction