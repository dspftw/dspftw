function [o, fm] = gmskmod(d, c, ps, spb)
  
  #USAGE: outSig = gmskmod(data, constl, pulseShape, sampsPerBaud)
  #
  # Create a GMSK signal from the given parameters.
  #
  # -Data must be values that are lookups into the constellation.
  # -SampsPerBaud must be an integer.
  
  pt = kron(c(d), [1, zeros(1, spb-1)]);
  fm = fconv(pt, ps(:).')(spb:end);
  
  #plot(fm)
  o = exp(j*cumsum(fm));
end  