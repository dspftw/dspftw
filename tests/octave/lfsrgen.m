function o = lfsrgen(iF, taps, n)
  
  #USAGE: outBits = lfsrgen(initFill, polyTaps, numOutBits)
  
  # taps into bits.
  pt = zeros(1,max(taps)+1);
  pt(taps+1) = 1;
  pt = pt(1:end-1);
  nt = length(pt);
  
  
  iF = [iF, zeros(1, nt-length(iF))];
  
  o = [iF, zeros(1, n-length(iF))];
  
  for k = nt+1:n
    o(k) = mod(o(k-nt:k-1)*pt', 2);
  end
end
  