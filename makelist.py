#
# makelist.py
# ===========
#
# Syntax:
#
#   python3 makelist.py [input-file] [output-file]
#
# Parameters:
#
#   [input-file] is the path to the ISO-639-3.tab file to read and parse
#
#   [output-file] is the path to the JSON file to generate
#
# Operation
# ---------
#
# This script reads a ISO-639-3.tab tabulated data text file and writes
# a JSON file that contains a parsed representation of the mappings from
# language codes to language names.
#
# The input data file is available from SIL International, which is the
# official registrar for ISO-639-3.  See https://iso639-3.sil.org/ for
# further information and to obtain an up-to-date copy of the text file.
# This script is designed to work with the UTF-8 version of the main
# ISO-639-3.tab file.
#
# The output file contains a JSON object that has two fields, the first
# named "codes" and the second named "names".  The "codes" field stores
# another JSON object that maps language code strings to integer values.
# The language code strings are all either two characters or three
# characters, and each character is a lowercase US-ASCII letter a-z.
# The "names" field is a JSON array of string elements.  Each string
# element is a language name.  The integer values in the "codes" field
# are zero-based element indices into this "names" array.  This allows
# multiple language codes to map to the same language name string.
#
# This JSON object is then encoded in UTF-8 as a string of binary data.
# This binary data is run through gzip, and the compressed result is
# then run through a base-64 encoder so it can be embedded within a
# source file.
#

import base64
import gzip
import io
import sys
import unicodedata

# Check command argument count (should include the program name and the
# two arguments)
#
if len(sys.argv) != 3:
  print('Wrong number of program arguments!')
  sys.exit(1)

#
# Function used to check that language codes are in the proper format.
#
# Language codes must have exactly two or three characters, and each
# character must be a lowercase letter a-z
#
# Parameters:
#
#   sval : str | mixed - the string to check
#
# Return:
#
#   True if a valid language code, False otherwise
#
def check_code(sval):
  
  # Check that parameter is string
  if not isinstance(sval, str):
    return False
  
  # Check length of parameter and proceed
  if len(sval) == 2:
    # Two-character code, check that both are lowercase ASCII letters
    for cv in sval:
      c = ord(cv)
      if (c < ord('a')) or (c > ord('z')):
        return False
  
  elif len(sval) == 3:
    # Three-character code, check that all are lowercase ASCII letters
    for cv in sval:
      c = ord(cv)
      if (c < ord('a')) or (c > ord('z')):
        return False
    
  else:
    # Invalid length of code
    return False
  
  # If we got here, check passes
  return True

# Open the input file as a text file in UTF-8 encoding and parse it
#
codes = dict()
lnames = []
try:
  with open(sys.argv[1], mode='rt',
            encoding='utf-8', errors='strict') as fin:
    
    # We have the input file open -- read line by line
    line_num = 0
    code_idx = 0
    for line in fin:
    
      # Update line count
      line_num = line_num + 1
    
      # If on first line, skip the header line and continue to next line
      if line_num <= 1:
        continue
      
      # Not on first line, so next step is to filter blank lines that
      # are empty or contain only spaces, tabs, and line breaks
      if len(line.strip(' \t\n')) < 1:
        continue
      
      # We have an actual content line, so split it into fields using
      # the tab characters as a delimiter
      fv = line.split('\t')
      
      # We need at least 7 fields for the line to be valid
      if len(fv) < 7:
        print('Error on line', line_num, '\nNot enough fields!')
        sys.exit(1)
      
      # The first four fields hold the language codes (or they might be
      # blank)
      lc_1 = fv[0]
      lc_2 = fv[1]
      lc_3 = fv[2]
      lc_4 = fv[3]
      
      # Trim each of the first four fields of whitespace
      lc_1 = lc_1.strip(' \t\n')
      lc_2 = lc_2.strip(' \t\n')
      lc_3 = lc_3.strip(' \t\n')
      lc_4 = lc_4.strip(' \t\n')
      
      # Add non-blank codes to the lcode array
      lcode = []
      if len(lc_1) > 0:
        lcode.append(lc_1)
      if len(lc_2) > 0:
        lcode.append(lc_2)
      if len(lc_3) > 0:
        lcode.append(lc_3)
      if len(lc_4) > 0:
        lcode.append(lc_4)
      
      # There must be at least one non-blank code
      if len(lcode) < 1:
        print('Error on line', line_num, '\nMissing language codes!')
        sys.exit(1)
      
      # Remove duplicate codes from the lcode array
      if len(lcode) > 1:
        # Go from last code in array down to second code
        for i in range(len(lcode) - 1, 0, -1):
          # Remove if in earlier array elements
          if lcode[i] in lcode[0:i]:
            if i >= len(lcode) - 1:
              lcode = lcode[0:i]
            else:
              lcode = lcode[0:i] + lcode[i + 1:len(lcode)]
      
      # Check that each unique code is a valid language code and that it
      # is not already in the codes dictionary
      for nbc in lcode:
        if not check_code(nbc):
          print('Error on line', line_num,
                  '\nLanguage code is invalid!')
          sys.exit(1)
        if nbc in codes:
          print('Error on line', line_num,
                  '\nRedefinition of language code!')
      
      # Add each unique code to the codes dictionary, mapping to the
      # current code index
      for nbc in lcode:
        codes[nbc] = code_idx
      
      # Update the current code index
      code_idx = code_idx + 1
      
      # Get the language name and trim it
      ln = fv[6]
      ln = ln.strip(' \t\n')
      
      # Normalize the language name to NFC
      ln = unicodedata.normalize('NFC', ln)
      
      # Language name must not be empty
      if len(ln) < 1:
        print('Error on line', line_num, '\nEmpty language name!')
        sys.exit(1)
      
      # Add the language name to the list
      lnames.append(ln)

except FileNotFoundError:
  # Couldn't find the input file
  print('Can\'t find the input file!')
  sys.exit(1)

except ValueError:
  # Some kind of text encoding problem
  print('Invalid UTF-8 in input!')
  print('(Please use the UTF-8 version of the data file.)')
  sys.exit(1)

except Exception:
  # Some other kind of problem
  print('Unknown problem while reading input file!')
  sys.exit(1)

# We now have a mapping from language codes to indices in the codes
# dictionary, and an array of language names; build a JSON file from
# this data
#
jsfile = io.StringIO()
jsfile.write('{\n')

# Build the "codes" field
#
jsfile.write('  "codes": {\n')
keys = list(codes)
keys.sort()
first_key = True
for c in keys:
  if first_key:
    first_key = False
  else:
    jsfile.write(',\n')
  jsfile.write('    "' + c + '": ' + str(codes[c]))
jsfile.write('\n  },\n')

# Build the "names" field
#
jsfile.write('  "names": [\n')
first_name = True
for n in lnames:
  if first_name:
    first_name = False
  else:
    jsfile.write(',\n')
  jsfile.write('    "' + n + '"')
jsfile.write('\n  }\n')

# Finish the JSON file and turn it into a binary string encoded in UTF-8
#
jsfile.write('}\n')
jsfile = jsfile.getvalue().encode(encoding='utf-8')

# Compress the binary string with gzip
#
jsfile = gzip.compress(jsfile)

# Encode the compressed file in base64
#
jsfile = base64.b64encode(jsfile)

# Open the output file as a text file in ASCII encoding and store the
# base-64 encoded result therein with lines limited to 72 characters
#
try:
  with open(sys.argv[2], mode='wt', encoding='ascii') as fout:
    
    # Start at offset zero in the base-64 data and store total length of
    # base-64
    x = 0
    jslen = len(jsfile)
    
    # Keep outputting full lines of 72 characters while data remains
    while jslen - x > 72:
      # Get the base-64 content of this line
      ldata = jsfile[x:x + 72]
      ldata = ldata.decode(encoding='ascii')
      
      # Add a line break and output the line
      ldata = ldata + '\n'
      fout.write(ldata)
      
      # Advance file offset
      x = x + 72
    
    # Remaining data should be at least one character and at most 72,
    # so output the last line
    ldata = jsfile[x:jslen]
    ldata = ldata.decode(encoding='ascii')
    ldata = ldata + '\n'
    fout.write(ldata)

except Exception:
  # Some kind of problem
  print('Unknown problem while writing output file!')
  sys.exit(1)
