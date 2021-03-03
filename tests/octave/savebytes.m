function out = savebytes(fn, dat)
  
  # USAGE: bytesSaved = loadbytes(outFileName, data)
  #
  # save the data into bytes

  fid = fopen(fn, "w", "n");
  out = fwrite(fid, dat, "uint8");
end
