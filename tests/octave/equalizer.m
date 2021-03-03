function [oS, oE, oT] = equalizer(s, ks, c, spb, nt, m, a, it)
  
  #USAGE: [oSig, oErr, oTaps] = equalizer(sig, knownSyms, constl, sampsPerBaud,...
  #                                          numTaps, mu, alpha, initTaps)
  #
  # numTaps must be an odd integer
  # mu should be in the range 0.0001 to 0.2
  # alpha should be in the range 0.0 to 0.1*mu
  
  nt = nt+mod(nt+1, 2);
  nth = (nt-1)/2;
  sp = [zeros(1, nth), s, zeros(1, nth)];
  
  nStps = floor(length(s)/spb);
  
  oS = zeros(1,nStps);
  oE = zeros(1,nStps);
  
  nit = length(it);
  nith = (nit-mod(nit,2))/2;
  nks = length(ks);
  oT = [zeros(1, nth-nith), it, zeros(1, nt-(nth-nith)-nit)];
  
  for k = 1:nStps
    x = sp((k-1)*spb+[1:nt]);
    oS(k) = x*oT';
    
    if(k <= nks)
      oE(k) = ks(k)-oS(k);
    else
      [~, mi] = min(abs(oS(k) - c(:)));
      oE(k) = c(mi)-oS(k);
    end
  
    oT = (1-a)*oT + m*x*conj(oE(k))/sqrt(x*x');  
  end  
end
