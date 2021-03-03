function outArr = medfilt(inArr, num)
  
# Usage: outputArray = medfilt( inputArray, numVals )
#
# This function will return the output array the same size
# as the input array with the median values calculated
# for the running window of length num long.

  if(nargin ~= 2)
    print_usage;
  endif
  
  strt = floor(num/2);
  stop = num-strt;
  
  idx = convmtx([ones(1, strt), [1:length(inArr)], ones(1, stop)*length(inArr)], num)(:,
num:num+length(inArr)-1) ;

  outArr = median(inArr(idx));
endfunction