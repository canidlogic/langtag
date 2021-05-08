#
# subtag.py
# =========
#
# Syntax:
#
#   python3 subtag.py [input-file]
#
# Parameters:
#
#   [input-file] is the path to the subtag registry file
#
# Operation
# ---------
#
# This script reads and parses the Language Subtag Registry from IANA.
# A current copy of the registry can be downloaded from IANA at the
# following address:
#
#   https://www.iana.org/assignments/
#   language-subtag-registry/language-subtag-registry
#
# The format of this registry file is defined in RFC 5646 "Tags for
# Identifying Languages"
#

import sys

#
# Exceptions
# ----------
#

class LogicError(Exception): pass

class BadContinueLine(Exception): pass
class MultiFieldError(Exception): pass
class NoColonError(Exception): pass

#
# Function definitions
# --------------------
#

# @@TODO:
def handle_rec(rec):
  pass

# Function that processes a raw record.
#
# A raw record requires an array of record lines.  Trailing whitespace
# and line breaks should have been stripped from these lines already.
# Furthermore, continuation lines should be assembled so that the lines
# here are logical record lines rather than the physical record lines
# that occur in the file.
#
# Parameters:
#
#   lines : list of strings - the logical lines of the record
#
def raw_record(lines):
  
  # Check parameter
  if not isinstance(lines, list):
    raise LogicError()
  for e in lines:
    if not isinstance(e, str):
      raise LogicError()

  # Convert each logical line into a mapping of field names in lowercase
  # to field values 
  rec = dict()
  for e in lines:
    
    # Find the location of the first : character, which must be present
    ci = e.find(':')
    if ci < 0:
      raise NoColonError()
    
    # Split into a field name and a field value around the colon
    fname = ''
    fval = ''
    if ci > 0:
      fname = e[0:ci]
    if ci < len(e) - 1:
      fval = e[ci + 1:]
    
    # Trim field name and field value of leading and trailing space
    fname = fname.strip(' \t\n')
    fval = fval.strip(' \t\n')
    
    # Convert field name to lowercase
    fname = fname.lower()
    
    # Different handling based on whether the field name is a special
    # field that can occur multiple times
    if (fname == 'description') or (fname == 'comments') or \
        (fname == 'prefix'):
      # This field can occur multiple times, so check if already present
      # and handle differently
      if fname in rec:
        # We already have a previous instance of this field, so just add
        # the new value as another array element
        rec[fname].append(fval)
        
      else:
        # We don't have a previous instance of this field, so create a
        # new field entry with our value as the first element of a list
        rec[fname] = [fval]
      
    else:
      # This field can only occur once, so make sure it's not already
      # present
      if fname in rec:
        raise MultiFieldError()
      
      # Add a mapping for this field name to value
      rec[fname] = fval
  
  # We got a mapping of field names to values, so pass to the record
  # processing function
  handle_rec(rec)

#
# Program entrypoint
# ------------------
#

# Check command argument count (should include the program name and the
# one argument)
#
if len(sys.argv) != 2:
  print('Wrong number of program arguments!')
  sys.exit(1)

# Open the input file as a text file in UTF-8 encoding and parse all the
# records
#
line_num = 0  # Current line number
rec_line = 1  # Line at start of current record
try:
  with open(sys.argv[1], mode='rt',
            encoding='utf-8', errors='strict') as fin:

    # We have the input file open -- read line by line
    lbuf = []     # Buffers record lines
    for line in fin:
      
      # Update line count
      line_num = line_num + 1
      
      # Trim trailing whitespace and linebreaks, but NOT leading
      # whitespace, which is significant in case of line continuations
      line = line.rstrip(' \t\n')
      
      # Filter out blank lines that are empty or contain only spaces,
      # tabs, and line breaks
      if len(line) < 1:
        continue
      
      # If this line is %% then handle end of record and continue to
      # next record
      if line == '%%':
        # If the record line of this record is 1, then just clear the
        # line buffer, update the record line, and continue to next line
        # without any further processing so that we skip the special
        # first record
        if rec_line <= 1:
          lbuf = []
          rec_line = line_num + 1
          continue
        
        # If we got here, we're not in the special case of the first
        # record, so we want to process the raw record
        raw_record(lbuf)
        
        # Clear the line buffer and update the record line
        lbuf = []
        rec_line = line_num + 1
        
        # Continue on to next line
        continue
      
      # If the first character of this line is a tab or a space, then we
      # have a continuation line, so process that and continue to next
      # line
      fchar = line[0]
      if (fchar == ' ') or (fchar == '\t'):
        # Continuation line, so this must not be first line of record
        if len(lbuf) < 1:
          raise BadContinueLine()
        
        # Drop leading whitespace and replace with a single leading
        # space
        line = ' ' + line.lstrip(' \t')
        
        # Add this line to the end of the last line in the record line
        # buffer
        lbuf[-1] = lbuf[-1] + line
        
        # Continue on to next line
        continue
      
      # If we got here, we have a regular record line, so just add that
      # to the line buffer
      lbuf.append(line)
  
    # If after the loop will still have something in the record buffer,
    # flush this last record
    if len(lbuf) > 0:
      raw_record(lbuf)
      lbuf = []

except BadContinueLine:
  print('On line', line_num, 'invalid continuation line!')
  sys.exit(1)

except MultiFieldError:
  print('On record beginning on line', rec_line)
  print('Regular field defined more than once!')
  sys.exit(1)

except NoColonError:
  print('On record beginning on line', rec_line)
  print('A field is missing a colon!')
  sys.exit(1)

except FileNotFoundError:
  # Couldn't find the input file
  print('Can\'t find the input file!')
  sys.exit(1)

except ValueError:
  # Some kind of text encoding problem
  print('Invalid UTF-8 in input!')
  sys.exit(1)
