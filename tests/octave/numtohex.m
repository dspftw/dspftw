function o = numtohex(iA)
  
  #USAGE: outStr = numtohex(inArr)
  #
  # Convert the input array to byte hex strings.  The values
  # in the input array must all be between 0 and 255.
  
  o = "";
  for k = 1:rows(iA)
    t = "";
    for l = iA(k,:)
      t = [t, sprintf(" %02X", l)];
    end
    o = strvcat(o, t);
  end
end
  