#
# iso5.py
# =======
#
# Python-3 module for loading and parsing the ISO-639-5 data file.
#
# A current copy of the data file is available at the ISO-639-5
# registrar:
#
#   https://www.loc.gov/standards/iso639-5/
#
# IMPORTANT:  Use the UTF-8 version of the data file.
#
# To use this module, import iso5 and then call iso5.parse() with the
# path to the data file.  If this is successful, the result will be
# placed in the iso5.rec variable.  The iso5.code variable will then
# also hold a mapping of all language codes to their records.
#

#
# Exceptions
# ----------
#
# Each exception overloads the __str__ operator so that it can be
# printed as a user-friendly error message.  The error message includes
# line number information if relevant.  It has punctuation at the end,
# but it does NOT have a line break at the end.
#
# All exceptions defined by this module are subclasses of ISO5Error.
#

class ISO5Error(Exception):
  def __str__(self):
    return 'Unknown ISO-639-5 parsing error!'

class BadCode(ISO5Error):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'ISO-639-5 data line ' + str(self.m_line) + ': ' + \
        'Invalid language code!'
    else:
      return 'Invalid language code!'

class BadDataFile(ISO5Error):
  def __str__(self):
    return 'ISO-639-5 data file must be the UTF-8 version!'

class BadHeader(ISO5Error):
  def __str__(self):
    return 'ISO-639-5 data file has invalid header line!'

class BadRecord(ISO5Error):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'ISO-639-5 data line ' + str(self.m_line) + ': ' + \
        'Invalid record syntax!'
    else:
      return 'Invalid record syntax!'

class FieldMissingError(ISO5Error):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'ISO-639-2 data line ' + str(self.m_line) + ': ' + \
        'Record missing required field!'
    else:
      return 'Record missing required field!'

class LogicError(ISO5Error):
  def __str__(self):
    return 'Internal logic error within ISO-639-2 module!'

class NoDataFileError(ISO5Error):
  def __init__(self, fpath=None):
    self.m_fpath = fpath
  def __str__(self):
    if self.m_fpath is not None:
      return 'Can\'t find ISO-639-5 data file ' + self.m_fpath
    else:
      return 'Can\'t find ISO-639-5 data file!'

class RedefineError(ISO5Error):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'ISO-639-5 record at line ' + str(self.m_line) + ': ' + \
        'Language code ' + self.m_tname + ' is already defined!'
    
    elif self.m_line is not None:
      return 'ISO-639-5 record at line ' + str(self.m_line) + ': ' + \
        'Language code is already defined!'
      
    else:
      return 'Language code is already defined!'

#
# Module-level variables
# ----------------------
#

# The module-level variable that stores the result of parsing the data
# file, or None if the file hasn't been parsed yet.
#
# Use the parse() function to set this variable.  Once it is set
# successfully, it will be a list of zero or more records, stored in the
# order they appear in the data file.
#
# Each record is a tuple with two elements.  The first element is an
# integer that stores the line number of the first line of the record in
# the data file.  The second element is a dictionary that maps field
# names to field values.
#
# The column names in the official data file are mapped to the names
# used in the dictionary using the following table:
#
#    Official name  | Dictionary field name
#   ----------------|-----------------------
#   URI             | uri
#   code            | code
#   Label (English) | en
#   Label (French)  | fr
#
# All four fields are required for all records.
#
rec = None

# The module-level variable that stores the index of language codes to
# parsed records, or None if the file hasn't been parsed yet.
#
# Use the parse() function to set this variable.  Once it is set
# successfully, it will be a dictionary with string keys and values that
# are the same tuple objects used in the rec module-level variable.
#
code = None

#
# Local functions
# ---------------
#

# Verify that a given string is a three-letter code with all letters
# being lowercase ASCII letters.
#
# Parameters:
#
#   cd : string | mixed - the value to check
#
# Return:
#
#   True if valid three-letter code, False otherwise
#
def check_code_3(cd):
  if not isinstance(cd, str):
    return False
  if len(cd) != 3:
    return False
  for c in cd:
    if (ord(c) < ord('a')) or (ord(c) > ord('z')):
      return False
  return True

# Check whether the given language code is one of the private-use
# language codes.
#
# Parameters:
#
#   cd : string | mixed - the value to check
#
# Return:
#
#   True if a private-use code, False otherwise
#
def is_private(cd):
  
  # If parameter isn't string, it isn't a private-use code
  if not isinstance(cd, str):
    return False
  
  # If code isn't exactly three characters, it isn't private-use
  if len(cd) != 3:
    return False
  
  # Language code matching is case-insensitive, so make the given
  # language code lowercase
  cd = cd.lower()
  
  # If first letter of language code isn't q, then it isn't private-use
  if cd[0] != 'q':
    return False
  
  # In order to be private use, second character must be in range a-t
  # and third character must be in range a-z
  if (ord(cd[1]) >= ord('a')) and (ord(cd[1]) <= ord('t')) and \
      (ord(cd[2]) >= ord('a')) and (ord(cd[2]) <= ord('z')):
    return True
  else:
    return False

# Given a string holding the first line of text in a file, strip a
# leading UTF-8 Byte Order Mark (BOM) if present.
#
# Only use this function on the very first line of the file, as that is
# the only place a BOM may be present.
#
# The return value is the string as-is if there is no BOM.
#
# Parameters:
#
#   line : string - the first line to process
#
# Return:
#
#   the first line, with the BOM stripped out if present
#
def strip_bom(line):
  if not isinstance(line, str):
    raise LogicError()
  if len(line) < 1:
    return line
  if ord(line[0]) == 0xfeff:
    if len(line) > 1:
      return line[1:]
    else:
      return ''
  else:
    return line

#
# Public functions
# ----------------
#

# Parse the given ISO-639-5 data file and store the parsed result in the
# module-level rec and code variables.
#
# See the module documentation and the documentation of the rec variable
# for further information.
#
# If the rec value is already set, this function call will be ignored.
#
# If the function fails, the rec and code values will be set to None.
#
# Parameters:
#
#   fpath : string - the path to the data file
#
def parse(fpath):

  global rec, code

  # Ignore call if rec already set
  if rec is not None:
    return

  # Check parameter
  if not isinstance(fpath, str):
    rec = None
    code = None
    raise LogicError()

  # Clear the records variable to an empty list and set the code
  # dictionary to an empty dictionary
  rec = []
  code = dict()

  # Open the input file as a text file in UTF-8 encoding and parse all
  # the records
  try:
    with open(fpath, mode='rt',
              encoding='utf-8', errors='strict') as fin:
  
      # We have the input file open -- read line by line
      line_num = 0  # Current line number
      fmap = None   # Mapping of fields to column indices
      max_req = 0   # Required number of columns in each line
      for line in fin:
        
        # Update line count
        line_num = line_num + 1
        
        # If this is the first line, remove UTF-8 Byte Order Mark (BOM)
        # if present
        if line_num <= 1:
          line = strip_bom(line)
        
        # Trim trailing whitespace and linebreaks
        line = line.rstrip(' \t\n')
        
        # If this is the first line, set up fmap and skip rest of
        # processing
        if line_num <= 1:
          
          # Parse into columns
          cn = line.split('\t')
          
          # Should be at least four columns
          if len(cn) < 4:
            raise BadHeader()
            
          # Trim all column names and make them lowercase
          for x in range(0, len(cn)):
            cn[x] = cn[x].strip(' \t').lower()
          
          # Set fmap and max_req variables
          fmap = dict()
          for i in range(0, len(cn)):
            # Get current column name
            n = cn[i]
            
            # Only process this column if one of the recognized column
            # names (in lowercase)
            if (n == 'uri') or (n == 'code') or \
                (n == 'label (english)') or (n == 'label (french)'):
              
              # Map name to standard dictionary name
              if (n == 'uri'):
                n = 'uri'
              elif (n == 'code'):
                n = 'code'
              elif (n == 'label (english)'):
                n = 'en'
              elif (n == 'label (french)'):
                n = 'fr'
              else:
                raise LogicError()
              
              # Make sure name not already mapped
              if n in fmap:
                raise BadHeader()
              
              # Store name to column index mapping
              fmap[n] = i
              
              # Update max_req
              max_req = i + 1
          
          # Make sure we found all the four required columns
          if ('uri' not in fmap) or ('code' not in fmap) or \
              ('en' not in fmap) or ('fr' not in fmap):
            raise BadHeader()
          
          # Skip rest of processing
          continue
        
        # Filter out blank lines that are empty or contain only spaces,
        # tabs, and line breaks
        if len(line) < 1:
          continue
        
        # We have a content line, so parse into fields using the
        # horizontal tab as separator
        fv = line.split('\t')
        
        # Each record must have at least the required number of columns
        if len(fv) < max_req:
          raise BadRecord(line_num)
        
        # Trim each field of leading and trailing whitespace
        for i in range(0, len(fv)):
          fv[i] = fv[i].strip(' \t')
        
        # Make sure the required fields are not empty
        if (len(fv[fmap['uri']]) < 1) or \
            (len(fv[fmap['code']]) < 1) or \
            (len(fv[fmap['en']]) < 1) or \
            (len(fv[fmap['fr']]) < 1):
          raise FieldMissingError(line_num)
        
        # Create a new record and assign the required fields
        r = dict()
        r['uri'] = fv[fmap['uri']]
        r['code'] = fv[fmap['code']]
        r['en'] = fv[fmap['en']]
        r['fr'] = fv[fmap['fr']]
        
        # Check the language code format
        if not check_code_3(r['code']):
          raise BadCode(line_num)
        
        # Make sure that the language code is not in the index yet and
        # that it isn't in reserved private range
        if r['code'] in code:
          raise RedefineError(line_num, r['code'])
        if is_private(r['code']):
          raise RedefineError(line_num, r['code'])
  
        # Define the tuple pair of the line number and the record
        pr = (line_num, r)
        
        # Add the tuple to the parsed variables
        rec.append(pr)
        code[r['code']] = pr
  
  except FileNotFoundError:
    rec = None
    code = None
    raise NoDataFileError(fpath)
  
  except ValueError:
    rec = None
    code = None
    raise BadDataFile()
    
  except ISO5Error as se:
    rec = None
    code = None
    raise se
  
  except Exception as exc:
    rec = None
    code = None
    raise ISO5Error() from exc
