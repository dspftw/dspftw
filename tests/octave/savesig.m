function numSamps = savesig(fileName, inSig, fileType = "16t", cmplxFlg = 0)
# Usage: numSampsSaved = savesig(fileName, sig, fileTipe <64|32f|16t|16o|8o|8t|8u>, complexFlag
# <0|1>)
#
# This function will save sig in filename with filetype. Data must
# be a l x n or n x 1 real or complex array. The supported file types
# are 64f, 32f, 16t, 16o, 8o, 8t and 8u. If the signal is complex
# then set complexFlag to 1.
#
# The return is the total number of samples saved. If sig is complex then this
# will be twice the number of samples.

  if(nargin > 4 || nargin < 2 )
    print_usage;
  endif

  sig = inSig/max(abs(inSig));
  
  if(iscomplex(sig) && cmplxFlg == 0)
    printf("Input sig is complex (not real) and will be written as such.\n");
    cmplxFlg = 1;
  endif
  
  if(cmplxFlg == 0)
    data = sig(:).';
  elseif(cmplxFlg == 1)
    data = reshape([real(sig(:).'); imag(sig(:).')], 1, []);
  else
    print_usage;
  endif
  
  fid = fopen(fileName, "w", "native");
  
  switch fileType
    case "64f"
      numSamps = fwrite(fid, data, "float64");
    case "32f"
      numSamps = fwrite(fid, data, "float32");
    case "16t"
      numSamps = fwrite(fid, round(data*32767), "int16");
    case "16o"
      numSamps = fwrite(fid, round((data + 1)*32767.5), "uint16");
    case "8o"
      numSamps = fwrite(fid, round((data + 1)*127.5), "uint8");
    case "8t"
      numSamps = fwrite(fid, round(data + 127), "int8");
    case "8u"
      numSamps = fwrite(fid, lin2mu(data, 0), "uint8");
    otherwise
      print_usage;
      fclose(fid);
      return;
   endswitch

   fclose(fid);
  endfunction