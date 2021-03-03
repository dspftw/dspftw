function [vals, indx] = findpeaks2(list, minDist=1, minHeight=1, numPeaks=inf)
  
# Usage:[peaks, peakIndx] = findpeaks2(inputArray, minDist, minHeight, numPeaks)
#
# This function will return a list of peaks and corresponding peak indexes
# in inputArray. The peaks are at least minDist apart and have a height
# of at least minHeight. The peaks/peakIndx arrays are returned in
# decreasing order of peak height (i.e. the highest peak first). This
# function will return up to numPeaks.

  if(nargin < 2)
    print_usage;
  endif
  
  indx1 = find(list > minHeight)(:).';
  indx1 = indx1+minDist;
  
  list1 = [zeros(1, minDist), list(:).', zeros(1, minDist)];
  
  vals = [];
  indx = [];
  
  cntPks = 0;
  
  zs = zeros(1, 2*minDist + 1);
  
  do
    [currMax, currMaxIndx] = max(list1(indx1));
    currMaxIndx = indx1(currMaxIndx);
      if(currMaxIndx <= minDist)
      return;
    endif
    
    # If the minimum is the same as the maximum over the given search area
    # then return because (hopefutly) everything has just been zeroed out
    # at this point.
    currMin = min(list1(currMaxIndx - minDist:currMaxIndx + minDist));
      if currMin == currMax
      return;
    endif
    
    vals(cntPks+1) = currMax;
    indx(cntPks+1) = currMaxIndx - minDist;
    if(length(vals) >= numPeaks)
      return;
    endif
    
    cntPks += 1;
    
    list1(currMaxIndx - minDist:currMaxIndx + minDist) = zs;
  until(currMaxIndx == 0)
endfunction