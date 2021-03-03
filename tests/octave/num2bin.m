function o = num2bin(iA, n)
  
  #USAGE: outArr = num2bin(inArr, num)
  #
  # Convert the input array to bits.
  
  o = zeros(rows(iA), columns(iA)*n);
  for l = 1:n
    o(:, l:n:end) = floor(mod(iA, 2^(n-l+1))/(2^(n-l)));
  end
end
