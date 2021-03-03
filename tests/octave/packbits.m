function [out] = packbits(iArr)
  
  # USAGE: out = packbits(inArray)
  #length(iArr)
  iArr1 = [iArr, zeros(rows(iArr), mod(8-columns(iArr), 8))];

  out = iArr1(:, 1:8:end)*128 + iArr1(:, 2:8:end)*64 + iArr1(:, 3:8:end)*32 + iArr1(:, 4:8:end)*16 + iArr1(:, 5:8:end)*8 + iArr1(:, 6:8:end)*4 + iArr1(:, 7:8:end)*2 + iArr1(:, 8:8:end);  
end
  