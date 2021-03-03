function out = loadbytes(iFile)
  
  # USAGE: [arr] = loadbytes(inFileName)
  #
  # load the data into bytes

  fid = fopen(iFile, "r", "n");
  out = fread(fid).';
end
