function [outFilt, t] = rrcfiltgen(bw, br, sr, ro)
  
# Usage: [outFilter, tVals] = rrcfiltgen(baud_width, baud_rate, sample_rate, roll_off)
# 
# This function will return the taps of a root-raised-cosine filter (RRC) given
# the following input parameters:
#   baud_width - the numer of bauds wide that the filter should be (an odd number)
#                will give the filter starting and stopping at baud boundaries)
#   baud_rate - the baud rate (in Hz)
#   sample_rate - the sample rate (in Hz)
#   roll_off - the roll off factor should be betwen 0 and q, inlusive
#
# You can also have returned the time values of where the filter was evaluated.

    if(nargin ~= 4)
        print_usage;
    endif
    
    # Set the value Ts as the baud time
    Ts = 1/br;
    
    # Create the time values
    t = [-ceil((bw/2)*Ts*sr):ceil((bw/2)*Ts*sr)]/sr;
    
    # Create output filter
    outFilt = zeros(size(t));
    
    # Loop through the values of t, assigning the correct values of the funciton
    if(ro == 0)
        tLen = length(t);
        indcs = [1:floor(tLen/2), ceil(tLen/2) + 1:tLen];
        outFilt(indcs) = sin(pi*t(indcs)/Ts) ./ (pi*t(indcs)/Ts);
        outFilt((tLen + 1)/2) = 1;
    else
        for k = 1:length(t)
            outFilt(k) = rrcfunct(t(k),Ts,ro);
        endfor
    endif
endfunction