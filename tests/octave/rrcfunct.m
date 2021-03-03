function outVal = rrcfunct(t, Ts, b)
  
# Usage: outVal = rrcfunct(t, Ts, b)
#   t - the input time value
#   Ts - the input baud time value
#   b - the input roll-off value
#
# Output the value of the root raisded cosine funciton at the point t.

    # Set numerator and the derivative of the numerator wrt t
    n = sin(pi*t/Ts*(1-b)) + 4*b*t/Ts*cos(pi*t/Ts*(1+b));
    nd = pi*(1-b)*cos(pi*t*(1-b)/Ts)/Ts + 4*b*cos(pi*t*(1+b)/Ts)/Ts - 4*pi*t*b*(1+b)*sin(pi*t*(1+b)/Ts)/(Ts^2);
    
    # Set the denominator and the derivative of tne denominator wrt t
    d = pi*t/Ts*(1-16*b^2*t^2/(Ts^2));
    dd = pi*(Ts^2 - 48*t^2*b^2)/(Ts^3);
    
    # Set the return values using L'Hopital's rule when the denominator is 0
    # The reson for the condition below and not the condition d ~= 0 is that
    # I was having underflow issues. Setting it this way takes core of that.
    
    if(abs(d) > 10^(-12))
        outVal = n/d;
    else
        outVal = nd/dd;
    endif
    
endfunction